from tracker.views import ProjectNew, ProjectsList, ProjectInfo
from . import views
from django.urls import path, include
import django.contrib.auth.views as auth_views

app_name = 'tracker'

urlpatterns = [
    path('', views.index, name='home'),
    path('projects/', ProjectsList.as_view(), name='projects'),
    path('projects/new', ProjectNew.as_view(template_name='new_project.html'), name='project_new'),
    path('projects/<int:project_id>', ProjectInfo.as_view(), name='project_info'),
    #path('signup/', vi,ews.signup, name='signup'),
]

handler404 = 'views.handler404'