import unittest
from MessageBoard.users.forms import (RegistrationForm, 
									LoginForm, 
									RequestResetForm, 
									ResetPasswordForm)
from MessageBoard.unit_tests.base_test import BaseTestCase

class RegistrationFormTest(BaseTestCase):

    def test_validate_success_register_form(self):
        # Ensure only Spotx email addresses can validate.
        form = RegistrationForm(
            email = 'cerealbox@spotx.tv',
            password='example', confirm='example')
        self.assertTrue(form.validate())

    def test_validate_invalid_password_format(self):
        # Ensure non-Spotx email addresses do not validate.
        form = RegistrationForm(
            email = 'randomPenTest@randomEmail.com',
            password='example', confirm='')
        self.assertFalse(form.validate())

    def test_validate_email_already_registered(self):
        # Ensure user can't register when a duplicate email is used
        form = RegistrationForm(
            email = 'cerealbox@spotx.tv',
            password = 'test',
            confirm = 'test'
        )
        self.assertFalse(form.validate())


class LoginFormTest(BaseTestCase):

    def test_validate_success_login_form(self):
        # Ensure correct data validates.
        form = LoginForm(email='cerealbox@spotx.tv', password='test')
        self.assertTrue(form.validate())

    def test_validate_invalid_email_format(self):
        # Ensure invalid email format throws error.
        form = LoginForm(email='unknown', password='example')
        self.assertFalse(form.validate())


if __name__ == '__main__':
    unittest.main()
