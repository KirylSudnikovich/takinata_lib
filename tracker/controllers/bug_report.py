from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tracker.models import BugReport

engine = create_engine(
    'sqlite:////home/snitch/PycharmProjects/VersionTwo/venv/lib/python3.5/site-packages/takinata_lib-0.1-py3.5.egg/database.sqlite3',
    echo=True)


class BugController:
    @classmethod
    def add_bug(cls, username, name, description):
        Session = sessionmaker(bind=engine)
        session = Session()
        bug = BugReport(username=username, name=name, description=description)
        session.add(bug)
        session.commit()
        session.close()

    @classmethod
    def get_all_bugs(cls):
        Session = sessionmaker(bind=engine)
        session = Session()
        bugs = session.query(BugReport).all()
        session.close()
        return bugs
