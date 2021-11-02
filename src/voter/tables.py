from sqlalchemy import Column, Integer, Boolean, Text, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(40), nullable=False, unique=True)
    username = Column(String(40), nullable=False)
    hashed_password = Column(String, nullable=False)


class Questions(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    text = Column(Text)
    pros = Column(Integer, default=0)
    cons = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    author = Column(Integer, ForeignKey("users.id"))
    created_date = Column(Date)


class Choices(Base):
    __tablename__ = "choices"

    id = Column(Integer, primary_key=True)
    names = Column(String, primary_key=True, unique=True, nullable=False)


class Voted(Base):
    __tablename__ = "voted"

    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    choices_names = Column(String, ForeignKey("choices.names"))
