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

    def test_url_generateExercise_is_resolved(self):
        url = reverse("generate_exercise")
        self.assertEquals(resolve(url).func, generate_exercise_view)
    
    def test_url_virtualAssistant_is_resolved(self):
        url = reverse("chatbot")
        self.assertEquals(resolve(url).func, chatbot_view)
    
    def test_url_faq_is_resolved(self):
        url = reverse("faq")
        self.assertEquals(resolve(url).func, faq)
    
    def test_url_contactUs_is_resolved(self):
        url = reverse("contact_us")
        self.assertEquals(resolve(url).func, contact_us)
    
    def test_url_profile_is_resolved(self):
        url = reverse("profile", kwargs={'username' : 'test'})
        self.assertEquals(resolve(url).func, Profile)
    
    def test_url_editProfile_is_resolved(self):
        url = reverse("edit_profile")
        self.assertEquals(resolve(url).func, edit_profile)
    
    def test_url_changePassword_is_resolved(self):
        url = reverse("change_password")
        self.assertEquals(resolve(url).func, change_password)
    
    def test_url_presentationPreview_is_resolved(self):
        url = reverse("presentation_preview")
        self.assertEquals(resolve(url).func, presentation_preview)
    
    def test_url_loadingPage_is_resolved(self):
        url = reverse("loading_page")
        self.assertEquals(resolve(url).func, loading_page_view)
    
    def test_url_exerciseLoadingPage_is_resolved(self):
        url = reverse("exercise_loading_page")
        self.assertEquals(resolve(url).func, exercise_loading_page_view)

    def test_url_generateAdaptedContent_is_resolved(self):
        url = reverse("generate_adapted_content")
        self.assertEquals(resolve(url).func, generate_adapted_content_view)
    
    def test_url_openChats_is_resolved(self):
        url = reverse("open_chats")
        self.assertEquals(resolve(url).func, open_chats)
    
    def test_url_newChats_is_resolved(self):
        url = reverse("new_chats")
        self.assertEquals(resolve(url).func, new_chats)
    
    def test_url_chats_is_resolved(self):
        url = reverse("chat", kwargs={'username' : 'test'})
        self.assertEquals(resolve(url).func, chat)
    
    