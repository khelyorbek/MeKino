"""MeKino Flask Web Application

Made by: Elyorbek Khudaybergenov
Github Profile: https://github.com/khelyorbek

This product uses "The Movie Database" API but is not endorsed or certified by TMDB.	
Find out more abour TMDB API: https://www.themoviedb.org/documentation/api
TMDB API docs for developers: https://developers.themoviedb.org/3
"""

# Importing the necessary libraries
from crypt import methods
from flask import Flask, request, render_template,  redirect, session, flash, g, abort ### main Flask components
from sqlalchemy.exc import IntegrityError ### for handling SQLA issues within WTForms
from models import db, connect_db, User, Playlist, Shared_Playlist, Watched_Movies, Playlist_Movies ### for connecting and accesing SQLA Data Models
import requests ### for handling REST requests
from forms import RegisterForm, LoginForm, UserEditForm, CreateNewPlaylistForm  ### WTForms for dynamic form creation
from string import ascii_letters    ### for url generation
from random import choice   ### for url generation

# importing the API key saved in our environmental variables
# if you are planning to use this project, you need to visit https://developers.themoviedb.org/3/getting-started/introduction and sign up for your own API Key and save it into a API_KY environmental variable  
import os

# mapping the base URL of the API into a variable
BASE_URL = "https://api.themoviedb.org/3/"
# mapping the list of genres into a variable
GENRES_LIST = (requests.get(f"{BASE_URL}genre/movie/list",params={"api_key": os.environ['API_KEY']})).json()['genres']

# mapping the Flask object into a variable
app = Flask(__name__)

# configuring Flask and SQL Alchemy
# OLD postgresql://test:test@localhost/mekino
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

# connecting to a database
connect_db(app)

@app.before_request
def add_user_to_g():
    """Before any request, if we're logged in, add curr user to Flask global."""

    # if the current user is stored in session cookies
    if "curr_user" in session:
        # set the user object into a global user variable
        g.user = User.query.get(session["curr_user"])

    else:
        # if the cookie is not found, settings the global user variable to None
        g.user = None

def do_login(user):
    """Log in user."""
    # Settings the curr_user cookie variable as the id of the user. user is passed into this method.
    session["curr_user"] = user.id

def do_logout():
    """Logout user."""
    # If the curr_user is stored in the session, delete it. This will log the user out.
    if "curr_user" in session:
        del session["curr_user"]

####################### HOME ROUTE LOGIC #######################
@app.route('/')
def show_home():
    """For home route logic"""
    # redirects immediately to /trending. Can me modified in the future to perform something else.
    return redirect('/trending')

####################### USER PROFILE LOGIC #######################
# Registration route. Accepts GET and POST requests and performs operations based on the REST method received.
@app.route('/register', methods=['GET','POST'])
def register_user():
    """For registration logic. Accepts GET and POST requests"""
    # mapping a registration form into a variable
    form = RegisterForm()

    # for handling POST requests
    if form.validate_on_submit():
        # if the CSRF token has been validated successfully,
        # maps all the data received from the form into variables
        first_name = form.first_name.data
        last_name = form.last_name.data
        username = form.username.data
        password = form.password.data
        
        # Calls the register class method inside the User Data Model. The method is stored under models.py. 
        # This method returns the user object.. Creates a new instance of the User object and stored into a variable.
        new_user = User.register(first_name, last_name, username, password)

        # Add the newly created user object into the DB.
        db.session.add(new_user)

        try:
            # Will try to commit the newly created user into the DB.
            db.session.commit()

        # If the commit errors out,
        except IntegrityError:
            # Appends the errors into the form error field
            form.username.errors.append('Username taken.  Please pick another')
            # Will redirect user back to the same page and have user try again
            return render_template('user/register.html', form=form)

        # Once the commit is successful, adding the newly created user into session["curr_user"]
        do_login(new_user)

        # Flashing a message to the user
        flash('Successfully Created Your Account! Welcome to MeKino!', "success")
        # Redirecting to the main page.
        return redirect('/')

    # for handling GET request
    # will render a template and pass the form into it.
    return render_template('user/register.html', form=form)

