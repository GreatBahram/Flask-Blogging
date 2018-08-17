#!/usr/bin/env python3
# Author: GreatBahram

import os
import secrets

# third-party imports
from flask import current_app
from flask_mail import Message
from PIL import Image

# local imports
from blog import mail


def resent_email(user):
    token = user.get_reset_token()
    msg = Message(
            'Password Reset Request',
            sender='johni.mcafee@yandex.com',
            recipients=[user.email])
    msg.body = f"""To reset your password visit the following link:
{url_for('reset_token', token=token, _external=True)}
"""
    mail.send(msg)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    print(picture_path)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

