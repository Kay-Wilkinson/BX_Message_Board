from flask import (render_template, 
					request, 
					Blueprint)
from MessageBoard.models import Post, Attachment 
from flask import Blueprint

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int) #default page number of 1. Will throw an error if user passes anything other than an integer to the URL
    post = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=4) #Pass page number into query with page=page
    # attach_file = Attachment()
    return render_template('home.html', posts=post)


@main.route("/about")
def about():
    return render_template('about.html', title='About')