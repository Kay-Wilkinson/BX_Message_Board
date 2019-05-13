import unittest
from flask.ext.testing import TestCase 
from MessageBoard import app, db 
from MessageBoard.posts.forms import PostForm, UploadForm
from MessageBoard.config import TestingConfig  
from MessageBoard.unit_tests.base_test import BaseTestCase
#Below class to be put in utils file!!

class PostFormTest(BaseTestCase):

    def correct_form_submission_test(self):
        form = PostForm(
            title = "Cereal Box Testing One",
            content = "Running Unit Tests - Form validation for post updates."
        self.assertTrue(form.validate())

    def invalid_form_submission_test(self):
        # Parsing empty data should invalidate the DataRequired() fields in the form submission
        form = FormForm(
            title = "",
            content = ""
        self.assertFalse(form.validate())


class UploadFormTest(BaseTestCase):

    def attachment_file_type_test(self):
        # Ensure correct data validates. 
        # Only 'gif', 'jpeg', 'png' and 'txt' should pass the FileAllowed() validation
        file_type = UploadForm(attachment = "default.png")
        self.assertTrue(form.validate())

    def invalid_attachment_file_type_test(self):
        # Ensure invalid file type throws error.
        file_type = UploadForm(attachment = "random_file.pdf")
        self.assertTrue(form.validate())


if __name__ == '__main__':
    unittest.main()
