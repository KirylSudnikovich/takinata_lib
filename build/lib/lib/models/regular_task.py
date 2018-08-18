class RegularTask:
    """
    The essence of a Regular type job. A regular task differs from a regular one in that it has some periodicity
    after which the task will be re-created. Has fields and step type_of_step that determine how long the task should
    repeat
    """
    def __init__(self, name, desc, project_id, column_id, user_id, first_date, second_date, step, type_of_step,
                 tags, priority, archive=0, id=0, edit_date = None):
        self.name = name
        self.desc = desc
        self.project_id = project_id
        self.column_id = column_id
        self.user_id = user_id
        self.first_date = first_date
        self.second_date = second_date
        self.step = step
        self.type_of_step = type_of_step
        self.edit_date = edit_date
        self.tags = tags
        self.priority = priority
        self.archive = archive
        self.id = id

    def __str__(self):
        return self.name