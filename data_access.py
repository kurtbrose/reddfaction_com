from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import clastic

Base = declarative_base()
SESSION = sessionmaker()
ENGINE = create_engine('sqlite:///:memory:', echo=True)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    reddit_name = Column(String(64))

    def __init__(self, reddit_name):
        self.reddit_name = reddit_name

    def __repr__(self):
        return "<User "+self.reddit_name+">"

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    parent  = Column(Integer, ForeignKey('messages.id'))
    created = DateTime()
    edited  = DateTime()
    contents = Text()

#NOTE: this must go after classes are defined
Base.metadata.create_all(ENGINE)
SESSION.configure(bind=ENGINE)

class DBSessionMiddleware(clastic.Middleware):
    provides = ('db_session',)

    def request(self, next):
        session = SESSION()
        ret = next(session)
        session.commit() #if exception is raised, do not commit
        return ret


