"""For creation of dynamic forms using WTForms

MeKino Flask Web Application

Made by: Elyorbek Khudaybergenov
Github Profile: https://github.com/khelyorbek

This product uses "The Movie Database" API but is not endorsed or certified by TMDB.	
Find out more abour TMDB API: https://www.themoviedb.org/documentation/api
TMDB API docs for developers: https://developers.themoviedb.org/3
"""
# importing the necessary libraries
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField 
from wtforms.validators import InputRequired, Length

# Registration form
class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[InputRequired(), Length(max=35)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=35)])
    username = StringField("Username", validators=[InputRequired(), Length(max=15)])
    password = PasswordField("Password", validators=[InputRequired()])

# Logic form
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(max=15)])
    password = PasswordField("Password", validators=[InputRequired()])

# Edit Profile forms
class UserEditForm(FlaskForm):
    first_name = StringField("First Name", validators=[InputRequired(), Length(max=35)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=35)])
    username = StringField("Username", validators=[InputRequired(), Length(max=15)])
    password = PasswordField("Password", validators=[InputRequired()])

# Create a new playlist form
class CreateNewPlaylistForm(FlaskForm):
    name = StringField("Playlist Name", validators=[InputRequired(), Length(max=40)])