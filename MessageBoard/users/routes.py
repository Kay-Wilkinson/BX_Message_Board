from flask import (render_template, 
                    url_for, 
                    flash, 
                    redirect, 
                    request, 
                    Blueprint)
from flask_login import (login_user, 
                        current_user, 
                        logout_user, 
                        login_required)
from MessageBoard import db, bcrypt
from MessageBoard.models import User, Post, Attachment
from MessageBoard.users.forms import (RegistrationForm, 
                                    LoginForm, 
                                    UpdateAccountForm,
                                    RequestResetForm, 
                                    ResetPasswordForm)
from MessageBoard.users.utils import save_picture, send_reset_email
import logging 


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s:%(message)s:%(asctime)s')
file_handler = logging.FileHandler('user_routes.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created! You are now able to log in', 'success')
        logger.info(f'{user} registered at ') #should print the user registration data with the ascitime of creation
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        logger.info(f'{current_user.username} updated thier account details at ')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next') # I knew to use next as the param here from looking in the URI when browsing the site
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login was unsuccessful. Check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


# @users.route("/main.home")
@users.route("/user/<string:username>") #For some reason str does not work
def user_posts(username):
    page = request.args.get('page', 1, type=int) #default page number of 1. Will throw an error if user passes anything other than an integer to the URL
    user = User.query.filter_by(username=username).first_or_404()
    post = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5) #Pass page number into query with page=page
    return render_template('user_posts.html', posts=post, user=user)

@users.route("/reset_password",  methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent for you to reset your email. Don\'t forget to check your spam folder!', 'info')
        logger.info(f'User with email:{user} requested to reset at ')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>",  methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token) #This works because I pass in token to the User db and set it to the user_id 
    if not user:
        flash('Token expired or invalid.', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user.password = hashed_password #This will update the db via the ResetPasswordForm 
        db.session.commit()
        current_user.username = form.username.data
        flash('Your password has successfully updated.')
        logger.info(f'{current_user.username} updated their password at ')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)












