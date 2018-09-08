import argparse
import sys

import lib.conf as config
from lib.controllers.user import UserController
from lib.controllers.project import ProjectController
from lib.controllers.category import CategoryController
from lib.controllers.task import TaskController
from console.presentations.user import success_reg, success_del
from console.presentations import project as pr_pres
from console.presentations import category as ct_pres
from console.presentations import task as ts_pres


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


def parse():
    parser = MyParser()
    parser.add_argument('-l', dest='login', help='login of user')
    parser.add_argument('-p', dest='password', help='password of user')
    subparsers = parser.add_subparsers(dest='action')

    user_parser = subparsers.add_parser('user', help='Menu to work with users')
    user_root_subparser = user_parser.add_subparsers(dest='user', help='Choose action')

    user_reg_parser = user_root_subparser.add_parser('reg', help="Register new user")
    user_reg_parser.add_argument('-u', dest='username', help='login of new user')
    user_reg_parser.add_argument('-p', dest='password', help='password of new user')
    user_reg_parser.add_argument('-m', dest='mail', help='mail of new user')

    user_delete_parser = user_root_subparser.add_parser('delete', help="Delete user")
    user_delete_parser.add_argument('-u', dest='username', help='username')
    user_delete_parser.add_argument('-p', dest='password', help='password of user')

    init_project_parser(subparsers)
    init_category_parser(subparsers)
    init_task_parser(subparsers)
    # init_plan_parser(subparsers)
    #  init_show_parser(subparsers)
    # test_parser = subparsers.add_parser('tests', help='Start tests')

    parsed = parser.parse_args()
    print(parsed)

    try:
        proccess_parsed(parsed)
    except Exception as error:
        print(error)


def proccess_parsed(parsed):
    if parsed.action == 'user':
        proccess_user(parsed)
    elif parsed.action == 'project':
        proccess_project(parsed)
    elif parsed.action == 'category':
        proccess_category(parsed)
    elif parsed.action == 'task':
        proccess_task(parsed)


def proccess_user(parsed):
    username = getattr(parsed, 'username', None)
    password = getattr(parsed, 'password', None)
    email = getattr(parsed, 'mail', None)

    if parsed.user == 'reg':
        UserController.reg(username, password, email)
        success_reg()
    elif parsed.user == 'delete':
        UserController.delete(username, password)
        success_del()


def init_project_parser(root):
    project_parser = root.add_parser('project', help='Menu, that will help you to work with projects')
    project_root_subparser = project_parser.add_subparsers(dest='project', help='Choose action')

    create_project_parser = project_root_subparser.add_parser('create', help='Create new project')
    create_project_parser.add_argument('-u', dest='username', type=str, help='Username of project creator',
                                       required=True)
    create_project_parser.add_argument('-p', dest='password', type=str, help='User password', required=True)
    create_project_parser.add_argument('-n', dest='name', type=str, help='Project name', required=True)
    create_project_parser.add_argument('-d', dest='description', type=str, help='Project description')

    delete_project_parser = project_root_subparser.add_parser('delete', help='Delete project')
    delete_project_parser.add_argument('-u', dest='username', type=str, help='Username of project creator',
                                       required=True)
    delete_project_parser.add_argument('-p', dest='password', type=str, help='User password', required=True)
    delete_project_parser.add_argument('-pid', dest='id', type=int, help="ID of project to delete", required=True)

    add_user_to_project_parser = project_root_subparser.add_parser("add_user", help='Add user to project')
    add_user_to_project_parser.add_argument('-u', dest='username', type=str, help='Username of project creator',
                                            required=True)
    add_user_to_project_parser.add_argument('-p', dest='password', type=str, help='User password', required=True)
    add_user_to_project_parser.add_argument('-pid', dest='project id', type=int, help='ID of project where adds user',
                                            required=True)
    add_user_to_project_parser.add_argument('-uid', dest='user id', type=int, help='ID of user which adds to project',
                                            required=True)

    delete_user_from_project_parser = project_root_subparser.add_parser("remove_user", help="Remove user from project")
    delete_user_from_project_parser.add_argument('-u', dest='username', type=str, help='Username of project creator',
                                                 required=True)
    delete_user_from_project_parser.add_argument('-p', dest='password', type=str, help='Password of project creator',
                                                 required=True)
    delete_user_from_project_parser.add_argument('-pid', dest='project id', type=int,
                                                 help='ID of project where user will be deleted', required=True)
    delete_user_from_project_parser.add_argument('-uid', dest='user id', type=int,
                                                 help='ID of user which will be deleted', required=True)

    edit_project_name_parser = project_root_subparser.add_parser("edit_name", help="Edit name of project")
    edit_project_name_parser.add_argument('-u', dest='username', type=str, help='Username of project creator',
                                          required=True)
    edit_project_name_parser.add_argument('-p', dest='password', type=str, help='Password of project creator',
                                          required=True)
    edit_project_name_parser.add_argument('-pid', dest='project id', type=int,
                                          help='ID of project where user will be deleted', required=True)
    edit_project_name_parser.add_argument('-n', dest='name', type=str, help='New of of the project')

    edit_project_description_parser = project_root_subparser.add_parser("edit_description",
                                                                        help="Edit description of project")
    edit_project_description_parser.add_argument('-u', dest='username', type=str, help='Username of project creator',
                                                 required=True)
    edit_project_description_parser.add_argument('-p', dest='password', type=str, help='Password of project creator',
                                                 required=True)
    edit_project_description_parser.add_argument('-pid', dest='project id', type=int,
                                                 help='ID of project where user will be deleted', required=True)
    edit_project_description_parser.add_argument('-d', dest='description', type=str, help='New of of the project')

    project_show_parser = project_root_subparser.add_parser("show", help="Show information about project")
    project_show_parser.add_argument('-u', dest='username', type=str, help='Username of project executor',
                                     required=True)
    project_show_parser.add_argument('-p', dest='password', type=str, help='Password of project executor',
                                     required=True)
    project_show_parser.add_argument('-pid', dest='project id', type=int, help="ID of project to show info",
                                     required=True)


