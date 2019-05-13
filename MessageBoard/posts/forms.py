from flask_wtf import FlaskForm
from wtforms import (StringField, 
					SubmitField, 
					TextAreaField,
					FileField)
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed 

class PostForm(FlaskForm):
	title = StringField('Title', 
						validators=[DataRequired()])
	content = TextAreaField('Content', 
							validators=[DataRequired()])
	attachment = FileField('Attach an image',
						validators=[FileAllowed(['gif', 'jpeg', 'png'])])
	submit = SubmitField('Post')

class UploadForm(FlaskForm):
    attachment = FileField('Add an Attachment',
						validators=[FileAllowed(['gif', 'jpeg', 'png', 'txt'])])
    submit = SubmitField('Upload File')

 #    def validate_image(form, field):
 #        if field.data:
 #            field.data = re.sub(r'[^a-z0-9_.-]', '_', field.data)

	# def upload(request):
	#     form = UploadForm(request.POST)
	#     if form.image.data:
	#         image_data = request.FILES[form.image.name].read()
	#         open(os.path.join(UPLOAD_PATH, form.image.data), 'w').write(image_data)