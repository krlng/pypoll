import sqlalchemy as db
from typing import List, Any
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.types import PickleType


Base = declarative_base()

class Question(Base):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    #options = Column(MutableList.as_mutable(PickleType), default=[])
    options = relationship("Option", back_populates="question")

class Option(Base):
    __tablename__ = 'option'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    votes = Column(Integer, default=0)
    question_id = Column(Integer, ForeignKey('question.id'))
    question = relationship("Question", back_populates="options")

    message = Column(String)
    

def create_db(engine):
    Base.metadata.create_all(engine)
    return Question, Option

def add_question(session, question_str, options: List[Any]):
    q = Question(
        question=question_str,
        options = [Option(text=x) for x in options]
    )

    session.add(q)
    session.commit()
    
#add_question(engine, "Did you like the event", ["a", "b", "c"])

def get_all(engine, schema: Base = Question):
    connection = engine.connect()
    #metadata = db.MetaData()

    questions = db.Table(schema.__name__, schema.metadata, autoload=True, autoload_with=engine)
    
    query = db.select([questions])

    result_proxy = connection.execute(query)
    result_set = result_proxy.fetchall()
    return questions

def get_one(session):
    from sqlalchemy import select
    result = session.execute(select(Question).order_by(Question.id.desc()))
    return result.fetchone()[0]

if __name__ == "__main__":
    engine = db.create_engine('sqlite:///survey.sqlite3'+'?check_same_thread=False')
    Question, Option = create_db(engine)
