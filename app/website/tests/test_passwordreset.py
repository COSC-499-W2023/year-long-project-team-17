from django.test import TestCase, override_settings
from django.core import mail
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.cache import cache
from django.contrib import auth

class TestPasswordReset(TestCase):
    @override_settings(RATELIMIT_ENABLE = False)

    def setUp(self) -> None:
        cache.clear()
        user = User.objects.create_user(username='test', email = 'test@hotmailtestttt.com', password='passpass22')
        return super().setUp()

    def test_password_reset_successful(self):
        
        #check to see if you can get the correct page 
        response = self.client.get(reverse("password_reset"))
        self.assertEqual(response.status_code, 200)
        #check if correct template was used
        self.assertTemplateUsed(response, 'password_reset.html')

        #pass email address for password reset
        response = self.client.post(reverse("password_reset"), {'email' : 'test@hotmailtestttt.com'})
        #check if it redirects after sending email
        self.assertEquals(response.status_code, 302)
        #check to see that if one email was sent 
        self.assertEqual(len(mail.outbox), 1)
        #check to see if the subject line for email was correct
        self.assertEquals(mail.outbox[0].subject, "Password reset on " + response.wsgi_request.get_host() + " (EduPrompt)")

   
        #get the link to the password reset from the email
        email = mail.outbox[0].body
        url = email[email.find('/reset/'):].split()[0]
        #print(url)
        response = self.client.get(url)
        #get the secure password reset url for password change from the get response
        url = response.url
        #check if the response was successful and you are redirected to password reset form html
        self.assertEqual(response.status_code, 302)
        #Check to see if you can change password sucessfully
        response = self.client.post(url, {'new_password1' : 'passpass2234', 'new_password2' : 'passpass2234'})
        #check if to see it redirects since password changed succesfully
        self.assertEqual(response.status_code, 302)
        #if the password was changed successfully it should redirect to password reset complete
        self.assertRedirects(response, reverse('password_reset_complete'))

        #check to see if user can login with new password
        response = self.client.post(reverse("home"), {
            'username':'test',
            'password':'passpass2234'}, follow=True)
        #check if post response was a success
        self.assertEqual(response.status_code, 200)
        #Check if user is logged in 
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)

    #This test checks to see if an email gets sent out when its not registered to a user
    def test_password_reset_email_not_registered(self):
        #pass email address
        response = self.client.post(reverse("password_reset"), {'email' : 'bill@hotmailbilll.com'})
        #check if it redirects after trying to send the email 
        self.assertEquals(response.status_code, 302)
        #check to see that if no email was sent 
        self.assertEqual(len(mail.outbox), 0)




