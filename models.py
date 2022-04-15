"""SQL Alchemy Data Models for MeKino Web App.

MeKino Flask Web Application

Made by: Elyorbek Khudaybergenov
Github Profile: https://github.com/khelyorbek

This product uses "The Movie Database" API but is not endorsed or certified by TMDB.	
Find out more abour TMDB API: https://www.themoviedb.org/documentation/api
TMDB API docs for developers: https://developers.themoviedb.org/3
"""
# Importing all the required libraries
from __future__ import unicode_literals
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Initializing Database Connection and Password Hashing
db = SQLAlchemy()
bcrypt = Bcrypt()

# Connecting to the database in app
def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """Data model for the user table"""
    # Table name
    __tablename__ = 'user'

    # Table columns
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(35), nullable=False)
    last_name = db.Column(db.String(35), nullable=False)
    username = db.Column(db.String(15), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)

    # Relationships
    playlists = db.relationship('Playlist', backref="author_obj")
    shared_playlists = db.relationship('Shared_Playlist')

    @classmethod
    def register(cls, fname, lname, uname, pwd):
        """Register user w/hashed password and return user"""
        # take password and generate hash using bcrypt
        hashed = bcrypt.generate_password_hash(pwd)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")
        # return instance of user w/username and hashed pwd
        return cls(username=uname, password=hashed_utf8, first_name=fname, last_name=lname)

    @classmethod
    def authenticate(cls, uname, pwd):
        """Validate that user exists & password is correct.
        Return user if valid; else return False.
        """
        # Finding the first result from the User object that matched the username passed to this method
        u = User.query.filter_by(username=uname).first()
        # Using bcrpyt to make sure the password hash matches the one in DB
        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance if matched
            return u
        else:
            # else return False
            return False

class Playlist(db.Model):
    """Data model for the playlist table"""
    # Table Name
    __tablename__ = 'playlist'

    # Columns
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    author = db.Column(db.Integer, db.ForeignKey('user.id')) # FK on table user column id

    # Relationships
    movies = db.relationship('Playlist_Movies', cascade='all, delete')

class Shared_Playlist(db.Model):
    """Data model for shared playlists"""
    # Table name
    __tablename__ = 'shared_playlist'

    # Columns
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id', ondelete="CASCADE")) # FK on table playlist column id
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE")) # FK on table user column id
    # URL code must be unique because we don't want 2 playlists to have same URL
    url_code = db.Column(db.String(20), nullable=False, unique=True)

    # Relationships
    playlist = db.relationship('Playlist')

class Playlist_Movies(db.Model):
    """Data model for playlist to movie mapping"""
    # Table name
    __tablename__= 'playlist_movies'

    # Columns
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id', ondelete="CASCADE")) # FK on table playlist column id
    movie_id = db.Column(db.Integer, nullable=False)

class Watched_Movies(db.Model):
    """Data model for marking movies as watched"""
    # Table Name
    __tablename__ = 'watched_movies'

    # Columns
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # FK on table user column id
    movie_id = db.Column(db.Integer, nullable=False)

    # Relationships
    user = db.relationship('User', backref="watched_movies")
    

