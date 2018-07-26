# third-party imports
from flask import render_template

# local imoprts
from . import errors

@errors.app_errorhandler(401)
def unauthorized(error):
    return render_template('errors/401.html', title='Unauthorized'), 401

@errors.app_errorhandler(403)
def forbidden(error):
    return render_template('errors/403.html', title='Forbidden'), 403

@errors.app_errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html', title='Page Not Found'), 404

@errors.app_errorhandler(500)
def internal_server_error(error):
    return render_template('errors/500.html', title='Server Error'), 500
