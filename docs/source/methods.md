# Methods #

## User ##
- reg(username, password, email)  

Registers this user and adds it to the database

Example:
```bash
   $ takinata user reg -u username -p password -m email
```
- delete(username, password) 

Delete ths user from the database

Example:
```bash
   $ takinata user delete -u username -p password
```

## Project ##
- create(username, password, name, description)

Creates a project with the specified name description. The user name and password are required to bind the project to a specific user.

Example:
```bash
	$ takinata project create -u username -p password -n name -d description
```

- delete(username, password, name) 

Deletes the project with the specified name

Example:
```bash
	$ takinata project delete -u username -p password -n name
```
- add_user  

Adds the user with the transmitted id to the project. If the user has already been added, an exception will be thrown

Example:
```bash
	$ takinata project add_user -u username -p password -pid project_id -uid user_id
```
- remove_user  

Deletes the user with the transmitted id from the project. If the user was not in the project, an exception will be thrown

Example:
```bash
	$ takinata project remove_user -u username -p password -pid project_id -uid user_id
```
- edit_name

Changes the name of the specified project, provided that the user is the creator of this project

Example:
```bash
	$ takinata project edit_name -u username -p password  -pid project_id -n name
```
- edit_description

Changes the description of the specified project, provided that the user is the creator of this project

Example:
```bash
	$ takinata project edit_name -u username -p password -pid project_id -d description
```
- show

Returns information about the specified project if the user has access to the project (he is the creator or executor)
Example:
```bash
	$ takinata project show -u username -p password -pid project_id
```

## Category ##
- create
  
Creates a category with the specified name and description within the transferred project, provided that the user is the creator of this project
Example:
```bash
	$ takinata category create -u username -p password -pid project_id -n name -d description
```
- delete
  
Delete a category with the specified name from category 
Example:
```bash
	$ takinata category delete -u username -p password -pid project_id -n name
```
- edit_name
  
Changes the name of the specified category, provided that the user is the creator of this project
Example:
```bash
	$ takinata category edit_name -u username -p password -cid category_id -n name
```
- edit_description

Changes the description of the specified category, provided that the user is the creator of this project
Example:
```bash
	$ takinata category edit_description -u username -p password -cid category_id -d description
```
- show_all

Show all categories in project
Example:
```bash
	$ takinata category show_all -u username -p password -pid project_id
```
## Task ##

- create
  
Creates a task with the parameters passed. The description and necessity of the fields can be viewed in the "Classes"
Example:
```bash
	$ takinata task create -u username -p password -pid project_id -cid category_id -n name -d description -t type -sd start_date -st start_time -ed end_date -et end_time -p priority
```
- cancel
  
Set 'DONE' status for the task with the specified id
Example
```bash
	$ takinata task cancel -u username -p password -tid task_id
```

- set_assosiated_task
  
It connects two tasks. At the completion of one connected task, the second one is completed automatically
Example:
```bash
	$ takinata task assosiate -u username -p password -tid task_id -atid to_assosiate_task_id
```
- set_parent_task

Sets the parent task for the transferred task. Parent task can not be completed until all subtasks are completed
Example:
```bash
	$ takinata task set_parent_task -u username -p password -sid subtask_id -ptid parent_task_id
```
- start_again
  
Updates the dates of the regular task from today, provided that the attempt to update the regular task
Example:
```bash
	$ takinata task start_again -u username -p password -tid task_id
```
- show
  
Returns information about the task
Example:
```bash
	$ takinata task show -u username -p password -tid task_id
```