from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('password/reset/', views.password_reset, name='password_reset'),
    path('search/', views.user_search, name='user_search'),
]