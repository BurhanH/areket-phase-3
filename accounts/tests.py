from django.contrib.auth import get_user_model
from django.test import TestCase

TEST_USER = 'test_user'
TEST_PASS = 'Supercallifragilisticexpialidocious!'
TEST_EMAIL = 'test_user@mail.com'

class AccountTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username=TEST_USER,
            email=TEST_EMAIL,
            password=TEST_PASS,
        )

    def test_signup_view(self):
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_login_view(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_functionality(self):
        self.assertTrue(
            self.client.login(username=TEST_USER, password=TEST_PASS),
            'Unable to log in with provided credentials')

    def test_logout_functionality(self):
        self.client.login(username=TEST_USER, password=TEST_PASS)
        session_id = self.client.session.session_key
        self.client.logout()
        self.assertNotEqual(
            session_id, self.client.session.session_key,
            'Something went wrong, getting equivalent session id, unable to log out')
