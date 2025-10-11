from django.urls import path
from . import views

app_name = 'job'

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('post/', views.job_post_create, name='job_post_create'),
    path('apply/<int:job_id>/', views.job_apply, name='job_apply'),
    path('delete/<int:job_id>/', views.job_delete, name='job_delete'),
    path('my-applications/', views.my_job_applications, name='my_job_applications'),
    path('my-post-applications/', views.my_post_job_applications, name='my_post_job_applications'),
    path('application-manage/<int:application_id>/', views.job_application_manage, name='job_application_manage'),
]