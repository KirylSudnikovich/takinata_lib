def show_all(cols):
    print("Information about columns:")
    for i in cols:
        print("Name - {}\nDescription - {}\n".format(i.name, i.desc))


def success_create():
    print("Column is successfully created")


def success_delete():
    print("Columns is successfully deleted")


def success_edit():
    print("Column is successfully edited")


def create_format():
    print("Wrong format. To create a column, enter a command like column create 'username' 'password' 'project name' "
          "'name of column' 'description of column'")


def delete_format():
    print("Wrong format. To delete a column, enter a command like column delete 'username' 'password' 'project name' "
          " 'column name")


def edit_format():
    print("Wrong format. To edit a column, enter a command like column edit name/description 'username' 'password' "
          "'project name' 'column name'")


def show_format():
    print(
        "Wrong format. To show all columns, enter a command like column show 'username' 'password' 'project name' all")
