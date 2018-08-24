import sys

from django.contrib.auth import logout
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.views import View
from django.views.generic import TemplateView, FormView
from lib.controllers.category import CategoryController
from lib.controllers.project import ProjectController
from lib.storage.category import CategoryStorage
from lib.storage.project import ProjectStorage
from lib.storage.user import UserStorage
from lib.controllers.task import TaskController
from lib.storage.task import TaskStorage
from .controllers.tracker_controller import BugController, all_users, all_projects, all_categories, all_tasks
from .forms import ToDoForm


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
            print(project_list)
            return render(request, 'projects/list.html', {'project_list': project_list})
        else:
            return render(request, '501.html')


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
            return render(request, '501.html')


class ProjectInfo(View):
    def get(self, request, project_id):
        if request.user.is_authenticated:
            project = ProjectStorage.get_project_by_id(project_id)
            categories = CategoryController.show_all(request.user.username, request.user.password, project.id)
            task_list = []
            for category in categories:
                tasks = TaskStorage.get_all_tasks(category.id)
                task_list = task_list + tasks
            available_tasks = []
            canceled_tasks = []
            for task in task_list:
                if task.is_archive == 0:
                    available_tasks.append(task)
                else:
                    canceled_tasks.append(task)
            task_list = available_tasks + canceled_tasks
            all_users = UserStorage.get_all_users()
            guys = ProjectStorage.get_all_persons_in_project_by_id(project)
            all_guys = []
            guys_names = []
            for i in guys:
                guys_names.append(i.username)
            for i in all_users:
                if i.username not in guys_names:
                    all_guys.append(i)
            creator = guys[0]
            guys = guys[1:]
            return render(request, 'projects/info.html',
                          {'project': project, 'categories': categories, 'tasks': task_list, 'guys': guys,
                           'creator': creator, 'all_guys': all_guys})
        else:
            return render(request, '501.html')

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
            if ProjectStorage.check_permission(UserStorage.get_user_by_name(request.user.username), project):
                return render(request, 'projects/delete.html', {'project': project})
            else:
                return render(request, '501.html')
        else:
            return render(request, '501.html')

    def post(self, request, project_id):
        if request.method == 'POST':
            if request.user.is_authenticated:
                ProjectController.delete_by_id(request.user.username, request.user.password, project_id)
                return redirect('tracker:projects')
            else:
                return render(request, '501.html')


class ProjectEdit(View):
    def get(self, request, project_id):
        if request.user.is_authenticated:
            project = ProjectStorage.get_project_by_id(project_id)
            if ProjectStorage.check_permission(UserStorage.get_user_by_name(request.user.username), project):
                return render(request, 'projects/edit.html', {'project': project})
            else:
                return render(request, '501.html')
        else:
            return render(request, '501.html')

    def post(self, request, project_id):
        if request.method == 'POST':
            if request.user.is_authenticated:
                project = ProjectStorage.get_project_by_id(project_id)
                ProjectController.edit_name_by_id(request.user.username, request.user.password, project.id,
                                                  request.POST['name'])
                ProjectController.edit_description_by_id(request.user.username, request.user.password, project.id,
                                                         request.POST['description'])
                return redirect('tracker:projects')
            else:
                return render(request, '501.html')


class CategoryList(View):
    def get(self, request):
        if request.user.is_authenticated:
            username = request.user.username
            password = request.user.password
            projects = ProjectController.show_all(username, password)
            category_list = []
            for project in projects:
                categories = CategoryController.show_all(username, password, project.id)
                category_list = category_list + categories
            return render(request, 'categories/list.html', {'category_list': category_list})
        else:
            return render(request, '501.html')