# Login route logic
@app.route('/login', methods=['GET','POST'])
def login_user():
    """For login logic. Accepts GET and POST requests."""
    # mapping a logic form into a variable
    form = LoginForm()

    # for handling POST requests
    if form.validate_on_submit():
        # if the CSRF token has been validated successfully,
        # maps all the data received from the form into variables
        username = form.username.data
        password = form.password.data

        # Calls the logic class method inside the User Data Model. The method is stored under models.py. 
        # This method returns the user object if the password passed into the method has been validated succesffully.
        user = User.authenticate(username, password)

        # Making sure that the user has been authenticated successfully
        if user:
            # If so, adding the logged in user into session["curr_user"]
            do_login(user)
            # Flashing a message to the user
            flash(f"Welcome Back, {user.username}!", "success")
             # Redirecting to the main page.
            return redirect('/')
        else:
            # If the user hasn't authenticated successfully, show an error in the form.
            # Have the user try again.
            form.username.errors = ['Invalid username and/or password.']

    # for handling GET request
    # will render a template and pass the form into it.
    return render_template('user/login.html', form=form)

# Profile edit logic, accepts GET and POST requests.
@app.route('/profile_edit', methods=['GET','POST'])
def edit_user_profile():
    """For user profile edit logic. Accepts GET and POST requests."""
    
    # Making sure that only logged in users can edit their profile.
    if not g.user:
        # Flashing a message if not logged in
        flash("Access unauthorized. You must be logged in to use this feature!", "danger")
        # Redirecting to main page.
        return redirect("/")    

    # Making the user edit form into a variable and passing the current user object
    # This ensures that current values from the user object are passed into the form
    form = UserEditForm(obj=g.user)

    # For handling POST requests
    if form.validate_on_submit():
        # Authenticating the user
        user = User.authenticate(g.user.username,
                                 form.password.data)

        # If authenticated successfully,
        if user:
            # Updating the user object with the values from the form
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.username = form.username.data
            
            # Adding the changes to be sent to DB
            db.session.add(user)
            # Sending the changes to the DB
            db.session.commit()
            # Flashing a message to the user
            flash("Successfully updated your profile.", "success")
            # Redirecting to home page
            return redirect("/")

        # if authentication fails, it should flash an error and return to the same page.
        flash("Invalid password. Please try again.", 'danger')
        return redirect('/profile_edit')
    
    # For GET requests, displays a template and passed the form and the user
    return render_template('user/user_profile_edit.html', form=form, user=g.user)

# Logout route logic
@app.route('/logout')
def logout_user():
    """Logout logc. Will remove the curr_user from the session if it exists. GET requests only."""

    # Making sure only logged in users can logout
    if "curr_user" not in session:
        # Flashes a message if you are not logged in. This is to catch manual typers. Logout page is not present in the UI for guest visitors.
        flash("Please login first!", "danger")
        # Redirects to login page
        return redirect('/login')
    
    # If the user is logged in, calling the method and removing the user from the session
    do_logout()
    # Flashing a message below to the user
    flash("Goodbye! We will miss you!", "info")
    # Redirecting to homepage
    return redirect('/')

####################### MOVIE GRID PAGES LOGIC #######################
# Trending page logic
@app.route('/trending')
def show_trending_nopage():
    """Redirects to trending page 1 if no page number is provided. Could be used for other logic in the future. GET request only."""
    return redirect('/trending/1')

