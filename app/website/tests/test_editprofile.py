from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import FileSystemStorage
import logging

class TestEditProfile(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username='test11', email = 'test11@hotmailtt.com', password='passpass22', first_name='Bob',last_name='Johnson')
        #create second user to test username already exists error
        self.user2 = User.objects.create_user(username='test12', email = 'test12@hotmailtt.com', password='passpass22', first_name='Dave',last_name='Johnson')
        self.client.force_login(self.user)
        #disable logging for theses tests so that DEBUG:PIL.Image is ignored
        logging.disable(logging.CRITICAL)
        return super().setUp()

    #Test changing all fields for user settings
    def test_all_settings_updated_successful(self):
        response = self.client.post(reverse("edit_profile"), {
            'username':'test13',
            'first_name':'Bobby',
            'last_name':'Wilson',
            'email':'test13@hotmailtt.com',
            'settings_form':True
        }, follow=True)
        #check if post request was a success
        self.assertEqual(response.status_code, 200)
        #check if a user exists containing all of the updated information
        self.assertTrue(User.objects.filter(username = 'test13', first_name='Bobby', last_name='Wilson', email='test13@hotmailtt.com').exists())
        #Check to see if correct template was used 
        self.assertTemplateUsed(response, 'edit_profile.html')

    #Test chosening a taken username
    def test_unsuccessful_username_taken(self):
        response = self.client.post(reverse("edit_profile"), {
            'username':'test12',
            'first_name':'Bobby',
            'last_name':'Wilson',
            'email':'test13@hotmailtt.com',
            'settings_form':True
        }, follow=True)
        #check if post request was a success
        self.assertEqual(response.status_code, 200)
        form = response.context['settings_form']
        #print(form.errors['username'][0])
        #check if form has 1 error (username is taken)
        self.assertEqual(len(form.errors), 1)
        #check if a user exists containing all of the updated information
        self.assertFalse(User.objects.filter(username = 'test12', first_name='Bobby', last_name='Wilson', email='test13@hotmailtt.com').exists())
        #Check to see if correct template was used 
        self.assertTemplateUsed(response, 'edit_profile.html')


    #Test character limit on username
    def test_username_unsuccessful_character_limit(self):
        #create username longer than 150 characters
        usernamee = 'testtest12' * 16 
        response = self.client.post(reverse("edit_profile"), {
            'username':usernamee,
            'first_name':'Bobby',
            'last_name':'Wilson',
            'email':'test13@hotmailtt.com',
            'settings_form':True
        }, follow=True)
        #check if post request was a success
        self.assertEqual(response.status_code, 200)  
        form = response.context['settings_form']
        #print(form.errors['username'][0])
        #check if form has 1 error (username char limit 150)
        self.assertEqual(len(form.errors), 1)
        #check if a user exists containing all of the updated information
        self.assertFalse(User.objects.filter(username = usernamee, first_name='Bobby', last_name='Wilson', email='test13@hotmailtt.com').exists())
        #Check to see if correct template was used 
        self.assertTemplateUsed(response, 'edit_profile.html')

    #testing character limit on first_name 
    def test_firstname_unsuccessful_character_limit(self):
        #create name longer than 100 characters
        name = 'Bobby' * 21 #105 chars
        response = self.client.post(reverse("edit_profile"), {
            'username':'test13',
            'first_name':name,
            'last_name':'Wilson',
            'email':'test13@hotmailtt.com',
            'settings_form':True
        }, follow=True)
        #check if post request was a success
        self.assertEqual(response.status_code, 200)
        form = response.context['settings_form']
        #print(form.errors['first_name'][0])
        #check if form has 1 error (first_name char limit 100)
        self.assertEqual(len(form.errors), 1)
        #check if a user exists containing all of the updated information
        self.assertFalse(User.objects.filter(username = 'test13', first_name=name, last_name='Wilson', email='test13@hotmailtt.com').exists())
        #Check to see if correct template was used 
        self.assertTemplateUsed(response, 'edit_profile.html')
    
    #testing character limit on last_name 
    def test_lastname_unsuccessful_character_limit(self):
        #create name longer than 100 characters
        lastname = 'Wilson' * 21 #126 chars
        response = self.client.post(reverse("edit_profile"), {
            'username':'test13',
            'first_name':'Bobby',
            'last_name': lastname,
            'email':'test13@hotmailtt.com',
            'settings_form':True
        }, follow=True)
        #check if post request was a success
        self.assertEqual(response.status_code, 200)
        form = response.context['settings_form']
        #print(form.errors['last_name'][0])
        #check if form has 1 error (last_name char limit 100)
        self.assertEqual(len(form.errors), 1)
        #check if a user exists containing all of the updated information
        self.assertFalse(User.objects.filter(username = 'test13', first_name='Bobby', last_name= lastname, email='test13@hotmailtt.com').exists())
        #Check to see if correct template was used 
        self.assertTemplateUsed(response, 'edit_profile.html')
    

    #Test changing email unsuccessfully
    def test_email_change_unsuccessful_invalid(self):
        response = self.client.post(reverse("edit_profile"), {
            'username':'test13',
            'first_name':'Bobby',
            'last_name':'Johnson',
            'email':'test13hotmailtt.com',
            'settings_form':True
        }, follow=True)
        #check if post request was a success
        self.assertEqual(response.status_code, 200)
        #Check to see if correct template was used 
        self.assertTemplateUsed(response, 'edit_profile.html')
        form = response.context['settings_form']
        #print(form.errors['email'][0])
        #check if form has 1 error (invalid email)
        self.assertEqual(len(form.errors), 1)
        user = User.objects.get(username=self.user.username)
        #Should return false since email was invalid
        self.assertFalse(User.objects.filter(username='test13',first_name='Bobby',last_name='Johnson',email='test13hotmailtt.com').exists())

    #The following tests are testing the page form (profile page information)

    #Test changing just bio successfully and if users profile pic stays the same
    def test_bio_change_successful(self):
        response = self.client.post(reverse("edit_profile"), {
            'bio':'Test Update Bio',
            'page_form':True
        }, follow=True)
        #Check if post request was a success
        self.assertEqual(response.status_code, 200)
        #Check to see if correct template was used 
        self.assertTemplateUsed(response, 'edit_profile.html')
        user = User.objects.get(username=self.user.username)
        #check if bio updated correctly should return true
        self.assertEqual(user.profile.bio, 'Test Update Bio')
        #check if profile picture remains the same (should be default image)
        self.assertEqual(user.profile.profile_pic.url, "/media/default.jpg")

    #Test bio unsuccessful (longer than 300 chars)
    def test_bio_change_unsuccessful_character_limit(self):
        #Create bio longer than 300 chars
        bio = 'Test11 Updated Bio' * 20 #360 chars
        response = self.client.post(reverse("edit_profile"), {
            'bio':bio,
            'page_form':True
        }, follow=True)
        #Check if post request was a success
        self.assertEqual(response.status_code, 200)
        #Check to see if correct template was used 
        self.assertTemplateUsed(response, 'edit_profile.html')
        form = response.context['page_form']
        #print(form.errors['bio'][0])
        #check if form has 1 error (bio char limit 300)
        self.assertEqual(len(form.errors), 1)
        user = User.objects.get(username=self.user.username)
        #should return true since bio is greater than 300 chars and did not update
        self.assertNotEqual(user.profile.bio, bio)

    #Test adding profile pic successfully
    def test_profile_picture_change_successful(self):
        #creates a representation of a image file  
        pic = SimpleUploadedFile(name='test.jpg', content=open('media/default.jpg', 'rb').read(), content_type='image/jpeg')
        response = self.client.post(reverse("edit_profile"), {
            'bio':'Test11 Updated Bio',
            'profile_pic':pic,
            'page_form':True
        }, follow=True)
        #Check if post request was a success
        self.assertEqual(response.status_code, 200)
        #Check to see if correct template was used 
        self.assertTemplateUsed(response, 'edit_profile.html')
        user = User.objects.get(username=self.user.username)
        #check if profile picture updated correctly should return true
        self.assertEqual(user.profile.profile_pic.url, '/media/profile_pictures/test.jpg')
    
    #Test adding profile pic unsuccessful wrong file type
    def test_profile_picture_change_unsuccessful(self):
        #creates a representation of a image file 
        pic = SimpleUploadedFile(name='test.bmp', content=open('media/default.jpg', 'rb').read(), content_type='image/bmp')
        response = self.client.post(reverse("edit_profile"), {
            'bio':'Test11 Updated Bio',
            'profile_pic':pic,
            'page_form':True
        }, follow=True)
        #Check if post request was a success
        self.assertEqual(response.status_code, 200)
        #Check to see if correct template was used 
        self.assertTemplateUsed(response, 'edit_profile.html')
        form = response.context['page_form']
        #print(form.errors['profile_pic'][0])
        #check if form has 1 error (invalid file extension bmp not allowed)
        self.assertEqual(len(form.errors), 1)
        user = User.objects.get(username=self.user.username)
        #check if profile picture did not update should return false
        self.assertNotEqual(user.profile.profile_pic.url, '/media/profile_pictures/test.bmp')
        #check if profile picture remains the same (default image)
        self.assertEqual(user.profile.profile_pic.url, '/media/default.jpg')

    #Test without specifying name of form being passed
    def test_post_no_form_specified(self):
        response = self.client.post(reverse("edit_profile"), {
            'bio':'Test11 Updated Bio'
        }, follow=True)
        #Check if post request was a success
        self.assertEqual(response.status_code, 200)
        #Check to see if correct template was used 
        self.assertTemplateUsed(response, 'edit_profile.html')
        user = User.objects.get(username=self.user.username)
        #check if bio updated, should return true as bio did not update
        self.assertNotEqual(user.profile.bio, 'Test11 Updated Bio')

    
    def tearDown(self) -> None:
        #remove 'test.jpg' from storage if it exists
        fs = FileSystemStorage("media/profile_pictures/")
        if fs.exists('test.jpg'):
            fs.delete('test.jpg')
        #enable logging again after tests are completed
        logging.disable(logging.NOTSET)
        return super().tearDown()