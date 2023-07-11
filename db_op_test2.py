from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alt_models import Question, Questionpaper, Course, Choice, Level


CONNSTR = 'postgresql://postgres:qNN8VE2DMQTq6OGr@db.vfwutndecibvfznvrmis.supabase.co/postgres'

engine = create_engine(CONNSTR)

Session = sessionmaker(bind=engine)
session = Session()

level = Level(name="Foundation")

course = Course(
        code="CSC 101",
        name="Introduction to Computer Science",
        description="Computer Science course",
        level=level
        )
question_paper = Questionpaper(
        name="CSC 101 Test",
        course=course,
        type="Quiz1",

        )

question1 = Question(
        type="SCQ",
        text="What is the full meaning of HTML?",
        img="choice_images/abulaman.jpeg",
        question_paper=question_paper,
        marks=2
        )
question2 = Question(
        type="MCQ",
        text="Which of these is a programming language?",
        question_paper=question_paper,
        marks=4
        )
question3 = Question(
        type="Numeric",
        text="What is the value of 2 + 2?",
        question_paper=question_paper,
        marks=1,
        num_min=4,
        num_max=4
        )
question4 = Question(
        type="Text",
        text="Which is the best programming language?",
        question_paper=question_paper,
        marks=3,
        text_answer="Python"
        )

choice11 = Choice(
        choice="Hyper Text Markup Language",
        related_question=question1,
        is_correct=True
        )
choice12 = Choice(
        choice="Honda Toyota Mazda Lexus",
        related_question=question1,
        is_correct=False
        )
choice13 = Choice(
        choice="Hawaii Tokyo Manhatten Las Vegas",
        related_question=question1,
        is_correct=False
        )
choice14 = Choice(
        choice="Hills Trees Mountains, Lakes",
        related_question=question1,
        is_correct=False
        )
choice21 = Choice(
        choice="HTML",
        related_question=question2,
        is_correct=False
        )
choice22 = Choice(
        choice="JavaScript",
        related_question=question2,
        is_correct=True
        )
choice23 = Choice(
        choice="CSS",
        related_question=question2,
        is_correct=False
        )

choice24 = Choice(
        choice="Python",
        related_question=question2,
        is_correct=True
        )
question1.choices = [choice11, choice12, choice13, choice14]
question2.choices = [choice21, choice22, choice23, choice24]
print(question_paper.questions)
question_paper.questions = [question1, question2, question3, question4]

session.add_all([
    level, course, question_paper,
    question1, question2, question3, question4,
    choice11, choice12, choice13, choice14,
    choice21, choice22, choice23, choice24
    ])
session.commit()
