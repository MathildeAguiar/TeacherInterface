# coding: utf-8
import datetime
import random, string
from sqlalchemy import BigInteger, Column, DECIMAL, DateTime, Float, ForeignKey, Integer, SmallInteger, String, TIMESTAMP, Table, Text, delete
from sqlalchemy.dialects.mysql import INTEGER, LONGTEXT, SMALLINT, TEXT, TINYINT, VARCHAR
from sqlalchemy.sql.expression import update
from sqlalchemy.orm import relationship
#rom sqlalchemy.sql.expression import delete, null
from sqlalchemy.sql.sqltypes import BOOLEAN, Boolean, TIME
from .views import app
import logging as lg
from flask_sqlalchemy import SQLAlchemy, request
from random import choices, randint, randrange




#database 
db = SQLAlchemy(app)


#classes of our tables 

class MetalUser(db.Model):
    __tablename__ = 'metal_users'

    id = Column(INTEGER, primary_key=True)
    lastName = Column(VARCHAR(191), nullable=False)
    firstName = Column(VARCHAR(191), nullable=False)
    password = Column(VARCHAR(191), nullable=False)
    #many to one with groups  (many users can be in 1 group) --> might change to many to many 
    group_id = Column(Integer, ForeignKey('metal_groups.id'))
    group = relationship("MetalGroup", back_populates="users")
    type = Column(VARCHAR(191)) #role 

association_groups_chaps = Table('groups_chaps', db.metadata, Column('group_id', Integer, ForeignKey('metal_groups.id')), Column("chapter_id", Integer, ForeignKey('metal_chapters.id')))

class MetalGroup(db.Model):
    __tablename__ = 'metal_groups'

    id = Column(INTEGER, primary_key=True)
    level = Column(VARCHAR(191), unique=True, nullable=False)
    #many to one with users  --> might change into many to many 
    users = relationship("MetalUser", back_populates="group")
    #many to one avec session d'exercices 
    sessions = relationship("MetalAssignment", back_populates="group")
    #many to many with chapter table 
    chapters = relationship("MetalChapter", secondary= association_groups_chaps, back_populates="groups")

association_chap_exos= Table('chaps_exos', db.metadata, Column('chap_id', Integer, ForeignKey('metal_chapters.id')), Column('exo_id', Integer, ForeignKey('metal_exercises.id')))

association_chaps_notions = Table('exos_notions', db.metadata, Column('notion_id', Integer, ForeignKey('metal_notions.id')), Column('chap_id', Integer, ForeignKey('metal_chapters.id')))

class MetalChapter(db.Model):
    __tablename__ = 'metal_chapters'

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(191), unique=True, nullable=False)
    tags = Column(TEXT)
    slug = Column(VARCHAR(191))
    cycle = Column(TEXT)  #not in the form 
    summary = Column(TEXT)
    #many to many with the table Groups  
    groups = relationship("MetalGroup", secondary=association_groups_chaps, back_populates="chapters")
    #many to many with exercices 
    exos = relationship("MetalExercise", secondary=association_chap_exos, back_populates="chaps")
    #many to many with notions 
    notions = relationship("MetalNotion", secondary=association_chaps_notions, back_populates='chaps')

association_exos_quests = Table('quests_exos', db.metadata, Column('quest_id', Integer, ForeignKey('metal_questions.id')), Column('exo_id', Integer, ForeignKey('metal_exercises.id')))   

association_exos_sessions = Table('sess_exos', db.metadata, Column('sess_id', Integer, ForeignKey('metal_assignments.id')), Column('exo_id', Integer, ForeignKey('metal_exercises.id')))

association_exos_txts = Table('exos_txts', db.metadata, Column('txt_id', Integer, ForeignKey('metal_corpuses.id')), Column('exo_id', Integer, ForeignKey('metal_exercises.id')))

#association_exos_notions = Table('exos_notions', db.metadata, Column('notion_id', Integer, ForeignKey('metal_notions.id')), Column('exo_id', Integer, ForeignKey('metal_exercices.id')))