# Trending page logic with page number
@app.route('/trending/<int:page>')
def show_trending_paged(page):
    """Shows trending movies for the past week for page <int:page>. Get request only."""
    
    # Making sure that the requested page != 0, < 0 and 450 (works reliably. anything higher causes issues by API)
    if page > 450:
        page = 450
        flash("Page number too large. Setting page number to 450.", "info")
    elif page < 1:
        page = 1
        flash("Page number too low. Setting page number to 1.", "info")

    # getting the list of trending movies and mapping into a variable. Passing a page number from the url for use in pagination.
    trending = requests.get(f"{BASE_URL}trending/movie/week",params={"api_key": os.environ['API_KEY'], "page": page})
    # rendering a template and passing the json version of the results, also passing the genres and the page number
    return render_template('movie/trending.html', trending = trending.json()['results'], genres = GENRES_LIST, page = page)

# Popular page logic
@app.route('/popular')
def show_popular_nopage():
    """Redirects to trending page 1 if no page number is provided. Could be used for other logic in the future. GET request only."""
    return redirect('/popular/1')

# Popular page logic with page number
@app.route('/popular/<int:page>')
def show_popular_paged(page):
    """Shows popular movies for the past week. GET request only."""
    
    # Making sure that the requested page != 0, < 0 and 450 (works reliably. anything higher causes issues by API)
    if page > 450:
        page = 450
        flash("Page number too large. Setting page number to 450.", "info")
    elif page < 1:
        page = 1
        flash("Page number too low. Setting page number to 1.", "info")

    # getting the list of movies and mapping into a variable. Passing a page number from the url for use in pagination.
    popular = requests.get(f"{BASE_URL}movie/popular",params={"api_key": os.environ['API_KEY'], "page": page})
    # rendering a template and passing the json version of the results, also passing the genres and the page number
    return render_template('movie/popular.html', popular = popular.json()['results'], genres = GENRES_LIST, page = page)

# Top page logic
@app.route('/top')
def show_top_nopage():
    """Redirects to trending page 1 if no page number is provided. Could be used for other logic in the future. GET request only."""
    return redirect('/top/1')

# Top page logic with page number
@app.route('/top/<int:page>')
def show_top_paged(page):
    """Shows popular movies for the past week. GET request only."""
    
    # Making sure that the requested page != 0, < 0 and 450 (works reliably. anything higher causes issues by API)
    if page > 450:
        page = 450
        flash("Page number too large. Setting page number to 450.", "info")
    elif page < 1:
        page = 1
        flash("Page number too low. Setting page number to 1.", "info")

    # getting the list of movies and mapping into a variable. Passing a page number from the url for use in pagination.
    top = requests.get(f"{BASE_URL}movie/top_rated",params={"api_key": os.environ['API_KEY'], "page": page})
    # rendering a template and passing the json version of the results, also passing the genres and the page number
    return render_template('movie/top.html', top = top.json()['results'], genres = GENRES_LIST, page = page)

####################### INDIVIDUAL MOVIE LOGIC #######################
# Movie details logic for individual movies
@app.route('/movie/<int:id>')
def show_movie_details(id):
    """For displaying information about the individual movie. Not a list. GET request only."""
    
    # getting the movie information from API and storing into variable
    movie = requests.get(f"{BASE_URL}movie/{id}",params={"api_key": os.environ['API_KEY']})

    # only pulling watched if the user is logged in
    if "curr_user" in session:
        # getting watched movies so we can determine if this movie has been marked as watched already
        watched_mov = [x.movie_id for x in g.user.watched_movies]
    
        # rendering a template and passing the json version of the results, also passing the genres and the page number
        return render_template('movie/details.html', movie = movie.json(), genres = GENRES_LIST, mov_watched = id in watched_mov)
    
    # If the user is not logged in, just passing the movie info and the genres. Not passing watched movies.
    return render_template('movie/details.html', movie = movie.json(), genres = GENRES_LIST)

