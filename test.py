from alt_models import Questionpaper, Course
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


CONNSTR = 'postgresql://postgres:tVT7mOAcRm7u9C8k@db.tkldyrncdgypgyujnait.supabase.co/postgres'

# CONNSTR = 'sqlite:////home/ozymandias/Desktop/iitmp/mocktest/rewrite/db.sqlite3'
engine = create_engine(CONNSTR)


Session = sessionmaker(bind=engine)
session = Session()
c = session.query(Course).all()
for course in c:
    print(course.name)

