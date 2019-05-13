from flask import Blueprint
from flask import (render_template,
                    url_for,
                    flash,
                    redirect,
                    request,
                    abort,
                    Blueprint)
from flask_login import current_user, login_required
from MessageBoard import db
from MessageBoard.models import Post, Attachment 
from MessageBoard.posts.forms import PostForm, UploadForm 
from MessageBoard.posts.utils import save_attachment
import logging 

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
formatter = logging.Formatter('%(levelname)s:%(message)s:%(asctime)s')
file_handler = logging.FileHandler('posts_routes.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

posts = Blueprint('posts', __name__)
# I have not added logging to many of these as it felt a little excessive for every update and 
# to be honest, a bit invasive. 
@posts.route("/post/new", methods = ['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        # if form.attachment.data:
        #     attachment = save_attachment(form.attachment.data)
        #     attachment = attachment
        post = Post(
                    title=form.title.data, 
                    content=form.content.data, 
                    # attachment=form.attachment.data, 
                    author=current_user
                    )
        db.session.add(post)
        db.session.commit()
        flash('Your message has been posted.', 'success')
        return redirect(url_for('main.home'))
    # attachment = url_for('static', filename='attachments/' + attachment)
    return render_template('create_post.html', title='Create Post', 
                            form=form, legend="Post an Update")

# @posts.route("/post/new", methods=['GET', "POST"])
# @login_required
# def upload_attachment():
#     attachment = UploadForm()
#     if attachment.validate_on_submit():
#         attachment = save_attachment(attachment.attachments.data)
#         db.session.add(attachment)
#         db.session.commit()
#         flash('Your attachment has been successfully uploaded', 'success')
#         return redirect(url_for('main.home'))
#     return render_template('create_post.html', title='Create Post', 
#                             form=attachment, legend="Upload an Attachment") 

@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    #attach_form = UploadForm()
    if post.author != current_user:
        abort(403)
        logger.warning(f'{current_user} attempted to update a post made by {post.author}')
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        form.attachment = form.attachment.data 
        #logic for adding updating attachments via the UploadForm, only if user (via post) is authenticated.
        #May need to put the attach logic outside that if statement though as it might be the wrong scope...or
        # have if form.validate_on_submit() and or attach_form.validate_on_submit()??
        db.session.commit()
        flash('Your update has been successfully edited', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        # attach_form.attachment= attach_form.attachment.data

        # Not sure about keeping the above line as I am not sure I want to make GET requests 
        # to display attachments if they are super big. No need to view the attachement really, 
        # just update/delete them

    return render_template('create_post.html', title='Update Post', 
                            form=form, legend="Edit Your Update")


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
        logger.warning(f'{current_user} attempted to delete a post made by {post.author}')
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))