# Movie details poster logic for individual movies
@app.route('/movie/<int:id>/images')
def show_movie_images(id):
    """For showing movies for individual movies. GET request only."""

    # getting the movie information from API and storing into variable
    movie = requests.get(f"{BASE_URL}movie/{id}",params={"api_key": os.environ['API_KEY']})

    # getting the list of images available in english
    images = requests.get(f"{BASE_URL}movie/{id}/images",params={"api_key": os.environ['API_KEY'], "language": "en"})
    
    # if there are no backdrops to show, switches to backup plan -> showing movie posters.
    # if we don't have this, less popular/known movies will just show a broken image icon.
    if not images.json()['backdrops']:
        # passing movies and setting the images variable to posters if backdrops don't exist
        return render_template('movie/images.html', movie = movie.json(), images = images.json()['posters'])
    else:
        # passing movies and setting the images variable to backdrops if backdrops DO exist
        return render_template('movie/images.html', movie = movie.json(), images = images.json()['backdrops'])

# Back-end logic for marking an item watched or unwatched
@app.route('/watched_unwatched', methods=['PATCH'])
def mark_umark_watched():
    """Logic for marking movie watched and unwatched.
    Receives PATCH request from Axios on front end.
    Based on the request, will add or remove from the watched database table.
    """
    # Making sure that only a logged in user can mark a movie as watched/unwatched
    if "curr_user" not in session:
        # Flashing an image
        flash("Please login first!", "danger")
        # Redirecting to login page
        return redirect('/login')
       
    # Getting a mov_id from the payload sent to our API logic
    mov_id = int(request.json['mov_id'])
    # Getting a operation from the payload sent to our API logic
    operation = request.json['oper']

    # If the operation is w,
    if operation == "w":    
        # Creating a new instance of the object and passing the id of the global user  into the user_id column
        # Passing the mov_id that we received above as movie_id column
        w = Watched_Movies(user_id=g.user.id, movie_id=mov_id)
        # Adding the newly created object to be sent to the DB
        db.session.add(w)
        # Sending the data to DB
        db.session.commit()
        # Returning a string to the sender of the REST request
        return "Successfully marked as watched."

    # If the operation is u,
    elif operation == "u":
        # Going through the list of watched movies
        for i in g.user.watched_movies:
            # If the movie in question is in the watched movies list, proceed
            if i.movie_id == mov_id:
                # Creating a new instance of the Watched_Movies object by having SQL Alchemy find the right Watched_Movie for us
                uw = Watched_Movies.query.get_or_404(i.id)
                # queue the object for deletion in DB
                db.session.delete(uw)
                # sending the queued requests  to DB
                db.session.commit()
                # Returning a string to the sender of the REST request
                return "Successfully marked as not watched."
    else:
        # If the movie in question is not in watched movies, returning an error message
        return "Error! Server could not understand your request."

    
####################### PLAYLIST LOGIC #######################
# Watched Playlist Logic
@app.route('/playlist/watched')
def show_playlist_watched():
    """Logic for showing the watched playlist. GET requests only. """

    # Making sure that only a logged in user can view their watched playlist
    if "curr_user" not in session:
        # flashing a message
        flash("Please login first!", "danger")
        # redirecting the user
        return redirect('/login')

    # Getting a list of watched movie IDs
    watched_movie_ids = [x.movie_id for x in g.user.watched_movies]
    # Creating an empty list of watched_movies
    watched_movies = []
    # For each id in the watched movie IDs
    for id in watched_movie_ids:
        # Getting the info about the watched movie from the API in the json format
        # Appending the results into a watched movies list
        watched_movies.append(requests.get(f"{BASE_URL}movie/{id}",params={"api_key": os.environ['API_KEY']}).json())
    
    # Rendering a template and passing all the watched movies into it
    return render_template('/playlist/watched.html', watched_movies=watched_movies)

