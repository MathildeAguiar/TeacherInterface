# coding: utf-8
import datetime
import random, string
from re import L, escape
from sqlalchemy import Column, ForeignKey, Integer, TIMESTAMP, Table, Text
from sqlalchemy.dialects.mysql import INTEGER, TEXT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import user
from sqlalchemy.sql.sqltypes import Boolean
from .views import app
import logging as lg
from flask_sqlalchemy import SQLAlchemy, request
from random import choices, randint, randrange
from sqlalchemy import exc
from flask.helpers import flash
#from flask.ext.sqlalchemy import exc


#exceptions = exc.sa_exc



#database 
db = SQLAlchemy(app)


#classes of our tables 

class MetalUser(db.Model):
    """User table"""
    __tablename__ = 'metal_users'

    id = Column(INTEGER, primary_key=True)
    lastName = Column(VARCHAR(191), nullable=False)
    firstName = Column(VARCHAR(191), nullable=False)
    password = Column(VARCHAR(191), nullable=False)
    #many to one with groups (many users can be in 1 group) --> might change to many to many 
    group_id = Column(Integer, ForeignKey('metal_groups.id'))
    group = relationship("MetalGroup", back_populates="users")
    type = Column(VARCHAR(191)) #role 
    #comment from the teacher avaiable for the student
    comment_student = Column(VARCHAR(512))
    #comment from the teacher but only viewable by the teacher
    comment_teacher = Column(VARCHAR(512))

association_groups_chaps = Table('groups_chaps', db.metadata, Column('group_id', Integer, ForeignKey('metal_groups.id')), Column("chapter_id", Integer, ForeignKey('metal_chapters.id')))

class MetalGroup(db.Model):
    """Groups of students table"""
    __tablename__ = 'metal_groups'

    id = Column(INTEGER, primary_key=True)
    level = Column(VARCHAR(191), unique=True, nullable=False)
    #many to one with users  --> might change into many to many 
    users = relationship("MetalUser", back_populates="group")
    #many to one avec session d'exercices 
    sessions = relationship("MetalAssignment", back_populates="group")
    #many to many with chapter table 
    chapters = relationship("MetalChapter", secondary= association_groups_chaps, back_populates="groups")

    def __repr__(self) -> str:
        return repr(self.level) 


association_chap_exos= Table('chaps_exos', db.metadata, Column('chap_id', Integer, ForeignKey('metal_chapters.id')), Column('exo_id', Integer, ForeignKey('metal_exercises.id')))

association_chaps_notions = Table('exos_notions', db.metadata, Column('notion_id', Integer, ForeignKey('metal_notions.id')), Column('chap_id', Integer, ForeignKey('metal_chapters.id')))

class MetalChapter(db.Model):
    """Chapter table"""
    __tablename__ = 'metal_chapters'

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(191), unique=True, nullable=False)
    tags = Column(TEXT)
    slug = Column(VARCHAR(191))
    cycle = Column(VARCHAR(191))  
    summary = Column(TEXT)
    #many to many with the table Groups  
    groups = relationship("MetalGroup", secondary=association_groups_chaps, back_populates="chapters")
    #many to many with exercices 
    exos = relationship("MetalExercise", secondary=association_chap_exos, back_populates="chaps")
    #many to many with notions 
    notions = relationship("MetalNotion", secondary=association_chaps_notions, back_populates='chaps')
    #to handle files paths 
    files = relationship("MetalFile", back_populates='chapter')

    def __repr__(self) -> str:
        return repr(self.name) 
    

class MetalFile(db.Model):
    """File from a chapter table"""
    __tablename__ = 'metal_files'

    id = Column(Integer, primary_key=True) 
    name = Column(VARCHAR(512), unique=True, nullable=False)  
    chapter_id = Column(Integer, ForeignKey('metal_chapters.id'))
    chapter = relationship("MetalChapter", back_populates='files')

    def __repr__(self) -> str:
        return repr(self.name)

