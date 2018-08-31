# third-party imports
from flask import render_template

# local import
from . import admin
from blog.admin.forms import CreatePostForm
from blog.models.post import PostModel

@admin.route('/add_post')
def add_post():
    """
    Create an new post
    """
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = PostModel()
        new_post.save_to_db()
    return render_template('admin/add_post.html', title="Add Post", form=form)

@admin.route('/edit_post/<int:post_id>')
def edit_post(post_id):
    """
    Edit a post
    """
    pass

@admin.route('/delete_post/<int:post_id>')
def delete_post(post_id):
    """ 
    Delete a post
    """
    pass

