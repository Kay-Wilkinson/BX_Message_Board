from itsdangerous import TimedJSONWebSignatureSerializer as Serializer 
from datetime import datetime
from MessageBoard import db, login_manager
from flask import current_app
from flask_login import UserMixin 

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
        #1800 seconds == 30 mins. 

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    attachment = db.Column(db.String(20), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    #attachments = db.relationship('Attachment', backref='file_attachments', lazy=True) #one-to-many relationship between Post + Attachments as I want to link those.

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
	#Need Define one-to-many relationship between User.usernamne and Post as it will be the same usernanme regardless. use db.relationship for this


class Attachment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attachment = db.Column(db.String(20), nullable=True)
    post_attachment_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return f"Attachment('{self.attachment_file}'"







