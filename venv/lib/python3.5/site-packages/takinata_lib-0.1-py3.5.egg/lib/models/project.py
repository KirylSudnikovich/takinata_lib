from lib.models.base_model import *
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Project(object):
    """
    An entity of type Project. It is an aggregator of columns, which in turn contain tasks. The project must contain
    creators and can contain an unlimited number of artists, which the Creator can add or remove from the project

    """
    def __init__(self, name, description, user_id, members=None, id=None):
        if members is None:
            members = []
        self.name = name
        self.description = description
        self.user_id = user_id
        self.members = members
        self.id = id

    def __str__(self):
        return self.name

class AlchProject(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    owner_id = Column(String)
