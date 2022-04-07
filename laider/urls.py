"""laider URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from laiderapp import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('creatingproject/', views.creatingProject),
    path('gettingAllProjects/', views.gettingAllProjects),
    path('creatingtaskandfileupload/', views.creatingTaskAndFileUpload),
    path('deletingtasks/',views.deletingTasks),
    path('deletingprojects/', views.deletingProject),
    path('downloadinglasfiles/', views.downloadingLasFiles),
    path('updatingprojects/',views.updatingProject),
    path('updatingtasks/', views.updatingTasks),
    path('combiningtasks/', views.combining_tasks),
]

# if settings.DEBUG:
#     urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
