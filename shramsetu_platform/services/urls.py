from django.urls import path
from . import views

urlpatterns = [
    # Public Pages
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('services/', views.services_view, name='services'),
    path('projects/', views.projects_view, name='projects'),
    
    # Authentication
    path('auth/', views.auth_view, name='auth_view'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard & Actions
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/messages/', views.messages_view, name='messages'),
    path('dashboard/settings/', views.settings_view, name='settings'),
    path('hire/<int:worker_id>/', views.hire_worker, name='hire_worker'),
    path('accept-job/<int:job_id>/', views.accept_job, name='accept_job'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('accept-job/<int:job_id>/', views.accept_job, name='accept_job'),
    path('reject-job/<int:job_id>/', views.reject_job, name='reject_job'),
    path('dashboard/settings/', views.settings_view, name='settings'),
    path('job/update/<int:job_id>/<str:status>/', views.update_job_status, name='update_job_status'),
    path('job-status/<int:job_id>/<str:action>/', views.update_job_status, name='update_job_status'),
    path('chatbot-api/', views.chatbot_api, name='chatbot_api'),
]