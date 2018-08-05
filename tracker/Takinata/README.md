# Takinata tracker #

* Add, edit, and delete users
* Add, edit, delete a project. Add and remove artists to a project
* Create, delete, edit a column
* Create, delete, and modify tasks
* Demonstrating trash bin's files
* Adding/Removing new trash bins
* Showing all projects of user
* Showing all columns of user
* Showing all tasks of user
* Ability to create subtasks
  
### How to install? ###

    $ virtualenv env
    $ ./env/bin/python setupconsole.py install
    $ ./env/bin/python setuplib.py install

### How to use Takinata? ###

**User**

* $ user register > Register new user
* $ user delete > Remove user
* $ user edit > Edit user

**Project**

* $ project add > Create new project
* $ project delete > Delete project
* $ project edit > Edit project
* $ project show all > Show list of projects for current user
* $ project members add > Add new artist to project
* $ project members delete > Delete artist from project

**Column** 

* $ column add > Create column to project
* $ column delete > Remove column from project
* $ column edit > Edit column
* $ column show all > Show all columns of the project

**Task**

* $ task add > Create new task
* $ task delete > Remove task
* $ task edit > Edit task
* $ task show all > Show all tasks of the column
* $ task set_subtask > Set task1 as a subtask of task2

Sudnikovich Kirill
Group 653502