class ColumnNew(View):
    def get(self, request):
        projects = ProjectController.show_all(request.user.username, request.user.password)
        return render(request, 'categories/create.html', {'projects': projects})

    def post(self, request):
        if request.user.is_authenticated:
            if request.method == 'POST':
                name = request.POST['name']
                description = request.POST['description']
                project = ProjectStorage.get_project_by_id(request.POST['select_project'])
                projects = ProjectController.show_all(request.user.username, request.user.password)
                for i in projects:
                    if project.name == i.name:
                        project = i
                print("Project_id = ", request.POST['select_project'])
                CategoryController.create_category(username=request.user.username, password=request.user.password,
                                                   project_id=project.id, name=name, description=description)
                return redirect('tracker:column_list')
        else:
            return render(request, '501.html')


class ColumnInfo(View):
    def get(self, request, category_id):
        if request.user.is_authenticated:
            category = CategoryStorage.get_category_by_id(category_id)
            project = ProjectStorage.get_project_by_id(category.project_id)
            tasks = TaskStorage.get_all_tasks(category.id)
            if ProjectStorage.check_permission(UserStorage.get_user_by_name(request.user.username), project):
                return render(request, 'categories/info.html',
                              {'project': project, 'category': category, 'tasks': tasks})
            else:
                return render(request, '501.html')
        else:
            return render(request, '501.html')


class ColumnDelete(View):
    def get(self, request, category_id):
        if request.user.is_authenticated:
            category = CategoryStorage.get_category_by_id(category_id)
            project = ProjectStorage.get_project_by_id(category.project_id)
            if ProjectStorage.check_permission(UserStorage.get_user_by_name(request.user.username), project):
                return render(request, 'categories/delete.html', {'project': project, 'category': category})
            else:
                return render(request, '501.html')
        else:
            return render(request, '501.html')

    def post(self, request, category_id):
        if request.method == 'POST':
            if request.user.is_authenticated:
                category = CategoryStorage.get_category_by_id(category_id)
                CategoryStorage.delete_column_from_db(category)
                return redirect('tracker:projects')
            else:
                return render(request, '501.html')


class ColumnEdit(View):
    def get(self, request, category_id):
        if request.user.is_authenticated:
            category = CategoryStorage.get_category_by_id(category_id)
            project = ProjectStorage.get_project_by_id(category.project_id)
            if ProjectStorage.check_permission(UserStorage.get_user_by_name(request.user.username), project):
                return render(request, 'categories/edit.html', {'project': project, 'category': category})
            else:
                return render(request, '501.html')
        else:
            return render(request, '501.html')

    def post(self, request, category_id):
        if request.method == 'POST':
            if request.user.is_authenticated:
                project = ProjectStorage.get_project_by_id(CategoryStorage.get_category_by_id(category_id).project_id)
                CategoryController.edit_name_by_id(request.user.username, request.user.password, project.id,
                                                   category_id,
                                                   request.POST['name'])
                CategoryController.edit_desc_by_id(request.user.username, request.user.password, project.id,
                                                   category_id,
                                                   request.POST['description'])
                return redirect("tracker:column_list")
            else:
                return render(request, '501.html')


class TaskList(View):
    def get(self, request):
        if request.user.is_authenticated:
            task_list = TaskController.get_all_users_task(request.user.username, request.user.password)

            available_tasks = []
            canceled_tasks = []
            for task in task_list:
                if task.is_archive == 0:
                    available_tasks.append(task)
                else:
                    canceled_tasks.append(task)
            task_list = available_tasks + canceled_tasks
            return render(request, 'tasks/list.html', {'task_list': task_list})
        else:
            return render(request, '501.html')


class SampleView(FormView):
    def get(self, request, **kwargs):
        f = ToDoForm
        projects = ProjectController.show_all(request.user.username, request.user.password)
        categories_to_send = []
        for project in projects:
            categories = CategoryController.show_all(request.user.username, request.user.password, project.id)
            categories_to_send += categories
        return render(request, 'tasks/create.html', {'form': f, 'projects': projects, 'categories': categories_to_send})

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
            priority = request.POST['priority']
            project_id = int(request.POST.get('select_project', False))
            category_id = int(request.POST.get('select_column', False))
            task_type = int(request.POST.get('select_type', False))
            if project_id == False or category_id == False:
                TaskController.add_task(request.user.username, request.user.password, None, None, name, desc, task_type,
                                        start_date, start_time, end_date, end_time, priority)
            TaskController.add_task(request.user.username, request.user.password, project_id, category_id, name, desc,
                                    task_type, start_date, start_time, end_date, end_time, priority)
            return redirect('tracker:task_list')


