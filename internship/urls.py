from django.urls import path
from . import views

urlpatterns = [
    path('', views.internship_list, name='internship_list'),
    path('post/', views.internship_post_create, name='internship_post_create'),
    path('apply/<int:internship_id>/', views.internship_apply, name='internship_apply'),
    path('delete/<int:internship_id>/', views.internship_delete, name='internship_delete'),
    path('application/manage/<int:application_id>/', views.internship_application_manage, name='internship_application_manage'),
    path('my-applications/', views.my_internship_applications, name='my_internship_applications'),
    path('my-post-applications/', views.my_post_internship_applications, name='my_post_internship_applications'),
]