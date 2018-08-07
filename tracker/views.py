from django.contrib.auth import authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView
from .forms import SignupForm
from django.views import View
from lib.controllers.project import ProjectController
from lib.controllers.column import ColumnController
from lib.storage.column import ColumnStorage
from lib.storage.project import ProjectStorage
from lib.storage.user import UserStorage


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
            guys = ProjectStorage.right_get_personts(project)
            all_users = UserStorage.right_get_all_users()
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
            print("ALARM - ", request.user.username)
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
            column_list = ColumnController.show_all(username, password)
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
                ColumnController.create_columm(request.user.username, request.user.password, project.name, name,
                                               description)
                return redirect('tracker:projects')
        else:
            return render(request, 'no_permission.html')


class ColumnInfo(View):
    def get(self, request, project_id, column_id):
        if request.user.is_authenticated:
            project = ProjectStorage.get_project_by_id(project_id)
            column = ColumnStorage.get_column_by_id(project.name, column_id)
            return render(request, 'column.html', {'project': project,'column': column})
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
