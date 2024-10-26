# MeKino

How do you usually find information about your favorite movie? How about newly released ones? Would you like to create a private list of movies to keep track of your watch history? Or maybe you'd like to create a playlist for your friend with all the Horror movies you like so your friend can wake up at night from terror as well? If so, I have an offer for you that you can't refuse.

<br>
MeKino is a web app that allows you to register, login, edit your profile, view trending/popular/top movie lists, search for movies by keywords, mark movies as watched, create private playlists and create shareable playlists.

<br>

# 1. Usage

## Using the app online

Please **[click on this link](https://mekino.elyorbek.com/)** to open the application in Heroku.

## Running the app locally

1. Download the contents of this github repo
2. Extract all the files into a folder
3. Create a PostgreSQL database called `mekino`
4. Open python3 and run the `app.py` file. I use iPython3 and use `%run app.py` command.
5. In python3, type in `db.create_all()` to create all the tables in the `mekino` PostgreSQL database.
6. Visit [TMDB](https://developers.themoviedb.org/3/getting-started/introduction) and sign up for your own API Key.
7. Create an environmental variable called API_KEY
8. Set the API_KEY environmental variable to the API_KEY you received from TMDB.
9. Open your terminal and go into the folder of the application
10. Type in `python3 -m venv venv` which will create a virtual environment for you
11. Type in `source venv/bin/active` which should add venv infront of your username.
12. Type in `pip install -r requirements.txt` which should install all the dependency packages.
13. Type in `export FLASK_ENV=development` which should set your flask server to development / debug mode.
14. Type in `flask run` which will start the server for you
15. Open the website url displayed by Flask. Its usually `http://127.0.0.1:5000/`

# 2. Pages

### _Trending_ - displays trending movies for this week from TMDB.

### _Popular_ - displays current popular movies from TMDB.

### _Top_ - displays top rate movies of all time from TMDB.

### _Search results_ - displays movie results based on the criteria provided in the search bar at the top of any page.

<br>
All the movies above are arranged in a card layout with a movie poster, movie title, release date and genres for each movie. At the bottom of the page there is pagination where you can go to next or previous page. Upon clicking on any movie card, it takes you to the movie details page.

<br>

# 3.Tech Stack

### [Vultr](https://vultr.com) - hosting this application, static resources and the database.

### [Gunicorn](https://gunicorn.org/) - python server for running our flask application on Heroku.

### [Github](https://github.com/about) - storing the source code of this web application.

### [HTML5](https://developer.mozilla.org/en-US/docs/Glossary/HTML) - creating the foundational elements and the layout of the pages.

### [CSS3](https://developer.mozilla.org/en-US/docs/Web/CSS) - styling of the elements created by HTML5.

### [JavaScript (ES2015+)](https://developer.mozilla.org/en-US/docs/Web/JavaScript) - performing DOM changes based on values or behaviors. Also used for redirecting and clipboard manipulation.

### [Axios JS](https://axios-http.com/docs/intro) - JavaScript library used for sending REST requests from the front-end to the server side.

### [Bootstrap v5.1](https://getbootstrap.com/docs/5.1/getting-started/introduction/) - Template based web framework used for creating responsive pages.

### [Bootstrap Icons](https://icons.getbootstrap.com/) - Standalone icon library used with over 1600 icons.

### [Python](https://www.python.org/about/) - programming language used as a foundation for our Flask application.

- `requests` - receiving REST requests on server-side and converting them into JSON format.
- `string` - generating a list of a-z and A-Z characters used for URL generation.
- `random` - randomly picking a letter for the URL generation.

### [Jinja2](https://jinja.palletsprojects.com/en/3.1.x/) - creating dynamic html files based on the data received from the back-end server.

### [Flask](https://flask.palletsprojects.com/en/2.1.x/) - Micro web development framework based on Python programming language.

- `render_template` - rendering Jinja 2 templates and passing variable into the template.
- `redirect` - redirecting the user to specific pages based on different logic.
- `session` - storing, retrieving and updating encrypted cookies.
- `flash` - showing one time messages to the user. useful for alerts and errors.
- `abort` - for triggering specific HTML error pages (Example: 404 page).
- `g` - allows to use global variables within Flask and Jinja 2 templates.

### [PostgreSQL](https://www.postgresql.org/) - a powerful yet free and open source RDBMS. Used for storing all of our user and playlist data.

### [SQL Alchemy (Flask version)](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) - an extension for the Flask application that allows us to interact with various RDBMS.

### [WTForms (Flask version)](https://flask-wtf.readthedocs.io/en/1.0.x/) - generating dynamic web forms based on python3 code.

### [BCrypt (Flask version)](https://flask-bcrypt.readthedocs.io/en/1.0.1/) - hashing of user passwords and verifying that the hashes are correct upon user logic.

<br>

# 4. How is TMDB API utilized at MeKino?

| Route                                        | Method | Query Params                                                                                       | Usage                                                      |
| -------------------------------------------- | ------ | -------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| genre/movie/list                             | GET    | NA                                                                                                 | Getting a list of all the genre ids and genre names        |
| trending/movie/week                          | GET    | page = `x` (where x is the pagination page number)                                                 | Getting the trending movies for this week.                 |
| movie/popular                                | GET    | page = `x` (where x is the pagination page number)                                                 | Getting the current popular movies.                        |
| movie/top_rated                              | GET    | page = `x` (where x is the pagination page number)                                                 | Getting Top rated movies of all time.                      |
| movie/`id` (where id is the id of the movie) | GET    | NA                                                                                                 | Getting all the details of a singular movie.               |
| movie/`id`/images                            | GET    | language = `en`                                                                                    | Getting all the English images of a singular movie.        |
| search/movie                                 | GET    | query = `q` (where q is the search term typed), page = `x` (where x is the pagination page number) | Getting all the results based on the search term criteria. |

**Note:** For all TMDB API requests, an `API_KEY` is required. If you are planning to use this project locally, you need to visit https://developers.themoviedb.org/3/getting-started/introduction and sign up for your own API Key and save it into a `API_KEY` environmental variable.
<br>

# 5. How are RESTful Routes configured?

| Route                       | Method | Login Required?                                                                                       | Query Params                                                                                                                    | Usage                                                                                                                                                         |
| --------------------------- | ------ | ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| /register                   | GET    | No                                                                                                    | NA                                                                                                                              | Displaying the registration form generated by WTForms.                                                                                                        |
| /register                   | POST   | No                                                                                                    | NA. Handled by WTForms                                                                                                          | Creating a new user with data provided in the WTForm                                                                                                          |
| /login                      | GET    | No                                                                                                    | NA                                                                                                                              | Displaying the login form generated by WTForms.                                                                                                               |
| /login                      | POST   | No                                                                                                    | NA. Handled by WTForms                                                                                                          | Authenticating the user with data provided by WTForms                                                                                                         |
| /profile_edit               | GET    | Yes                                                                                                   | NA                                                                                                                              | Displaying the profile edit form generated by WTForms.                                                                                                        |
| /profile_edit               | POST   | Yes                                                                                                   | NA. Handled by WTForms                                                                                                          | Updating the current user with the new data provided by WTForms.                                                                                              |
| /logout                     | GET    | No                                                                                                    | NA                                                                                                                              | Logging the user out                                                                                                                                          |
| /trending/`page`            | GET    | No                                                                                                    | `page` must be included in the url (not query param). used for pagination                                                       | Displaying a list of trending movies for the past week.                                                                                                       |
| /popular/`page`             | GET    | No                                                                                                    | `page` must be included in the url (not query param). used for pagination                                                       | Displaying a list of popular movies                                                                                                                           |
| /top/`page`                 | GET    | No                                                                                                    | `page` must be included in the url (not query param). used for pagination                                                       | Displaying a list of top movies of all time                                                                                                                   |
| /movie/`id`                 | GET    | Yes for marking as watched and adding to playlist functionality. Buttons are hidden if not logged in. | `id` must be included in the url (not query param). used for identifying the movie                                              | Showing the details of one singular movie                                                                                                                     |
| /movie/`id`/images          | GET    | No                                                                                                    | `id` must be included in the url (not query param). used for identifying the movie                                              | Showing the images in a slideshow for one singular movie                                                                                                      |
| /watched_unwatched          | PATCH  | Yes                                                                                                   | `mov_id` which is a movie id. `oper` which is an operation (w for mark wached. u for mark unwatched)                            | Marking the movie as watched / unwatched                                                                                                                      |
| /playlist/watched           | GET    | Yes                                                                                                   | NA                                                                                                                              | Displaying all the watched movies in a horizontal list.                                                                                                       |
| /playlist/create            | GET    | Yes                                                                                                   | NA                                                                                                                              | Displaying a WTForms for creating a new private playlist.                                                                                                     |
| /playlist/create            | POST   | Yes                                                                                                   | NA. Handled by WTForms                                                                                                          | Creating a new playlist based on the data received from WTForms.                                                                                              |
| /playlist/delete            | DELETE | Yes                                                                                                   | `plist_id` which is a playlist id.                                                                                              | Deleting a private playlist.                                                                                                                                  |
| /playlist/add_remove        | PATCH  | Yes                                                                                                   | `mov_id` which is a movie id. `plist_id` which is a playlist                                                                    | Adding a movie to a private playlist                                                                                                                          |
| /playlist/add_remove        | DELETE | Yes                                                                                                   | `mov_id` which is a movie id. `plist_id` which is a playlist                                                                    | Removing a movie to a private playlist                                                                                                                        |
| /playlist/private           | GET    | Yes                                                                                                   | NA                                                                                                                              | Displaying a list of private playlists on a page. Will have options to delete and share the playlist.                                                         |
| /playlist/private/`id`      | GET    | Yes                                                                                                   | `id` must be included in the url (not query param). `id` is the playlist id                                                     | Showing details of an individual private playlist. Has an option to delete or share the playlist.                                                             |
| /playlist/share             | PUT    | Yes                                                                                                   | `plist_id` which is a playlist id                                                                                               | Generating a random hash to be used as the URL of an external/shared playlist                                                                                 |
| /playlist/shared            | GET    | Yes                                                                                                   | NA                                                                                                                              | Displaying all the shared playlists on 1 page.                                                                                                                |
| /playlist/shared            | DELETE | Yes                                                                                                   | `plist_id` which is a playlist id                                                                                               | For deleting a shared playlist. The private playlist linked to the shared playlist will stay as is. Only unshares it.                                         |
| /playlist/shared/`url_code` | GET    | No                                                                                                    | `url_code` must be included in the url (not query param).                                                                       | Displaying the details of a shared playlist. Have an author name and button to copy the URL compared to private playlists. Does not have an option to delete. |
| /search/`q`/`page`          | GET    | No                                                                                                    | page and q must be included in the url (not query param). `page` is used for pagination. `q` is used for search term keyaowrds. | Displaying the results of a search performed by the TMDB API.                                                                                                 |

<br>

# 6. Data Schema and Relationships.

![Data Schema Image](/schema/Data_Schema.png)
<br>

## Relationships

1. `user` table

   - does not reference any tables or columns

2. `watched_movies` table

   - `user_id` references the `user` table `id` column

3. `playlist` table

   - `author` references the `user` table `id` column

4. `shared_playlist` table

   - `playlist_id` references the `playlist` table `id` column
   - `user_id` references the `user` table `id` column

5. `playlist_movies` table
   - `playlist_id` references the `playlist` table `id` column