association_exos_quests = Table('quests_exos', db.metadata, Column('quest_id', Integer, ForeignKey('metal_questions.id')), Column('exo_id', Integer, ForeignKey('metal_exercises.id')))   

association_exos_sessions = Table('sess_exos', db.metadata, Column('sess_id', Integer, ForeignKey('metal_assignments.id')), Column('exo_id', Integer, ForeignKey('metal_exercises.id')))

association_exos_txts = Table('exos_txts', db.metadata, Column('txt_id', Integer, ForeignKey('metal_corpuses.id')), Column('exo_id', Integer, ForeignKey('metal_exercises.id')))

#association_exos_notions = Table('exos_notions', db.metadata, Column('notion_id', Integer, ForeignKey('metal_notions.id')), Column('exo_id', Integer, ForeignKey('metal_exercices.id')))

class MetalExercise(db.Model):
    """Exercise table"""
    __tablename__ = 'metal_exercises'

    id = Column(INTEGER, primary_key=True)
    #many to many with chapters 
    chaps = relationship("MetalChapter", secondary=association_chap_exos, back_populates="exos")
    name = Column(VARCHAR(191), unique=True, nullable=False)
    limited_time = Column(Integer)
    #limited_time = Column(Boolean) #does boolean works here ? 
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
    #question d??j?? li??e ?? la notion et au texte donc pas besoin de redondance 
    #text_related = Column(ForeignKey('metal_corpuses.name'))
    # 
    # test Repr()
    def __repr__(self) -> str:
        return repr(self.name) 


#add question type et metal question aswers ? 
class MetalQuestion(db.Model):
    """Question table"""
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

    def __repr__(self) -> str:
        return repr(self.slug) 



class MetalAssignment(db.Model): #exercices session
    """Assignment table""" 
    __tablename__ = 'metal_assignments'

    id = Column(INTEGER, primary_key=True, unique=True)
    user_id = Column(INTEGER, ForeignKey('metal_users.id'))  #? keep??? , nullable=False
    name = Column(VARCHAR(191), nullable=False, unique=True)
    code = Column(INTEGER, unique=True) #some have codes (mandatory groups of exercices) and some don't (non mandatory ones)
    #mark = Column(Integer, nullable=False) --> doit ??tre par rapport ?? un ??l??ve 
    #many to one with Groups 
    group_id = Column(Integer, ForeignKey('metal_groups.id') )
    group = relationship("MetalGroup", back_populates="sessions")
    #many to many with exercices 
    exos = relationship("MetalExercise", secondary=association_exos_sessions, back_populates="sessions")
    #one to many with Usr answer
    usr_answers = relationship("MetalAnswerUser", back_populates="session")
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    def __repr__(self) -> str:
        return repr(self.name) 


 

association_notions_txts = Table('notions_txts', db.metadata, Column('notion_id', Integer, ForeignKey('metal_notions.id')), Column('txt_id', Integer, ForeignKey('metal_corpuses.id')))

class MetalCorpus(db.Model):
    """Corpus table"""
    __tablename__ = 'metal_corpuses'

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(191), unique=True, nullable=False)
    #notion_id = Column(ForeignKey('metal_notions.id'), nullable=False)
    author = Column(VARCHAR(191))
    #many to many with exercices
    exos = relationship("MetalExercise", secondary=association_exos_txts, back_populates="corpuses")
    #many to many with notions
    notions = relationship("MetalNotion", secondary=association_notions_txts, back_populates="corpuses")

    def __repr__(self) -> str:
        return repr(self.name) 



class MetalNotion(db.Model): #equivalent to grammatical element 
    """Grammatical Notion table"""
    __tablename__ = 'metal_notions'

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(191), unique=True, nullable=False)
    #many to many with exos 
    #exos = relationship("MetalExercices", secondary=association_exos_notions, back_populates="notions")
    #many to many with corpus
    corpuses = relationship("MetalCorpus", secondary=association_notions_txts, back_populates="notions")
    #one to many with notion item 
    notion_item = relationship("MetalNotionItem")
    #many to one with questions
    questions = relationship("MetalQuestion",back_populates="notion")
    #question_id = Column(INTEGER, ForeignKey('metal_questions.id')) 
    #many to many with chapters
    chaps = relationship("MetalChapter", secondary=association_chaps_notions, back_populates="notions")
    #status if this notion has been verified by a human or not 
    checked_status = Column(Boolean)

    def __repr__(self) -> str:
        return repr(self.name) 



