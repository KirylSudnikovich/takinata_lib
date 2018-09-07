import sys

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.views import View
from django.views.generic import TemplateView, FormView
from lib.controllers.category import CategoryController
from lib.controllers.project import ProjectController
from lib.controllers.task import TaskController
from lib.controllers.user import UserController
from lib.storage.task import TaskStorage
from .controllers.tracker_controller import BugController, all_users, all_projects, all_categories, all_tasks
from .forms import ToDoForm


def handler500(request):
    type_, value, traceback = sys.exc_info()
    response = render_to_response('500.html', {'type': type_, 'value': value})
    response.status_code = 500
    return response


def index(request):
    if 'been_before' in request.COOKIES:
        if 'have_account' in request.COOKIES:
            if request.user.is_authenticated:
                red_list, yellow_list, green_list = TaskController.check_notifications(request.user.username,
                                                                                       request.user.password)
                dict_to_template = {'users': all_users(), 'projects': all_projects, 'categories': all_categories(),
                                    'tasks': all_tasks(), 'red_list': red_list, 'yellow_list': yellow_list,
                                    'green_list': green_list}
                response = render(request, 'index.html', dict_to_template)
            else:
                response = redirect('accounts:login')
                return response
        else:
            response = redirect('accounts:registration')
            return response
    else:
        response = render(request, 'welcome.html')
        response.set_cookie(key='been_before', value='1')
    return response


class ProjectsList(View):
    @method_decorator(login_required)
    def get(self, request):
        project_list = ProjectController.show_all(request.user.username, request.user.password)
        return render(request, 'projects/list.html', {'project_list': project_list})


class ProjectNew(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'projects/create.html')

    def post(self, request):
        ProjectController.create(request.user.username, request.user.password, request.POST['name'],
                                 request.POST['description'])
        return redirect('tracker:projects')


class ProjectInfo(View):
    @method_decorator(login_required)
    def get(self, request, project_id):
        dict_to_render = ProjectController.show(request.user.username, request.user.password, project_id)
        return render(request, 'projects/info.html', dict_to_render)

    def post(self, request, project_id):
        if 'add_to_project' in request.POST:
            username = request.POST['add_select']
            user = UserController.get_user_by_name(username)
            ProjectController.add_person_to_project(request.user.username, request.user.password, project_id,
                                                    user)
            return redirect('tracker:project_info', project_id)
        elif 'remove_from_project' in request.POST:
            username = request.POST['remove_select']
            project = ProjectController.get_project_by_id(request.user.username, request.user.password,
                                                          project_id)
            user = UserController.get_user_by_name(username)
            ProjectController.delete_person_from_project(request.user.username, request.user.password, project,
                                                         user)
            return redirect('tracker:project_info', project_id)


class ProjectDelete(View):
    @method_decorator(login_required)
    def get(self, request, project_id):
        if ProjectController.is_admin(request.user.username, project_id):
            project = ProjectController.get_project_by_id(request.user.username, request.user.password,
                                                          project_id)
            return render(request, 'projects/delete.html', {'project': project})
        else:
            return render(request, '501.html')

    def post(self, request, project_id):
        ProjectController.delete_by_id(request.user.username, request.user.password, project_id)
        return redirect('tracker:projects')


class ProjectEdit(View):
    @method_decorator(login_required)
    def get(self, request, project_id):
        if ProjectController.is_admin(request.user.username, project_id):
            project = ProjectController.get_project_by_id(request.user.username, request.user.password,
                                                          project_id)
            return render(request, 'projects/edit.html', {'project': project})
        else:
            return render(request, '501.html')

    def post(self, request, project_id):
        project = ProjectController.get_project_by_id(request.user.username, request.user.password, project_id)
        if project.name != request.POST['name']:
            ProjectController.edit_name_by_id(request.user.username, request.user.password, project.id,
                                              request.POST['name'])
        ProjectController.edit_description_by_id(request.user.username, request.user.password, project.id,
                                                 request.POST['description'])
        return redirect('tracker:project_info', project_id=project_id)


class CategoryList(View):
    @method_decorator(login_required)
    def get(self, request):
        username = request.user.username
        password = request.user.password
        projects = ProjectController.show_all(username, password)
        category_list = []
        for project in projects:
            categories = CategoryController.show_all(username, password, project)
            category_list = category_list + categories
        return render(request, 'categories/list.html', {'category_list': category_list})


class ColumnNew(View):
    @method_decorator(login_required)
    def get(self, request):
        projects = ProjectController.show_all(request.user.username, request.user.password)
        return render(request, 'categories/create.html', {'projects': projects})

    def post(self, request):
        name = request.POST['name']
        description = request.POST['description']
        project = ProjectController.get_project_by_id(request.user.username, request.user.password,
                                                      request.POST['select_project'])
        CategoryController.create_category(username=request.user.username, password=request.user.password,
                                           project_id=project.id, name=name, description=description)
        return redirect('tracker:column_list')


class ColumnInfo(View):
    @method_decorator(login_required)
    def get(self, request, category_id):
        category = CategoryController.get_category_by_id(category_id)
        project = ProjectController.get_project_by_id(request.user.username, request.user.password,
                                                      category.project_id)
        tasks = TaskStorage.get_all_tasks(category.id)
        if ProjectController.check_permission(request.user.username, request.user.password, project.id):
            return render(request, 'categories/info.html',
                          {'project': project, 'category': category, 'tasks': tasks})
        else:
            return render(request, '501.html')


