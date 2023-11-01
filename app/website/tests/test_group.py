from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import  User, Group

class TestGroup(TestCase):

    #Creates the student and teacher groups for the test 
    def setUp(self) -> None:
        Group.objects.get_or_create(name='teacher')
        Group.objects.get_or_create(name='student')
        return super().setUp()

    
    """
    These tests below check to see if a user given a role (student or teacher) 
    can access certain pages of the site or are denied access.
    """

    #checks to see if user with teacher role can access detect_plagiarism page correctly
    def test_role_teacher_plagiarism_access(self):
        response = self.client.post(reverse("register"),{ 
            'username' : 'bob17',
            'first_name' : 'Bob',
            'last_name' : 'Johnson',
            'email' : 'bobj@hotmaill.com',
            'password1' : 'passpass22',
            'password2' : 'passpass22',
            'user_group' : 'teacher'
        })
        #If registration is successful then it will redirect to homepage
        self.assertEquals(response.status_code, 302) 
        #check if it redirects to home page after registeration 
        self.assertRedirects(response, reverse("home"))
        #Gets all user objects in test database
        users = User.objects.all()
        self.assertEquals(users.count(), 1)
        response = self.client.post(reverse("home"), {'username':'bob17', 'password':'passpass22'}, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
        response = self.client.post(reverse("detect_plagiarism"))
        #check if post request to plagiarism page was success
        self.assertEquals(response.status_code, 200)
        

    #checks to see if user with student role is denied access to detect_plagiarism page correctly
    def test_role_student_plagiarism_access(self):
        response = self.client.post(reverse("register"),{ 
            'username' : 'bob14',
            'first_name' : 'Bob',
            'last_name' : 'Johnson',
            'email' : 'bobj@hotmaill.com',
            'password1' : 'passpass22',
            'password2' : 'passpass22',
            'user_group' : 'student'
        })
        #If registration is successful then it will redirect to homepage
        self.assertEquals(response.status_code, 302) 
        #check if it redirects to home page after registeration 
        self.assertRedirects(response, reverse("home"))
        #Gets all user objects in test database
        users = User.objects.all()
        self.assertEquals(users.count(), 1)
        self.client.login(username="bob14", password="passpass22", follow=True)
        response = self.client.post(reverse("detect_plagiarism"))
        #check if post request to plagiarism page was a redirect to home page due to student role
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))

