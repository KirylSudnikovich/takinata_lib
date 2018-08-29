def success_create():
    print("Category is successfully created")

def success_delete():
    print("Category is successfully deleted")

def success_edit():
    print("Category was successfully edited")


def show_all(cats):
    print("Information about category in project:")
    for i in cats:
        print("Name - {}\nDescription - {}\n\n".format(i.name, i.desc))