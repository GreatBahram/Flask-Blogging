# third-party imports
from flask import render_template

# local import
from . import home

@home.route('/')
@home.route('/home')
def homepage():
    """
    Render the homepage template on the / and /home route
    """
    return render_template('home/dashboard.html', title="Welcome")

@home.route('/post/<int:post_id>')
def postpage(post_id):
    """
    Render the homepage template on the /post
    """
    return render_template('home/post.html', title="Welcome")

@home.route('/about')
def about_page():
    """
    Render the about template on the /about route
    """
    return render_template('home/about.html', title="About")
