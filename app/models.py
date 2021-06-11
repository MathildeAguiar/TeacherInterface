# coding: utf-8
import datetime
from re import L
from sqlalchemy import BigInteger, Column, DECIMAL, DateTime, Float, ForeignKey, Integer, SmallInteger, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import INTEGER, LONGTEXT, SMALLINT, TEXT, TINYINT, VARCHAR
from sqlalchemy.sql.functions import now
from .views import app
import logging as lg
from flask_sqlalchemy import SQLAlchemy, request



#database 
db = SQLAlchemy(app)



#collecting some interesting classes :

class MetalChapter(db.Model):
    __tablename__ = 'metal_chapters'

    id = Column(INTEGER, primary_key=True)
    #grade_id = Column(INTEGER, nullable=False)
    name = Column(VARCHAR(191), nullable=False)
    slug = Column(VARCHAR(191), nullable=False)
    course = Column(TEXT) #problem with longtext
    request = Column(TEXT)
    rank_chapter = Column(Integer)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)


class MetalCorpus(db.Model):
    __tablename__ = 'metal_corpuses'

    id = Column(INTEGER, primary_key=True)
    user_id = Column(INTEGER, nullable=False)
    name = Column(VARCHAR(500), nullable=False)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

class MetalExerciseQuestion(db.Model):
    __tablename__ = 'metal_exercise_question'

    id = Column(Integer, primary_key=True)
    exercise_id = Column(INTEGER, nullable=False)
    question_id = Column(INTEGER, nullable=False)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

class MetalExercise(db.Model):
    __tablename__ = 'metal_exercises'

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(500), nullable=False)
    chapter_id = Column(INTEGER) #I removed this: nullable=False
    #user_id = Column(INTEGER, nullable=False)
    exercise_type = Column(VARCHAR(191), nullable=False, server_default=text("'training'"))
    question_duration = Column(SMALLINT, nullable=False, server_default=text("'30'"))
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    #I added those fields 
    texts_related = Column(VARCHAR(191)) #just a test for now 
    questions = Column(INTEGER) #I fetch the questions Id instead of their string content 
    level = Column(INTEGER) #Id of the level/class
    #optional tags
    tag = Column(VARCHAR(500))
    

#often reffered as notion 
class MetalGrammaticalElement(db.Model):
    __tablename__ = 'metal_grammatical_elements'

    id = Column(INTEGER, primary_key=True)
    slug = Column(VARCHAR(191), nullable=False)
    name = Column(VARCHAR(191), nullable=False)
    type = Column(VARCHAR(191), nullable=False)
    #query = Column(TEXT, nullable=False)
    take_children = Column(INTEGER, nullable=False, server_default=text("'0'")) #TINYINT(1)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

class MetalQuestionType(db.Model):
    __tablename__ = 'metal_question_types'

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(191), nullable=False)
    slug = Column(VARCHAR(191), nullable=False)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)


class MetalQuestion(db.Model):
    __tablename__ = 'metal_questions'

    id = Column(INTEGER, primary_key=True)
    #chapter_id = Column(INTEGER, nullable=False)
    #grammatical_element_id = Column(Integer, nullable=False)
    #sentence_id = Column(INTEGER, nullable=False)
    points = Column(INTEGER, nullable=False, server_default=text("'1'"))
    instructions = Column(TEXT, nullable=False) #longtext
    text = Column(TEXT, nullable=False) #longtext
    feedback = Column(TEXT) #longtext
    #question_type_id = Column(INTEGER, nullable=False)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)


class MetalText(db.Model):
    __tablename__ = 'metal_texts'

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(500), nullable=False)
    corpus_id = Column(INTEGER, nullable=False)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)


#database initialization
def init_db():
    db.drop_all()
    db.create_all()

    #random questions
    for i in range(20):
        q = MetalQuestion(
            text='Test message {}'.format(i+1),
            instructions='Author {}'.format(i+1),
            #category='Category {}'.format(i+1),
            points=4321*(i+1)
            )

        db.session.add(q)

    #random chapters
    for i in range(20):
        chap = MetalChapter(
            name='Test message {}'.format(i+1),
            slug='Author {}'.format(i+1),
            #category='Category {}'.format(i+1),
            #points=4321*(i+1)
            )

        db.session.add(chap)

    #random exercices
    for i in range(20):
        """
        exo = MetalExercise(
            name='Test message {}'.format(i+1),
            exercise_type='Author {}'.format(i+1),
            #category='Category {}'.format(i+1),
            question_duration=50
            )
        """
        exo = MetalExercise()
        exo.name = 'hello'
        exo.question_duration = 0
        exo.created_at = datetime.datetime.now() 
        exo.updated_at = datetime.datetime.now() #now() is the sql one 
        exo.chapter_id = 1
        exo.questions = 1
        exo.texts_related = 'text'
        exo.level = 1
        db.session.add(exo)

    #random grammatical elements 
    for i in range(20):
        gramElem = MetalGrammaticalElement(
            slug='Test message {}'.format(i+1),
            name='Author {}'.format(i+1),
            type='Category {}'.format(i+1),
            #points=4321*(i+1)
            )

        db.session.add(gramElem)
    
    #random texts
    for i in range(20):
        text = MetalText(
            name = 'test_txt',
            corpus_id= i,
            created_at = datetime.datetime.now(), 
            updated_at = datetime.datetime.now()
        )
        db.session.add(text)


    db.session.commit()
    lg.warning('Database initialized!')

