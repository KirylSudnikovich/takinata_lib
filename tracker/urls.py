from tracker.views import ProjectNew, ProjectsList, ProjectInfo, ProjectDelete, ProjectEdit
from . import views
from django.urls import path, include
import django.contrib.auth.views as auth_views

app_name = 'tracker'

urlpatterns = [
    path('', views.index, name='home'),
    path('projects/', ProjectsList.as_view(), name='projects'),
    path('projects/new/', ProjectNew.as_view(template_name='new_project.html'), name='project_new'),
    path('projects/<int:project_id>/', ProjectInfo.as_view(), name='project_info'),
    path('projects/<int:project_id>/delete/', ProjectDelete.as_view(), name='project_delete'),
    path('projects/<int:project_id>/edit/', ProjectEdit.as_view(), name='project_edit'),
    # path('signup/', vi,ews.signup, name='signup'),
]

handler404 = 'views.handler404'
