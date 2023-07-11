from sqlalchemy import (
        Column,
        Integer,
        ForeignKey,
        Table,
        VARCHAR,
        DECIMAL,
        TEXT,
        create_engine,
        BigInteger,
        Boolean
        )


from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


qp_question_choices = Table(
        'qp_question_choices',
        Base.metadata,
        Column('id', Integer, primary_key=True, autoincrement=True, nullable=False),
        Column('question_id', BigInteger, ForeignKey('qp_question.id'), nullable=False),
        Column('choice_id', BigInteger, ForeignKey('qp_choice.id'), nullable=False)
        )


qp_questionpaper_questions = Table(
        'qp_questionpaper_questions',
        Base.metadata,
        Column('id', Integer, primary_key=True, autoincrement=True, nullable=False),
        Column('questionpaper_id', BigInteger, ForeignKey('qp_questionpaper.id'), nullable=False),
        Column('question_id', BigInteger, ForeignKey('qp_question.id'), nullable=False)
        )


class Question(Base):
    __tablename__ = 'qp_question'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    type = Column(VARCHAR(10), nullable=False)
    text = Column(TEXT, nullable=False)
    marks = Column(Integer, nullable=False)
    num_min = Column(DECIMAL(5, 2), nullable=True)
    num_max = Column(DECIMAL(5, 2), nullable=True)
    text_answer = Column(TEXT, nullable=True)
    img = Column(VARCHAR(100), nullable=True)
    choices = relationship('Choice', secondary=qp_question_choices)
    question_paper_id = Column(BigInteger, ForeignKey('qp_questionpaper.id'), nullable=False,)


class QuestionPaper(Base):
    __tablename__ = 'qp_questionpaper'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(VARCHAR(300), nullable=False)
    type = Column(VARCHAR(10), nullable=False)
    questions = relationship('Question', secondary=qp_questionpaper_questions)
    course_id = Column(BigInteger, ForeignKey('course_course.id'), nullable=False)


class Choice(Base):
    __tablename__ = 'qp_choice'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    choice = Column(TEXT, nullable=False)
    img = Column(VARCHAR(100), nullable=True)
    is_correct = Column(Boolean, nullable=False)
    related_question_id = Column(BigInteger, ForeignKey('qp_question.id'), nullable=False)
    related_question = relationship('Question')


class Course(Base):
    __tablename__ = 'course_course'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    code = Column(VARCHAR(10), nullable=False)
    name = Column(VARCHAR(100), nullable=False)
    description = Column(TEXT, nullable=True)
    level_id = Column(BigInteger, ForeignKey('course_level.id'), nullable=False)
    question_papers = relationship('QuestionPaper', backref='course')


class Level(Base):
    __tablename__ = 'course_level'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(VARCHAR(100), nullable=False)
    courses = relationship('Course', backref='level')


engine = create_engine('sqlite:///test.sqlite3')
Base.metadata.create_all(engine)
