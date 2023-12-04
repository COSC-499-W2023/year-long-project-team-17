from . import views
from django.urls import path
from .views import UserEditView, EditProfilePageView, CreateProfilePageView, AboutUsView, chat, send_message
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    #path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    # path('record/<int:pk>', views.customer_record, name='record'),
    # path('delete_record/<int:pk>', views.delete_record, name='delete_record'),
    # path('add_record/', views.add_record, name='add_record'),
    # path('update_record/<int:pk>', views.update_record, name='update_record'),
    path("generate_summary", views.generate_summary_view, name="generate_summary"),
    path('about_page', AboutUsView.as_view(), name='about_page'),
    path("generate_presentation", views.generate_presentation_view, name="generate_presentation"),
    path("detect_plagiarism", views.detect_plagiarism_view, name="detect_plagiarism"),
    path("generate_exercise", views.generate_exercise_view, name="generate_exercise"),
    path('edit_profile/', UserEditView.as_view(), name='edit_profile'),
    path('edit_profile_page/', EditProfilePageView.as_view(), name='edit_profile_page'),
    path('create_profile_page/', CreateProfilePageView.as_view(), name='create_profile_page'),
    path("chatbot", views.chatbot_view, name="chatbot"),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name = "password_reset.html", 
    email_template_name = "password_reset_email.html", subject_template_name = "password_reset_subject.txt"), name = 'password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = "password_reset_sent.html"), name = 'password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = "password_reset_form.html"), name = 'password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "password_reset_done.html"), name = 'password_reset_complete'),
    path('chat/<str:username>/', chat, name='chat'),
    path('send_message/<str:username>/', send_message, name='send_message'),    
]