#définir les fct des queries 

#get all the chapters and order them by their names 
def query_all_chaps():
    chaps = MetalChapter.query.order_by(MetalChapter.name).all()
    return chaps

#get all the exercices and order them by their names 
def query_all_exos():
    exos = MetalExercise.query.order_by(MetalExercise.name).all()
    return exos

#get all the questions and order them by their names 
def query_all_quests():
    quests = MetalQuestion.query.order_by(MetalQuestion.instructions).all()
    return quests

#get all the grammatical elements and order them by their names 
def query_all_gram():
    gram = MetalGrammaticalElement.query.order_by(MetalGrammaticalElement.name).all()
    return gram 


#insert a newly created exercice in the database 
def new_exo(name, lvl, chapId, duration, text, quest, tags):

    #fct to insert a new exercice in the db after clicking on "create" button
    exo = MetalExercise()
    exo.name = name
    exo.question_duration = duration
    exo.created_at = datetime.datetime.now()
    exo.updated_at = datetime.datetime.now()
    exo.chapter_id = chapId
    exo.questions = quest
    exo.texts_related = text
    exo.level = lvl
    exo.tags = tags

    #the query itself 
    db.session.add(exo)
    db.session.commit()
    lg.warning('Addition done !')

    
    """
    id = Column(INTEGER, primary_key=True) #use
    name = Column(VARCHAR(500), nullable=False) #use
    #chapter_id = Column(INTEGER, nullable=False) #should
    #user_id = Column(INTEGER, nullable=False) #not use
    #not gonna use this for now 
    exercise_type = Column(VARCHAR(191), nullable=False, server_default=text("'training'")) #not use
    question_duration = Column(SMALLINT, nullable=False, server_default=text("'30'")) #True or False instead
    created_at = Column(TIMESTAMP) #use
    updated_at = Column(TIMESTAMP) #use 
    """


#home query 
def general_query(query):
    #cas d'un nom d'exercise
    tmp_chap = MetalChapter.query.filter_by(name=query).all()
    print(tmp_chap)
    tmp_exo = MetalExercise.query.filter_by(name=query).all()
    print(tmp_exo)
    tmp_quest = MetalQuestion.query.filter_by(instructions=query).all()
    tmp_gramm = MetalGrammaticalElement.query.filter_by(name=query).all()

    if tmp_chap is not None:
        return tmp_chap
    elif tmp_exo is not None:
        return tmp_exo
    elif tmp_quest is not None:
        return tmp_quest
    elif tmp_gramm is not None:
        return tmp_gramm    
    else:
        return "Aucun résultat"


#home query 
def general_query2(query, category):

    res = list()

    #would like a "switch" Java like 

    if category == 'None':
        #we check all the possibilities 
        tmp_chap = MetalChapter.query.filter_by(name=query).all()
        print(tmp_chap)
        tmp_exo = MetalExercise.query.filter_by(name=query).all()
        print(tmp_exo)
        tmp_quest = MetalQuestion.query.filter_by(instructions=query).all()
        tmp_gramm = MetalGrammaticalElement.query.filter_by(name=query).all()

        if tmp_chap!=[]:
            res.append(tmp_chap) #might have to change the data form here 
        
        if tmp_exo !=[]:
            res.append(tmp_exo)
        
        if tmp_gramm !=[]:
            res.append(tmp_gramm)
        
        if tmp_quest!=[]:
            res.append(tmp_quest)
        elif len(res)==0: return "Aucun résultat !" #might need to change the data form here too 
    
    if category == 'Chapitres':
        tmp_chap = MetalChapter.query.filter_by(name=query).all()
        print(tmp_chap)
        res.append(tmp_chap)
    
    if category=='Exercices':
        tmp_exo = MetalExercise.query.filter_by(name=query).all()
        print(tmp_exo)
        res.append(tmp_exo)
    if category== 'Notions':
        tmp_gramm = MetalGrammaticalElement.query.filter_by(name=query).all()
        res.append(tmp_gramm)
    if category=='Questions':
        tmp_quest = MetalQuestion.query.filter_by(instructions=query).all()
        res.append(tmp_quest)
    
    elif len(res)==0: return "Aucun résultat !"

    for o in res:
        return o



    


#query for 'validation' page  TODO

def query_validaiton(txtName):
    if txtName!=[]:
        texts = MetalText.query.filter_by(name = txtName).all() 
        if texts !=[]:
            return texts
        else: return "Aucun texte ne correspond à votre demande !"    
    else: return "Aucun texte ne correspond à votre demande !"
        
    