class MainException(Exception):
    pass


class UserException(MainException):
    pass


class UserAlreadyExist(UserException):
    def __init__(self):
        super().__init__("A user with this name is already registered")


class WrongPassword(UserException):
    def __init__(self):
        super().__init__("Incorrect password")


class NoUser(UserException):
    def __init__(self):
        super().__init__("There is no user with this name")


class ProjectException(MainException):
    pass


class CannotGetProject(ProjectException):
    def __init__(self):
        super().__init__("It is impossible to get project with the specified name")


class NoProjectWithThisName(ProjectException):
    def __init__(self):
        super().__init__("There is no project with this name")

class NoProjectWithThisId(ProjectException):
    def __init__(self):
        super().__init__("There is no project with this id")


class ProjectWithThisNameAlreadyExist(ProjectException):
    def __init__(self):
        super().__init__("Project with this name is already exist")


class ProjectIsNotExist(ProjectException):
    def __init__(self):
        super().__init__("Project is not exist")


class NoPermission(ProjectException):
    def __init__(self):
        super().__init__("You do not have access to this project")


class UAreNotAdmin(ProjectException):
    def __init__(self):
        super().__init__("You are not the Creator of this project")


class UserAlreadyExistInProject(ProjectException):
    def __init__(self):
        super().__init__("This user is already exist in this project")


class UserIsNotExistInProject(ProjectException):
    def __init__(self):
        super().__init__("User is not already exist in this project")


class CannotDeleteCreator(ProjectException):
    def __init__(self):
        super().__init__("You can't delete creator of project")


class ColumnException(MainException):
    pass


class NoColumnWithThisName(ProjectException):
    def __init__(self):
        super().__init__("There is no column with this name")


class ColumnWithThisNameAlreadyExist(ColumnException):
    def __init__(self):
        super().__init__("Column with this name is already exist")


class TaskException(MainException):
    pass


class AlreadyInArchive(TaskException):
    def __init__(self):
        super().__init__("This task is already in the archive")


class TaskWithThisNameAlreadyExist(TaskException):
    def __init__(self, name):
        super().__init__("A task with the name {} already exists in the selected column".format(name))


class NotDate(TaskException):
    def __init__(self):
        super().__init__("The entered date does not match the required format")


class EndBeforeStart(TaskException):
    def __init__(self):
        super().__init__("The specified task end date is before the task start date")


class StartBeforeToday(TaskException):
    def __init__(self):
        super().__init__("The task can not be started until today")


class NoTask(TaskException):
    def __init__(self):
        super().__init__("Cannot find a task with this name")


class SubTaskDateException(TaskException):
    def __init__(self):
        super().__init__("The time boundaries of the subtask must be within the time boundaries of the parent task")


class SubTaskPriorityException(TaskException):
    def __init__(self):
        super().__init__("The priority of the subtask cannot be higher than the priority of the parent task")


class AlreadySubtask(TaskException):
    def __init__(self):
        super().__init__("This task is already a subtask")


class CanNotDeleteBecauseSubtasks(TaskException):
    def __init__(self):
        super().__init__("You cannot delete a task until all subtasks are completed")


class ItsNotANumber(TaskException):
    def __init__(self):
        super().__init__("Priority - it's not a number")


class IncorrentDate(TaskException):
    def __init__(self):
        super().__init__("Incorrect date")

class CanNotAssosiateWithDoneTask(TaskException):
    def __init__(self):
        super().__init__("You can't assosiate with done task")

class CanNotAssosiateWithRegularTask(TaskException):
    def __init__(self):
        super().__init__("You can't assosiate with regular task")


class IncorrectTypeOfStep(TaskException):
    def __init__(self):
        super().__init__("Incorrect type of step. Choose one from [day,month,year]")


class ThisFeatureDoesNotExist(TaskException):
    def __init__(self):
        super().__init__("This feature does not exist for sorting")


class StartBeforeToday(TaskException):
    def __init__(self):
        super().__init__("Your start date is before today")


class EndBeforeToday(TaskException):
    def __init__(self):
        super().__init__("Your end date is before today")


class IncorrectPriority(TaskException):
    def __init__(self):
        super().__init__("Incorrect priority")


class TypeErr(BaseException):
    def __init__(self):
        super().__init__("Type conversion error")


class ThereIsNoSuchCategory(MainException):
    def __init__(self):
        super().__init__("There is no category with that id")


class ThereIsNoSuchSubcategory(MainException):
    def __init__(self):
        super().__init__("There is no such command")
