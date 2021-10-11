from sqlalchemy import Column, Integer, Boolean, Text, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Questions(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    text = Column(Text)
    pros = Column(Integer, default=0)
    cons = Column(Integer, default=0)
    is_active = Column(Boolean)
    author = Column(Integer)
    created_date = Column(Date)


class Choice(Base):
    __tablename__ = "choice"

    id = Column(Integer, primary_key=True)
    pros = Column(String)
    cons = Column(String)