class MetalExercise(db.Model):
    __tablename__ = 'metal_exercises'

    id = Column(INTEGER, primary_key=True)
    #many to many with chapters 
    chaps = relationship("MetalChapter", secondary=association_chap_exos, back_populates="exos")
    name = Column(VARCHAR(191), unique=True, nullable=False)
    limited_time = Column(Boolean) #does boolean works here ? 
    tags = Column(VARCHAR(191))
    slug = Column(VARCHAR(191))
    #many to many with questions 
    quests = relationship("MetalQuestion", secondary=association_exos_quests, back_populates="exos")
    #many to many with sessions 
    sessions = relationship("MetalAssignment", secondary=association_exos_sessions, back_populates="exos")
    #many to many with corpus
    corpuses = relationship("MetalCorpus", secondary=association_exos_txts, back_populates="exos")
    #many to may with notions --> simplify
    #notions = relationship("MetalNotion", secondary=association_exos_notions, back_populates="exos")
    #question déjà liée à la notion et au texte donc pas besoin de redondance 
    #text_related = Column(ForeignKey('metal_corpuses.name')) 


#add question type et metal question aswers ? 
class MetalQuestion(db.Model):
    __tablename__ = 'metal_questions'

    id = Column(INTEGER, primary_key=True)
    type = Column(VARCHAR(191)) #to link with the different types 
    grade = Column(INTEGER) #should we keep it ? 
    duration = Column(Integer)
    slug = Column(VARCHAR(191))
    #many to many with exos 
    exos = relationship("MetalExercise", secondary=association_exos_quests, back_populates="quests")
    #many to one with notion
    notion_id = Column(Integer, ForeignKey('metal_notions.id'))
    notion = relationship("MetalNotion", back_populates="questions")
    #relation with usr answer
    usr_answer = relationship("MetalAnswerUser", back_populates="question")
    #different types of questions relationships 
    questTF = relationship("MetalQuestionTrueFalse", back_populates="questions")
    questFillBlank = relationship("MetalQuestionFillBlank", back_populates="questions")
    questHighlight = relationship("MetalQuestionHighlight", bake_queries="questions")

    #do we need to add a type ? since we already have the link with question id in QUestion Highlight etc I don't think so but idk 


class MetalAssignment(db.Model): #exercices session 
    __tablename__ = 'metal_assignments'

    id = Column(INTEGER, primary_key=True)
    user_id = Column(INTEGER, ForeignKey('metal_users.id'), nullable=False)  #? keep???
    name = Column(VARCHAR(191), nullable=False)
    code = Column(INTEGER) #some have codes (mandatory groups of exercices) and some don't (non mandatory ones)
    mark = Column(Integer, nullable=False)
    #many to one with Groups 
    group_id = Column(Integer, ForeignKey('metal_groups.id') )
    group = relationship("MetalGroup", back_populates="sessions")
    #many to many with exercices 
    exos = relationship("MetalExercise", secondary=association_exos_sessions, back_populates="sessions")
    #one to many with Usr answer
    usr_answers = relationship("MetalAnswerUser", back_populates="session")
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

 

association_notions_txts = Table('notions_txts', db.metadata, Column('notion_id', Integer, ForeignKey('metal_notions.id')), Column('txt_id', Integer, ForeignKey('metal_corpuses.id')))

class MetalCorpus(db.Model):
    __tablename__ = 'metal_corpuses'

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(191), unique=True, nullable=False)
    #notion_id = Column(ForeignKey('metal_notions.id'), nullable=False)
    author = Column(VARCHAR(191))
    #many to many with exercices
    exos = relationship("MetalExercise", secondary=association_exos_txts, back_populates="corpuses")
    #many to many with notions
    notions = relationship("MetalNotion", secondary=association_notions_txts, back_populates="corpuses")


