import unittest
from lib.controllers.category import CategoryController
from lib.controllers.project import ProjectController

class TestCategory(unittest.TestCase):
    def test_cetegory_create(self):
        login = "tester"
        password = "tester228"
        project_id = 9
        category_name = "test_category"
        category_description = "test description"
        try:
            CategoryController.create_category(login, password, project_id, category_name, category_description)
            status = True
        except:
            status = False
        self.assertEquals(status, True)

    def test_cetegory_create(self):
        login = "KReal"
        password = "1337"
        project_id = 9
        category_name = "test_category"
        category_description = "test description"
        try:
            CategoryController.create_category(login, password, project_id, category_name, category_description)
            status = True
        except:
            status = False
        self.assertEquals(status, False)

    def test_category_create_in_project_no_permission(self):
        login = "tester"
        password = "tester228"
        project_id = 1
        category_name = "test_category"
        category_description = "test description"
        try:
            CategoryController.create_category(login, password, project_id, category_name, category_description)
            status = True
        except:
            status = False
        self.assertEquals(status, False)

    def test_category_create_no_id(self):
        login = "tester"
        password = "tester228"
        project_id = -1
        category_name = "test_category"
        category_description = "test description"
        try:
            CategoryController.create_category(login, password, project_id, category_name, category_description)
            status = True
        except:
            status = False
        self.assertEquals(status, False)

    def test_cetegory_delete(self):
        login = "tester"
        password = "tester228"
        project_id = 9
        category_name = "test_category"
        try:
            CategoryController.delete_category(login, password, project_id, category_name)
            status = True
        except Exception as error:
            print(error)
            status = False
        self.assertEquals(status, True)

    def test_cetegory_delete_no_permisison(self):
        login = "tester"
        password = "tester228"
        project_id = 1
        category_name = "test_category"
        try:
            CategoryController.delete_category(login, password, project_id, category_name)
            status = True
        except:
            status = False
        self.assertEquals(status, False)

    def test_cetegory_delete_no_id(self):
        login = "tester"
        password = "tester228"
        project_id = -1
        category_name = "test_category"
        try:
            CategoryController.delete_category(login, password, project_id, category_name)
            status = True
        except:
            status = False
        self.assertEquals(status, False)

    def test_cetegory_delete_incorrect_name(self):
        login = "tester"
        password = "tester228"
        project_id = 9
        category_name = "test_category_1"
        try:
            CategoryController.delete_category(login, password, project_id, category_name)
            status = True
        except:
            status = False
        self.assertEquals(status, False)

    def test_cetegory_delete_incorrect_username(self):
        login = "tester111"
        password = "tester228"
        project_id = 9
        category_name = "test_category"
        try:
            CategoryController.delete_category(login, password, project_id, category_name)
            status = True
        except:
            status = False
        self.assertEquals(status, False)

    def test_cetegory_delete_incorrect_password(self):
        login = "tester"
        password = "tester2281337"
        project_id = 9
        category_name = "test_category"
        try:
            CategoryController.delete_category(login, password, project_id, category_name)
            status = True
        except:
            status = False
        self.assertEquals(status, False)

    def test_cetegory_delete(self):
        login = "KReal"
        password = "1337"
        project_id = 9
        category_name = "test_category"
        try:
            CategoryController.delete_category(login, password, project_id, category_name)
            status = True
        except:
            status = False
        self.assertEquals(status, False)

    def test_edit_name_by_id(self):
        login = "tester"
        password = "tester228"
        project_id = 9
        category_name = "edited_name"
        category_name1 = "category_for_test"
        try:
            CategoryController.edit_name_by_id(login, password, project_id, 6, category_name)
            CategoryController.edit_name_by_id(login, password, project_id, 6, category_name1)
            status = True
        except Exception as error:
            print(error)
            status = False
        self.assertEquals(status, True)

    def test_edit_name_by_id_no_column(self):
        login = "tester"
        password = "tester228"
        project_id = 9
        category_name = "category_for_test"
        try:
            CategoryController.edit_name_by_id(login, password, project_id, -1, category_name)
            status = True
        except:
            status = False
        self.assertEquals(status, False)

    def test_edit_name_by_id_no_column(self):
        login = "tester"
        password = "tester228"
        project_id = -1
        category_name = "category_for_test"
        try:
            CategoryController.edit_name_by_id(login, password, project_id, 6, category_name)
            status = True
        except:
            status = False
        self.assertEquals(status, False)


    def test_edit_name_by_id(self):
        login = "KReal"
        password = "1337"
        project_id = 9
        category_name = "edited_name"
        category_name1 = "category_for_test"
        try:
            CategoryController.edit_name_by_id(login, password, project_id, 6, category_name)
            CategoryController.edit_name_by_id(login, password, project_id, 6, category_name1)
            status = True
        except Exception as error:
            status = False
        self.assertEquals(status, False)

    def test_edit_desc_by_id(self):
        login = "tester"
        password = "tester228"
        project_id = 9
        category_id = 6
        try:
            CategoryController.edit_desc_by_id(login, password, project_id, category_id, "new desc")
            status = True
        except:
            status = False
        self.assertEquals(status, True)

    def test_edit_desc_by_id_no_permission(self):
        login = "KReal"
        password = "1337"
        project_id = 9
        category_id = 6
        try:
            CategoryController.edit_desc_by_id(login, password, project_id, category_id, "new desc")
            status = True
        except:
            status = False
        self.assertEquals(status, False)

    def test_edit_desc_by_id_no_category(self):
        login = "tester"
        password = "tester228"
        project_id = 9
        category_id = 1
        try:
            CategoryController.edit_desc_by_id(login, password, project_id, category_id, "new desc")
            status = True
        except:
            status = False
        self.assertEquals(status, False)

    def test_edit_desc_by_id_no_project(self):
        login = "tester"
        password = "tester228"
        project_id = 1
        category_id = 6
        try:
            CategoryController.edit_desc_by_id(login, password, project_id, category_id, "new desc")
            status = True
        except:
            status = False
        self.assertEquals(status, False)

    def test_edit_desc_by_id_no_category(self):
        login = "tester"
        password = "tester228"
        project_id = -1
        category_id = -1
        try:
            CategoryController.edit_desc_by_id(login, password, project_id, category_id, "new desc")
            status = True
        except:
            status = False
        self.assertEquals(status, False)

    def test_get_all_categories(self):
        login = "tester"
        password = "tester228"
        project_id = 9
        project = ProjectController.get_project_by_id(login, password, project_id)
        try:
            CategoryController.get_all_categories(login, password, project)
            status = True
        except Exception as error:
            print(error)
            status = False
        self.assertEquals(status, True)

    def test_get_all_categories_incorrect_password(self):
        login = "tester"
        password = "tester228"
        project_id = -1
        try:
            project = ProjectController.get_project_by_id(login, password, project_id)
            CategoryController.get_all_categories(login, password, project)
            status = True
        except:
            status = False
        self.assertEquals(status, False)

    def test_get_category_by_id(self):
        login = "tester"
        password = "tester228"
        try:
            CategoryController.get_category_by_id(6)
            status = True
        except:
            status = False
        self.assertEquals(status, True)

    def test_get_category_by_no_id(self):
        login = "tester"
        password = "tester228"
        try:
            CategoryController.get_category_by_id(-1)
            status = True
        except:
            status = False
        self.assertEquals(status, False)

    def test_show_all(self):
        login = "tester"
        password = "tester228"
        try:
            project = ProjectController.get_project_by_id(login, password, 9)
            CategoryController.show_all(login, password, project)
            status = True
        except:
            status = False
        self.assertEquals(status, True)

