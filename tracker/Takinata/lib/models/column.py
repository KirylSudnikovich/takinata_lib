class Column:
    """
    The entity type Column. It contains tasks and is a way of grouping them within the project

    """
    def __init__(self, name, desc, project_id, id = None):
        self.name = name
        self.desc = desc
        self.project_id  = project_id
        self.id = id

    def __str__(self):
        return self.name