def proccess_project(parsed):
    if parsed.project == 'create':
        proccess_create_project(parsed)
    elif parsed.project == 'delete':
        proccess_delete_project(parsed)
    elif parsed.project == 'add_user':
        proccess_add_user_project(parsed)
    elif parsed.project == 'remove_user':
        proccess_remove_user_project(parsed)
    elif parsed.project == 'edit_name':
        proccess_edit_name_project(parsed)
    elif parsed.project == 'edit_description':
        proccess_edit_description_project(parsed)
    elif parsed.project == 'show':
        proccess_show_project(parsed)


def proccess_create_project(parsed):
    username = getattr(parsed, 'username', None)
    password = getattr(parsed, 'password', None)
    name = getattr(parsed, 'name', None)
    description = getattr(parsed, 'description', None)

    ProjectController.create(username, password, name, description)
    pr_pres.success_create()


def proccess_delete_project(parsed):
    username = getattr(parsed, 'username', None)
    password = getattr(parsed, 'password', None)
    id = getattr(parsed, 'id', None)

    ProjectController.delete_by_id(username, password, id)
    pr_pres.success_delete()


def proccess_add_user_project(parsed):
    username = getattr(parsed, 'username', None)
    password = getattr(parsed, 'password', None)
    pid = getattr(parsed, 'project id', None)
    uid = getattr(parsed, 'user id', None)

    ProjectController.add_person_to_project(username, password, pid, uid)
    pr_pres.success_added()


def proccess_remove_user_project(parsed):
    username = getattr(parsed, 'username', None)
    password = getattr(parsed, 'password', None)
    pid = getattr(parsed, 'project id', None)
    uid = getattr(parsed, 'user id', None)
    ProjectController.delete_person_from_project(username, password, pid, uid)
    pr_pres.success_removed()


def proccess_edit_name_project(parsed):
    username = getattr(parsed, 'username', None)
    password = getattr(parsed, 'password', None)
    pid = getattr(parsed, 'project id', None)
    name = getattr(parsed, 'name', None)
    ProjectController.edit_name_by_id(username, password, pid, name)
    pr_pres.success_edit()


def proccess_edit_description_project(parsed):
    username = getattr(parsed, 'username', None)
    password = getattr(parsed, 'password', None)
    pid = getattr(parsed, 'project id', None)
    description = getattr(parsed, 'description', None)
    ProjectController.edit_description_by_id(username, password, pid, description)
    pr_pres.success_edit()


