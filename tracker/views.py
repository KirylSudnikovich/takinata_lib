from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.views import View
from django.views.generic import TemplateView, FormView
from lib.controllers.column import ColumnController
from lib.controllers.project import ProjectController
from lib.storage.column import ColumnStorage
from lib.storage.project import ProjectStorage
from lib.storage.user import UserStorage
from lib.controllers.task import TaskController
from lib.storage.task import TaskStorage

from .controllers.tracker_controller import BugController, all_users, all_projects, all_categories, all_tasks
from .forms import SignupForm, ToDoForm


def index(request):
    dict_to_template = {'users': all_users(), 'projects': all_projects, 'categories': all_categories(),
                        'tasks': all_tasks()}
    response = render(request, 'index.html', dict_to_template)
    if 'been_before' in request.COOKIES:
        print("sosi")
    else:
        response.set_cookie(key='been_before', value='1')
    return response


class ProjectsList(View):
    def get(self, request):
        if request.user.is_authenticated:
            username = request.user.username
            password = request.user.password
            project_list = ProjectController.show_all(username, password)
            return render(request, 'projects/list.html', {'project_list': project_list})
        else:
            return render(request, 'no_permission.html')


class ProjectNew(TemplateView):
    def post(self, request):
        if request.user.is_authenticated:
            if request.method == 'POST':
                name = request.POST['name']
                description = request.POST['description']
                if request.user.is_authenticated:
                    username = request.user.username
                    password = request.user.password
                    ProjectController.create(username, password, name, description)
                    return redirect('tracker:projects')
        else:
            return render(request, 'no_permission.html')


class ProjectInfo(View):
    def get(self, request, project_id):
        if request.user.is_authenticated:
            project = ProjectStorage.get_project_by_id(project_id)
            columns = ColumnController.show_all(request.user.username, request.user.password, project.id)
            all_users = UserStorage.get_all_users()
            guys = ProjectStorage.get_all_persons_in_project(project)
            all_guys = []
            guys_names = []
            for i in guys:
                guys_names.append(i.username)
            for i in all_users:
                if i.username not in guys_names:
                    all_guys.append(i)
            return render(request, 'projects/info.html',
                          {'project': project, 'columns': columns, 'guys': guys, 'all_guys': all_guys})
        else:
            return render(request, 'no_permission.html')

    def post(self, request, project_id):
        if request.method == 'POST':
            if 'add_to_project' in request.POST:
                username = request.POST['add_select']
                project = ProjectStorage.get_project_by_id(project_id)
                user = UserStorage.get_user_by_name(username)
                ProjectController.add_person_to_project(request.user.username, request.user.password, project, user)
                return redirect('tracker:project_info', project_id)
            elif 'remove_from_project' in request.POST:
                username = request.POST['remove_select']
                project = ProjectStorage.get_project_by_id(project_id)
                user = UserStorage.get_user_by_name(username)
                ProjectController.delete_person_from_project(request.user.username, request.user.password, project,
                                                             user)
                return redirect('tracker:project_info', project_id)


class ProjectDelete(View):
    def get(self, request, project_id):
        if request.user.is_authenticated:
            project = ProjectStorage.get_project_by_id(project_id)
            return render(request, 'projects/delete.html', {'project': project})
        else:
            return render(request, 'no_permission.html')

    def post(self, request, project_id):
        if request.method == 'POST':
            if request.user.is_authenticated:
                project = ProjectStorage.get_project_by_id(project_id)
                ProjectStorage.delete_with_object(project)
                return redirect('tracker:projects')
            else:
                return render(request, 'no_permission.html')


