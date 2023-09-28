# coding: utf-8
from sqlalchemy import BigInteger, Boolean, CheckConstraint, Column, DateTime, ForeignKey, Integer, Numeric, SmallInteger, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import INTERVAL, UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Level(Base):
    __tablename__ = 'course_level'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(100), nullable=False)


class Imagecontent(Base):
    __tablename__ = 'qp_imagecontent'

    id = Column(BigInteger, primary_key=True)
    img = Column(String(100), nullable=False)


class Course(Base):
    __tablename__ = 'course_course'

    id = Column(BigInteger, primary_key=True)
    code = Column(String(10), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    level_id = Column(ForeignKey('course_level.id'))

    level = relationship('Level')


class Questionpaper(Base):
    __tablename__ = 'qp_questionpaper'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(300), nullable=False)
    type = Column(String(10), nullable=False)
    course_id = Column(ForeignKey('course_course.id'))
    exam_date = Column(DateTime(True))

    course = relationship('Course')

class Comprehension(Base):
    __tablename__ = 'qp_comprehension'

    id = Column(BigInteger, primary_key=True)
    text = Column(Text, nullable=False)
    question_paper_id = Column(ForeignKey('qp_questionpaper.i

    question_paper = relationship('QpQuestionpaper')


class QpQuestion(Base):
    __tablename__ = 'qp_question'

    id = Column(BigInteger, primary_key=True)
    type = Column(String(10), nullable=False)
    text = Column(Text, nullable=False)
    marks = Column(Integer, nullable=False)
    num_min = Column(Numeric(10, 2))
    num_max = Column(Numeric(10, 2))
    text_answer = Column(Text)
    question_paper_id = Column(ForeignKey('qp_questionpaper.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)
    qn_no = Column(Integer)

    question_paper = relationship('QpQuestionpaper')


class TestPaperTestpaper(Base):
    __tablename__ = 'test_paper_testpaper'

    id = Column(BigInteger, primary_key=True)
    score = Column(Numeric(5, 2), nullable=False)
    time_spent = Column(INTERVAL)
    submitted = Column(Boolean, nullable=False)
    question_paper_id = Column(ForeignKey('qp_questionpaper.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)
    user_id = Column(ForeignKey('custom_user_user.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)

    question_paper = relationship('QpQuestionpaper')
    user = relationship('CustomUserUser')


class QpChoice(Base):
    __tablename__ = 'qp_choice'

    id = Column(BigInteger, primary_key=True)
    choice = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    related_question_id = Column(ForeignKey('qp_question.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)

    related_question = relationship('QpQuestion')


class QpComprehensionImage(Base):
    __tablename__ = 'qp_comprehension_images'
    __table_args__ = (
        UniqueConstraint('comprehension_id', 'imagecontent_id'),
    )

    id = Column(BigInteger, primary_key=True)
    comprehension_id = Column(ForeignKey('qp_comprehension.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)
    imagecontent_id = Column(ForeignKey('qp_imagecontent.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)

    comprehension = relationship('QpComprehension')
    imagecontent = relationship('QpImagecontent')


class QpComprehensionQuestion(Base):
    __tablename__ = 'qp_comprehension_questions'
    __table_args__ = (
        UniqueConstraint('comprehension_id', 'question_id'),
    )

    id = Column(BigInteger, primary_key=True)
    comprehension_id = Column(ForeignKey('qp_comprehension.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)
    question_id = Column(ForeignKey('qp_question.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)

    comprehension = relationship('QpComprehension')
    question = relationship('QpQuestion')


class QpQuestionImage(Base):
    __tablename__ = 'qp_question_images'
    __table_args__ = (
        UniqueConstraint('question_id', 'imagecontent_id'),
    )

    id = Column(BigInteger, primary_key=True)
    question_id = Column(ForeignKey('qp_question.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)
    imagecontent_id = Column(ForeignKey('qp_imagecontent.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)

    imagecontent = relationship('QpImagecontent')
    question = relationship('QpQuestion')


class QpQuestionpaperComprehension(Base):
    __tablename__ = 'qp_questionpaper_comprehensions'
    __table_args__ = (
        UniqueConstraint('questionpaper_id', 'comprehension_id'),
    )

    id = Column(BigInteger, primary_key=True)
    questionpaper_id = Column(ForeignKey('qp_questionpaper.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)
    comprehension_id = Column(ForeignKey('qp_comprehension.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)

    comprehension = relationship('QpComprehension')
    questionpaper = relationship('QpQuestionpaper')


class QpQuestionpaperQuestion(Base):
    __tablename__ = 'qp_questionpaper_questions'
    __table_args__ = (
        UniqueConstraint('questionpaper_id', 'question_id'),
    )

    id = Column(BigInteger, primary_key=True)
    questionpaper_id = Column(ForeignKey('qp_questionpaper.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)
    question_id = Column(ForeignKey('qp_question.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)

    question = relationship('QpQuestion')
    questionpaper = relationship('QpQuestionpaper')


class TestPaperTestcomprehension(Base):
    __tablename__ = 'test_paper_testcomprehension'

    id = Column(BigInteger, primary_key=True)
    comprehension_id = Column(ForeignKey('qp_comprehension.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)
    test_paper_id = Column(ForeignKey('test_paper_testpaper.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)

    comprehension = relationship('QpComprehension')
    test_paper = relationship('TestPaperTestpaper')


class TestPaperTestquestion(Base):
    __tablename__ = 'test_paper_testquestion'

    id = Column(BigInteger, primary_key=True)
    type = Column(String(10), nullable=False)
    marks = Column(Numeric(5, 2), nullable=False)
    score = Column(Numeric(5, 2), nullable=False)
    time_spent = Column(INTERVAL)
    user_text_answer = Column(Text)
    user_num_answer = Column(Numeric(10, 2))
    submitted = Column(Boolean, nullable=False)
    question_id = Column(ForeignKey('qp_question.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)
    test_paper_id = Column(ForeignKey('test_paper_testpaper.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)

    question = relationship('QpQuestion')
    test_paper = relationship('TestPaperTestpaper')


class QpChoiceImage(Base):
    __tablename__ = 'qp_choice_images'
    __table_args__ = (
        UniqueConstraint('choice_id', 'imagecontent_id'),
    )

    id = Column(BigInteger, primary_key=True)
    choice_id = Column(ForeignKey('qp_choice.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)
    imagecontent_id = Column(ForeignKey('qp_imagecontent.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)

    choice = relationship('QpChoice')
    imagecontent = relationship('QpImagecontent')


class QpQuestionChoice(Base):
    __tablename__ = 'qp_question_choices'
    __table_args__ = (
        UniqueConstraint('question_id', 'choice_id'),
    )

    id = Column(BigInteger, primary_key=True)
    question_id = Column(ForeignKey('qp_question.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)
    choice_id = Column(ForeignKey('qp_choice.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)

    choice = relationship('QpChoice')
    question = relationship('QpQuestion')


class TestPaperTestpaperTestComprehension(Base):
    __tablename__ = 'test_paper_testpaper_test_comprehensions'
    __table_args__ = (
        UniqueConstraint('testpaper_id', 'testcomprehension_id'),
    )

    id = Column(BigInteger, primary_key=True)
    testpaper_id = Column(ForeignKey('test_paper_testpaper.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)
    testcomprehension_id = Column(ForeignKey('test_paper_testcomprehension.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)

    testcomprehension = relationship('TestPaperTestcomprehension')
    testpaper = relationship('TestPaperTestpaper')


class TestPaperTestpaperTestQuestion(Base):
    __tablename__ = 'test_paper_testpaper_test_questions'
    __table_args__ = (
        UniqueConstraint('testpaper_id', 'testquestion_id'),
    )

    id = Column(BigInteger, primary_key=True)
    testpaper_id = Column(ForeignKey('test_paper_testpaper.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)
    testquestion_id = Column(ForeignKey('test_paper_testquestion.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)

    testpaper = relationship('TestPaperTestpaper')
    testquestion = relationship('TestPaperTestquestion')


class TestPaperTestquestionUserChoice(Base):
    __tablename__ = 'test_paper_testquestion_user_choices'
    __table_args__ = (
        UniqueConstraint('testquestion_id', 'choice_id'),
    )

    id = Column(BigInteger, primary_key=True)
    testquestion_id = Column(ForeignKey('test_paper_testquestion.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)
    choice_id = Column(ForeignKey('qp_choice.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)

    choice = relationship('QpChoice')
    testquestion = relationship('TestPaperTestquestion')
