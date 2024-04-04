from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class TestChangePassword(TestCase):
    def setUp(self) -> None:
        user = User.objects.create_user(username='test3', email = 'test3@hotmailtestttt.com', password='passpass22')
        user = User.objects.get(username = 'test3')
        self.user_id = user.pk
        self.client.force_login(user)
        return super().setUp()
    
    #Test changing password successful
    def test_password_change_successful(self):
        response = self.client.post(reverse("change_password"), {
            'old_password':'passpass22',
            'new_password1':'passpass2222',
            'new_password2':'passpass2222'
        })
        #Check if post request was successful
        self.assertEqual(response.status_code, 200)
        #Check to see if correct template was used 
        self.assertTemplateUsed(response, 'change_password.html') 
        user = User.objects.get(id=self.user_id)
        #should return true if password was changed successfully
        self.assertTrue(user.check_password('passpass2222'))

    #Test changing password unsuccessful (wrong old password)
    def test_password_change_unsuccessful_old(self):
        response = self.client.post(reverse("change_password"), {
            'old_password':'passpass23',
            'new_password1':'passpass2223',
            'new_password2':'passpass2223'
        })
        #Check if post request was successful
        self.assertEqual(response.status_code, 200)
        #Check to see if correct template was used 
        self.assertTemplateUsed(response, 'change_password.html') 
        form = response.context['form']
        #print(form.errors['old_password'][0])
        #check if form has 1 error (wrong old password)
        self.assertEqual(len(form.errors), 1)
        #Check if password stayed the same should return true
        user = User.objects.get(id=self.user_id)
        self.assertTrue(user.check_password('passpass22'))
    
    #Test password unsuccessful (don't match)
    def test_password_change_unsuccessful_matching(self):
        response = self.client.post(reverse("change_password"), {
            'old_password':'passpass22',
            'new_password1':'passpass2224',
            'new_password2':'passpass2223'
        })
        #Check if post request was successful
        self.assertEqual(response.status_code, 200)
        #Check to see if correct template was used 
        self.assertTemplateUsed(response, 'change_password.html') 
        form = response.context['form']
        #print(form.errors['new_password2'][0])
        #check if form has 1 error (don't match)
        self.assertEqual(len(form.errors), 1)
        #Check if password stayed the same should return true
        user = User.objects.get(id=self.user_id)
        self.assertTrue(user.check_password('passpass22'))

    #Test password unsuccessful (too common)
    def test_password_change_unsuccessful_too_common(self):
        response = self.client.post(reverse("change_password"), {
            'old_password':'passpass22',
            'new_password1':'password1234',
            'new_password2':'password1234'
        })
        #Check if post request was successful
        self.assertEqual(response.status_code, 200) 
        #Check to see if correct template was used 
        self.assertTemplateUsed(response, 'change_password.html')
        form = response.context['form']
        #print(form.errors['new_password2'][0])
        #check if form has 1 error (too common)
        self.assertEqual(len(form.errors), 1)
        #Check if password stayed the same should return true
        user = User.objects.get(id=self.user_id)
        self.assertTrue(user.check_password('passpass22'))
        
    #Test password unsuccessful (can't be just numeric)
    def test_password_change_unsuccessful_all_numeric(self):
        response = self.client.post(reverse("change_password"), {
            'old_password':'passpass22',
            'new_password1':'11102103104',
            'new_password2':'11102103104'
        })
        #Check if post request was successful
        self.assertEqual(response.status_code, 200) 
        #Check to see if correct template was used 
        self.assertTemplateUsed(response, 'change_password.html')
        form = response.context['form']
        #print(form.errors['new_password2'][0])
        #check if form has 1 error (can't be just numeric)
        self.assertEqual(len(form.errors), 1)
        #Check if password stayed the same should return true
        user = User.objects.get(id=self.user_id)
        self.assertTrue(user.check_password('passpass22'))
