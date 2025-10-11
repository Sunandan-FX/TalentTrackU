from django.urls import path
from . import views

urlpatterns = [
    path('', views.research_paper_list, name='research_paper_list'),
    path('post/', views.research_paper_post_create, name='research_paper_post_create'),
    path('apply/<int:paper_id>/', views.research_paper_apply, name='research_paper_apply'),
    path('delete/<int:paper_id>/', views.research_paper_delete, name='research_paper_delete'),
]