class TaskInfo(View):
    def get(self, request, task_id):
        if request.user.is_authenticated:
            task = TaskStorage.get_task_by_id(task_id)
            project = ProjectStorage.get_project_by_id(task.project_id)
            if ProjectStorage.check_permission(UserStorage.get_user_by_name(request.user.username), project):
                category = CategoryStorage.get_category_by_id(task.category_id)
                badge = None
                status_badge = None
                if task.priority == "max":
                    badge = "label label-danger"
                elif task.priority == "medium":
                    badge = "label label-primary"
                elif task.priority == "low":
                    badge = "label label-success"
                status = None
                archive = None
                if task.is_archive == 0:
                    status_badge = "label label-danger"
                    status = "In progress"
                elif task.is_archive == 1:
                    status_badge = "label label-success"
                    status = "Done"
                    archive = 1
                task_list = TaskStorage.get_all_tasks(task.category_id)
                new_list = []
                for tsk in task_list:
                    if tsk.id == task_id:
                        task_list.remove(tsk)
                for tsk in task_list:
                    if tsk.is_archive == 1 or tsk.assosiated_task_id is not None or tsk.type == 2:
                        pass
                    else:
                        new_list.append(tsk)
                print("task_list - ", task_list)
                a_task = TaskController.get_assosiated_task(task)
                parent_task = TaskController.get_parent_task(task)
                subtasks = None
                if task.is_parent == 1:
                    subtasks = TaskController.get_all_subtask(task)
                return render(request, 'tasks/info.html',
                              {'project': project, 'category': category, 'task': task, 'badge': badge, 'status': status,
                               'status_badge': status_badge, 'archive': archive, 'task_list': new_list,
                               'a_task': a_task,
                               'parent': parent_task, 'subtasks': subtasks})
            else:
                return render(request, '501.html')
        else:
            return render(request, '501.html')

    def post(self, request, task_id):
        if 'cancel_task' in request.POST:
            task = TaskStorage.get_task_by_id(task_id)
            TaskController.cancel_task(task)
            return redirect('tracker:task_list')
        if 'start_again' in request.POST:
            task = TaskStorage.get_task_by_id(task_id)
            TaskController.start_again(task)
            return self.get(request, task_id)
        if 'add_assosiate' in request.POST:
            task = TaskStorage.get_task_by_id(task_id)
            task_with_id = int(request.POST.get('add_assosiate', False))
            TaskController.set_assosiated_task(task, task_with_id)
            return self.get(request, task_id)
        if 'add_subtask' in request.POST:
            task = TaskStorage.get_task_by_id(task_id)
            task_with_id = int(request.POST.get('add_subtask', False))
            TaskController.new_set_subtask(task, TaskStorage.get_task_by_id(task_with_id))
            return self.get(request, task_id)


class TaskDelete(View):
    def get(self, request, task_id):
        if request.user.is_authenticated:
            task = TaskStorage.get_task_by_id(task_id)
            project = ProjectStorage.get_project_by_id(task.project_id)
            category = CategoryStorage.get_category_by_id(task.category_id)
            if ProjectStorage.check_permission(UserStorage.get_user_by_name(request.user.username), project):
                return render(request, 'tasks/delete.html', {'project': project, 'category': category, 'task': task})
            else:
                return render(request, '501.html')
        else:
            return render(request, '501.html')

    def post(self, request, task_id):
        if request.method == 'POST':
            if request.user.is_authenticated:
                task = TaskStorage.get_task_by_id(task_id)
                TaskController.delete_task(task.id)
                return redirect('tracker:task_list')
            else:
                return render(request, '501.html')


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


def handler500(request):
    type_, value, traceback = sys.exc_info()
    print(type_)
    response = render_to_response('500.html', {'type': type_, 'value': value})
    response.status_code = 500
    return response
