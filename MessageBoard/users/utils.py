import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from MessageBoard import mail

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)

    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Message Board Password Reset Request', sender='kwilkinson@cerealbox.com', recipients=[user.email])
    msg.body = f'''
Well hello there,

To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
        
( ͡° ͜ʖ ͡°) ...Weren't expecting a message from me? 
        

Not to worry - just ignore this email and no changes can be made.
It would be great if you let me know that you recieved this in error though.

Kind regards,

K.Wilkinson 

'''
#Keep the above f string formatting against the margin or it messes up the formatting and readability of the email
    mail.send(msg)