class MetalNotion(db.Model): #equivalent to grammatical element 
    __tablename__ = 'metal_notions'

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(191), unique=True, nullable=False)
    #many to many with exos 
    #exos = relationship("MetalExercices", secondary=association_exos_notions, back_populates="notions")
    #one to many with notion items 
    notion_item = relationship('MetalNotionItems')
    #many to many with corpus
    corpuses = relationship("MetalCorpus", secondary=association_notions_txts, back_populates="notions")
    #one to many with notion item 
    notion_item = relationship("MetalNotionItem")
    #many to one with questions
    questions = relationship("MetalQuestion",back_populates="notion")
    #question_id = Column(INTEGER, ForeignKey('metal_questions.id')) 
    #many to many with chapters
    chaps = relationship("MetalChapter", secondary=association_chaps_notions, back_populates="notions")


class MetalNotionItem(db.Model): #equivalent to grammatical marker 
    __tablename__ = 'metal_notion_items'

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(191), nullable=False)
    notion_id = Column(INTEGER, ForeignKey('metal_notions.id'),  nullable=False)



########################### MANY TO MANY AND SO ON TO DEFINE FROM HERE

class MetalQuestionHighlight(db.Model):
    __tablename__ = 'metal_question_highlights'

    id = Column(INTEGER, primary_key=True)
    question_id = Column(INTEGER, ForeignKey('metal_questions.id'), nullable=False)
    questions = relationship("MetalQuestion", back_populates="questHighlight")
    word_position = Column(INTEGER, nullable=False)
    instructions = Column(TEXT, nullable=False)

class MetalQuestionFillBlank(db.Model):
    __tablename__ = 'metal_question_fill_blanks'

    id = Column(INTEGER, primary_key=True)
    question_id = Column(INTEGER, ForeignKey('metal_questions.id'), nullable=False)
    questions = relationship("MetalQuestion", back_populates="questFillBlank")
    word_position = Column(INTEGER, nullable=False)
    instructions = Column(TEXT, nullable=False)

class MetalQuestionTrueFalse(db.Model):
    __tablename__ = 'metal_question_true_falses'

    id = Column(INTEGER, primary_key=True)
    question_id = Column(INTEGER, ForeignKey('metal_questions.id'), nullable=False)
    questions = relationship("MetalQuestion", back_populates="questTF")
    instructions = Column(TEXT, nullable=False)
    #do we need to add the available choices (Vrai, faux) ???? 



class MetalAnswerUser(db.Model):
    __tablename__ = 'metal_answer_users'

    id = Column(INTEGER, primary_key=True)
    user_id = Column(INTEGER, ForeignKey('metal_users.id'), nullable=False)
    #chapter_id = Column(INTEGER, ForeignKey('metal_chapters.id'), nullable=False)
    #many to one with questions
    question_id = Column(INTEGER, ForeignKey('metal_questions.id'), nullable=False)
    question = relationship("MetalQuestion", back_populates="usr_answer")
    #one to many with sessions  
    session_id = Column(INTEGER, ForeignKey('metal_assignments.id'))
    session = relationship("MetalAssignment", back_populates="usr_answers") 
    #correct_answer = Column(Text, nullable=False) #do we need it or is it done by the analyser or smth already in the question type table 
    user_answer = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP) #should we keep that ?
    updated_at = Column(TIMESTAMP) # "   "  "  "


####### database initialization ########


