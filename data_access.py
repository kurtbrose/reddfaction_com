from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text

Base = declarative_base()

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

def test():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine('sqlite:///:memory:', echo=True)
    Base.metadata.create_all(engine)

    Session = sessionmaker()
    Session.configure(bind=engine)

    session = Session()

if __name__ == "__main__":
    test()


