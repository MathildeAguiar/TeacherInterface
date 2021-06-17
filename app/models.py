# coding: utf-8
import datetime
from re import L
from types import FrameType
from sqlalchemy import BigInteger, Column, DECIMAL, DateTime, Float, ForeignKey, Integer, SmallInteger, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import INTEGER, LONGTEXT, SMALLINT, TEXT, TINYINT, VARCHAR
from sqlalchemy.sql.sqltypes import BOOLEAN, Boolean, TIME
from .views import app
import logging as lg
from flask_sqlalchemy import SQLAlchemy, request
from random import choices, randint



#database 
db = SQLAlchemy(app)


#classes of our tables 

class MetalChapter(db.Model):
    __tablename__ = 'metal_chapters'

    id = Column(INTEGER, primary_key=True)
    #grade_id = Column(INTEGER, nullable=False)
    name = Column(VARCHAR(191), unique=True, nullable=False) #, unique=True
    #exercise_id = Column(Integer, ForeignKey('metal_exercises.id'), nullable=False)
    group_id = Column(Integer, ForeignKey('metal_groups.id'))
    tags = Column(TEXT)
    slug = Column(VARCHAR(191))
    course = Column(TEXT) 
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

class MetalUser(db.Model):
    __tablename__ = 'metal_users'

    id = Column(INTEGER, primary_key=True)
    lastName = Column(VARCHAR(191), nullable=False)
    firstName = Column(VARCHAR(191), nullable=False)
    password = Column(VARCHAR(191), nullable=False)
    group_id = Column(Integer, ForeignKey('metal_groups.id'))
    type = Column(VARCHAR(191))


class MetalGrade(db.Model):
    __tablename__ = 'metal_grades'

    id = Column(INTEGER, primary_key=True)
    user_id = Column(INTEGER, ForeignKey('metal_users.id'), nullable=False)
    exercise_id = Column(Integer, ForeignKey('metal_exercises.id'), nullable=False)
    slug = Column(VARCHAR(191))
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)


class MetalCorpus(db.Model):
    __tablename__ = 'metal_corpuses'

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(191), unique=True, nullable=False)
    analysed_at = Column(TIMESTAMP)
    notion_id = Column(ForeignKey('metal_notions.id'), nullable=False)
    author = Column(VARCHAR(191))


class MetalNotion(db.Model): #equivalent to grammatical element 
    __tablename__ = 'metal_notions'

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(191), unique=True, nullable=False)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    question_id = Column(ForeignKey('metal_questions.id'))


class MetalNotionItem(db.Model): #equivalent to grammatical item 
    __tablename__ = 'metal_notion_items'

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(191), nullable=False)
    notion_id = Column(INTEGER, ForeignKey('metal_notions.id'),  nullable=False)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)


class MetalGroup(db.Model):
    __tablename__ = 'metal_groups'

    id = Column(INTEGER, primary_key=True)
    level = Column(VARCHAR(191), unique=True, nullable=False)

#add question type ? 
class MetalQuestion(db.Model):
    __tablename__ = 'metal_questions'

    id = Column(INTEGER, primary_key=True)
    instructions = Column(TEXT, nullable=False)
    answers = Column(VARCHAR(512), nullable=False)
    grade = Column(INTEGER)
    duration = Column(Integer)
    slug = Column(VARCHAR(191))
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

class MetalExercise(db.Model):
    __tablename__ = 'metal_exercises'

    id = Column(INTEGER, primary_key=True)
    chapter_id = Column(ForeignKey('metal_chapters.id'), nullable=False)
    question_id = Column(ForeignKey('metal_questions.id'), nullable=False)
    name = Column(VARCHAR(191), unique=True, nullable=False)
    type = Column(VARCHAR(191))
    limited_time = Column(Boolean) #does boolean works here ? 
    tags = Column(VARCHAR(191))
    slug = Column(VARCHAR(191))
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    group_lvl = Column(ForeignKey('metal_groups.level'))
    text_related = Column(ForeignKey('metal_corpuses.name'))
    #add a notion field ? 


# database initialization 

