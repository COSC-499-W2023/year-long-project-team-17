from django.test import TestCase
from website.forms import SignUpForm, ChangePasswordForm, EditProfileForm, EditProfilePageForm
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import FileSystemStorage
import logging

class TestSignUpForm(TestCase):
    
    def test_form_with_valid_data(self):
        form = SignUpForm(data={
            'username' : 'bob12',
            'first_name' : 'Bob',
            'last_name' : 'Johnson',
            'email' : 'bobj@hotmaill.com',
            'password1' : 'passpass22',
            'password2' : 'passpass22',
            'user_group' : 'student'
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0) #No errors since the form is valid

    def test_form_with_no_data(self): 
        form = SignUpForm(data={})
        self.assertFalse(form.is_valid()) 
        #print(form.errors) 
        self.assertEqual(len(form.errors), 7) #7 errors since 6 empty fields in form

    def test_form_with_diff_password(self): 
        form = SignUpForm(data={
            'username' : 'bob12',
            'first_name' : 'Bob',
            'last_name' : 'Johnson',
            'email' : 'bobj@hotmaill.com',
            'password1' : 'passpass22',
            'password2' : 'passpass2222',
            'user_group' : 'teacher'
            })
        
        self.assertFalse(form.is_valid()) 
        #print(form.errors) 
        self.assertEqual(len(form.errors), 1) #error from password2
    
    def test_form_with_invalid_password_length(self): 
        form = SignUpForm(data={
            'username' : 'bob12',
            'first_name' : 'Bob',
            'last_name' : 'Johnson',
            'email' : 'bobj@hotmaill.com',
            'password1' : 'pass22',
            'password2' : 'pass22',
            'user_group' : 'teacher'
            })
        
        self.assertFalse(form.is_valid()) 
        #print(form.errors)
        self.assertEqual(len(form.errors), 1) #error from password1 less than 8 char

    def test_form_with_invalid_password_personalinfo(self): 
        form = SignUpForm(data={
            'username' : 'bob12',
            'first_name' : 'Bob',
            'last_name' : 'Johnson',
            'email' : 'bobj@hotmaill.com',
            'password1' : 'BobJohnson22',
            'password2' : 'BobJohnson22',
            'user_group' : 'student'
            })
        
        self.assertFalse(form.is_valid()) 
        #print(form.errors)
        self.assertEqual(len(form.errors), 1) #error from password1, can't contain user's personal information

    def test_form_with_invalid_password_numeric(self): 
        form = SignUpForm(data={
            'username' : 'bob12',
            'first_name' : 'Bob',
            'last_name' : 'Johnson',
            'email' : 'bobj@hotmaill.com',
            'password1' : '123456789',
            'password2' : '123456789',
            'user_group' : 'student'
            })
        
        self.assertFalse(form.is_valid()) 
        #print(form.errors)
        self.assertEqual(len(form.errors), 1) #error from password1 can't be only numeric
 
    def test_form_with_invalid_email(self): 
        form = SignUpForm(data={
            'username' : 'bob12',
            'first_name' : 'Bob',
            'last_name' : 'Johnson',
            'email' : 'bobjhotmaill.com',
            'password1' : 'passpass22',
            'password2' : 'passpass22',
            'user_group' : 'student'
            })
        
        self.assertFalse(form.is_valid()) 
        #print(form.errors)
        self.assertEqual(len(form.errors), 1) #error invalid email

    def test_form_with_invalid_userGroup(self): 
        form = SignUpForm(data={
            'username' : 'bob12',
            'first_name' : 'Bob',
            'last_name' : 'Johnson',
            'email' : 'bob@hotmaill.com',
            'password1' : 'passpass22',
            'password2' : 'passpass22',
            'user_group' : 'Customer'
            })
        
        self.assertFalse(form.is_valid()) 
        #print(form.errors)
        self.assertEqual(len(form.errors), 1) #error invalid user_group  


class TestChangePasswordForm(TestCase):

    def setUp(self) -> None:
        user = User.objects.create_user(username='test33', email = 'test3@hotmailtestttt.com', password='passpass22', first_name = 'Bob', last_name='Johnson')
        user = User.objects.get(username = 'test33')
        self.user = user
        return super().setUp()

    def test_form_successful(self):
        form =  ChangePasswordForm(user=self.user,data={
            'old_password' : 'passpass22',
            'new_password1' : 'passpass222',
            'new_password2' : 'passpass222'
            })
        
        self.assertTrue(form.is_valid()) 
        #print(form.errors)
        self.assertEqual(len(form.errors), 0)

    def test_form_invalid_too_common(self):
        form =  ChangePasswordForm(user=self.user,data={
            'old_password' : 'passpass22',
            'new_password1' : 'password123',
            'new_password2' : 'password123'
            })
        
        self.assertFalse(form.is_valid()) 
        #print(form.errors)
        self.assertEqual(len(form.errors), 1) #Error password is too common

    def test_form_invalid_too_short(self):
        form =  ChangePasswordForm(user=self.user, data={
            'old_password' : 'passpass22',
            'new_password1' : 'pass22',
            'new_password2' : 'pass22'
            })
        
        self.assertFalse(form.is_valid()) 
        #print(form.errors)
        self.assertEqual(len(form.errors), 1) #1 error due to length
    
    def test_form_invalid_all_numeric(self):
        form =  ChangePasswordForm(user=self.user,data={
            'old_password' : 'passpass22',
            'new_password1' : '123456789',
            'new_password2' : '123456789'
            })
        
        self.assertFalse(form.is_valid()) 
        #print(form.errors)
        self.assertEqual(len(form.errors), 1) #1 error password can't be entirely numeric

    def test_form_invalid_empty(self):
        form =  ChangePasswordForm(user=self.user, data={ })
        self.assertFalse(form.is_valid()) 
        #print(form.errors)
        self.assertEqual(len(form.errors), 3) #3 errors due to empty fields
    
    def test_form_password_personal_info(self):
        form =  ChangePasswordForm(user=self.user, data={
            'old_password' : 'passpass22',
            'new_password1' : 'Johnson2244',
            'new_password2' : 'Johnson2244'
         })
        
        self.assertFalse(form.is_valid()) 
        #print(form.errors)
        self.assertEqual(len(form.errors), 1) #1 error password can't contain personal information



class TestEditProfileForm(TestCase):
    def setUp(self) -> None:
        user = User.objects.create_user(username='test44', email = 'test4@hotmailtestttt.com', password='passpass22')
        user = User.objects.get(username = 'test44')
        self.user = user
        return super().setUp()

    def test_form_valid(self):
        form =  EditProfileForm(instance = self.user, data={
            'username' : 'test44',
            'first_name' : 'bob',
            'last_name' : 'johnson',
            'email' : 'test23@test.com'
            })
        
        self.assertTrue(form.is_valid()) 
        #print(form.errors)
        self.assertEqual(len(form.errors), 0)

    def test_form_username_taken(self):
        form =  EditProfileForm(data={
            'username' : 'test44',
            'first_name' : 'bob',
            'last_name' : 'johnson',
            'email' : 'test23@test.com'
            })
        
        self.assertFalse(form.is_valid()) 
        #print(form.errors)
        self.assertEqual(len(form.errors), 1) #Error username already taken

    def test_form_invalid_email(self):
        form =  EditProfileForm(instance = self.user, data={
            'username' : 'test44',
            'first_name' : 'bob',
            'last_name' : 'johnson',
            'email' : 'test23com'
            })
        
        self.assertFalse(form.is_valid()) 
        #print(form.errors)
        self.assertEqual(len(form.errors), 1) #Error email is invalid  

    def test_form_invalid_name_length(self):
        name = 'bobby' * 35 #175 char
        last_name = 'davis' * 35 #175 char
        form =  EditProfileForm(instance = self.user, data={
            'username' : 'test44',
            'first_name' : name,
            'last_name' : last_name,
            'email' : 'test23@test.com'
            })
        
        self.assertFalse(form.is_valid()) 
        #print(form.errors)
        self.assertEqual(len(form.errors), 2) #Error char limit first_name and last_name 

    def test_form_invalid_username(self):
        form =  EditProfileForm(data={
            'username' : 'test&*@',
            'first_name' : 'bob',
            'last_name' : 'johnson',
            'email' : 'test23@test.com'
            })
        
        self.assertFalse(form.is_valid()) 
        #print(form.errors)
        self.assertEqual(len(form.errors), 1) #Error invalid username

    def test_form_invalid_form(self):
        form =  EditProfileForm(data={})
        self.assertFalse(form.is_valid()) 
        #print(form.errors)
        self.assertEqual(len(form.errors), 4) #4 errors due to 4 empty fields    
