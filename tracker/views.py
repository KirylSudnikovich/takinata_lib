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
from lib.storage.project import ProjectStorage


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
        if request.method == 'POST':
            name = request.POST['name']
            description = request.POST['description']
            if request.user.is_authenticated:
                username = request.user.username
                password = request.user.password
                ProjectController.create(username, password, name, description)
                return redirect('tracker:projects')


class ProjectInfo(View):
    def get(self, request, project_id):
        project = ProjectStorage.get_project_by_id(project_id)
        guys = ProjectStorage.right_get_personts(project)
        print("gays - ", guys)
        return render(request, 'project.html', {'project': project, 'guys': guys})


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