def init_db():
    
    db.drop_all()
    db.create_all()

    #population of the db 

    #random grades 

    for i in range(3): #usr 1
        grade = MetalGrade()
        grade.user_id = 1 
        grade.slug = "exo 1"
        grade.exercise_id = 1
        grade.created_at = datetime.datetime.now()
        grade.updated_at = datetime.datetime.now()
        db.session.add(grade)

    for i in range(3): #usr 2
        grade = MetalGrade()
        grade.slug = "exo 1"
        grade.exercise_id = 1
        grade.user_id = 2
        grade.created_at = datetime.datetime.now()
        grade.updated_at = datetime.datetime.now()
        db.session.add(grade)


    #random groups 

    for i in range(2):
        grp = MetalGroup()
        grp.level = "3ème.{}".format(i+1)
        db.session.add(grp)

    for i in range(3):
        grp = MetalGroup(level="4ème.{}".format(i+1))
        db.session.add(grp)

    #random users 
    groups = ["3ème.1", "3ème.2", "4ème.2", "4ème.1"]
    for i in range(5):
        usr = MetalUser()
        usr.lastName = "Dupont".format(i+1)
        usr.firstName = "Pierre".format(i+1)
        usr.group_id = groups[i-1]
        usr.password = randint(1, 99)
        db.session.add(usr)
    
    #random chaps:
    chap_name = ['Les conjonctions de subordination', 'Pronoms personnels', 'Complément du verbe', 'Temps du subjonctif', "Temps de l'indicatif"]
    for i in range(5):
        chap = MetalChapter()
        chap.name = chap_name[i]
        #choices(chap_name).pop(0)
        chap.slug = str(chap.name)
        chap.updated_at = datetime.datetime.now()
        chap.created_at = datetime.datetime.now()
        chap.course = 'cours {}'.format(i)
        #chap.exercise_id = 1
        chap.tags = 'un tag'
        chap.group_id = randint(1, 3)
        db.session.add(chap)
    
    # random quests 
    instruct = ['instr 1', 'instr 2', 'instr 3']
    answers_possible = [ "'oui', 'non'", "'yes', 'no'", "1, 2, 3"]
    for i in range(8):
        quest = MetalQuestion()
        quest.updated_at = datetime.datetime.now()
        quest.created_at = datetime.datetime.now()
        quest.answers = choices(answers_possible).pop(0)
        quest.duration = randint(1, 60)
        quest.instructions = choices(instruct).pop(0)
        quest.grade = randint(0, 20)
        db.session.add(quest)

    #random exo
    for i in range(5):
        exo = MetalExercise()
        exo.updated_at = datetime.datetime.now()
        exo.created_at = datetime.datetime.now()
        exo.limited_time = choices([True, False]).pop(0)
        exo.name = "name {}".format(i+1)
        exo.slug = "this is an exo slug"
        exo.tags = "exo's tags"
        exo.chapter_id = randint(1, 4)
        exo.question_id = randint(1,3)
        db.session.add(exo)


    #random corpus
    texts = ['Vingt mille lieues sous les mers', 'Le Grand Meaulnes', 'Maupassant', 'Corpus test']
    for i in range(4):
        corp = MetalCorpus()
        corp.name = texts[i]
        #choices(['Vingt mille lieues sous les mers', 'Le Grand Meaulnes', 'Maupassant', 'Corpus test']).pop(0)
        corp.notion_id = randint(1, 3)
        corp.author = "author".format(i+1)
        corp.analysed_at = datetime.datetime.now()
        db.session.add(corp)


    #random notion 
    n = ['conjonction-subordination', 'groupe nominal', 'groupe-nominal-sujet', 'pronom relatif', 'indicatif-present', 'complement-d-agent']
    for i in range(5):
        notion = MetalNotion()
        notion.name = n[i]
        #choices(['conjonction-subordination', 'groupe nominal', 'groupe-nominal-sujet', 'pronom relatif', 'indicatif-present', 'complement-d-agent']).pop(0)
        notion.question_id = randint(1, 3)
        notion.updated_at = datetime.datetime.now()
        notion.created_at = datetime.datetime.now()
        db.session.add(notion)

    #random notion item 
    for i in range(5):
        notion_item = MetalNotionItem()
        notion_item.name = 'notion_itm.{}'.format(i+1)
        notion_item.notion_id = randint(1,4)
        notion_item.updated_at = datetime.datetime.now()
        notion_item.created_at = datetime.datetime.now()
        db.session.add(notion_item)

    db.session.commit()
    lg.warning('Database initialized!')

#fct queries 


#get all the chapters and order them by their names 
def query_all_chaps():
    chaps = MetalChapter.query.order_by(MetalChapter.name).all()
    return chaps

