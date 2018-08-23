import sqlite3

import lib.conf as conf
from lib.models.models import Category, Project
from lib.storage.project import ProjectStorage
from lib.exception import *
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
engine = create_engine(conf.get_path_to_db())
from sqlalchemy.ext.declarative import declarative_base


class ColumnStorage:

    Session = sessionmaker(bind=engine)
    session = Session()

    @classmethod
    def add_column_to_db(cls, category):
        """
        Add the sent column to the database
        :param column: an instance of the Column type to be added to the database
        :return:
        """
        all_columns = ColumnStorage.session.query(Category).all()
        have = False
        for i in all_columns:
            if i.name == category.name and category.project_id == i.project_id:
                have = True
        if not have:
            ColumnStorage.session.add(category)
            ColumnStorage.session.commit()
            ColumnStorage.session.close()
        else:
            raise ColumnWithThisNameAlreadyExist

    @classmethod
    def save(self, category):
        """
        Saves all instance fields to the database
        :param column: the instance that you want to keep
        :return:
        """
        new_column = ColumnStorage.session.query(Category).filter(Category.id == category.id).first()
        new_column.name = column.name
        new_column.description = column.description
        ColumnStorage.session.commit()
        ColumnStorage.session.close()

    @classmethod
    def delete_column_from_db(cls, category):
        """
        Remove the transferred instance from the database
        :param column: the instance you want to delete
        :return:
        """
        ColumnStorage.session.delete(category)
        ColumnStorage.session.commit()
        ColumnStorage.session.close()

    @classmethod
    def get_column(cls, project_name, name):
        """
        Get an instance of a class with the specified name
        :param project_name: the name of the project that contains the column
        :param name: the name of the column
        :return:
        """
        f_column = ColumnStorage.session.query(Category).filter(Category.name == name and Category.project_id == project.id).first()
        ColumnStorage.session.close()
        return f_column

    @classmethod
    def get_column_by_id(cls, project_name, id):
        """
        Get an instance of a class with the specified name
        :param project_name: the name of the project that contains the column
        :param name: the name of the column
        :return:
        """
        project = ColumnStorage.session.query(Category).filter(Category.id == id).first()
        ColumnStorage.session.close()
        return project

    @classmethod
    def get_all_columns(cls, project_id):
        """
        Get a list consisting of all columns included in the project
        :param project_name: the name of the project
        :return:
        """
        cols = []
        project = ColumnStorage.session.query(Project).filter(Project.id == project_id).first()
        columns = ColumnStorage.session.query(Category).filter(Category.project_id==project.id).first()
        ColumnStorage.session.close()
        if columns is list:
            return columns
        elif columns is None:
            return []
        else:
            cols.append(columns)
            return cols
