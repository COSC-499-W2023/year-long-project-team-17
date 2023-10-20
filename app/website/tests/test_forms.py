from django.test import TestCase
from website.forms import SignUpForm


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