def init_db():
    
    db.drop_all()
    db.create_all()

    #population of the db 

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
        usr.lastName = "Dupont{}".format(i+1)
        usr.firstName = "Pierre{}".format(i+1)
        usr.group_id = groups[i-1]
        usr.password = randint(1, 99)
        db.session.add(usr)
    
    #random chaps:
    chap_name = ['Les conjonctions de subordination', 'Pronoms personnels', 'Complément du verbe', 'Temps du subjonctif', "Temps de l'indicatif"]
    for i in range(5):
        chap = MetalChapter()
        chap.name = chap_name[i]
        chap.slug = str(chap.name)
        chap.summary = "Ceci est un résumé de chapitre"
        chap.cycle = 'cours du cycle {}'.format(i)
        chap.tags = 'un tag'
        db.session.add(chap)
    
    # random quests 
    for i in range(9):
        quest = MetalQuestion()
        quest.duration = randint(1, 60)
        #quest.instructions = "instruction n° {}".format(i) dépend du type de quest 
        quest.grade = randint(0, 20) #keep it ? 
        quest.type = "question type " #keep it ? 
        quest.notion_id = randint(1, 4)
        quest.slug = "this is a question slug"
        db.session.add(quest)

    #random question types -- highlights

    for i in range(3):
        questHighlight =  MetalQuestionHighlight()
        questHighlight.instructions = "this is instructions for quest highlight"
        questHighlight.question_id = randint(1,3)
        questHighlight.word_position = randint(1, 15)
        db.session.add(questHighlight)

    #random quest types -- fill blank 

    for i in range(3):
        questFill = MetalQuestionFillBlank()
        questFill.instructions = "this is instructions for quest fill"
        questFill.word_position = randint(1, 12)
        questFill.question_id = randint(4,6)
        db.session.add(questFill)

    #random question types -- true false 

    for i in range(3):
        questTF  = MetalQuestionTrueFalse()
        questTF.instructions = "this is instructions for quest T/F"
        questTF.question_id = randint(7,9)
        db.session.add(questTF)
           
   
    #random exo 
    for i in range(5):
        exo = MetalExercise()
        exo.limited_time = choices([True, False]).pop(0)
        exo.name = "name {}".format(i+1)
        exo.slug = "this is an exo slug"
        exo.tags = "exo's tags"
        #exo.chapter_id = randint(1, 4)
        db.session.add(exo)


    #random corpus 
    texts = ['Vingt mille lieues sous les mers', 'Le Grand Meaulnes', 'Maupassant', 'Corpus test']
    for i in range(4):
        corp = MetalCorpus()
        corp.name = texts[i]
        #corp.notion_id = randint(1, 3)
        corp.author = "author {}".format(i+1)
        db.session.add(corp)


    #random notion 
    n = ['conjonction-subordination', 'groupe nominal', 'groupe-nominal-sujet', 'pronom relatif', 'indicatif-present', 'complement-d-agent']
    for i in range(5):
        notion = MetalNotion()
        notion.name = n[i]
        #notion.question_id = randint(1, 3)
        db.session.add(notion)

    #random notion item 
    for i in range(5):
        notion_item = MetalNotionItem()
        notion_item.name = 'notion_itm.{}'.format(i+1)
        notion_item.notion_id = randint(1,4)
        db.session.add(notion_item)

    #random exercices sessions 
    for i in range(4):
        sess = MetalAssignment()
        sess.created_at = datetime.datetime.now()
        sess.mark = randint(0, 20)
        sess.code = "".join([random.choice(string.ascii_uppercase + string.digits) for _ in range(10)])
        sess.name = "session n° {}".format(i)
        sess.updated_at = datetime.datetime.now()
        sess.user_id = i
        db.session.add(sess)

    #random usr answers 
    for i in range(4):
        usrans = MetalAnswerUser()
        usrans.user_id = i
        usrans.created_at = datetime.datetime.now()
        usrans.session_id = i
        usrans.user_answer = "user {} answer".format(i)
        usrans.question_id = randint(1,4)
        db.session.add(usrans)

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

#get all the questions and order them by their names  TODO there is no more instructions in here !!!
def query_all_quests():
    questsTF = MetalQuestionTrueFalse.query.order_by(MetalQuestionTrueFalse.instructions).all()
    questsFB = MetalQuestionFillBlank.query.order_by(MetalQuestionFillBlank.instructions).all()
    questsH = MetalQuestionHighlight.query.order_by(MetalQuestionHighlight.instructions).all()
    return quests

#get all the grammatical elements and order them by their names 
def query_all_gram():
    gram = MetalNotion.query.order_by(MetalNotion.name).all()
    return gram 

def query_all_groups():
    grp = MetalGroup.query.order_by(MetalGroup.level).all()
    return grp

#query all the exercices sessions avaiable 
def query_all_sessions():
    session = MetalAssignment.query.order_by(MetalAssignment.name).all()
    return session

#query all the texts avaiable 
def query_all_corpuses():
    corpuses = MetalCorpus.query.order_by(MetalCorpus.name).all()
    return corpuses