# Create new playlist logic
@app.route('/playlist/create', methods=['GET','POST'])
def create_new_playlist():
    """For creating new playlist logic. Accepts GET and POST requests"""
    # Mapping the CreateNewPlaylistForm form into a variable
    form = CreateNewPlaylistForm()

    # Making sure that only a logged in user can create a new private playlist
    if "curr_user" not in session:
        # If not, flashing a message
        flash("Please login first!", "danger")
        # Redirecting
        return redirect('/login')

    # For POST requests
    if form.validate_on_submit():
        # If the CSRF token is validated successfully
        # setting the form data into a new variable
        playlist_name = form.name.data
        
        # creating a new instance of Playlist object and passing the info received from the form and the global user variable
        new_playlist = Playlist(name=playlist_name, author=g.user.id)
        # queueing the new changes to be added to the DB
        db.session.add(new_playlist)

        # trying to push the changes to the DB
        try:
            db.session.commit()
        # Catching an error
        except IntegrityError:
            # appending the error into the form errors
            form.username.errors.append('Error. Please try again with different playlist name')
            # rendering the same template
            return render_template('/playlist/create_new.html', form=form)

        # If the push to DB is successfuly, displaying a message
        flash('Successfully created new playlist!', "success")
        # Redirecting to the list of playlists
        return redirect('/playlist/private')

    # For the GET request. Returns a template and passes the form into it
    return render_template('/playlist/create_new.html', form=form)

# Delete playlist logic
@app.route('/playlist/delete', methods=['DELETE'])
def delete_playlist():
    """For deleting a playlist. Used for private and shared deletion. Expects a DELETE request."""
    
    # Making sure that only a logged in user can delete a playlist
    if "curr_user" not in session:
        # If not, flashing a message
        flash("Please login first!", "danger")
        # Redirecting
        return redirect('/login')

    # Getting the id of the playlist from the REST request and mapping to variable
    plist_id = int(request.json['plist_id'])
    # Querying the playlist table for that id
    plist = Playlist.query.get_or_404(plist_id)

    # Making sure that the user is only deleting the playlists that belong to them
    if g.user.id != plist.author:
        # if doesn't belong to them, returning an error string to the requester
        return "You are not authorized to access this resource!"

    # if its the right author, queueing the delete change to the DB
    db.session.delete(plist)
    # pushing the queued changed
    db.session.commit()

    # returning a message string to the requester
    return "Successfully deleted a playlist."

# Add movie to playlist logic
@app.route('/playlist/add_remove', methods=['PATCH'])
def add_movie_to_playlist():
    """For adding a movie to a playlist. Expects a PATCH request."""
    
    # Making sure that only a logged in user can add a movie to a private playlsit 
    if "curr_user" not in session:
        # if not, flashing a message
        flash("Please login first!", "danger")
        # redirecting
        return redirect('/login')
    
    # getting the REST request data and mapping into variables
    mov_id = int(request.json['mov_id'])
    plist_id = request.json['plist_id']

    # creating a new instance of object and passing the received data in variables
    pm = Playlist_Movies(playlist_id = plist_id, movie_id = mov_id)
    
    # queueing the changes to the DB
    db.session.add(pm)
    # pushing the queued changes
    db.session.commit()

    # returning a string message to the requester
    return "Successfully added to playlist."

# Remove movie from playlist
@app.route('/playlist/add_remove', methods=['DELETE'])
def remove_movie_from_playlist():
    """For removing a movie from the playlist. Expects a DELETE request."""
    
    # Making sure that only a logged in user can remove a movie from a private playlist
    if "curr_user" not in session:
        # if not logged in, flsahing a message
        flash("Please login first!", "danger")
        # redirecting to login
        return redirect('/login')
       
    # getting the REST request data and mapping into variables
    mov_id = int(request.json['mov_id'])
    plist_id = int(request.json['plist_id'])

    # creating a new instance of object and passing the received data in variables
    pm = Playlist_Movies.query.filter_by(playlist_id=plist_id,movie_id=mov_id).first()

    # havign Playlist object query and find the playlist by the ID received
    plist = Playlist.query.get_or_404(plist_id)

    # Making sure that the user is only deleting the playlists that belong to them
    if g.user.id != plist.author:
        # if not the author, will return a message to the requester
        return "You are not authorized to access this resource!"
    
    # queueing the delete change to the DB
    db.session.delete(pm)
    # pushing the queued change
    db.session.commit()

    # returning a string to the requester.
    return "Successfully removed from playlist."

