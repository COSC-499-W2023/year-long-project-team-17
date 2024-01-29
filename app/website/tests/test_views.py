from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.core.cache import cache

class TestViews(TestCase):

    #Creates the student and teacher groups for the tests needed for detect plagiarism view 
    def setUp(self) -> None:
        Group.objects.get_or_create(name='teacher')
        Group.objects.get_or_create(name='student')
        return super().setUp()

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

    def test_faq_view(self):
        response = self.client.get(reverse("faq"))
        #check to see if get request was successful
        self.assertEquals(response.status_code, 200)
        #check to see if the correct template was used
        self.assertTemplateUsed(response, 'faq.html')
    
    def test_contactUs_view(self):
        response = self.client.get(reverse("contact_us"))
        #check to see if get request was successful
        self.assertEquals(response.status_code, 200)
        #check to see if the correct template was used
        self.assertTemplateUsed(response, 'contact_us.html')

    """This is testing to see if a logged in user trys to access the register page,
       if they do they should be redirected back to the home page.
    """
    def test_authenticated_register_view(self):
        #creates the user and saves it in the test database
        user = User.objects.create_user(username='test1', email = 'test1@hotmailtestttt.com', password='passpass22')
        #login
        response = self.client.post(reverse("home"), {
            'username':'test1',
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
        user = User.objects.create_user(username='test2', email = 'test2@hotmailtestttt.com', password='passpass22')
        #login
        response = self.client.post(reverse("home"), {
            'username':'test2',
            'password':'passpass22'}, follow=True)
        #check if post request was successful
        self.assertEqual(response.status_code, 200)
        #check if user is authenticated (logged in)
        self.assertTrue(response.context['user'].is_authenticated)
        response = self.client.get(reverse("generate_summary"))
        #check to see if get request was successful
        self.assertEqual(response.status_code, 200)
        #Check to see if correct template was used
        self.assertTemplateUsed(response, 'summary_generation.html')
    
    def test_generatePresentation_view_authenticated(self):
        #creates the user and saves it in the test database
        user = User.objects.create_user(username='test3', email = 'test3@hotmailtestttt.com', password='passpass22')
        #login
        response = self.client.post(reverse("home"), {
            'username':'test3',
            'password':'passpass22'}, follow=True)
        #check if post request was successful
        self.assertEqual(response.status_code, 200)
        #check if user is authenticated (logged in)
        self.assertTrue(response.context['user'].is_authenticated)
        response = self.client.get(reverse("generate_presentation"))
        #check if get request was successful
        self.assertEqual(response.status_code, 200)
        #Check to see if correct template was used
        self.assertTemplateUsed(response, 'presentation_generation.html')
    
    def test_generateExercise_view_authenticated(self):
        #creates the user and saves it in the test database
        user = User.objects.create_user(username='test4', email = 'test4@hotmailtestttt.com', password='passpass22')
        #login
        response = self.client.post(reverse("home"), {
            'username':'test4',
            'password':'passpass22'}, follow=True)
        #check if post request was successful
        self.assertEqual(response.status_code, 200)
        #check if user is authenticated (logged in)
        self.assertTrue(response.context['user'].is_authenticated)
        response = self.client.get(reverse("generate_exercise"))
        #check if get request was successful
        self.assertEqual(response.status_code, 200)
        #Check to see if correct template was used
        self.assertTemplateUsed(response, 'exercise_generation.html')

    def test_virtualAssistant_view_authenticated(self):
        #creates the user and saves it in the test database
        user = User.objects.create_user(username='test5', email = 'test5@hotmailtestttt.com', password='passpass22')
        #login
        response = self.client.post(reverse("home"), {
            'username':'test5',
            'password':'passpass22'}, follow=True)
        #check if post request was successful
        self.assertEqual(response.status_code, 200)
        #check if user is authenticated (logged in)
        self.assertTrue(response.context['user'].is_authenticated)
        response = self.client.get(reverse("chatbot"))
        #check if get request was successful
        self.assertEqual(response.status_code, 200)
        #check to see if correct template was used
        self.assertTemplateUsed(response, 'chatbot.html')

    def test_detectPlagiarism_view_authenticated_teacher_group(self):
        #Creates as user with the teacher group and logs in
        response = self.client.post(reverse("register"),{ 
            'username' : 'bob12',
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
        response = self.client.get(reverse("detect_plagiarism"))
        #check if get request was successful
        self.assertEqual(response.status_code, 200)
        #Check to see if correct template was used
        self.assertTemplateUsed(response, 'plagiarism_detection.html')

    def test_detectPlagiarism_view_authenticated_student_group(self):
        #Creates as user with the student group and logs in
        response = self.client.post(reverse("register"),{ 
            'username' : 'bob13',
            'first_name' : 'Bob',
            'last_name' : 'Johnson',
            'email' : 'bobj13@hotmaill.com',
            'password1' : 'passpass22',
            'password2' : 'passpass22',
            'user_group' : 'student'
        })
        #If registration is successful then it will redirect to homepage
        self.assertEquals(response.status_code, 302) 
        #check if it redirects to home page after registeration 
        self.assertRedirects(response, reverse("home"))
        response = self.client.get(reverse("detect_plagiarism"))
        #Check to see if user is redirected to home page since user is part of the student group
        self.assertEqual(response.status_code, 302)
        #Redirects user back to home page since user is part of the student group
        self.assertRedirects(response, reverse("home"))

    """These two tests below check to see if an unauthenticated user is trying to
       view the generateSummary and generatePresentation pages. If they are they will
       be redirected back to the home page.
    """    
    def test_generateSummary_view_not_authenticated(self):
        response = self.client.get(reverse("generate_summary"))
        #If user is not authenticated then it will redirect to homepage
        self.assertEqual(response.status_code, 302)
        #Redirects user back to home page since user is not authenticated
        self.assertRedirects(response, reverse("home"))
    
    def test_generatePresentation_view_not_authenticated(self):
        response = self.client.get(reverse("generate_presentation"))
        #If user is not authenticated then it will redirect to homepage
        self.assertEqual(response.status_code, 302)
        #Redirects user back to home page since user is not authenticated
        self.assertRedirects(response, reverse("home"))

    def test_generateExercise_view_not_authenticated(self):
        response = self.client.get(reverse("generate_exercise"))
        #If user is not authenticated then it will redirect to homepage
        self.assertEqual(response.status_code, 302)
        #Redirects user back to home page since user is not authenticated
        self.assertRedirects(response, reverse("home"))

    def test_virtualAssistant_view_not_authenticated(self):
        response = self.client.get(reverse("chatbot"))
        #If user is not authenticated then it will redirect to homepage
        self.assertEqual(response.status_code, 302)
        #Redirects user back to home page since user is not authenticated
        self.assertRedirects(response, reverse("home"))

    def test_detectPlagiarism_view_not_authenticated(self):
        response = self.client.get(reverse("detect_plagiarism"))
        #If user is not authenticated then it will redirect to homepage
        self.assertEqual(response.status_code, 302)
        #Redirects user back to home page since user is not authenticated
        self.assertRedirects(response, reverse("home"))

