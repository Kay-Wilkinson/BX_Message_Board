'''
*Basic Set Up*

Set env variable to MessageBoard.py 

$ export FLASK_APP=MessageBoard.py

This then enables us to run the below cmd to get the app running 
$ flask run 
This should open up the py file in 120.0.0.1:5000

Set server to auto-update any changes made:
(ctrl c first!)
$ export FLASK_DEBUG=1
$ flask run 

To run MessageBoard.py directy with python, add the if __name__ == '__main__' conditional,
rather than running the file via the env variable (flask run)
This is useful as you don't need to set env variable each time you open your terminal
back up (can otherwise set env variable to run on virtual env start-up but hey ho, hacky project here)
Test this by running
$ python MessageBoard.py

*Templates*
Access html pages from the MessageBoard file -
add render_templates to the Flask import
from flask import Flask, render_template
Then in the various @app.route() decorated functions (like def home()), return the html file as the output
using the render_template() method. Just pass in the file path and or name to the html doc into the render_templates
method. 

Dynamically pass json objects to html pages by looping over json content (using render_template() and the Jinja2 engine in Flask)
Make sure to pass that in as an argument to the render_template() method! 

I've created templates that will inherit html from a parent file (layout.html) - this is to avoid repeating myself
and so I only have to update code in one place. 
When ending the code block in the Jinja2 renders, you don't have to be explicit in what code block you are ending.
I have decided to be explicit though as it can be easy to lose track of which code blocks are what when having many
many templates. 
{% endblock content%} and {% endblock visuals %} rather than {% endblock %} {% endblock %}

*Adding CSS*
Static files like html and css need to be in a static file. 
Make sure to replace the path to the css file from your html files using the Jinja2 notation (add add url_for method to import in py file)

*Create Forms*
Creating forms can be a pain for form validation (regular expressions for inserting email, password validation etc.) so I am using a Flask
module here so not to re-invent the wheel. 
$ pip install flask-wtf

I'm using Python classes that will be parsed into html forms here rather than straight-up creating a HTML form from scratch in order to use some 
of that functionality. 
Additionally, I want people to stay logged in for a while so need to set cookie info for that (can do this via the BooleanField module). To keep this
safe from easy XSS attacks etc. I need to protect that cookie info so will be setting a secret key. 
I set this using app.config settings in the MessageBoard.py file. 
To generate a random string that would work as a key, use the following:
$ python
$ import secrets
>>> secrets.token_hex(16)
^^ I'll want to set this as an env variable later :) 

form.hidden_tag() --> This adds a CRF (Cross Site Reference) token to protect against certain attacks
To make sure that the forms will actually submit, don't forget to add GET and POST methods to the register @app route

*DB Setup*

I need a DB to hold user creds, posts etc. 
I also want to extend towards the Shadows and Tableau databases for future add-ons to this project. 

Using SQLAlchemy ORM so I can connect to both mysql, hadoop (and whatever else I want to connect to) later. 
(I just need to pass in a different url). I'm doing this to future-proof the app for it's data-piplines for
as long as possible.
I'm using the flask-sqlalchemy distribution as it provides some handy extensions for Flask

$ pip install flask-sqlalchemy 

For the DB itself, I am using sql_lite as it's jsut easy to set up. 
/// for path to relative file 

Create db by declaring objects in py file. Then create and test the db with:
$ python
>>> from MessageBoard import db
/Users/kaywilkinson/.venvs/MessageBoard/lib/python3.6/site-packages/flask_sqlalchemy/__init__.py:794: FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.  Set it to True or False to suppress this warning.
  'SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and '
>>> db.create_all()
>>> from MessageBoard import User, Post
>>> user_1 = User(username='Test', email='k@test.com', password='test')
>>> db.session.add(user_1)
>>> user_2 = User(username='JaneDoe', email='jd@test.com', password='test2')
>>> db.session.add(user_2)
>>> db.session.commit()
>>> User.query.all()
[User('Test', 'k@test.com', 'default.jpg'), User('JaneDoe', 'jd@test.com', 'default.jpg')]
>>> User.query.first()
User('Test', 'k@test.com', 'default.jpg')
>>> User.query.filter_by(username='Test').all()
[User('Test', 'k@test.com', 'default.jpg')]
>>> User.query.filter_by(username='Test').first()
User('Test', 'k@test.com', 'default.jpg')
>>> user = User.query.filter_by(username='Test').first()
>>> user
User('Test', 'k@test.com', 'default.jpg')
>>> user.id
1
>>> user = User.query.get(1)
>>> user
User('Test', 'k@test.com', 'default.jpg')
>>> user.posts
[]
>>> post_1 = Post(title='Blog 1', content='Cereal Box Testing', user_id=user.id) 
>>> post_2 = Post(titel='Update 2', content='Special K cereal', user_id=user.id)
>>> post_2 = Post(title='Update 2', content='Special K cereal', user_id=user.id)
>>> db.session.add(post_1)
>>> db.session.add(post_2) 
>>> db.session.commit()
>>> user.posts
[Post('Blog 1', '2019-01-13 12:08:59.032600'), Post('Update 2', '2019-01-13 12:08:59.033236')]
>>> for post in user.posts:
...     print(post.title)
... 
Blog 1
Update 2
>>> post = Post.query.first()
>>> 
>>> post
Post('Blog 1', '2019-01-13 12:08:59.032600')
>>> post.user_id
1
>>> post.author
User('Test', 'k@test.com', 'default.jpg')
>>> db.drop_all()
>>> db.create_all()
>>> User.query.all()
[]
>>> Post.query.all()
[]
>>> 


*Convert to package* 
To to avoid circular imports when doing this. This can be caused by the if/main conditional as app. Look at flask-at-scale py con talk
Need to set up code to have MessageBoard not running directly - by running the whole directory as a package. 
Do this by setting up a __init__.py file. 
After mirgrating packages around - start running the package using:
$ python run.py
May need to re-create db again because of restructure 

*User Authentication*
$  pip install flask-bcrypt
>>> from flask_bcrypt import Bcrypt
>>> bcrypt = Bcrypt()
>>> bcrypt.generate_password_hash('testing') 
b'$2b$12$V3JCqu6maLnG5/fdts4eOen5g7rlSllUkJPD/XJLollfcfDJznkly'
>>> bcrypt.generate_password_hash('testing').decode('utf-8')
'$2b$12$AUXTA9kggFAX/xAMhR5lqOZsbnSOvuvi/5t7ZWu5aDBrCjBvnHhg6'

^^ used decode('utf-8') to change from bytes to string 

>>> hashed_pw = bcrypt.generate_password_hash('testing').decode('utf-8')
>>> bcrypt.check_password_hash(hashed_pw, 'password')
False
>>> bcrypt.check_password_hash(hashed_pw, 'testing')


Put this in for better error display
enctype="multipart/form-data"

*Pagination and sorting posts

$ workon MessageBoard
$ python
>>> from MessageBoard.models import Post
>>> posts.Post.query.paginate()
>>> posts = Post.query.paginate()
>>> posts
<flask_sqlalchemy.Pagination object at 0x108efffd0>
>>> dir(posts)
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'has_next', 'has_prev', 'items', 'iter_pages', 'next', 'next_num', 'page', 'pages', 'per_page', 'prev', 'prev_num', 'query', 'total']
>>> posts.per_page
20
>>> posts.page
1
>>> for post in posts.items:
...     print(post)
... 
Post('Cereal Box', '2019-01-13 20:01:51.555162')
Post('Test updating post', '2019-01-13 20:27:28.113338')
Post('Test upload', '2019-01-13 22:51:39.181061')
>>> 
>>> posts = Post.query.paginate(per_page=5) 

This will set the number of posts per page to 5 
Add a loop to loop over home page (use Jinja2) to display the next batch of posts.
Add buttons to flick between pages

use order_by(Post.date_posted(desc)) to show the latest posts. 
Need to put this to our home page and any other page that will show posts so update routes.py accordingly

Link username in post bootsrrap-card to a list of thier posts (will be useful for tracking personal updates)

*Email reset and password reset*

Need to add an element of time senstitivity here for reset
Link email to password reset. 
Probably use mail_gun for this 

Time dependency on password update - 

$ python 
$ from itsdangerous import TimedJSONWebSignatureSerializer as Serializer 
# Pass in a secret key and a timer 
>>> s = Serializer('secret', 30)
>>> token = s.dumps({'user_id': 1}).decode('utf-8')
>>> token
'eyJhbGciOiJIUzI1NiIsImlhdCI6MTU0NzUwNjIzMCwiZXhwIjoxNTQ3NTA2MjYwfQ.eyJ1c2VyX2lkIjoxfQ.BQbdnDknZIbsbxKyr1lof3IxdI9EI6vUSd7YsQqXgsU'
>>> s.loads(token)
{'user_id': 1}
>>> s.loads(token)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/kaywilkinson/.venvs/MessageBoard/lib/python3.6/site-packages/itsdangerous.py", line 807, in loads
    date_signed=self.get_issue_date(header))
itsdangerous.SignatureExpired: Signature expired


*Blueprints

Refactored to use blueprints as the application grows.
As blueprints are ran as packages, each directory needs an __init__.py file. 
This can be kept empty :) 
This init file is then read as __main__

create blueprint instance with this template

from flask import Blueprint

bp_name = Blueprint('bp_name', __name__)


Then add the blueprint to the config.py file -
e.g. 
from MessageBoard.main.routes import main
or .. from flask_application_name.directory_name.python_file_that_handles_page_routing import __name__

Then below that block, register the blueprint

app.register_blueprint(users)

*Spotx email only

I added functionality to the register form to only accept Spotx emails via regexp in the form validation.


* Unit/Integration Test Suite *

Used Flask-Testing extension over unittest in the end. Can add unittest func. later if need be.
Test suite to check forms.py across templates work as expected. 
Created a set up/tear down context manager as the BaseTestCase. 
Extended test suite to use a seperate DB for testing instances. 
Future plans are to use mocks instead of this in order to be closer to actual unittests, rather that
at current, being more likle integration tests so to speak. 

Added TestSuite DB to config.py
Added unit_tests directory to hold test suite 

For future API/Data-Visualisaton functionality, I'll want to set up some unittest.mock instances that 
will mimic the api instance. Important as it is an integration with a third party .

This site was super useful for this: https://github.com/mjhea0/flask-basic-registration/blob/master/project/config.py

'''









