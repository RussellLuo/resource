#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import (
    create_engine,
    Column, Integer, String
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    password = Column(String(50))


SQLALCHEMY_DATABASE_URI = 'sqlite:///sqlite.db'

engine = create_engine(SQLALCHEMY_DATABASE_URI)
Base.metadata.create_all(engine)
