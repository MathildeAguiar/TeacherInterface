# coding: utf-8
from sqlalchemy import BigInteger, Column, DECIMAL, DateTime, Float, ForeignKey, Integer, SmallInteger, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import INTEGER, LONGTEXT, SMALLINT, TEXT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

#collecting some interesting classes :

class MetalChapter(Base):
    __tablename__ = 'metal_chapters'

    id = Column(INTEGER, primary_key=True)
    grade_id = Column(INTEGER, nullable=False)
    name = Column(VARCHAR(191), nullable=False)
    slug = Column(VARCHAR(191), nullable=False)
    course = Column(LONGTEXT)
    request = Column(TEXT)
    rank_chapter = Column(Integer)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)


class MetalCorpus(Base):
    __tablename__ = 'metal_corpuses'

    id = Column(INTEGER, primary_key=True)
    user_id = Column(INTEGER, nullable=False)
    name = Column(VARCHAR(500), nullable=False)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

class MetalExerciseQuestion(Base):
    __tablename__ = 'metal_exercise_question'

    id = Column(Integer, primary_key=True)
    exercise_id = Column(INTEGER, nullable=False)
    question_id = Column(INTEGER, nullable=False)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

class MetalExercise(Base):
    __tablename__ = 'metal_exercises'

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(500), nullable=False)
    chapter_id = Column(INTEGER, nullable=False)
    user_id = Column(INTEGER, nullable=False)
    exercise_type = Column(VARCHAR(191), nullable=False, server_default=text("'training'"))
    question_duration = Column(SMALLINT, nullable=False, server_default=text("'30'"))
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)


class MetalGrammaticalElement(Base):
    __tablename__ = 'metal_grammatical_elements'

    id = Column(INTEGER, primary_key=True)
    slug = Column(VARCHAR(191), nullable=False)
    name = Column(VARCHAR(191), nullable=False)
    type = Column(VARCHAR(191), nullable=False)
    query = Column(TEXT, nullable=False)
    take_children = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

class MetalQuestionType(Base):
    __tablename__ = 'metal_question_types'

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(191), nullable=False)
    slug = Column(VARCHAR(191), nullable=False)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)


class MetalQuestion(Base):
    __tablename__ = 'metal_questions'

    id = Column(INTEGER, primary_key=True)
    chapter_id = Column(INTEGER, nullable=False)
    grammatical_element_id = Column(Integer, nullable=False)
    sentence_id = Column(INTEGER, nullable=False)
    points = Column(INTEGER, nullable=False, server_default=text("'1'"))
    instructions = Column(LONGTEXT, nullable=False)
    text = Column(LONGTEXT, nullable=False)
    feedback = Column(LONGTEXT)
    question_type_id = Column(INTEGER, nullable=False)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
