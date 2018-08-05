def create_format():
    print("Wrong format. To create a task, enter a command like task add 'username' 'password' 'project name' "
          "'column name' 'task name' 'description' 'first date' 'second date' 'tags' 'priority'")


def add_subtask_format():
    print("Wrong format. To create a task, enter a command like task subtask add 'username' 'password' "
          "'project name' 'column name' 'first task' 'second task'")


def edit_format():
    print("Wrong format. To create a task, enter a command like tadk edit 'name/desc/tags/priority' 'username' "
          "'password' 'project name' 'column name' 'task name' 'new value")


def show_tasks(tasks):
    print("Information about current tasks:\n")
    for i in tasks:
        print("Name  - {}\nDescription - {}\nStart - {}\nEnd - {}\nTags - {}\nPriority - "
              "{}\n".format(i.name, i.desc, i.first_date, i.second_date, i.tags, i.priority))


def success_create(i):
    print("Task is successfully created")
    print("Name  - {}\nDescription - {}\nStart - {}\nEnd - {}\nTags - {}\nPriority - "
          "{}\n".format(i.name, i.desc, i.first_date, i.second_date, i.tags, i.priority))


def success_edit(cls):
    print("Task is successfully edited")