class MetalNotionItem(db.Model): #equivalent to grammatical marker 
    """Grammatical Element table"""
    __tablename__ = 'metal_notion_items'

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(191), nullable=False)
    notion_id = Column(INTEGER, ForeignKey('metal_notions.id'),  nullable=False)

    def __repr__(self) -> str:
        return repr(self.name) 


class MetalQuestionHighlight(db.Model):
    """Question type 'Highlighting' table"""
    __tablename__ = 'metal_question_highlights'

    id = Column(INTEGER, primary_key=True)
    question_id = Column(INTEGER, ForeignKey('metal_questions.id'), nullable=False)
    questions = relationship("MetalQuestion", back_populates="questHighlight")
    word_position = Column(INTEGER, nullable=False)
    instructions = Column(TEXT, nullable=False)

    def __repr__(self) -> str:
        return repr(self.instructions) 

class MetalQuestionFillBlank(db.Model):
    """Question type 'FillBlank' table"""
    __tablename__ = 'metal_question_fill_blanks'

    id = Column(INTEGER, primary_key=True)
    question_id = Column(INTEGER, ForeignKey('metal_questions.id'), nullable=False)
    questions = relationship("MetalQuestion", back_populates="questFillBlank")
    word_position = Column(INTEGER, nullable=False)
    instructions = Column(TEXT, nullable=False)

    def __repr__(self) -> str:
        return repr(self.instructions) 

class MetalQuestionTrueFalse(db.Model):
    """Question type 'TrueFalse' table"""
    __tablename__ = 'metal_question_true_falses'

    id = Column(INTEGER, primary_key=True)
    question_id = Column(INTEGER, ForeignKey('metal_questions.id'), nullable=False)
    questions = relationship("MetalQuestion", back_populates="questTF")
    instructions = Column(TEXT, nullable=False)
    #do we need to add the available choices (Vrai, faux) ???? 

    def __repr__(self) -> str:
        return repr(self.instructions) 



class MetalAnswerUser(db.Model):
    """User answers to questions table"""
    __tablename__ = 'metal_answer_users'

    id = Column(INTEGER, primary_key=True)
    user_id = Column(INTEGER, ForeignKey('metal_users.id'), nullable=False)
    #chapter_id = Column(INTEGER, ForeignKey('metal_chapters.id'), nullable=False)
    #many to one with questions
    question_id = Column(INTEGER, ForeignKey('metal_questions.id')) #, nullable=False --> conflic when u delete a question notion in validate page 
    question = relationship("MetalQuestion", back_populates="usr_answer")
    #one to many with sessions  
    session_id = Column(INTEGER, ForeignKey('metal_assignments.id'))
    session = relationship("MetalAssignment", back_populates="usr_answers") 
    #correct_answer = Column(Text, nullable=False) #do we need it or is it done by the analyser or smth already in the question type table 
    user_answer = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP) #should we keep that ?
    updated_at = Column(TIMESTAMP) # "   "  "  "
    #ajouter un feedback de la part du prof ??? 

    def __repr__(self) -> str:
        return repr(self.user_answer) 


####### database initialization ########


