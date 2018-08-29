# Takinata Lib #

## About ##

Takinata lib is a library written in Python, which is a task tracker 
application that can help you manage your personal time or, if you are a 
team leader, set tasks correctly and share time within the team. 
You can use this library both to develop your console application and to 
develop a complete web application based on this library.

## Library features ##

    

* User registration system. Log in/out system in web application
* Add, edit, delete a project. Add/Remove executors to/from a project
* Create, delete, edit a category for tasks
* Create, delete, and modify tasks
* Showing all projects of user
* Showing all columns of user
* Showing all tasks of user
* Ability to create subtasks
* Ability to create assosiation between to tasks
* Pretty presentation page in web application

## The contents of the repository ##
In addition to the library itself, the content of the repository includes a command-line parser that allows you to 
interact with the library.

Content:
- takinata lib
- console parser for lib
- web application

## How to install? ##
1. Swap to your virtual enviroment
2. Write the following command in terminal


    $ python setuplib.py install
    $ python setupconsole.py install
    
or

    $ pip install -r requirements.txt
    
if you want to install web application

 During the installation of the library all the necessary dependencies are 
 installed automatically and you can start using the application immediately
 
## The use of the application ##
To test the application, write 

    $ takinata -h
    to the console. This is a keyword that you can use to print to the console to 
interact with the library. The console parser provides communication with 
the library and thus forms a single application.
For start web application write:

    $ python manage.py runserver

and open andress localhost:8000 in your browser
   
    
# Running tests
1. Go to the library directory
2. Write


    $ cd tests
    $ python -m unittest
or

    $ cd tests
    $ python run_tests.py

## Author ##

> Sudnikovich Kirill
Group 653502