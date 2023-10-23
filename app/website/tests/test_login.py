from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class TestLogin(TestCase):
    """These three test simulate a user trying to login to their account. 
    If a user logs in with the correct login info their account will be 
    authenticated; if the user's password or username is incorrect they will
    not be authenticated meaning logged in.
    """

    def test_login(self):
        #creates the user and saves it in the test database
        user = User.objects.create_user(username='test', password='passpass22')
        response = self.client.post(reverse("home"), {
            'username':'test',
            'password':'passpass22'}, follow=True)
        #check if post response was a success
        self.assertEqual(response.status_code, 200)
        #Should return true if user is logged in
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_wrongPass(self):
        #creates the user and saves it in the test database
        user = User.objects.create_user(username='test', password='passpass22')
        response = self.client.post(reverse("home"), {
            'username':'test',
            'password':'passpass2224'}, follow=True)
        #check if post response was a success
        self.assertEqual(response.status_code, 200)
        #Should return false since the password is wrong
        self.assertFalse(response.context['user'].is_authenticated)

    def test_login_wrongUsername(self):
        #creates the user and saves it in the test database
        user = User.objects.create_user(username='test', password='passpass22')
        response = self.client.post(reverse("home"), {
            'username':'testtt',
            'password':'passpass22'}, follow=True)
        #check if post response was a success
        self.assertEqual(response.status_code, 200)
        #Should return false since the username is wrong
        self.assertFalse(response.context['user'].is_authenticated)