def init_db():
    """To init the database with some random data. TO DELETE in the final version."""
    db.drop_all()
    db.create_all()

    #population of the db 

    #random groups 

    for i in range(2):
        grp = MetalGroup()
        grp.level = "3??me.{}".format(i+1)
        db.session.add(grp)

    for i in range(3):
        grp = MetalGroup(level="4??me.{}".format(i+1))
        db.session.add(grp)

    #random users 
    for i in range(5):
        usr = MetalUser()
        usr.lastName = "Dupont{}".format(i+1)
        usr.firstName = "Pierre{}".format(i+1)
        usr.group_id = randint(1, 4)
        usr.password = randint(1, 99)
        db.session.add(usr)
    
    #random chaps:
    chap_name = ['Les conjonctions de subordination', 'Pronoms personnels', 'Compl??ment du verbe', 'Temps du subjonctif', "Temps de l'indicatif"]
    for i in range(5):
        chap = MetalChapter()
        chap.name = chap_name[i]
        chap.slug = str(chap.name)
        chap.summary = "Ceci est un r??sum?? de chapitre"
        chap.cycle = 'cours du cycle {}'.format(i)
        chap.tags = 'un tag'
        db.session.add(chap)
    
    # random quests 
    for i in range(9):
        quest = MetalQuestion()
        quest.duration = randint(1, 60)
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
        exo.limited_time = randint(3,20)
        exo.name = "name {}".format(i+1)
        exo.slug = "this is an exo slug"
        exo.tags = "exo's tags"
        db.session.add(exo)


    #random corpus 
    texts = ['Vingt mille lieues sous les mers', 'Le Grand Meaulnes', 'Maupassant', 'Corpus test']
    for i in range(4):
        corp = MetalCorpus()
        corp.name = texts[i]
        corp.author = "author {}".format(i+1)
        n = MetalNotion()
        n.name = "test corpus/notions {}".format(i)
        corp.notions.append(n)
        n1 = MetalNotion()
        n1.name = "Test 2 {}".format(i)
        corp.notions.append(n1)
        n2 = MetalNotion()
        n2.name = "Test 3 {}".format(i)
        corp.notions.append(n2)
        db.session.add(corp)


    #random notion 
    n = ['conjonction-subordination', 'groupe nominal', 'groupe-nominal-sujet', 'pronom relatif', 'indicatif-present', 'complement-d-agent']
    for i in range(5):
        notion = MetalNotion()
        notion.name = n[i]
        #populate the corpuses field 
        c = MetalCorpus()
        c.name = "test notion {}".format(i)
        notion.corpuses.append(c)
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
        sess.code = "".join([random.choice(string.ascii_uppercase + string.digits) for _ in range(10)])
        sess.name = "session n?? {}".format(i)
        sess.updated_at = datetime.datetime.now()
        sess.user_id = i
        sess.group_id = i
        db.session.add(sess)

    #random usr answers 
    for i in range(4):
        usrans = MetalAnswerUser()
        usrans.user_id = 1
        usrans.created_at = datetime.datetime.now()
        usrans.session_id = i
        usrans.user_answer = "user {} answer".format(i)
        usrans.question_id = randint(1,4)
        db.session.add(usrans)

    db.session.commit()
    lg.warning('Database initialized!')



################# Queries that fetch all items of one kind #################

#get all the chapters and order them by their names 
def query_all_chaps():
    """Get all the chapters and order them by their names"""

    chaps = MetalChapter.query.order_by(MetalChapter.name).all()
    """" test for escaping html
    for c in chaps:
        c.summary = escape(c.summary)
    """
    return chaps

#get all the exercises and order them by their names 
def query_all_exos():
    """Get all the exercises and order them by their names"""
    exos = MetalExercise.query.order_by(MetalExercise.name).all()
    return exos

#get all the questions and order them by their names
def query_all_quests():
    """Get all the questions (any kind) and order them by their names"""
    quests = MetalQuestion()
    questsTF = MetalQuestionTrueFalse.query.order_by(MetalQuestionTrueFalse.instructions).all()
    questsFB = MetalQuestionFillBlank.query.order_by(MetalQuestionFillBlank.instructions).all()
    questsH = MetalQuestionHighlight.query.order_by(MetalQuestionHighlight.instructions).all()
    return quests.append(questsTF, questsFB, questsH)