# Show list of private playlists on a page
@app.route('/playlist/private')
def show_private_playlists():
    """For showing private playlists on a page. Will have option to delete and share. GET request."""

    # Making sure that only a logged in user can view list of private playlists
    if "curr_user" not in session:
        # if not logged in, flashing message
        flash("Please login first!", "danger")
        # redirecting to login
        return redirect('/login')

    # if logged in, rendering a private list template
    return render_template('playlist/private_list.html')

# Show details of an individual private playlist
@app.route('/playlist/private/<int:id>')
def show_private_playlist_details(id):
    """Logic for showing details of an individual private playlist. GET request."""

    # Querying the PLaylist table for the ID passed into this method
    p = Playlist.query.get_or_404(id)
    
    # Making sure that only a logged in user can view individual private playlists
    if "curr_user" not in session:
        # If not logged, flashing a message
        flash("Please login first!", "danger")
        # redirecting to login
        return redirect('/login')
    # Also making sure that the private list author is the logged in user
    elif g.user.id != p.author:
        # If not, flsahing a message
        flash("You are not authorized to access this resource!", "danger")
        # Redirecting ot login
        return redirect('/login')

    # getting the list of movie ids that belong to the playlist
    p_movie_ids = [x.movie_id for x in p.movies]
    # creating an empty list to store the movies under the playlist
    p_movies = []
    # for each movie in the playlist
    for m_id in p_movie_ids:
        # sending a GET request to the API and getting the movie details in JSON format
        # appending each movie details into the list variable
        p_movies.append(requests.get(f"{BASE_URL}movie/{m_id}",params={"api_key": os.environ['API_KEY']}).json())

    # rendering a template and passing the playlist and movies inside the playlist as variables
    return render_template('playlist/private_single.html', playlist = p, playlist_movies = p_movies)

####################### SHARED PLAYLIST LOGIC #######################
# Share a private playlist
@app.route('/playlist/share', methods=['PUT'])
def share_private_playlist():
    """Logic for generating a random hash and adding a private playlist into shared playlist table. Expects a PUT request."""

    # Making sure that only a logged in user can share a private playlist
    if "curr_user" not in session:
        # If not, logged in, flashing message
        flash("Please login first!", "danger")
        # Redirecting to login
        return redirect('/login')

    # getting the REST data and mapping into a variable
    plist_id = int(request.json['plist_id'])

    # Logic for generating a random 10 character url from lowercase and uppercase alphabet    
    letters = ascii_letters # from string library. will print a-z lowercase and A-Z uppercase letters.
    url = (''.join(choice(letters) for i in range(10))) # picks a random sequence of 10 chars

    # creating a new instance of the Shared_Playlist object and passing the playlist id, user id and the newly generated URL
    sp = Shared_Playlist(playlist_id=plist_id, user_id=g.user.id, url_code=url)

    # queueing the changed to be added to the DB
    db.session.add(sp)
    # pushing the queued changed
    db.session.commit()
    
    # returning the url code to be used in the front end for copy url logic
    return url

# Show a list of shared playlists
@app.route('/playlist/shared', methods=['GET'])
def show_shared_playlists():
    """Logic for displaying all the shared playlists on 1 page. GET request only."""

    # Making sure that only a logged in user can view list of their shared playlists
    if "curr_user" not in session:
        # if not, flashing a message
        flash("Please login first!", "danger")
        # redirecting
        return redirect('/login')
    # if logged in, rendering a template
    return render_template('playlist/shared_list.html')

