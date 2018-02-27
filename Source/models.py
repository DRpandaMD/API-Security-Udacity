# Models.py
# where we set up the data base and describe that data

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as password_context

# passlib is a installed package that lets us hash passwords and check them

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), index=True)
    password_hash = Column(String(64))

    def hash_password(self, password):
        self.password_hash = password_context.encrypt(password)

    def verify_password(self, password):
        return password_context.verify(password, self.password_hash)


engine = create_engine('sqlite:///users.db')

Base.metadata.create_all(engine)