#get all the questions True False and order them by their instructions
def query_all_qTF():
    """Get all the questions True False and order them by their instructions"""
    questsTF = MetalQuestionTrueFalse.query.order_by(MetalQuestionTrueFalse.instructions).all()
    return questsTF

#get all the questions Fill blank and order them by their instructions
def query_all_qFB():
    """Get all the questions Fill blank and order them by their instructions"""
    questsFB = MetalQuestionFillBlank.query.order_by(MetalQuestionFillBlank.instructions).all()
    return questsFB

#get all the questions Highlight and order them by their instructions
def query_all_qH():
    """Get all the questions Highlight and order them by their instructions"""
    questsH = MetalQuestionHighlight.query.order_by(MetalQuestionHighlight.instructions).all()
    return questsH


#get all the grammatical elements and order them by their names 
def query_all_gram():
    """Get all the grammatical notions and order them by their names"""
    gram = MetalNotion.query.order_by(MetalNotion.name).all()
    return gram 

def query_all_groups():
    """Query all groups avaiable """
    grp = MetalGroup.query.order_by(MetalGroup.level).all()
    return grp

#query all the exercices sessions avaiable 
def query_all_sessions():
    """Query all the exercices sessions/assignments avaiable"""
    session = MetalAssignment.query.order_by(MetalAssignment.name).all()
    return session

#query all the texts avaiable 
def query_all_corpuses():
    """Query all the texts avaiable"""
    corpuses = MetalCorpus.query.order_by(MetalCorpus.name).all()
    return corpuses




########### Queries to create a new exercise/chapter/assignment ################

#insert a newly created exercice in the database 
def new_exo(name, chaps, duration, texts, questsTF, questsFB, questsH, tags): 
    """Insert a newly created exercice in the database"""

    try:
        #fct to insert a new exercice in the db after clicking on "create" button
        if name and chaps and texts and (questsFB or questsH or questsTF): #the case where one of a kind of quest is not selected !!!
            exo = MetalExercise()
            exo.name = name
            exo.limited_time = duration
            exo.slug = tags

            for c in chaps: 
                q = db.session.query(MetalChapter).get(c)
                if q:
                    exo.chaps.append(q)
            
            for t in texts:
                q = db.session.query(MetalCorpus).get(t)
                exo.corpuses.append(q)
            
            if questsTF:
                for q1 in questsTF:
                    qTF = db.session.query(MetalQuestionTrueFalse).get(q1)
                    q = db.session.query(MetalQuestion).get(qTF.question_id)
                    exo.quests.append(q)

            if questsFB:
                for q2 in questsFB:
                    qFB = db.session.query(MetalQuestionFillBlank).get(q2)
                    q = db.session.query(MetalQuestion).get(qFB.question_id)
                    exo.quests.append(q)

            if questsH:
                for q3 in questsH:
                    qH = db.session.query(MetalQuestionHighlight).get(q3)
                    q = db.session.query(MetalQuestion).get(qH.question_id)
                    exo.quests.append(q)

            exo.tags = tags

            #the query itself 
            db.session.add(exo)
            db.session.commit()
            lg.warning('Addition done !')

    except exc.SQLAlchemyError as e:

        if e.args == ('(sqlite3.IntegrityError) UNIQUE constraint failed: metal_exercises.name',):

            return flash("Ce nom est d??j?? utilis?? !", 'danger')

#insert a newly created chapter to the database
def query_new_chapter(name, levels, cycle, exos, notions, summary, files, tags):
    """Insert a newly created chapter to the database"""
    try:
        chap = MetalChapter()
        chap.name = name
        if levels is not None:
            for l in levels:
                q = db.session.query(MetalGroup).get(l)
                chap.groups.append(q)
        if exos is not None:
            for e in exos:
                q = db.session.query(MetalExercise).get(e)
                chap.exos.append(q)

        if notions is not None:
            for n in notions:
                q = db.session.query(MetalNotion).get(n)
                chap.notions.append(q)
        
        if files is not None:
            for f in files:
                new_file = MetalFile()
                date = datetime.datetime.now()
                new_file.name = str('{}'.format(str(date.day)+"_"+str(date.month)+"_"+str(date.year)+"_"+ str(date.hour)+"_"+str(date.minute)+"_")+f)
                new_file.chapter_id = chap.id
                chap.files.append(new_file)

        chap.cycle = cycle
        chap.slug = summary
        chap.summary = summary
        chap.tags = tags

        #the query itself 
        db.session.add(chap)
        db.session.commit()
        lg.warning('Addition done !')

    except exc.SQLAlchemyError as e:
        db.session.rollback()
        if e.args == ('(sqlite3.IntegrityError) UNIQUE constraint failed: metal_chapters.name',):
            return flash("Ce nom est d??j?? utilis?? !", 'danger')


