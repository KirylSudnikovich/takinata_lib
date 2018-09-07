"""lib - is a package that contains a library for creating and managing tasks, the so-called task manager.
In turn, the package includes several more packages and files.

__________

Description of internal packages

controllers - a package that describes the logic of incoming data processing and subsequent interaction with the database

models - package describing the content (fields) of all entities

storage - a package that describes the database interaction logic. The data from the controller is received to the
input, which, in turn, are loaded or, conversely, unloaded from the database

__________

Description of internal files

conf.py - A configuration file that searches for the path to the database, log files, and a database for tests

Exception.py - A file that contains a list and description of all exceptions that may occur while the library is running

logger.py - A file that describes the settings of the logger and the logic of its operation

"""