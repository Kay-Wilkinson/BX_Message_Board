import os
import secrets
from PIL import Image
from flask import url_for, current_app


def save_attachment(form_attachment):
	attachment = form_attachment
	attachment_path = os.path.join(
									current_app.root_path, 
									'static/attachments', 
									attachment)
	output_size = (400, 600)
	attach = Image.open(attachment_path)	
	attach.save(attachment_path)
	return attach



    # random_hex = secrets.token_hex(8)
    # _, f_ext = os.path.splitext(form_attachment.filename)
    # attachment_fn = random_hex + f_ext
    # attachment_path = os.path.join(current_app.root_path, 'static/attachments', attachment_fn)

    # output_size = (400, 600)
    # attach = Image.open(form_attachment_path)
    # attach.thumbnail(output_size)

    # attach.save(attachment_path)

    # return attachment_fn

# save_attachment('~/Downloads/Benelux.png')


# def save_picture(form_picture):
#     random_hex = secrets.token_hex(8)
#     _, f_ext = os.path.splitext(form_picture.filename)
#     picture_fn = random_hex + f_ext
#     picture_path = os.path.join(current_app.root_path, 'static/attachments', picture_fn)

#     output_size = (125, 125)
#     i = Image.open(form_picture)
#     i.thumbnail(output_size)

#     i.save(picture_path)

#     return picture_fn

# save_picture('~/Downloads/Benelux.png')