def query_new_assignment(name, choosenExos, groups, code):
    """Query to create a new assignment"""
  
    try:
        assignment = MetalAssignment()
        assignment.name = name
        assignment.code = code 
        assignment.created_at = datetime.datetime.now()
        assignment.updated_at = datetime.datetime.now()
        if choosenExos is not None:
            for e in choosenExos:
                q = db.session.query(MetalExercise).get(e)
                assignment.exos.append(q)
        if groups is not None:
            for g in groups:
                q = db.session.query(MetalGroup).get(g)
                assignment.group = q 
        
        #the query itself 
        db.session.add(assignment)
        db.session.commit()
        lg.warning('Addition done !')

    except exc.SQLAlchemyError as e:
        db.session.rollback()
        if e.args == ('(sqlite3.IntegrityError) UNIQUE constraint failed: metal_assignments.code',):
            return flash("Veuillez choisir un nouveau code !", 'danger')
        if e.args == ('(sqlite3.IntegrityError) UNIQUE constraint failed: metal_assignments.name',):
            return flash("Ce nom est d??j?? utilis?? !", 'danger')
        
        


######################### Home page query ###########################################
def general_query2(query, category):
    """Home page query"""

    res = list()

    #I changed the format of the input so the query acts like a LIKE and the user gets more results 
    search = "%{}%".format(query)
 

    if category == 'All':
        #we check all the possibilities 
        tmp_chap = MetalChapter.query.filter(MetalChapter.name.like(search)).all()
        tmp_exo = MetalExercise.query.filter(MetalExercise.name.like(search)).all()
        tmp_questTF = MetalQuestionTrueFalse.query.filter(MetalQuestionTrueFalse.instructions.like(search)).all() 
        tmp_questFB = MetalQuestionFillBlank.query.filter(MetalQuestionFillBlank.instructions.like(search)).all() 
        tmp_questH = MetalQuestionHighlight.query.filter(MetalQuestionHighlight.instructions.like(search)).all() 
        tmp_gramm = MetalNotion.query.filter(MetalNotion.name.like(search)).all()
        tmp_txt = MetalCorpus.query.filter(MetalCorpus.name.like(search)).all()


        if tmp_chap!=[]:
            res.append(tmp_chap) 
        
        if tmp_exo !=[]:
            res.append(tmp_exo)
        
        if tmp_gramm !=[]:
            res.append(tmp_gramm)
        
        if tmp_questTF!=[]:
            res.append(tmp_questTF)

        if tmp_questFB!=[]:
            res.append(tmp_questFB)
        
        if tmp_questH!=[]:
            res.append(tmp_questH)
        
        if tmp_txt!=[]:
            res.append(tmp_txt)

        elif len(res)==0: return "Aucun r??sultat !"
    
    if category == 'Chapitres':
        tmp_chap = MetalChapter.query.filter(MetalChapter.name.like(search)).all()
        res.append(tmp_chap)
    
    if category=='Exercices':
        tmp_exo = MetalExercise.query.filter(MetalExercise.name.like(search)).all()
        res.append(tmp_exo)
    if category== 'Notions':
        tmp_gramm = MetalNotion.query.filter(MetalNotion.name.like(search)).all()
        res.append(tmp_gramm)
    if category=='Questions':
        tmp_questTF = MetalQuestionTrueFalse.query.filter(MetalQuestionTrueFalse.instructions.like(search)).all() 
        tmp_questFB = MetalQuestionFillBlank.query.filter(MetalQuestionFillBlank.instructions.like(search)).all() 
        tmp_questH = MetalQuestionHighlight.query.filter(MetalQuestionHighlight.instructions.like(search)).all()
        if tmp_questH != []:
            res.append(tmp_questH) 
        if tmp_questFB != []:
            res.append(tmp_questFB)
        if tmp_questTF !=[]:
            res.append(tmp_questTF)
    if category == 'Textes':
        tmp_txt = MetalCorpus.query.filter(MetalCorpus.name.like(search)).all()
        res.append(tmp_txt)
    
    elif len(res)==0: return "Aucun r??sultat !"

    for o in res:
        return o