def proccess_show_project(parsed):
    username = getattr(parsed, 'username', None)
    password = getattr(parsed, 'password', None)
    pid = getattr(parsed, 'project id', None)
    projectdict = ProjectController.show(username, password, pid)
    pr_pres.project_info(projectdict)


def init_category_parser(root):
    category_parser = root.add_parser('category', help='Menu, that will help you to work with categories')
    category_root_subparser = category_parser.add_subparsers(dest='category', help='Choose action')

    create_category_parser = category_root_subparser.add_parser('create', help='Create new category')
    create_category_parser.add_argument('-u', dest='username', type=str, help='Username of project creator',
                                        required=True)
    create_category_parser.add_argument('-p', dest='password', type=str, help='User password', required=True)
    create_category_parser.add_argument('-pid', dest='project id', type=int, help="ID of project to show info",
                                        required=True)
    create_category_parser.add_argument('-n', dest='name', type=str, help='Category name', required=True)
    create_category_parser.add_argument('-d', dest='description', type=str, help='Category description', required=True)

    delete_category_parser = category_root_subparser.add_parser('delete', help='Create new category')
    delete_category_parser.add_argument('-u', dest='username', type=str, help='Username of project creator',
                                        required=True)
    delete_category_parser.add_argument('-p', dest='password', type=str, help='User password', required=True)
    delete_category_parser.add_argument('-pid', dest='project id', type=int, help="ID of project to show info",
                                        required=True)
    delete_category_parser.add_argument('-n', dest='name', type=str, help='Category name', required=True)

    edit_name_category_parser = category_root_subparser.add_parser('edit_name', help='Create new category')
    edit_name_category_parser.add_argument('-u', dest='username', type=str, help='Username of project creator',
                                           required=True)
    edit_name_category_parser.add_argument('-p', dest='password', type=str, help='User password', required=True)
    edit_name_category_parser.add_argument('-pid', dest='project id', type=int, help="ID of project to show info",
                                           required=True)
    edit_name_category_parser.add_argument('-cid', dest='category id', type=int, help='Category id', required=True)
    edit_name_category_parser.add_argument('-n', dest='new name', type=str, help='New name for category', required=True)

    edit_desc_category_parser = category_root_subparser.add_parser('edit_desc', help='Create new category')
    edit_desc_category_parser.add_argument('-u', dest='username', type=str, help='Username of project creator',
                                           required=True)
    edit_desc_category_parser.add_argument('-p', dest='password', type=str, help='User password', required=True)
    edit_desc_category_parser.add_argument('-pid', dest='project id', type=int, help="ID of project to show info",
                                           required=True)
    edit_desc_category_parser.add_argument('-cid', dest='category id', type=int, help='Category id', required=True)
    edit_desc_category_parser.add_argument('-d', dest='new desc', type=str, help='New name for category', required=True)

    show_all_category_parser = category_root_subparser.add_parser('show_all', help='Create new category')
    show_all_category_parser.add_argument('-u', dest='username', type=str, help='Username of project creator',
                                          required=True)
    show_all_category_parser.add_argument('-p', dest='password', type=str, help='User password', required=True)
    show_all_category_parser.add_argument('-pid', dest='project id', type=int, help="ID of project to show info",
                                          required=True)


def proccess_category(parsed):
    if parsed.category == 'create':
        proccess_create_category(parsed)
    elif parsed.category == 'delete':
        proccess_delete_category(parsed)
    elif parsed.category == 'edit_name':
        proccess_edit_name_category(parsed)
    elif parsed.category == 'edit_desc':
        proccess_edit_desc_category(parsed)
    elif parsed.category == 'show_all':
        proccess_show_all_category(parsed)


def proccess_create_category(parsed):
    username = getattr(parsed, 'username', None)
    password = getattr(parsed, 'password', None)
    pid = getattr(parsed, 'project id', None)
    name = getattr(parsed, 'name', None)
    description = getattr(parsed, 'description', None)
    CategoryController.create_category(username, password, pid, name, description)
    ct_pres.success_create()


def proccess_delete_category(parsed):
    username = getattr(parsed, 'username', None)
    password = getattr(parsed, 'password', None)
    pid = getattr(parsed, 'project id', None)
    name = getattr(parsed, 'name', None)
    CategoryController.delete_category(username, password, pid, name)
    ct_pres.success_delete()


