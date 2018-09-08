def success_create():
    print("Project is successfully created")


def success_delete():
    print("Project is successfully deleted")


def success_added():
    print("User was successfully added to the project")


def success_removed():
    print("User was successfully removed from the project")


def success_edit():
    print("Pproject was successfully edited")


def project_info(projectdict):
    project = projectdict['project']
    categories = projectdict['categories']
    tasks = projectdict['tasks']
    creator = projectdict['creator']
    guys = projectdict['guys']
    print('project id - {}\nproject name - {}\nproject description - {}\n'.format(project.id, project.name, project.description))
    cat_str = ""
    for category in categories:
        cat_str += category.name
        cat_str += ', '
    print("categories - {}".format(cat_str))
    task_str = ""
    for task in tasks:
        task_str += task.name
        task_str += ', '
    print("tasks - {}".format(task_str))
    print("creator - {}".format(creator.username))
    executors = ""
    for guy in guys:
        executors += guy.username
        executors += ', '
    print("executors - {}".format(executors))
