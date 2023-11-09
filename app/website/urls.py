from . import views
from django.urls import path
from .views import UserEditView, EditProfilePageView, CreateProfilePageView, AboutUsView

urlpatterns = [
    path('', views.home, name='home'),
    #path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('delete_record/<int:pk>', views.delete_record, name='delete_record'),
    path("generate_summary", views.generate_summary_view, name="generate_summary"),
    path("generate_presentation", views.generate_presentation_view, name="generate_presentation"),
    path('edit_profile/', UserEditView.as_view(), name='edit_profile'),
    path('edit_profile_page/', EditProfilePageView.as_view(), name='edit_profile_page'),
    path('create_user_profile_page/', CreateProfilePageView.as_view(), name='create_user_profile_page'),
    path("detect_plagiarism", views.detect_plagiarism_view, name="detect_plagiarism"),
    path("about_us", AboutUsView.as_view(), name="about_us")
]