def proccess_edit_name_category(parsed):
    username = getattr(parsed, 'username', None)
    password = getattr(parsed, 'password', None)
    pid = getattr(parsed, 'project id', None)
    cid = getattr(parsed, 'category id', None)
    name = getattr(parsed, 'new name', None)
    CategoryController.edit_name_by_id(username, password, pid, cid, name)
    ct_pres.success_edit()


def proccess_edit_desc_category(parsed):
    username = getattr(parsed, 'username', None)
    password = getattr(parsed, 'password', None)
    pid = getattr(parsed, 'project id', None)
    cid = getattr(parsed, 'category id', None)
    desc = getattr(parsed, 'new desc', None)
    CategoryController.edit_desc_by_id(username, password, pid, cid, desc)
    ct_pres.success_edit()


def proccess_show_all_category(parsed):
    username = getattr(parsed, 'username', None)
    password = getattr(parsed, 'password', None)
    pid = getattr(parsed, 'project id', None)
    cats = CategoryController.show_all(username, password, pid)
    ct_pres.show_all(cats)


def init_task_parser(root):
    task_parser = root.add_parser('task', help='Menu, that will help you to work with tasks')
    task_root_subparser = task_parser.add_subparsers(dest='task', help='Choose action')

    create_task_parser = task_root_subparser.add_parser('create', help='Create new task')
    create_task_parser.add_argument('-u', dest='username', type=str, help='Username of project executor', required=True)
    create_task_parser.add_argument('-p', dest='password', type=str, help='Password of project executor', required=True)
    create_task_parser.add_argument('-pid', dest='project id', type=int, help='ID of project where want to add task',
                                    required=True)
    create_task_parser.add_argument('-cid', dest='category id', type=int, help='ID of category where want to add task',
                                    required=True)
    create_task_parser.add_argument('-n', dest='name', type=str, help='Task name', required=True)
    create_task_parser.add_argument('-d', dest='description', type=str, help='Task description')
    create_task_parser.add_argument('-t', dest='type', type=int, help='Task type (1 - One-time, 2 - Regular)',
                                    required=True)
    create_task_parser.add_argument('-sd', dest='start date', type=str, help='Date of task start')
    create_task_parser.add_argument('-st', dest='start time', type=str, help='Time of task start')
    create_task_parser.add_argument('-ed', dest='end date', type=str, help='Date of task end')
    create_task_parser.add_argument('-et', dest='end time', type=str, help='Time of task end')
    create_task_parser.add_argument('-pr', dest='priority', type=str, help='Task priority', required=True)

    delete_task_parser = task_root_subparser.add_parser('delete', help='Delete a task with specified name')
    delete_task_parser.add_argument('-u', dest='username', type=str, help='Username of project executor', required=True)
    delete_task_parser.add_argument('-p', dest='password', type=str, help='Password of project executor', required=True)
    delete_task_parser.add_argument('-tid', dest='task id', type=int, help='Task ID', required=True)

    cancel_task_parser = task_root_subparser.add_parser('cancel', help='Set task status as done')
    cancel_task_parser.add_argument('-u', dest='username', type=str, help='Username of project executor', required=True)
    cancel_task_parser.add_argument('-p', dest='password', type=str, help='Password of project executor', required=True)
    cancel_task_parser.add_argument('-tid', dest='task id', type=int, help='Task ID', required=True)

    set_assosiated_task_parser = task_root_subparser.add_parser('set_assosiated_task', help='Set assosiated task')
    set_assosiated_task_parser.add_argument('-u', dest='username', type=str, help='Username of project executor',
                                            required=True)
    set_assosiated_task_parser.add_argument('-p', dest='password', type=str, help='Password of project executor',
                                            required=True)
    set_assosiated_task_parser.add_argument('-tid', dest='task id', type=int, help='Task ID', required=True)
    set_assosiated_task_parser.add_argument('-atid', dest='atask id', type=int, help='aTask ID', required=True)

    set_parent_task_parser = task_root_subparser.add_parser('set_assosiated_task', help='Set assosiated task')
    set_parent_task_parser.add_argument('-u', dest='username', type=str, help='Username of project executor',
                                        required=True)
    set_parent_task_parser.add_argument('-p', dest='password', type=str, help='Password of project executor',
                                        required=True)
    set_parent_task_parser.add_argument('-sid', dest='subtask id', type=int, help='Subask ID', required=True)
    set_parent_task_parser.add_argument('-ptid', dest='parent task id', type=int, help='Parent task ID', required=True)

    start_again_task_parser = task_root_subparser.add_parser('set_assosiated_task', help='Set assosiated task')
    start_again_task_parser.add_argument('-u', dest='username', type=str, help='Username of project executor',
                                         required=True)
    start_again_task_parser.add_argument('-p', dest='password', type=str, help='Password of project executor',
                                         required=True)
    start_again_task_parser.add_argument('-tid', dest='task id', type=int, help='Task ID', required=True)

    check_notification_parser = task_root_subparser.add_parser('check_notifications',
                                                               help='Check notifications for user')
    check_notification_parser.add_argument('-u', dest='username', type=str, help='Username of project executor')
    check_notification_parser.add_argument('-p', dest='password', type=str, help='Password')

    show_task_parser = task_root_subparser.add_parser('show', help='Show task info')
    show_task_parser.add_argument('-u', dest='username', type=str, help='Username of project executor')
    show_task_parser.add_argument('-p', dest='password', type=str, help='Password of project executor')
    show_task_parser.add_argument('-tid', dest='task id', type=int, help='Task ID')