class ColumnDelete(View):
    @method_decorator(login_required)
    def get(self, request, category_id):
        category = CategoryController.get_category_by_id(category_id)
        project = ProjectController.get_project_by_id(request.user.username, request.user.password,
                                                      category.project_id)
        if ProjectController.is_admin(request.user.username, project.id):
            return render(request, 'categories/delete.html', {'project': project, 'category': category})
        else:
            return render(request, '501.html')

    def post(self, request, category_id):
        category = CategoryController.get_category_by_id(category_id)
        CategoryController.delete_category(request.user.username, request.user.password, category.project_id,
                                           category.name)
        return redirect('tracker:column_list')


class ColumnEdit(View):
    @method_decorator(login_required)
    def get(self, request, category_id):
        category = CategoryController.get_category_by_id(category_id)
        project = ProjectController.get_project_by_id(request.user.username, request.user.password,
                                                      category.project_id)
        if ProjectController.is_admin(request.user.username, project.id):
            return render(request, 'categories/edit.html', {'project': project, 'category': category})
        else:
            return render(request, '501.html')

    def post(self, request, category_id):
        project = ProjectController.get_project_by_id(request.user.username, request.user.password,
                                                      CategoryController.get_category_by_id(category_id).project_id)
        CategoryController.edit_name_by_id(request.user.username, request.user.password, project.id,
                                           category_id,
                                           request.POST['name'])
        CategoryController.edit_desc_by_id(request.user.username, request.user.password, project.id,
                                           category_id,
                                           request.POST['description'])
        return redirect("tracker:column_info", category_id=category_id)


class TaskList(View):
    @method_decorator(login_required)
    def get(self, request):
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


class TaskCreate(FormView):
    @method_decorator(login_required)
    def get(self, request, **kwargs):
        f = ToDoForm
        projects = ProjectController.show_all(request.user.username, request.user.password)
        categories_to_send = []
        for project in projects:
            categories = CategoryController.show_all(request.user.username, request.user.password, project)
            categories_to_send += categories
        return render(request, 'tasks/create.html',
                      {'form': f, 'projects': projects, 'categories': categories_to_send})

    def post(self, request, **kwargs):
        f = ToDoForm(request.POST)
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
                TaskController.add_task(request.user.username, request.user.password, None, None, name, desc,
                                        task_type,
                                        start_date, start_time, end_date, end_time, priority)
            TaskController.add_task(request.user.username, request.user.password, project_id, category_id, name,
                                    desc,
                                    task_type, start_date, start_time, end_date, end_time, priority)
            return redirect('tracker:task_list')


class TaskInfo(View):
    @method_decorator(login_required)
    def get(self, request, task_id):
        task = TaskStorage.get_task_by_id(task_id)
        project = ProjectController.get_project_by_id(request.user.username, request.user.password,
                                                      task.project_id)
        if ProjectController.check_permission(request.user.username, request.user.password, project.id):
            category = CategoryController.get_category_by_id(task.category_id)
            badge = None
            status_badge = None
            if task.priority == "max":
                badge = "label label-danger"
            elif task.priority == "medium":
                badge = "label label-primary"
            elif task.priority == "min":
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
            a_task = None
            parent_task = None
            if task.assosiated_task_id is not None:
                a_task = TaskController.get_assosiated_task(request.user.username, request.user.password, task)
            if task.parent_task_id is not None:
                parent_task = TaskController.get_parent_task(request.user.username, request.user.password, task)
            subtasks = None
            if task.is_parent == 1:
                subtasks = TaskController.get_all_subtask(task)
            return render(request, 'tasks/info.html',
                          {'project': project, 'category': category, 'task': task, 'badge': badge,
                           'status': status,
                           'status_badge': status_badge, 'archive': archive, 'task_list': new_list,
                           'a_task': a_task,
                           'parent': parent_task, 'subtasks': subtasks})
        else:
            return render(request, '501.html')

    def post(self, request, task_id):
        if 'cancel_task' in request.POST:
            task = TaskStorage.get_task_by_id(task_id)
            TaskController.cancel_task(task)
            return redirect('tracker:task_list')
        if 'start_again' in request.POST:
            task = TaskStorage.get_task_by_id(task_id)
            TaskController.start_again(request.user.username, request.user.password, task)
            return self.get(request, task_id)
        if 'add_assosiate' in request.POST:
            task = TaskStorage.get_task_by_id(task_id)
            task_with_id = int(request.POST.get('add_assosiate', False))
            TaskController.set_assosiated_task(request.user.username, request.user.password, task, task_with_id)
            return self.get(request, task_id)
        if 'add_subtask' in request.POST:
            task = TaskStorage.get_task_by_id(task_id)
            task_with_id = int(request.POST.get('add_subtask', False))
            TaskController.new_set_subtask(request.user.username, request.user.password, task,
                                           TaskStorage.get_task_by_id(task_with_id))
            return self.get(request, task_id)


class TaskDelete(View):
    @method_decorator(login_required)
    def get(self, request, task_id):
        task = TaskStorage.get_task_by_id(task_id)
        project = ProjectController.get_project_by_id(request.user.username, request.user.password,
                                                      task.project_id)
        category = CategoryController.get_category_by_id(task.category_id)
        if ProjectController.check_permission(request.user.username, request.user.password, project.id):
            return render(request, 'tasks/delete.html',
                          {'project': project, 'category': category, 'task': task})
        else:
            return render(request, '501.html')

    def post(self, request, task_id):
        if request.user.is_authenticated:
            task = TaskStorage.get_task_by_id(task_id)
            TaskController.delete_task(task.id)
            return redirect('tracker:task_list')
        else:
            return render(request, '501.html')


class BugReport(View):
    @method_decorator(login_required)
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


def handler404(request, exception):
    context = RequestContext(request)
    err_code = 404
    response = render_to_response('404.html', {"code": err_code}, context)
    response.status_code = 404
    return response
