from django.test import TestCase
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.models import User

class TestLogout(TestCase):
    """
    This test simulates a user who is authenticated trying to log out of their
    account; if successful the user should be redirected back to the home page
    and their account is no longer authenticated.    
    """
    
    def test_logout(self):    
         #creates the user and saves it in test database
        user = User.objects.create_user(username='test', password='passpass22')
        response = self.client.post(reverse("home"), {
            'username':'test',
            'password':'passpass22'}, follow=True)
        #check if post response was a success
        self.assertEqual(response.status_code, 200)
        #Check if user is logged in 
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        #log out
        response = self.client.get(reverse("logout"))
        user = auth.get_user(self.client)
        #Should redirect home after logging out
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))
        #Should return false if user logged out successfully
        self.assertFalse(user.is_authenticated)
    