#get all the exercises and order them by their names 
def query_all_exos():
    exos = MetalExercise.query.order_by(MetalExercise.name).all()
    return exos

#get all the questions and order them by their names 
def query_all_quests():
    quests = MetalQuestion.query.order_by(MetalQuestion.instructions).all()
    return quests

#get all the grammatical elements and order them by their names 
def query_all_gram():
    gram = MetalNotion.query.order_by(MetalNotion.name).all()
    return gram 

def query_all_groups():
    grp = MetalGroup.query.order_by(MetalGroup.level).all()
    return grp

#query to fetch all exercices related to a chapter (used in side nav or not ? ) TODO test it 
def query_exo_related_chaps(chap_name):
    #list_exo = MetalExercise.query.select_from(MetalExercise.name).join(MetalChapter, MetalChapter.id == MetalExercise.chapter_id).filter(MetalChapter.name == chap_name)
    list_exo = db.session.query(MetalExercise.name).join(MetalChapter, MetalChapter.id==MetalExercise.chapter_id).filter(MetalChapter.name==chap_name).all()
    return list_exo


#insert a newly created exercice in the database 
def new_exo(name, lvl, chapId, duration, text, quest, tags):

    #fct to insert a new exercice in the db after clicking on "create" button
    exo = MetalExercise()
    exo.name = name
    exo.limited_time = duration
    exo.created_at = datetime.datetime.now()
    exo.updated_at = datetime.datetime.now()
    exo.chapter_id = chapId
    exo.question_id = quest #wrong I think 
    exo.group_lvl = lvl
    exo.texts_related = text
    #exo.level = lvl
    exo.tags = tags

    #the query itself 
    db.session.add(exo)
    db.session.commit()
    lg.warning('Addition done !')



#home query 
def general_query2(query, category):

    res = list()

    #I changed the format of the input so the query acts like a LIKE and the user gets more results 
    search = "%{}%".format(query)
    #I replaced all the previous "query" vars by "search" (with the new format)
    
    #would like a "switch" Java like 

    if category == 'All':
        #we check all the possibilities 
        tmp_chap = MetalChapter.query.filter(MetalChapter.name.like(search)).all()
        print(tmp_chap)
        tmp_exo = MetalExercise.query.filter(MetalExercise.name.like(search)).all()
        print(tmp_exo)
        tmp_quest = MetalQuestion.query.filter(MetalQuestion.instructions.like(search)).all()
        tmp_gramm = MetalNotion.query.filter(MetalNotion.name.like(search)).all()
        tmp_txt = MetalCorpus.query.filter(MetalCorpus.name.like(search)).all()


        if tmp_chap!=[]:
            res.append(tmp_chap) #might have to change the data form here 
        
        if tmp_exo !=[]:
            res.append(tmp_exo)
        
        if tmp_gramm !=[]:
            res.append(tmp_gramm)
        
        if tmp_quest!=[]:
            res.append(tmp_quest)
        
        if tmp_txt!=[]:
            res.append(tmp_txt)

        elif len(res)==0: return "Aucun résultat !" #might need to change the data form here too 
    
    if category == 'Chapitres':
        tmp_chap = MetalChapter.query.filter(MetalChapter.name.like(search)).all()
        print(tmp_chap)
        res.append(tmp_chap)
    
    if category=='Exercices':
        tmp_exo = MetalExercise.query.filter(MetalExercise.name.like(search)).all()
        print(tmp_exo)
        res.append(tmp_exo)
    if category== 'Notions':
        tmp_gramm = MetalNotion.query.filter(MetalNotion.name.like(search)).all()
        res.append(tmp_gramm)
    if category=='Questions':
        tmp_quest = MetalQuestion.query.filter(MetalQuestion.instructions.like(search)).all()
        res.append(tmp_quest)
    if category == 'Textes':
        tmp_txt = MetalCorpus.query.filter(MetalCorpus.name.like(search)).all()
        res.append(tmp_txt)
    
    elif len(res)==0: return "Aucun résultat !"

    for o in res:
        return o

#query for 'validation' page  TODO

def query_validation(txtName):
    if txtName is not None: 
        notions = db.session.query(MetalNotion.name).join(MetalCorpus, MetalCorpus.notion_id == MetalNotion.id).filter(MetalCorpus.name==txtName).all()       
        print(notions)
        if notions !=[]: 
            return notions 
        else: None #return "Aucun texte ne correspond à votre demande !"    
    else: None #return "Aucun texte ne correspond à votre demande !"
        