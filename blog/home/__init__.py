#app/home/__init__.py

from flask import Blueprint, render_template

home = Blueprint('home', __name__)

from . import views
