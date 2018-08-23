from tracker.views import ProjectNew, ProjectsList, ProjectInfo, ProjectDelete, ProjectEdit, ColumnNew, ColumnInfo, \
    ColumnDelete, ColumnEdit, BugReport, BugReportList, ColumnList, TaskList, SampleView, TaskInfo, TaskDelete
from . import views
from django.urls import path, include
import django.contrib.auth.views as auth_views

app_name = 'tracker'

urlpatterns = [
    path('', views.index, name='home'),
    path('projects/', ProjectsList.as_view(), name='projects'),
    path('projects/new/', ProjectNew.as_view(template_name='projects/create.html'), name='project_new'),
    path('projects/<int:project_id>/', ProjectInfo.as_view(), name='project_info'),
    path('projects/<int:project_id>/delete/', ProjectDelete.as_view(), name='project_delete'),
    path('projects/<int:project_id>/edit/', ProjectEdit.as_view(), name='project_edit'),
    path('columns/', ColumnList.as_view(), name='column_list'),
    path('columns/new/', ColumnNew.as_view(), name='column_new'),
    path('columns/<int:project_id>/<int:column_id>/', ColumnInfo.as_view(), name='column_info'),
    path('columns/<int:project_id>/<int:column_id>/delete', ColumnDelete.as_view(), name='column_delete'),
    path('columns/<int:project_id>/<int:column_id>/edit', ColumnEdit.as_view(), name='column_edit'),
    path('bug_report/', BugReport.as_view(), name='bug_report'),
    path('bug_list/', BugReportList.as_view(), name='bug_report_list'),
    path('tasks/', TaskList.as_view(), name='task_list'),
    path('tasks/<int:task_id>/', TaskInfo.as_view(), name='task_info'),
    path('tasks/create', SampleView.as_view(), name='task_create'),
    path('tasks/<int:task_id>/delete', TaskDelete.as_view(), name='task_delete'),
]

handler404 = 'views.handler404'
