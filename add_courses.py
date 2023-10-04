from alt_models import Level, Course
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


CONNSTR = 'postgresql://postgres:qNN8VE2DMQTq6OGr@db.vfwutndecibvfznvrmis.supabase.co/postgres'

engine = create_engine(CONNSTR)


Session = sessionmaker(bind=engine)
session = Session()

foundation = session.query(Level).filter_by(name='Foundation').first()
diploma = session.query(Level).filter_by(name='Diploma').first()
degree = session.query(Level).filter_by(name='Degree').first()


foundation_courses = [
        "Maths2",
        "Statistics2",
        "CT",
        "Intro to Python",
        ]
diploma_courses = [
        "DBMS",
        "PDSA",
        "AppDev1",
        "MLF",
        "Java",
        "AppDev2",
        "MLT",
        "MLP",
        "BDM",
        "Business Analytics",
        "System Commands",
        ]

course_objects = []
for course in foundation_courses:
    course_objects.append(Course(
        name=course,
        level=foundation,
        code=f'{course[:1]}101',
        description=f'{course} description'
        )
    )

for course in diploma_courses:
    course_objects.append(Course(
        name=course,
        level=diploma,
        code=f'{course[:1]}101',
        description=f'{course} description'
        )
    )

session.add_all(course_objects)
session.commit()
session.close()
