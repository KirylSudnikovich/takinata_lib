def success_create():
    print("Task was successfully created")

def success_delete():
    print("Task was successfully deleted")

def success_assosiate():
    print("Task was successfully assosiated")

def show(task):
    print("Task information:")
    print("Name - {}".format(task.name))
    if task.desc:
        print("Description - {}".format(task.desc))
    if task.start_date:
        print("Start date - {}".format(task.start_date))
    if task.start_time:
        print("Start time - {}".format(task.start_time))
    if task.end_date:
        print("End date - {}".format(task.end_date))
    if task.end_time:
        print("End time - {}".format(task.end_time))
    if task.type == 1:
        print("Type - one-time")
    elif task.type == 2:
        print("Type = regular")
    print("Priority - {}".format(task.priority))