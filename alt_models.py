from sqlalchemy import (
        Boolean,
        Column,
        DECIMAL,
        ForeignKey,
        Index,
        Integer,
        String,
        Text
        )
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Level(Base):
    __tablename__ = 'course_level'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)


class Course(Base):
    __tablename__ = 'course_course'

    id = Column(Integer, primary_key=True)
    code = Column(String(10), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    level_id = Column(ForeignKey('course_level.id'), nullable=False, index=True)

    level = relationship('Level')


class Questionpaper(Base):
    __tablename__ = 'qp_questionpaper'

    id = Column(Integer, primary_key=True)
    name = Column(String(300), nullable=False)
    type = Column(String(10), nullable=False)
    course_id = Column(ForeignKey('course_course.id'), nullable=False, index=True)

    course = relationship('Course')
    questions = relationship('Question', secondary='qp_questionpaper_questions')
    comprehensions = relationship('Comprehension', secondary='qp_questionpaper_comprehensions')


class Question(Base):
    __tablename__ = 'qp_question'

    id = Column(Integer, primary_key=True)
    type = Column(String(10), nullable=False)
    qn_no = Column(Integer)
    text = Column(Text, nullable=False)
    marks = Column(Integer, nullable=False)
    num_min = Column(DECIMAL)
    num_max = Column(DECIMAL)
    text_answer = Column(Text)
    question_paper_id = Column(ForeignKey('qp_questionpaper.id'), nullable=False, index=True)
    # img = Column(String(100))

    question_paper = relationship('Questionpaper')
    choices = relationship('Choice', secondary='qp_question_choices')
    images = relationship('Imagecontent', secondary='qp_question_images')


class Comprehension(Base):
    __tablename__ = 'qp_comprehension'

    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    question_paper_id = Column(ForeignKey('qp_questionpaper.id'), nullable=False, index=True)

    question_paper = relationship('Questionpaper')
    questions = relationship('Question', secondary='qp_comprehension_questions')
    images = relationship('Imagecontent', secondary='qp_comprehension_images')


class Choice(Base):
    __tablename__ = 'qp_choice'

    id = Column(Integer, primary_key=True)
    choice = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    related_question_id = Column(ForeignKey('qp_question.id'), nullable=False, index=True)
    # img = Column(String(100))

    related_question = relationship('Question')
    images = relationship('Imagecontent', secondary='qp_choice_images')


class Imagecontent(Base):
    __tablename__ = 'qp_imagecontent'

    id = Column(Integer, primary_key=True)
    img = Column(String(100), nullable=False)


class QuestionImage(Base):
    __tablename__ = 'qp_question_images'
    __table_args__ = ()

    id = Column(Integer, primary_key=True)
    question_id = Column(
            ForeignKey('qp_question.id', deferrable=True, initially='DEFERRED'),
            nullable=False, index=True
            )
    imagecontent_id = Column(
            ForeignKey('qp_imagecontent.id', deferrable=True, initially='DEFERRED'),
            nullable=False, index=True
            )

    # imagecontent = relationship('QpImagecontent')
    # question = relationship('QpQuestion')


class ChoiceImage(Base):
    __tablename__ = 'qp_choice_images'
    __table_args__ = ()

    id = Column(Integer, primary_key=True)
    choice_id = Column(ForeignKey('qp_choice.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)
    imagecontent_id = Column(
            ForeignKey('qp_imagecontent.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True
            )

    # choice = relationship('QpChoice')
    # imagecontent = relationship('QpImagecontent')


class QuestionpaperQuestion(Base):
    __tablename__ = 'qp_questionpaper_questions'
    __table_args__ = (
        Index(
            'qp_questionpaper_questions_questionpaper_id_question_id_49404281_uniq',
            'questionpaper_id', 'question_id', unique=True
            ),
    )

    id = Column(Integer, primary_key=True)
    questionpaper_id = Column(ForeignKey('qp_questionpaper.id'), nullable=False, index=True)
    question_id = Column(ForeignKey('qp_question.id'), nullable=False, index=True)

    # question = relationship('Question')
    # questionpaper = relationship('Questionpaper')


class QuestionChoice(Base):
    __tablename__ = 'qp_question_choices'
    __table_args__ = (
        Index('qp_question_choices_question_id_choice_id_eec7e69a_uniq', 'question_id', 'choice_id', unique=True),
    )

    id = Column(Integer, primary_key=True)
    question_id = Column(ForeignKey('qp_question.id'), nullable=False, index=True)
    choice_id = Column(ForeignKey('qp_choice.id'), nullable=False, index=True)

    # choice = relationship('Choice')
    # question = relationship('Question')


class ComprehensionImage(Base):
    __tablename__ = 'qp_comprehension_images'
    __table_args__ = ()

    id = Column(Integer, primary_key=True)
    comprehension_id = Column(ForeignKey('qp_comprehension.id'), nullable=False, index=True)
    imagecontent_id = Column(ForeignKey('qp_imagecontent.id'), nullable=False, index=True)


class ComprehensionQuestion(Base):
    __tablename__ = 'qp_comprehension_questions'
    __table_args__ = ()

    id = Column(Integer, primary_key=True)
    comprehension_id = Column(ForeignKey('qp_comprehension.id'), nullable=False, index=True)
    question_id = Column(ForeignKey('qp_question.id'), nullable=False, index=True)


class QuestionpaperComprehension(Base):
    __tablename__ = 'qp_questionpaper_comprehensions'

    id = Column(Integer, primary_key=True)
    questionpaper_id = Column(ForeignKey('qp_questionpaper.id'), nullable=False, index=True)
    comprehension_id = Column(ForeignKey('qp_comprehension.id'), nullable=False, index=True)


