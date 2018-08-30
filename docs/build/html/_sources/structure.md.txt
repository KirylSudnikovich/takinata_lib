# Repository structure #

Repository consists of three parts

## Takinata lib ##

```
 folder - lib
```

Takinata lib is a library written in Python, which is a task tracker 
application that can help you manage your personal time or, if you are a 
team leader, set tasks correctly and share time within the team. 
You can use this library both to develop your console application and to 
develop a complete web application based on this library.

- controllers - a package that contains the handler classes, within which all the interaction logic between the repository and a specific user occurs.
- models - a package that contains the classes of all models of task-trackers, namely : Project, Category, Task
- storage - a package that describes the database interaction logic. The data from the controller is received to the
input, which, in turn, are loaded or, conversely, unloaded from the database
- tests - the folder containing the tests for each abstraction to test the library
- conf.py A configuration file that searches for the path to the database, log files and create config.ini
- exception.py - A file that contains a list and description of all exceptions that may occur while the library is running
- logger.py - A file that describes the settings of the logger and the logic of its operation

## Console parser for Takinata lib ##
```
folder - console
```    
The console parser is a tool for interacting with the library. Allows the end user to use the library and interact with it using the terminal interface. To get started, write:

- parse_api - a folder containing the parser for interaction between libraries and user
- presentation - a package that defines the views for all entities
- start.py - a main package file that receives arguments and sends them for processing

## Takinata web ##
```
folder - current directory
```
A web application that uses the Takinata Lib library. Demonstrates to the user how to use the library when developing a web application using the Django framework


Basic structure of a Django application
- manage.py - file to manage the application
- requirements.txt - file with library requirements. All libraries specified in the file must be installed for the application to work correctly
- templates - a folder containing the template to display the content of web pages
- tracker - the main directory of the tracker application. Contains a description of forms, models, handlers, and a list of URLs
- VersionTwo - service folder containing application settings