from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
import logging


'''Note: You need to have Memcache setup and running in order to run this test, once you do remove the comment tags

class TestRateLimit(TestCase):
    def setUp(self) -> None:
        cache.clear()
        #Sets the threshold for the django.request logger to a higher severity level 
        #so that the 403 too many requests warning
        #which we are expected to get is ignored for these tests
        logger = logging.getLogger("django.request")
        #store the previous level to set it back to normal after tests are complete
        self.prev = logger.getEffectiveLevel()
        #Sets the threshold for this logger to a higher severity level so that it ignores the warning
        logger.setLevel(logging.ERROR)
        return super().setUp()
    
  
#testing the rate limit for login, it should block a specific username from being used to login 
#and still allow other usernames to be entered, rate = 5/5m so the user should be limited after 5 requests
    def test_limit_home(self):
        #first request
        response = self.client.post(reverse("home"), {"username" : 'test3', "password" : 'p'}, follow = True)
        req = response.wsgi_request
        #Checks to see if request was limited
        check = getattr(req, 'limited', False)
        self.assertFalse(check)
        #Check if response was successful
        self.assertEqual(response.status_code, 200)
        #second request
        response = self.client.post(reverse("home"), {"username" : 'test3', "password" : 'p'}, follow = True)
        req = response.wsgi_request
        check = getattr(req, 'limited', False)
        self.assertFalse(check)
        #Check if response was successful
        self.assertEqual(response.status_code, 200)
        #third request
        response = self.client.post(reverse("home"), {"username" : 'test3', "password" : 'p'}, follow = True)
        req = response.wsgi_request
        check = getattr(req, 'limited', False)
        self.assertFalse(check)
        #Check if response was successful
        self.assertEqual(response.status_code, 200)
        #fourth request
        response = self.client.post(reverse("home"), {"username" : 'test3', "password" : 'p'}, follow = True)
        req = response.wsgi_request
        check = getattr(req, 'limited', False)
        self.assertFalse(check)
        #Check if response was successful
        self.assertEqual(response.status_code, 200)
        #fifth request
        response = self.client.post(reverse("home"), {"username" : 'test3', "password" : 'p'}, follow = True)
        req = response.wsgi_request
        check = getattr(req, 'limited', False)
        self.assertFalse(check)
        #Check if response was successful
        self.assertEqual(response.status_code, 200)

        #This is the sixth request it should return true for limited and a 429 http response for too many requests
        response = self.client.post(reverse("home"), {"username" : 'test3', "password" : 'p'}, follow = True)
        req = response.wsgi_request
        check = getattr(req, 'limited', False)
        #should return true since user has reached the rate limit
        self.assertTrue(check)
        #Check if correct http status code was displayed 429 for too many requests
        self.assertEqual(response.status_code, 429)
        
        #Check to see if you can still try to attempt login using different username
        response = self.client.post(reverse("home"), {"username" : 'test1', "password" : 'p'}, follow = True)
        req = response.wsgi_request
        check = getattr(req, 'limited', False)
        #should return false since a different username is provided
        self.assertFalse(check)
        #Check if reponse was a success
        self.assertEqual(response.status_code, 200)

#Tests to see if the user is blocked from submitting a password reset email, they should be block at the ip meaning they are block
#from submitting any email for password reset, rate=8/5h meaning the user can make 8 requests in the 6 hour window they are given
    def test_limit_password_reset(self):
        #first request
        response = self.client.post(reverse("password_reset"), {"email" : 'test@hotmailll.com'}, follow = True)
        req = response.wsgi_request
        #Checks to see if request was limited
        check = getattr(req, 'limited', False)
        #Should return false since rate is not limited
        self.assertFalse(check)
        #Check if response was success
        self.assertEqual(response.status_code, 200)
        #second request
        response = self.client.post(reverse("password_reset"), {"email" : 'test1@hotmailll.com'}, follow = True)
        req = response.wsgi_request
        check = getattr(req, 'limited', False)
        self.assertFalse(check)
        #Check if response was success
        self.assertEqual(response.status_code, 200)
        #third request
        response = self.client.post(reverse("password_reset"), {"email" : 'test@hotmailll.com'}, follow = True)
        req = response.wsgi_request
        check = getattr(req, 'limited', False)
        self.assertFalse(check)
        #Check if response was success
        self.assertEqual(response.status_code, 200)
        #fourth request
        response = self.client.post(reverse("password_reset"), {"email" : 'test3@hotmailll.com'}, follow = True)
        req = response.wsgi_request
        check = getattr(req, 'limited', False)
        self.assertFalse(check)
        #Check if response was success
        self.assertEqual(response.status_code, 200)
        #fifth request
        response = self.client.post(reverse("password_reset"), {"email" : 'test3@hotmailll.com'}, follow = True)
        req = response.wsgi_request
        check = getattr(req, 'limited', False)
        self.assertFalse(check)
        #Check if response was success
        self.assertEqual(response.status_code, 200)
        #sixth request
        response = self.client.post(reverse("password_reset"), {"email" : 'test3@hotmailll.com'}, follow = True)
        req = response.wsgi_request
        check = getattr(req, 'limited', False)
        self.assertFalse(check)
        #Check if response was success
        self.assertEqual(response.status_code, 200)
        #seventh request
        response = self.client.post(reverse("password_reset"), {"email" : 'test3@hotmailll.com'}, follow = True)
        req = response.wsgi_request
        check = getattr(req, 'limited', False)
        self.assertFalse(check)
        #Check if response was success
        self.assertEqual(response.status_code, 200)
        #eighth request
        response = self.client.post(reverse("password_reset"), {"email" : 'test3@hotmailll.com'}, follow = True)
        req = response.wsgi_request
        check = getattr(req, 'limited', False)
        self.assertFalse(check)
        #Check if response was success
        self.assertEqual(response.status_code, 200)
        #ninth request the user should be limited from using the password reset
        response = self.client.post(reverse("password_reset"), {"email" : 'test3@hotmailll.com'}, follow = True)
        req = response.wsgi_request
        check = getattr(req, 'limited', False)
        #Should return true since user has made more than 8 requests
        self.assertTrue(check)
        #Check if correct http status code was displayed 429 for too many requests
        self.assertEqual(response.status_code, 429)


    def tearDown(self) -> None:
        #Sets the logger level for django.request back to its previous level
        logger = logging.getLogger("django.request")
        logger.setLevel(self.prev)
'''