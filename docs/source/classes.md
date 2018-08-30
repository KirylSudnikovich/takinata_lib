# Classes #

## Takinata lib ##

### models folder ###
Contains the definition of all library models

#### User ####
User - user of the library. It's impossible to interact with the library without the user
- username - user name, can use as login
- password - user password
- email - user email (no email activation)

#### Project ####
A project is an abstraction that will contain categories that in turn contain your tasks.
- name - the name of the project to be displayed in the project list. The name must be unique for each user. That is, two projects for one user will not be created, and for different projects will be created
- description - the description of the project, which should reflect its essence. Can be empty
- user_id - id of the user who created the project
- users - list (array) of all users participating in this project

#### Category ####
A category is a set of tasks grouped by one topic or area.
- name - name of category. It must be unique within one project
- desc - a description that should reflect the essence of what the category contains. Can be empty
- project_id - project id to which this category belongs 

#### Task ####
A task is some action that you want to do in the future.
- name - name of task. It must be unique within on category
- desc - a description that should reflect the essence of that the task need to done. Can be empty
- start_date - the date the task was started. It can not be earlier than 01/01/2018. Optional field
- start_time - the time the task was started. Optional field
- end_date - the date that task will be done. Optional field
- end_time - the time the task will be done. Optional field
- priority - priority of the task. There may be [max, medium, min]
- is_archive - shows the status of the task at this time. 0 - in progress, 1 - complete
- is_subtask - whether this task is a subtask. 1 - is. If the task is a subtask, the id of the parent task will be specified in the parent_task_id field
- parent_task_id - id of the parent task. It is important if the task is a subtask
- assosiated_task_id - if the task is associated with another task, the field contains the idi of the task with which the task is associated
- type - type of task. 1 - one time, 2 - regular
- period - if the task is periodic, this field contains the period of this task in days
- user_id - the user who created the task
- category_id - category to which the given task belongs 
- project_id - the project to which this task belongs

### controllers folder ###
Contains the logic of processing incoming data and the subsequent transfer of this data to the
database or, conversely, return data from the database to the user

#### UserContoller ####
The data handler for user. Allows to reg/delete or get user(s) or they information.

#### ProjectController ####
The data handler for project. Allows to create/delete, edit name/description of project, add/remove users to/from project, return projects tasks of project users.

#### CategoryController ####
The data handler for the category. Allows you to create, modify, show or return all prject categories and delete categories.

#### TaskController ####
The data handler for the Task. Allows to add/delete task, edit, assosiate with other task, set subtask.

### storage folder ###
Contains the logic for interacting with a database. The input receives data from the controller,
and the result of the interaction is returned

#### UserStorage ####
This class provides the interaction of objects of class User with a database (write / read / modify).

#### ProjectStorage ####
This class provides the interaction of objects of class Project with a database (write / read / modify).

#### CategoryStorage ####
This class provides the interaction of objects of class Category with a database (write / read / modify).

#### TaskStorage ####
This class provides the interaction of objects of class Task with a database (write / read / modify).