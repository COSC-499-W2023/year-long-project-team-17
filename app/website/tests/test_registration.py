from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import  User


class TestRegistration(TestCase):
    """These three tests simulate a user trying to register for an
    account. If registration is successful meaning they passed valid data
    they will be redirected back to the home page and the count of all users should be 
    1 in the test database. If not successful (invalid data), then the 
    user stays on the registration page and user count is 0 in the test database.
    """
    def test_signup(self):
        response = self.client.post(reverse("register"),{
            'username' : 'bob12',
            'first_name' : 'Bob',
            'last_name' : 'Johnson',
            'email' : 'bobj@hotmaill.com',
            'password1' : 'passpass22',
            'password2' : 'passpass22'
        })
        #If registration is successful then it will redirect to homepage
        self.assertEquals(response.status_code, 302) 
        #check if it redirects to home page after registeration 
        self.assertRedirects(response, reverse("home"))
        #Gets all user objects in test database
        users = User.objects.all()
        self.assertEquals(users.count(), 1)

    def test_signup_no_data(self):
        response = self.client.post(reverse("register"))
        #checks to see if post request was successful
        self.assertEquals(response.status_code, 200)
        #checks to see if sign up form is invalid, should return false 
        self.assertFalse(response.context['form'].is_valid())
        self.assertEquals(len(response.context['form'].errors), 6) #6 errors cause by 6 empty fields in form 
        #check to see if a user was created should be 0 since no data is passed
        self.assertEquals(User.objects.all().count(), 0)

    def test_signup_invalid_data(self):
        response = self.client.post(reverse("register"), {
            'username':'bob13',
            'first_name' : 'Bob',
            'last_name' : 'Johnson',
            'email' : 'bobjhotmaill.com',
            'password1' : 'passpass22',
            'password2' : 'passpass22'
        })
        #checks to see if post request was successful
        self.assertEquals(response.status_code, 200)
        #checks to see if sign up form is invalid, should return false 
        self.assertFalse(response.context['form'].is_valid())
        self.assertEquals(len(response.context['form'].errors), 1) # 1 error caused by invalid email
        #check to see if a user was created should be 0 since email is invalid
        self.assertEquals(User.objects.all().count(), 0)

