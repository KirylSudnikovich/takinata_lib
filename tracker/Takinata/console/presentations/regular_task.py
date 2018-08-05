class RegularTaskView:
    @staticmethod
    def create_format():
        print("To create a task, enter the command as a regular_task add 'username' 'password' 'project name' "
              "'column name' 'task name' 'description' 'first date' 'second date' 'step' 'type_of_step' 'tags' "
              "'priority'")


    @staticmethod
    def show_format():
        print("To display all tasks, enter the command in the following format regular_task show all 'username' "
              "'password' 'project name' 'column name'")

    @staticmethod
    def show_tasks(tasks):
        print("Information about current tasks:\n")
        for i in tasks:
            print("Name  - {}\nDescription - {}\nStart - {}\nEnd - {}\nTags - {}\nStep - {}\nType of step - {}\n"
                  "Priority - {}\n".format(i.name, i.desc, i.first_date, i.second_date, i.tags, i.step,
                                              i.type_of_step, i.priority))
