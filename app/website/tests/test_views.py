from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class TestViews(TestCase):
    """
    Testing to see if Users can view our pages correctly.
    """

    def test_home_view(self):
        response = self.client.get(reverse("home"))
        #check to see if get request was successful
        self.assertEquals(response.status_code, 200)
        #check to see if the correct template was used
        self.assertTemplateUsed(response, 'home.html')
       

    def test_register_view(self):
        response = self.client.get(reverse("register"))
        #check to see if get request was successful
        self.assertEqual(response.status_code, 200) 
        #check to see if correct template was used
        self.assertTemplateUsed(response, 'register.html')

    """This is testing to see if a logged in user trys to access the register page,
       if they do they should be redirected back to the home page.
    """
    
    def test_authenticated_register_view(self):
        #creates the user and saves it in the test database
        user = User.objects.create_user(username='test', password='passpass22')
        #login
        response = self.client.post(reverse("home"), {
            'username':'test',
            'password':'passpass22'}, follow=True)
        #check if post request was successful
        self.assertEqual(response.status_code, 200)
        #check if user is authenticated (logged in)
        self.assertTrue(response.context['user'].is_authenticated)
        response = self.client.get(reverse("register"))
        #Should redirect to home page as user has already registered an account
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))
    
    """These two tests below check to see if an authenticated user is 
       viewing the generateSummary and generatePresentation pages correctly
    """
    
    def test_generateSummary_view_authenticated(self):
        #creates the user and saves it in the test database
        user = User.objects.create_user(username='test', password='passpass22')
        #login
        response = self.client.post(reverse("home"), {
            'username':'test',
            'password':'passpass22'}, follow=True)
        #check if post request was successful
        self.assertEqual(response.status_code, 200)
        #check if user is authenticated (logged in)
        self.assertTrue(response.context['user'].is_authenticated)
        response = self.client.post(reverse("generate_summary"))
        #check to see if post request was successful
        self.assertEqual(response.status_code, 200)
        #Check to see if correct template was used
        self.assertTemplateUsed(response, 'summary_generation.html')
    
    def test_generatePresentation_view_authenticated(self):
         #creates the user and saves it in the test database
        user = User.objects.create_user(username='test2', password='passpass22')
        #login
        response = self.client.post(reverse("home"), {
            'username':'test2',
            'password':'passpass22'}, follow=True)
        #check if post request was successful
        self.assertEqual(response.status_code, 200)
        #check if user is authenticated (logged in)
        self.assertTrue(response.context['user'].is_authenticated)
        response = self.client.post(reverse("generate_presentation"))
        #check if post request was successful
        self.assertEqual(response.status_code, 200)
        #Check to see if correct template was used
        self.assertTemplateUsed(response, 'presentation_generation.html')
    

    """These two tests below check to see if an unauthenticated user is trying to
       view the generateSummary and generatePresentation pages. If they are they will
       be redirected back to the home page.
    """    
    def test_generateSummary_view_not_authenticated(self):
        response = self.client.post(reverse("generate_summary"))
        self.assertEqual(response.status_code, 302)
        #Redirects user back to home page since user is not authenticated
        self.assertRedirects(response, reverse("home"))
    
    def test_generatePresentation_view_not_authenticated(self):
        response = self.client.post(reverse("generate_presentation"))
        self.assertEqual(response.status_code, 302)
        #Redirects user back to home page since user is not authenticated
        self.assertRedirects(response, reverse("home"))