#query to fetch all exercices related to a chapter TODO changer le chapter_id 
def query_exo_related_chaps(chap_name):
    #list_exo = MetalExercise.query.select_from(MetalExercise.name).join(MetalChapter, MetalChapter.id == MetalExercise.chapter_id).filter(MetalChapter.name == chap_name)
    #list_exo = db.session.query(MetalExercise).join(MetalChapter, MetalChapter.id==MetalExercise.chapter_id).filter(MetalChapter.name==chap_name).all()
    #return list_exo
    return None


#insert a newly created exercice in the database 
def new_exo(name, lvl, chapId, duration, text, quest, tags):

    #fct to insert a new exercice in the db after clicking on "create" button
    exo = MetalExercise()
    exo.name = name
    exo.limited_time = duration
    #exo.chapter_id = chapId
    exo.question_id = quest #wrong I think 
    exo.group_lvl = lvl
    exo.texts_related = text
    exo.tags = tags

    #the query itself 
    db.session.add(exo)
    db.session.commit()
    lg.warning('Addition done !')


#insert a newly created chapter to the database TODO
def new_chapter(name, level, exos, texts, summary, tags):
    chap = MetalChapter()
    chap.group_id = level
    chap.name = name
    chap.slug = summary
    chap.summary = summary
    chap.tags = tags
    #il faut gérer l'update des exos ici et celui des texts

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
        tmp_quest = MetalQuestion.query.filter(MetalQuestion.instructions.like(search)).all() #instructions !! à changer
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
        tmp_quest = MetalQuestion.query.filter(MetalQuestion.instructions.like(search)).all()  #instructions !! à changer
        res.append(tmp_quest)
    if category == 'Textes':
        tmp_txt = MetalCorpus.query.filter(MetalCorpus.name.like(search)).all()
        res.append(tmp_txt)
    
    elif len(res)==0: return "Aucun résultat !"

    for o in res:
        return o

#query for 'validation' page  TODO

def query_validation(txtName): #TO CHANGE (the join is wrong)
    if txtName is not None: 
        #previously query(MetalNotion.name)... but I need objects and not just a string 
        notions = db.session.query(MetalNotion).join(MetalCorpus, MetalCorpus.notion_id == MetalNotion.id).filter(MetalCorpus.name==txtName).all()       
        print(notions)
        if notions !=[]: 
            return notions 
        else: None #return "Aucun texte ne correspond à votre demande !"    
    else: None #return "Aucun texte ne correspond à votre demande !"

#query to edit a notion find by the analyser 

def edit_notion(notionName, name): #TODO we can't change much with only those fields missing the sentence examined 
    if notionName is not None:
        #notionObject = db.session.query(MetalNotion).filter(MetalNotion.name==notionName)
        #notionObject.name = name
        update(MetalNotion).where(MetalNotion.name == notionName).values(name=name)
        db.session.commit()
        lg.warning('Modifications done !')


# DANS TOUS LES DELETE ATTENTION AUX DÉPENDANCES !!!!!!
#query to delete a notion "forever" TODO TO TEST

def delete_notion(notionName):
    if notionName is not None:
        delete(MetalNotion).where(MetalNotion.name == notionName) 
        #attention on doit supprimer une notion liée à une phrase en particulier là on va juste suppr toutes les notions de ce nom!!!!
        db.session.commit()
        lg.warning('Deleted notion !')

#query to delete a session TODO TO TEST

def delete_session(sessionName):
    if sessionName is not None:
        delete(MetalAssignment).where(MetalAssignment.name == sessionName) 
        db.session.commit()
        lg.warning('Deleted session !')

#query to delete a chapter TODO TO TEST

def delete_chapter(chapName):
    if chapName is not None:
        delete(MetalChapter).where(MetalChapter.name == chapName) 
        db.session.commit()
        lg.warning('Deleted chapter !')

#query to delete an exercise TODO TO TEST

def delete_exercise(exoName):
    if exoName is not None:
        delete(MetalExercise).where(MetalExercise.name == exoName) 
        #attention les dépendances !!!! 
        db.session.commit()
        lg.warning('Deleted exercise !')
