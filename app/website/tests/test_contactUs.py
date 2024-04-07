from django.test import TestCase
from django.core import mail
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import auth

class TestContactForm(TestCase):
    
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='test3', email = 'test3@hotmailtestttt.com', password='passpass22')
        self.client.force_login(self.user)
        return super().setUp()
    
    def test_contact_form_successful(self):
        #Makes a post request to the contact form on contact us page
        response = self.client.post(reverse("contact_us"), {
            'email':'test3@hotmailtestttt.com',
            'question':'Can I have a summary generated in a different language?'
        }, follow=True)

        #check if post response was a success
        self.assertEquals(response.status_code, 200)

        #check to see that if one email was sent 
        self.assertEqual(len(mail.outbox), 1)
        #check to see if the subject line for email was correct
        self.assertEquals(mail.outbox[0].subject, "Question from test3@hotmailtestttt.com")

    def test_contact_form_invalid_email(self):
        #Makes a post request to the contact form on contact us page passing an invalid email 
        response = self.client.post(reverse("contact_us"), {
            'email':'h',
            'question':'Can I have a summary generated in a different language?'
        }, follow=True)

        #check if post response was a success
        self.assertEquals(response.status_code, 200)

        #check to see that if no email was sent since the form is invalid
        self.assertEqual(len(mail.outbox), 0)

    def test_contact_form_invalid_question(self):
        #Makes a post request to the contact form on contact us page passing an empty question
        response = self.client.post(reverse("contact_us"), {
            'email':'bob12@hotmaill.commm',
            'question':''
        }, follow=True)

        #check if post response was a success
        self.assertEquals(response.status_code, 200)
        #check to see that if no email was sent since the form is invalid
        self.assertEqual(len(mail.outbox), 0)