def proccess_task(parsed):
    if parsed.task == 'create':
        proccess_create_task(parsed)
    elif parsed.task == 'delete':
        proccess_delete_task(parsed)
    elif parsed.task == 'set_assosiated_task':
        set_assosiated_task(parsed)
    elif parsed.task == 'set_parent_task':
        set_parent_task(parsed)
    elif parsed.task == 'start_again':
        start_again_task(parsed)
    elif parsed.task == 'show':
        proccess_show_task(parsed)


def proccess_category(parsed):
    if parsed.category == 'create':
        proccess_create_category(parsed)
    elif parsed.category == 'delete':
        proccess_delete_category(parsed)
    elif parsed.category == 'edit_name':
        proccess_edit_name_category(parsed)
    elif parsed.category == 'edit_desc':
        proccess_edit_desc_category(parsed)
    elif parsed.category == 'show_all':
        proccess_show_all_category(parsed)


def proccess_create_task(parsed):
    username = getattr(parsed, 'username', None)
    password = getattr(parsed, 'password', None)
    project_id = getattr(parsed, 'project id', None)
    category_id = getattr(parsed, 'category id', None)
    name = getattr(parsed, 'name', None)
    description = getattr(parsed, 'description', None)
    type = getattr(parsed, 'type', None)
    start_date = getattr(parsed, 'start date', None)
    start_time = getattr(parsed, 'start time', None)
    end_date = getattr(parsed, 'end date', None)
    end_time = getattr(parsed, 'end time', None)
    priority = getattr(parsed, 'priority', None)

    TaskController.add_task(username, password, project_id, category_id, name, description, type, start_date,
                            start_time, end_date, end_time, priority)
    ts_pres.success_create()


def proccess_delete_task(parsed):
    username = getattr(parsed, 'username', None)
    password = getattr(parsed, 'password', None)
    task_id = getattr(parsed, 'task id', None)

    TaskController.delete_task(username, password, task_id)
    ts_pres.success_delete()


def set_assosiated_task(parsed):
    username = getattr(parsed, 'username', None)
    password = getattr(parsed, 'password', None)
    task_id = getattr(parsed, 'task id', None)
    atask_id = getattr(parsed, 'atask id', None)

    TaskController.set_assosiated_task(username, password, task_id, atask_id)
    ts_pres.success_assosiate()


def set_parent_task(parsed):
    username = getattr(parsed, 'username', None)
    password = getattr(parsed, 'password', None)
    task_id = getattr(parsed, 'subtask id', None)
    ptask_id = getattr(parsed, 'parent task id', None)

    TaskController.new_set_subtask(username, password, task_id, ptask_id)


def start_again_task(parsed):
    username = getattr(parsed, 'username', None)
    password = getattr(parsed, 'password', None)
    task_id = getattr(parsed, 'subtask id', None)

    TaskController.start_again(username, password, task_id)


def proccess_show_task(parsed):
    username = getattr(parsed, 'username', None)
    password = getattr(parsed, 'password', None)
    task_id = getattr(parsed, 'task id', None)

    task = TaskController.show(username, password, task_id)
    ts_pres.show(task)
