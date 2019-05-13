from flask.ext.testing import TestCase 
from MessageBoard.config import TestingConfig
from MessageBoard import app, db 

class BaseTestCase(TestCase):
    # A base test case for all Flask Testing - Handles set-up and tear down
    def create_app(self):
        app.config.from_object('MessageBoard.config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        user = User(username = "CerealBoxTesting", email = "cerealbox@spotx.tv", password = "admin_user")
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()