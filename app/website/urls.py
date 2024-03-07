from . import views
from django.urls import path
from .views import UserEditView, EditProfilePageView, CreateProfilePageView, AboutUsView, chat, send_message
from django.contrib.auth import views as auth_views
from django_ratelimit.decorators import ratelimit
from django.conf import settings
from django.conf.urls.static import static


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
    path("generate_presentation/", views.generate_presentation_view, name="generate_presentation"),
    path("detect_plagiarism/", views.detect_plagiarism_view, name="detect_plagiarism"),
    path("generate_exercise/", views.generate_exercise_view, name="generate_exercise"),
    path("generate_adapted_content/", views.generate_adapted_content_view, name="generate_adapted_content"),
    path('edit_profile/', UserEditView.as_view(), name='edit_profile'),
    path('edit_profile_page/', EditProfilePageView.as_view(), name='edit_profile_page'),
    path('create_profile_page/', CreateProfilePageView.as_view(), name='create_profile_page'),
    path("chatbot/", views.chatbot_view, name="chatbot"),
    path('reset_password/', ratelimit(key='ip', method='POST', rate = '8/5h', group='b')(auth_views.PasswordResetView.as_view(template_name = "password_reset.html", 
    email_template_name = "password_reset_email.html", subject_template_name = "password_reset_subject.txt")), name = 'password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = "password_reset_sent.html"), name = 'password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = "password_reset_form.html"), name = 'password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "password_reset_done.html"), name = 'password_reset_complete'),
    path('chat/<str:username>/', chat, name='chat'),
    path('send_message/<str:username>/', send_message, name='send_message'),
    path('faq', views.faq, name='faq'),
    path('contact_us', views.contact_us, name='contact_us'),
    path("loading_page", views.loading_page_view, name="loading_page"),
    path('download_presentation/', views.presentation_download, name='presentation_download'),
    path('presentation_status/', views.presentation_status, name='presentation_status'),
    path('get_presentations', views.get_presentations, name='get_presentations'),
    path('presentation_preview/', views.presentation_preview, name='presentation_preview'),
    path('view-pdf/', views.view_pdf, name='view_pdf'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
