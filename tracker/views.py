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

from .controllers.bug_report import BugController
from .forms import SignupForm, ToDoForm


def index(request):
    return render(request, 'index.html')


class ProjectsList(View):
    def get(self, request):
        if request.user.is_authenticated:
            username = request.user.username
            password = request.user.password
            project_list = ProjectController.show_all(username, password)
            print(project_list)
            return render(request, 'projects.html', {'project_list': project_list})
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
            columns = ColumnController.show_all(request.user.username, request.user.password, project.name)
            all_users = UserStorage.get_all_users()
            guys = ProjectStorage.get_all_persons_in_project(project)
            all_guys = []
            guys_names = []
            for i in guys:
                guys_names.append(i.username)
            for i in all_users:
                if i.username not in guys_names:
                    all_guys.append(i)
            return render(request, 'project.html',
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
            return render(request, 'project_delete.html', {'project': project})
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
            return render(request, 'project_edit.html', {'project': project})
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
                columns = ColumnController.show_all(username, password, project.name)
                column_list = column_list + columns
            return render(request, 'columns.html', {'column_list': column_list})
        else:
            return render(request, 'no_permission.html')


class ColumnNew(View):
    def get(self, request):
        projects = ProjectController.show_all(request.user.username, request.user.password)
        return render(request, 'column_new.html', {'projects': projects})

    def post(self, request):
        if request.user.is_authenticated:
            if request.method == 'POST':
                name = request.POST['name']
                description = request.POST['description']
                project = ProjectStorage.get_project(request.POST['select_project'])
                ColumnController.create_columm(username=request.user.username, password=request.user.password,
                                               project_name=project.name, name=name, description=description)
                # column = Column(name=name, desc=description, project_id=project.id)
                # log.info("")
                # ColumnStorage.add_column_to_db(column)
                return redirect('tracker:columns')
        else:
            return render(request, 'no_permission.html')


class ColumnInfo(View):
    def get(self, request, project_id, column_id):
        if request.user.is_authenticated:
            project = ProjectStorage.get_project_by_id(project_id)
            column = ColumnStorage.get_column_by_id(project.name, column_id)
            return render(request, 'column.html', {'project': project, 'column': column})
        else:
            return render(request, 'no_permission.html')


class ColumnDelete(View):
    def get(self, request, project_id, column_id):
        if request.user.is_authenticated:
            project = ProjectStorage.get_project_by_id(project_id)
            column = ColumnStorage.get_column_by_id(project.name, column_id)
            return render(request, 'column_delete.html', {'project': project, 'column': column})
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
            return render(request, 'column_edit.html', {'project': project, 'column': column})
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
        return render(request, 'tasks/list.html')


class SampleView(FormView):
    def get(self, request, **kwargs):
        f = ToDoForm
        projects = ProjectController.show_all(request.user.username, request.user.password)
        columns_to_send = []
        for project in projects:
            columns = ColumnController.show_all(request.user.username, request.user.password, project.name)
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
            column = ColumnStorage.get_column_by_id(project.name, request.POST['select_column'])
            TaskController.add_task(request.user.username, request.user.password, project.name, column.name, name, desc,
                                    start_date, start_time, end_date, end_time, tags, priority)

    #
    # if request.method == 'POST':
    #     f = SignupForm(request.POST)
    #     if f.is_valid():
    #         f.save()
    #         messages.success(request, 'Account created successfully')
    #         return redirect('tracker:home')
    # else:
    #     f = SignupForm
    #
    # return render(request, 'registration/signup.html', {'form': f})


def filter_columns(columns, project):
    to_return = []
    for i in columns:
        if columns.project_id == project.id:
            to_return.append(i)
    return to_return


class BugReport(View):
    def get(self, request):
        return render(request, 'bug_fixing.html')

    def post(self, request):
        username = request.user.username
        name = request.POST['name']
        description = request.POST['description']
        BugController.add_bug(username, name, description)
        return redirect('tracker:home')


class BugReportList(View):
    def get(self, request):
        report_list = BugController.get_all_bugs()
        return render(request, 'bug_report_list.html', {'report_list': report_list})


def register(request):
    if request.method == 'POST':
        f = SignupForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            return redirect('tracker:home')
    else:
        f = SignupForm

    return render(request, 'registration/signup.html', {'form': f})


class UserLogin(TemplateView):
    def post(self, request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request)
                return redirect('tracker:home')
        else:
            form = AuthenticationForm()

        return render(request, 'registration/login.html', {'form': form})


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