############ Validation page's query ################# 

def query_validation(txtName): 
    """Validation page's query"""

    if txtName is not None: 
        notions = db.session.query(MetalNotion).join(MetalCorpus, MetalNotion.corpuses).filter(MetalCorpus.name==txtName).all()   
        if notions !=[]: 
            return notions 
        else: None    
    else: None 


def edit_notion(notionId, name, notionItem): #we can't change much with only those fields :(
    """Query to edit a notion found by the analyser"""

    notion = db.session.query(MetalNotion).get(notionId)
    if notion :
        notion.name = name
        if notionItem:
            for i in notionItem:
                q = db.session.query(MetalNotionItem).get(i)
                if q:
                    notion.notion_item.append(q)
    
        db.session.commit()
        lg.warning('Modified notion !')



def query_delete_notion(notionId, txt_name):
    """Query to delete a notion"""

    notion = db.session.query(MetalNotion).get(notionId)
    text = db.session.query(MetalCorpus).filter(MetalCorpus.name == txt_name).first() 
    if notion and text:
        #remove the corpus, notion side
        for t in notion.corpuses:
            if t == text :
                notion.corpuses.remove(t)
                db.session.commit()

        #remove the notion, corpus side
        for n in text.notions:
            if n == notion:
                text.notions.remove(n)
                db.session.commit()

        lg.warning('Deleted notion !')


def query_validate_notion(notionId, txt_name):
    notion = db.session.query(MetalNotion).get(notionId)
    #text = db.session.query(MetalCorpus).get(txt_name)

    if notion: #and text:
        #n = text.notions.get(notion)
        notion.checked_status = True
        db.session.commit()
        lg.warning("validated notion by a human!")



################# Modifications/deletions of chapters/exos/assignments ########################

def edit_assignment(assignId, newName, groups, exos):
    """Query to modify an exercice assignment"""

    #on r??cup??re l'objet ?? modifier et ensuite seulement on modifie ses params 
    assign = db.session.query(MetalAssignment).get(assignId)

    if newName:
        assign.name = newName
    if groups:
        for g in groups:
            q = db.session.query(MetalGroup).get(g)
            assign.group_id = q.id  
    if exos:
        for e in exos:
            q = db.session.query(MetalExercise).get(e)
            assign.exos.append(q)

    db.session.commit()
    lg.warning('Modified assignment !')

def edit_chapter(chapId, newName, groups, cycle, exos, notions, summary, files, tags): #txts?? 
    """Query to edit a chapter infos"""

    #on r??cup??re l'objet correspondant
    chap = db.session.query(MetalChapter).filter(MetalChapter.id==chapId).first()
    if newName:
        chap.name = newName
    if summary:
        chap.summary = summary
        chap.slug = summary

    if groups is not None:
        for l in groups:
            q = db.session.query(MetalGroup).get(l)
            chap.groups.append(q)
    if exos is not None:
        for e in exos:
            q = db.session.query(MetalExercise).get(e)
            chap.exos.append(q)

    if notions is not None:
        for n in notions:
            q = db.session.query(MetalNotion).get(n)
            chap.notions.append(q)    
  
    if files:
        for f in files:
            #creating a new obj File with a unique name 
            tmp_file = MetalFile()
            tmp_file.name = "{}".format(datetime.datetime.now()) + "_" + str(f)  #ajouter le login
            tmp_file.chapter_id = chapId
            db.session.add(tmp_file)
            chap.files.append(tmp_file)

    if tags:
        chap.tags = tags
    if cycle:
        chap.cycle = cycle
    
    db.session.commit()
    lg.warning('Modified chapter !')