class ProjectEdit(View):
    def get(self, request, project_id):
        if request.user.is_authenticated:
            project = ProjectStorage.get_project_by_id(project_id)
            return render(request, 'projects/edit.html', {'project': project})
        else:
            return render(request, 'no_permission.html')

    def post(self, request, project_id):
        if request.method == 'POST':
            if request.user.is_authenticated:
                project = ProjectStorage.get_project_by_id(project_id)
                project.name = request.POST['name']
                project.description = request.POST['description']
                ProjectStorage.save(project)
                return redirect('tracker:projects')
            else:
                return render(request, 'no_permission.html')


class ColumnList(View):
    def get(self, request):
        if request.user.is_authenticated:
            username = request.user.username
            password = request.user.password
            projects = ProjectController.show_all(username, password)
            column_list = []
            for project in projects:
                columns = ColumnController.show_all(username, password, project.id)
                print("LIST of COLUMNS - ", columns)
                column_list = column_list + columns
            return render(request, 'categories/list.html', {'column_list': column_list})
        else:
            return render(request, 'no_permission.html')


class ColumnNew(View):
    def get(self, request):
        projects = ProjectController.show_all(request.user.username, request.user.password)
        return render(request, 'categories/create.html', {'projects': projects})

    def post(self, request):
        if request.user.is_authenticated:
            if request.method == 'POST':
                name = request.POST['name']
                description = request.POST['description']
                project = ProjectStorage.get_project(request.POST['select_project'])
                projects = ProjectController.show_all(request.user.username, request.user.password)
                for i in projects:
                    if project.name == i.name:
                        project = i
                print("Project_id = ", request.POST['select_project'])
                ColumnController.create_columm(username=request.user.username, password=request.user.password,
                                               project_id=project.id, name=name, description=description)
                return redirect('tracker:column_list')
        else:
            return render(request, 'no_permission.html')


class ColumnInfo(View):
    def get(self, request, project_id, column_id):
        if request.user.is_authenticated:
            project = ProjectStorage.get_project_by_id(project_id)
            column = ColumnStorage.get_column_by_id(project.name, column_id)
            return render(request, 'categories/info.html', {'project': project, 'column': column})
        else:
            return render(request, 'no_permission.html')


class ColumnDelete(View):
    def get(self, request, project_id, column_id):
        if request.user.is_authenticated:
            project = ProjectStorage.get_project_by_id(project_id)
            column = ColumnStorage.get_column_by_id(project.name, column_id)
            return render(request, 'categories/delete.html', {'project': project, 'column': column})
        else:
            return render(request, 'no_permission.html')

    def post(self, request, project_id, column_id):
        if request.method == 'POST':
            if request.user.is_authenticated:
                project = ProjectStorage.get_project_by_id(project_id)
                column = ColumnStorage.get_column_by_id(project.name, column_id)
                ColumnStorage.delete_column_from_db(column)
                return redirect('tracker:projects')
            else:
                return render(request, 'no_permission.html')


class ColumnEdit(View):
    def get(self, request, project_id, column_id):
        if request.user.is_authenticated:
            project = ProjectStorage.get_project_by_id(project_id)
            column = ColumnStorage.get_column_by_id(project.name, column_id)
            return render(request, 'categories/edit.html', {'project': project, 'column': column})
        else:
            return render(request, 'no_permission.html')

    def post(self, request, project_id, column_id):
        if request.method == 'POST':
            if request.user.is_authenticated:
                project = ProjectStorage.get_project_by_id(project_id)
                column = ColumnStorage.get_column_by_id(project.name, column_id)
                column.name = request.POST['name']
                column.desc = request.POST['description']
                ColumnStorage.save(column)
                return redirect('tracker:projects')
            else:
                return render(request, 'no_permission.html')


class TaskList(View):
    def get(self, request):
        if request.user.is_authenticated:
            username = request.user.username
            password = request.user.password
            projects = ProjectController.show_all(username, password)
            column_list = []
            task_list = []
            for project in projects:
                columns = ColumnController.show_all(username, password, project.id)
                for column in columns:
                    tasks = TaskController.show_tasks(username, password, project.id, column.id)
                    print("tasks = ", tasks)
                    task_list = task_list + tasks
                column_list = column_list + columns
            print("task_list = ",task_list)
            return render(request, 'tasks/list.html', {'projects': projects, 'columns': column_list, 'task_list': task_list})
        else:
            return render(request, 'no_permission.html')


