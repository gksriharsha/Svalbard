from Svalbard import db
import csv
from sqlalchemy import Column, MetaData, Table, create_engine, ForeignKey

from sqlalchemy.schema import DropTable, CreateTable
from sqlalchemy.orm import scoped_session, sessionmaker
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Float, String, Table
from sqlalchemy import inspect, MetaData
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, mapper
import csv
#from Svalbard import db

global Base, engine, metadata


class ClassifierTemplate(object):    
    def __init__(self, structure):
        tablename=structure.pop('tablename')
        self.__table__ = Table(tablename, db.metadata, autoload=True, autoload_with=db.get_engine())
        self.__dict__.update(structure)

    def __repr__(self):
        return self.__dict__


def get_table(name):
    
    if name in db.metadata.tables:
        table = db.metadata.tables[name]

    cls = type(name.title(), (ClassifierTemplate,), {})
    mapper(cls, table)
    return cls


def inject(Data):

    t = get_table(Data['tablename'])

    #t = Table(tablename,db.metadata,autoload=True,autoload_with=db.get_engine())

    insertion = t(Data)
    db.session.add(insertion)
    db.session.commit()

    return insertion.id


if __name__ == '__main__':
    DR4 = csv.DictReader(open('Svalbard/csv/KNN.csv', 'r'))
    inject('KNN_py',next(DR4))