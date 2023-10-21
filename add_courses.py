from alt_models import Level, Course
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# CONNSTR = 'sqlite:////home/ozymandias/Desktop/iitmp/mocktest/rewrite/db.sqlite3'

CONNSTR = 'postgresql://postgres:tVT7mOAcRm7u9C8k@db.tkldyrncdgypgyujnait.supabase.co/postgres'
engine = create_engine(CONNSTR)


Session = sessionmaker(bind=engine)
session = Session()

foundation = session.query(Level).filter_by(name='foundation').first()
diploma = session.query(Level).filter_by(name='diploma').first()
degree = session.query(Level).filter_by(name='degree').first()


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

degree_courses = [
        "SPG",
        "Sw Testing",
        "Industry 4.0",
        "SW Engg",
        "AI",
        "Deep learning",
        "PSM",
        "Algo Thinking",
        "BBN",
        "Fin Forensics",
        "Data Viz",
        "Market Research",
        "LSM",
        "Intro to BigData",
        "Design Thinking",

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


for course in degree_courses:
    course_objects.append(Course(
        name=course,
        level=degree,
        code=f'{course[:1]}101',
        description=f'{course} description'
        )
    )

session.add_all(course_objects)
session.commit()
session.close()
