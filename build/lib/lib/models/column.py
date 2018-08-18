from sqlalchemy import Column, Integer, String, Table, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()
engine = create_engine(
    'sqlite:////home/snitch/PycharmProjects/VersionTwo/venv/lib/python3.5/site-packages/takinata_lib-0.1-py3.5.egg/database.sqlite3',
    echo=True)


# class Column(Base):
#     __tablename__ = 'columns'
#
#     def __init__(self, name, desc, project_id):
#         self.name = name
#         self.desc = desc
#         self.project_id = project_id
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     desc = Column(String)
#     project_id = Column(Integer, ForeignKey('projects.id'))
#
#
# Base.metadata.create_all(engine)