def edit_exo(exoId, newName, chaps, duration, txts, qTF, qH, qFB, tags):
    """Query to edit an exercise infos"""

    #on r??cup??re l'exercice correspondant
    exo = db.session.query(MetalExercise).filter(MetalExercise.id==exoId).first()
    if newName:
        exo.name = newName
    if tags:
        exo.tags = tags
    if duration:
        exo.limited_time = duration
    if chaps:
        for c in chaps: 
                q = db.session.query(MetalChapter).get(c)
                exo.chaps.append(q)
    if txts: 
        for t in txts:
            q = db.session.query(MetalCorpus).get(t)
            exo.corpuses.append(q)
        
    if qTF:
        for q1 in qTF:
            questTF = db.session.query(MetalQuestionTrueFalse).get(q1)
            q = db.session.query(MetalQuestion).get(questTF.question_id)
            exo.quests.append(q)

    if qFB:
        for q2 in qFB:
            questFB = db.session.query(MetalQuestionFillBlank).get(q2)
            q = db.session.query(MetalQuestion).get(questFB.question_id)
            exo.quests.append(q)

    if qH:
        for q3 in qH:
            questH = db.session.query(MetalQuestionHighlight).get(q3)
            q = db.session.query(MetalQuestion).get(questH.question_id)
            exo.quests.append(q)

    db.session.commit()
    lg.warning('Modified chapter')


def query_delete_session(sessionId):
    """Query to delete an assignment"""
    sess = MetalAssignment.query.get(sessionId)
    if sess:
        db.session.delete(sess)
        db.session.commit()
        lg.warning('Deleted session !')

    
def query_delete_chapter(chapId):
    """Query to delete a chapter"""
    chap = MetalChapter.query.get(chapId)
    if chap:
        db.session.delete(chap)
        db.session.commit()
        lg.warning('Deleted chapter !')
    

def query_delete_exercise(exoId):
    """Query to delete an exercise"""

    exo = MetalExercise.query.get(exoId)
    if exo:
        db.session.delete(exo)
        db.session.commit()
        lg.warning('Deleted exercise !')


def query_groups_sessions(group_id):
    """Query the exercises assignments done by one group """

    sess = db.session.query(MetalAssignment).filter(MetalAssignment.group_id==group_id).all()
    if sess:
        return sess
    else :
        return "Aucun r??sultat !"


def query_groups_students(group_id):
    """Query the students from one group"""

    stud = db.session.query(MetalUser).filter(MetalUser.group_id==group_id).all()
    if stud:
        return stud 
    else :
        return "Aucun r??sultat !"


def query_answers_user(user_id):
    """Query to get all the answers from a user"""

    answers = db.session.query(MetalAnswerUser).filter(MetalAnswerUser.user_id == user_id).all()
    if answers:
        return answers
    else :  return "Aucun r??sultat !"


def query_assignments_by_user(user_id):
    """Query all the assignments done by one user"""

    user = db.session.query(MetalUser).get(user_id)
    if user:
        assignments = db.session.query(MetalAssignment).filter(user.group_id == MetalAssignment.group_id).all()
        return assignments
    else : return 'Aucun r??sultat !'


def query_update_comment(user_id, zone, comment):
    """Query to update a comment for the student/for the teacher him.herself"""
    
    user = db.session.query(MetalUser).get(user_id)

    if zone == 'submitted_zone1':
        user.comment_student = comment
    elif zone == 'submitted_zone2':
        user.comment_teacher = comment
    
    db.session.commit()
    lg.warning('Modified comment !')


