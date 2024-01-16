# from django.contrib.auth.models import User
# from django.test import LiveServerTestCase
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time

# class ChatFunctionalityTest(LiveServerTestCase):
#     def setUp(self):
#         self.driver_user1 = webdriver.Chrome()
#         self.driver_user2 = webdriver.Chrome()

#         # Create two users
#         self.user1 = User.objects.create_user(username="user1", password="password1")
#         self.user2 = User.objects.create_user(username="user2", password="password2")

#     def tearDown(self):
#         self.driver_user1.quit()
#         self.driver_user2.quit()

#     def test_chat_functionality(self):
#         # User 1 logs in
#         self.login_user(self.driver_user1, "user1", "password1")

#         # User 2 logs in
#         self.login_user(self.driver_user2, "user2", "password2")

#         # User 1 opens the chat page
#         self.driver_user1.get(self.live_server_url + '/chat/user2/')

#         # User 1 sends a message
#         self.send_message(self.driver_user1, "Hello, User 2!")

#         # User 2 opens the chat page
#         self.driver_user2.get(self.live_server_url + '/chat/user1/')
#         time.sleep(1000)

#         # User 2 receives the message
#         received_message = self.receive_message(self.driver_user2)

#         # User 2 replies
#         self.send_message(self.driver_user2, "Hi, User 1!")

#         # User 1 receives the reply
#         received_reply = self.receive_message(self.driver_user1)

#     def login_user(self, browser, username, password):
#         browser.get(self.live_server_url + '/')
#         browser.find_element("name", 'username').send_keys(username)
#         browser.find_element("name", 'password').send_keys(password)
#         browser.find_element("name", 'password').send_keys(Keys.RETURN)


#     def send_message(self, browser, message):
#         message_input = browser.find_element("id", 'message-input')
#         message_input.send_keys(message)
#         message_input.send_keys(Keys.RETURN)

#     def receive_message(self, browser):
#         chat_messages = browser.find_element("id", 'chat-messages')
#         time.sleep(1)  # Wait for a short time to allow the message to be sent and received
#         return chat_messages.text


from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from website.models import Message  

class ChatFunctionalityTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='passpass22')
        self.user2 = User.objects.create_user(username='user2', password='passpass22')

    def test_send_message(self):
        # Log in user1
        self.client.login(username='user1', password='passpass22')

        # Send a message from user1 to user2
        response = self.client.post(reverse('send_message', kwargs={'username': 'user2'}), {
            'content': 'Hello, user2!'
        })

        # Check if the message was sent successfully
        self.assertEqual(response.status_code, 302)  # Assuming a redirect after sending a message

        # Get the IDs of user1 and user2
        user1_id = self.user1.id
        user2_id = self.user2.id

        # Check if the message is stored in the database using the IDs
        sent_message = Message.objects.filter(sender_id=user1_id, receiver_id=user2_id, content='Hello, user2!').first()
        # print(sent_message.content)
        self.assertIsNotNone(sent_message)

