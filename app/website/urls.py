from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    #path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('record/<int:pk>', views.customer_record, name='record'),
    path('delete_record/<int:pk>', views.delete_record, name='delete_record'),
    path('add_record/', views.add_record, name='add_record'),
    path('update_record/<int:pk>', views.update_record, name='update_record'),
    path("generate_summary", views.generate_summary_view, name="generate_summary"),
    path("generate_presentation", views.generate_presentation_view, name="generate_presentation"),
    path("detect_plagiarism", views.detect_plagiarism_view, name="detect_plagiarism")
]
