from django.test import SimpleTestCase
from django.urls import reverse, resolve
from website.views import *
class TestUrls(SimpleTestCase):
    """
    These tests are testing to see if the URL's are connecting to the correct view function
    """

    def test_url_home_is_resolved(self):
        url = reverse("home") #returns the actual url given a url name for the view
        self.assertEquals(resolve(url).func, home) #Checks if our url for home calls the correct view function 

    def test_url_logout_is_resolved(self):
        url = reverse("logout")
        self.assertEquals(resolve(url).func, logout_user)

    def test_url_register_is_resolved(self):
        url = reverse("register")
        self.assertEquals(resolve(url).func, register_user)

    def test_url_generateSummary_is_resolved(self):
        url = reverse("generate_summary")
        self.assertEquals(resolve(url).func, generate_summary_view)
    
    def test_url_generatePresentation_is_resolved(self):
        url = reverse("generate_presentation")
        self.assertEquals(resolve(url).func, generate_presentation_view)

    def test_url_detectPlagiarism_is_resolved(self):
        url = reverse("detect_plagiarism")
        self.assertEquals(resolve(url).func, detect_plagiarism_view)

    def test_url_generatePresentation_is_resolved(self):
        url = reverse("generate_exercise")
        self.assertEquals(resolve(url).func, generate_exercise_view)
