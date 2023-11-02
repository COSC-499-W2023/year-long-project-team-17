from . import views
from django.urls import path
from .views import UserEditView, EditProfilePageView, CreateProfilePageView

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
    path("generate_presentation", views.generate_presentation_view, name="generate_presentation"),
    path("detect_plagiarism", views.detect_plagiarism_view, name="detect_plagiarism"),
    path("generate_exercise", views.generate_exercise_view, name="generate_exercise"),
    path('edit_profile/', UserEditView.as_view(), name='edit_profile'),
    path('edit_profile_page/', EditProfilePageView.as_view(), name='edit_profile_page'),
    path('create_profile_page/', CreateProfilePageView.as_view(), name='create_profile_page'),
    path("chatbot", views.chatbot_view, name="chatbot")
]
