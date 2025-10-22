"""
URL configuration for opportunity project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from user.views import home  # Import home view

urlpatterns = [
    path('', home, name='home'),  # Root URL maps to user.views.home
    path('admin/', admin.site.urls),
    path('admin-panel/', include('admin_panel.urls')),
    path('user/', include('user.urls')),  # Other user views (signup, login, etc.)
    path('jobs/', include('job.urls')),  # Move job app to /jobs/
    path('research-papers/', include('research_paper.urls')),
    path('internships/', include('internship.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)