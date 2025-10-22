from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    # Dashboard
    path('', views.admin_dashboard, name='admin_dashboard'),
    
    # Users
    path('users/', views.admin_users, name='admin_users'),
    path('users/edit/<int:user_id>/', views.admin_edit_user, name='admin_edit_user'),
    path('users/delete/<int:user_id>/', views.admin_delete_user, name='admin_delete_user'),
    path('users/toggle-status/<int:user_id>/', views.quick_toggle_user_status, name='quick_toggle_user_status'),
    
    # Jobs
    path('jobs/', views.admin_jobs, name='admin_jobs'),
    path('jobs/edit/<int:job_id>/', views.admin_edit_job, name='admin_edit_job'),
    path('jobs/delete/<int:job_id>/', views.admin_delete_job, name='admin_delete_job'),
    
    # Applications
    path('applications/', views.admin_applications, name='admin_applications'),
    path('applications/edit/<int:application_id>/', views.admin_edit_application, name='admin_edit_application'),
    path('applications/delete/<int:application_id>/', views.admin_delete_application, name='admin_delete_application'),
    path('applications/quick-update-status/', views.quick_update_status, name='quick_update_status'),
    
    # Research Papers
    path('research-papers/', views.admin_research_papers, name='admin_research_papers'),
    path('research-papers/edit/<int:paper_id>/', views.admin_edit_research_paper, name='admin_edit_research_paper'),
    path('research-papers/delete/<int:paper_id>/', views.admin_delete_research_paper, name='admin_delete_research_paper'),
    
    # Internships
    path('internships/', views.admin_internships, name='admin_internships'),
    path('internships/edit/<int:internship_id>/', views.admin_edit_internship, name='admin_edit_internship'),
    path('internships/delete/<int:internship_id>/', views.admin_delete_internship, name='admin_delete_internship'),
]