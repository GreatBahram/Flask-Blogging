# third-party imports
from flask import render_template, abort
from flask_login import current_user, login_required

# local import
from . import admin
from blog.admin.forms import CreatePostForm
from blog.models.post import PostModel

@admin.route('/admin/dashboard')
def admin_dashboard():
    """

    """
    if not current_user.is_admin:
        abort(403)

    return render_template('home/admin_dashboard.html', title='Admin Dashboard')

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

