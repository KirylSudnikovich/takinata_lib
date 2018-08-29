import unittest
from lib.controllers.project import ProjectController, UserController


class TestProject(unittest.TestCase):
    def test_project_create(self):
        login = "tester"
        password = "tester228"
        project_name = "project for tests"
        project_description = "test_project description"
        try:
            ProjectController.create(login, password, project_name, project_description)
            status = True
        except Exception:
            status = False
        self.assertEquals(status, True)

    def test_project_create_incorrect_password(self):
        login = "tester"
        password = "tester"
        project_name = "project for tests"
        project_description = "test_project description"
        try:
            ProjectController.create(login, password, project_name, project_description)
            status = True
        except Exception:
            status = False
        self.assertEquals(status, False)

    def test_project_create_no_user(self):
        login = "tester_no"
        password = "tester228"
        project_name = "project for tests"
        project_description = "test_project description"
        try:
            ProjectController.create(login, password, project_name, project_description)
            status = True
        except Exception:
            status = False
        self.assertEquals(status, False)

    def test_project_delete_no_project(self):
        login = "tester"
        password = "tester228"
        project_name = "project for tests"
        project_description = "test_project description"
        try:
            ProjectController.delete(login, password, project_name)
            status = True
        except Exception:
            status = False
        self.assertEquals(status, False)

    def test_project_add_to_project(self):
        login = "tester"
        password = "tester228"
        project_id = 9
        project = ProjectController.get_project_by_id(login, password, project_id)
        person = UserController.get_user_by_id(45)
        try:
            ProjectController.add_person_to_project(login, password, project_id, person)
            status = True
        except Exception as error:
            status = False
        self.assertEquals(status, True)

    def test_project_delete_not_admin(self):
        login = "KReal"
        password = "1337"
        project_name = "project for tests"
        try:
            ProjectController.delete(login, password, project_name)
            status = True
        except Exception:
            status = False
        self.assertEquals(status, False)

    def test_project_delete(self):
        login = "tester"
        password = "tester228"
        project_name = "project for tests"
        project_description = "test_project description"
        try:
            ProjectController.delete(login, password, project_name)
            status = True
        except Exception:
            status = False
        self.assertEquals(status, True)

    def test_project_already_exist_in_project(self):
        login = "tester"
        password = "tester228"
        project_id = 9
        project = ProjectController.get_project_by_id(login, password, 9)
        person = UserController.get_user_by_id(45)
        try:
            ProjectController.add_person_to_project(login, password, project_id, person)
            status = True
        except Exception as error:
            status = False
        self.assertEquals(status, False)

    def test_project_delete_from_project(self):
        login = "tester"
        password = "tester228"
        project_id = 9
        project = ProjectController.get_project_by_id(login, password, 9)
        person = UserController.get_user_by_id(45)
        try:
            ProjectController.delete_person_from_project(login, password, project, person)
            status = True
        except Exception as error:
            status = False
        self.assertEquals(status, True)

    def test_project_delete_from_project_no_user(self):
        login = "tester"
        password = "tester228"
        project_id = 9
        project = ProjectController.get_project_by_id(login, password, 9)
        person = UserController.get_user_by_id(45)
        try:
            ProjectController.delete_person_from_project(login, password, project, person)
            status = True
        except Exception as error:
            status = False
        self.assertEquals(status, False)

    def test_edit_name_by_id_already_exist_this_name(self):
        login = "tester"
        password = "tester228"
        project_id = 9
        try:
            ProjectController.edit_name_by_id(login, password, project_id, "test1")
            status = True
        except:
            status = False
        self.assertEquals(status, False)

    def test_edit_name_by_id(self):
        login = "tester"
        password = "tester228"
        project_id = 9
        try:
            ProjectController.edit_name_by_id(login, password, project_id, "test-1")
            ProjectController.edit_name_by_id(login, password, project_id, "test1")
            status = True
        except:
            status = False
        self.assertEquals(status, True)

    def test_edit_name_by_no_id(self):
        login = "tester"
        password = "tester228"
        project_id = -1
        try:
            ProjectController.edit_name_by_id(login, password, project_id, "test-1")
            ProjectController.edit_name_by_id(login, password, project_id, "test1")
            status = True
        except:
            status = False
        self.assertEquals(status, False)

    def test_edit_description(self):
        login = "tester"
        password = "tester228"
        project_id = 9
        try:
            ProjectController.edit_description_by_id(login, password, project_id, "new_desc")
            status = True
        except:
            status = False
        self.assertEquals(status, True)

    def test_edit_description_no_id(self):
        login = "tester"
        password = "tester228"
        project_id = -1
        try:
            ProjectController.edit_description_by_id(login, password, project_id, "new_desc")
            status = True
        except:
            status = False
        self.assertEquals(status, False)

    def test_get_project_tasks(self):
        login = "tester"
        password = "tester228"
        project_id = 9
        try:
            project = ProjectController.get_project_by_id(login, password, project_id)
            ProjectController.get_project_tasks(login, password, project)
            status = True
        except:
            status = False
        self.assertEquals(status, True)

    def test_get_project_tasks_no_project(self):
        login = "tester"
        password = "tester228"
        project_id = -1
        try:
            project = ProjectController.get_project_by_id(project_id)
            ProjectController.get_project_tasks(login, password, project)
            status = True
        except:
            status = False
        self.assertEquals(status, False)

    def test_get_project_user_info(self):
        project_id = 9
        try:
            ProjectController.get_project_user_info(9)
            status = True
        except:
            status = False
        self.assertEquals(status, True)

    def test_get_project_by_id(self):
        login = "tester"
        password = "tester228"
        project_id = 9
        try:
            ProjectController.get_project_by_id(login, password, project_id)
            status = True
        except:
            status = False
        self.assertEquals(status, True)

    def test_get_project_by_no_id(self):
        login = "tester"
        password = "tester228"
        project_id = -1
        try:
            ProjectController.get_project_by_id(login, password, project_id)
            status = True
        except:
            status = False
        self.assertEquals(status, False)

    def test_is_admin(self):
        login = "tester"
        password = "tester228"
        project_id = 9
        try:
            ProjectController.is_admin(login, project_id)
            status = True
        except:
            status = False
        self.assertEquals(status, True)

    def test_is_no_admin(self):
        login = "tester"
        password = "tester228"
        project_id = -1
        try:
            ProjectController.is_admin(login, project_id)
            status = True
        except:
            status = False
        self.assertEquals(status, False)

    def test_is_no_admin_for_this(self):
        login = "tester"
        password = "tester228"
        project_id = 1
        if ProjectController.is_admin(login, project_id):
            status = True
        else:
            status = False
        self.assertEquals(status, False)

    def test_check_permission(self):
        login = "tester"
        password = "tester228"
        project_id = 20
        if ProjectController.check_permission(login, password, project_id):
            status = True
        else:
            status = False
        self.assertEquals(status, True)

    def test_check_permission_for_testr_project(self):
        login = "tester"
        password = "tester228"
        project_id = 9
        if ProjectController.check_permission(login, password, project_id):
            status = True
        else:
            status = False
        self.assertEquals(status, True)

    def test_check_permission_have_no_permission(self):
        login = "tester"
        password = "tester228"
        project_id = 1
        try:
            if ProjectController.check_permission(login, password, project_id):
                status = True
            else:
                status = False
        except:
            status = False
        self.assertEquals(status, False)

    def test_check_permission_incorrect_id(self):
        login = "tester"
        password = "tester228"
        project_id = -1
        try:
            if ProjectController.check_permission(login, password, project_id):
                status = True
            else:
                status = False
        except:
            status = False
        self.assertEquals(status, False)

    def test_show_project(self):
        login = "tester"
        password = "tester228"
        project_id = 9
        try:
            ProjectController.show(login, password, project_id)
            status = True
        except:
            ProjectController.show(login, password, project_id)
            status = False
        self.assertEquals(status, True)

    def test_show_project_executor(self):
        login = "tester"
        password = "tester228"
        project_id = 20
        try:
            ProjectController.show(login, password, project_id)
            status = True
        except:
            ProjectController.show(login, password, project_id)
            status = False
        self.assertEquals(status, True)

    def test_show_project_denied(self):
        login = "tester"
        password = "tester228"
        project_id = 1
        try:
            ProjectController.show(login, password, project_id)
            status = True
        except:
            status = False
        self.assertEquals(status, False)

    def test_show_project_no_id(self):
        login = "tester"
        password = "tester228"
        project_id = -1
        try:
            ProjectController.show(login, password, project_id)
            status = True
        except:
            status = False
        self.assertEquals(status, False)