class SampleView(FormView):
    def get(self, request, **kwargs):
        f = ToDoForm
        projects = ProjectController.show_all(request.user.username, request.user.password)
        columns_to_send = []
        for project in projects:
            columns = ColumnController.show_all(request.user.username, request.user.password, project.id)
            columns_to_send += columns
        return render(request, 'tasks/create.html', {'form': f, 'projects': projects, 'columns': columns_to_send})

    def post(self, request, **kwargs):
        f = ToDoForm(request.POST)
        print(f.errors)
        if f.is_valid():
            name = f['name'].value()
            desc = f['desc'].value()
            start_date = f['start_date'].value()
            start_time = f['start_time'].value()
            end_date = f['end_date'].value()
            end_time = f['end_time'].value()
            tags = f['tags'].value()
            priority = f['priority'].value()
            project = ProjectStorage.get_project_by_id(request.POST['select_project'])
            projects = ProjectController.show_all(request.user.username, request.user.password)
            for i in projects:
                if project.name == i.name:
                    project = i
            columns_to_send = []
            for project in projects:
                columns = ColumnController.show_all(request.user.username, request.user.password, project.id)
                columns_to_send += columns
            column = ColumnStorage.get_column_by_id(project.name, request.POST['select_column'])
            print("SELECTED_PROJECT = ", request.POST['select_project'])
            print("SELECTED_COLUMN = ", request.POST['select_column'])
            for i in columns_to_send:
                if column.name == i.name:
                    column = i
            TaskController.add_task(request.user.username, request.user.password, project.id, column.id, name, desc,
                                    start_date, start_time, end_date, end_time, tags, priority)


class TaskInfo(View):
    def get(self, request, project_id, column_id, task_id):
        if request.user.is_authenticated:
            project = ProjectStorage.get_project_by_id(project_id)
            column = ColumnStorage.get_column_by_id(project.id, column_id)
            task = TaskStorage.get_task_by_id(task_id)
            return render(request, 'tasks/info.html', {'project': project, 'column': column, 'task': task})
        else:
            return render(request, 'no_permission.html')


class TaskDelete(View):
    def get(self, request, project_id, column_id, task_id):
        if request.user.is_authenticated:
            project = ProjectStorage.get_project_by_id(project_id)
            column = ColumnStorage.get_column_by_id(project.name, column_id)
            task = TaskStorage.get_task_by_id(task_id)
            return render(request, 'tasks/delete.html', {'project': project, 'column': column, 'task': task})
        else:
            return render(request, 'no_permission.html')

    def post(self, request, project_id, column_id, task_id):
        if request.method == 'POST':
            if request.user.is_authenticated:
                task = TaskStorage.get_task_by_id(task_id)
                TaskStorage.delete_task_from_db(task)
                return redirect('tracker:task_list')
            else:
                return render(request, 'no_permission.html')

class BugReport(View):
    def get(self, request):
        return render(request, 'bug_tracker/bug_fixing.html')

    def post(self, request):
        username = request.user.username
        name = request.POST['name']
        description = request.POST['description']
        BugController.add_bug(username, name, description)
        return redirect('tracker:home')


class BugReportList(View):
    def get(self, request):
        report_list = BugController.get_all_bugs()
        return render(request, 'bug_tracker/bug_report_list.html', {'report_list': report_list})


def logout_view(request):
    logout(request)
    return redirect('tracker:login')
    # Redirect to a success page.


def handler404(request, exception):
    context = RequestContext(request)
    err_code = 404
    response = render_to_response('404.html', {"code": err_code}, context)
    response.status_code = 404
    return response