# Logic for un-sharing an already shared playlist
@app.route('/playlist/shared', methods=['DELETE'])
def un_share_private_playlist():
    """Logic for deleting a shared playlist. The private playlist itself will stay. Expects a DELETE request."""

    # Making sure that only a logged in user can delete their shared playlist.
    if "curr_user" not in session:
        # if not, flsahing a message
        flash("Please login first!", "danger")
        # redirecting to login
        return redirect('/login')
    
    # receiving the REST request and mapping into variable
    plist_id = int(request.json['plist_id'])

    # finding a first item in the Shared_Playlist object/table that has the correct playlist id
    p = Shared_Playlist.query.filter_by(id = plist_id).first()

    # Making sure that the user is only deleting the playlists that belong to them
    if g.user.id != p.playlist.author:
        # if not, sendinga message back to the requester
        return "You are not authorized to access this resource!"

    # queueing the delete change to the DB
    db.session.delete(p)
    # pushing the queued changes
    db.session.commit()

    # returning a message to the requester
    return "Successfully un-shared a shared playlist."

# Show details of a shared private playlist
@app.route('/playlist/shared/<string:url_code>')
def show_shared_playlist_details(url_code):
    """Logic for querying the DB for the URL provide and showing details of a shared playlist.
    This option is available to everyone. Not only to logged in users.
    Expects a GET request.
    """

    # Getting the first result from the Shared_Playlist object/table that matched the URL sent into this method
    sp = Shared_Playlist.query.filter_by(url_code=url_code).first()

    # If there is a typo in the URL or its invalid, redirect to 404 error page
    if sp is None:
        abort(404)

    # If the URL is valid, proceed as normal. Mapping the private playlist which has full playlist info into p variable
    p = sp.playlist

    # Getting the movie ids and putting them into a variable
    p_movie_ids = [x.movie_id for x in p.movies]
    # creating an empty list
    p_movies = []
    # for each id in the movie ids
    for m_id in p_movie_ids:
        # querying the API for the movie details for each movie id in the playlist
        # then appending each movie into the list variable
        p_movies.append(requests.get(f"{BASE_URL}movie/{m_id}",params={"api_key": os.environ['API_KEY']}).json())

    # Getting the author information by querying the p.author which is an id of the user
    a = User.query.get_or_404(p.author)

    # rendering a template with the playlist, movies and author as variables
    return render_template('playlist/shared_single_ext.html', playlist=p, movies=p_movies, author=a)

####################### SEARCH LOGIC #######################
@app.route('/search/<string:q>/<int:page>', methods=['GET'])
def show_search_results(q, page):
    """Logic for sending an API request and displaying the JSON response as an HTML. Expects a GET request."""

    # Making sure that a page is passed into the address bar, if not setting the page to 1
    if page is None:
        page = 1

    # New code to fix issue 8
    if ('.' in q) or ('/' in q) or ('%' in q) or ('\\' in q) or ('?' in q):
        flash("Search criteria contains unsupported characters. Please try searching again with a different keyword.", "danger")
        return redirect('/')

    # sending a GET request to the URL with the query passed to this method. then mapping the results into a variable
    # passing the page number to make sure we are displaying the search results for correct page number
    results = requests.get(f"{BASE_URL}search/movie",params={"api_key": os.environ['API_KEY'], "query": q, "page": page})

    if results is None:
        # Flash an error
        flash("Search criteria did not return any results. Please try searching again with a different keyword.", "warning")
        # Redirect to homepage
        return redirect('/')

    # TO DO 2
    # If results return nothing, flash a message that says no results found
    print("RESULTS")
    print(results.json()['results']);
    
    # Using try/except to catch any errors that might occur while sending a request to API. Such as sending empty string, space, multiple spaces, unsupported character, etc.
    try:
        # rendering a template and passing the json version of the result
        return render_template('movie/search_results.html', results = results.json()['results'], genres = GENRES_LIST, search_term=q, page = page)
    # if an exception is generated
    except Exception as e:
        # Flash an error
        flash("Search criteria did not return any results. Please try searching again with a different keyword.", "warning")
        # Redirect to homepage
        return redirect('/')