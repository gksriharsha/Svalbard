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
        self.__dict__.update(structure)

    def __repr__(self):
        return self.__dict__


def get_table(name):
    global Base
    if name in Base.metadata.tables:
        table = Base.metadata.tables[name]

    cls = type(name.title(), (ClassifierTemplate,), {})
    mapper(cls, table)
    return cls


def create_table_sql(name, cols):
    global engine, Base
    Base = declarative_base()
    Base.metadata.reflect(engine)
    if name in Base.metadata.tables:
        return

    table = type(name, (Base,), cols)
    table.__table__.create(bind=engine)


def create_table_structure(name, row):
    structure = {}
    structure.update({'__tablename__': name})
    structure.update({'id': Column(Integer, primary_key=True)})
    structure.update({'Result'})
    for item in row.items():
        try:
            float(item[1])
            try:
                int(item[1])
                structure.update({item[0]: Column(Integer)})
                continue
            except:
                structure.update({item[0]: Column(Float)})
                continue
        except:
            structure.update({item[0]: Column(String)})
    return structure


def create_table_api(table_name, sample_row):

    create_table_sql(table_name, create_table_structure(
        table_name, sample_row))


def create(table_name,csvfile):
    global engine, metadata

    engine = create_engine('sqlite:///site2.db')

    metadata = MetaData(engine)

    DR = csv.DictReader(open(csvfile))

    create_table_api(table_name,next(DR))

    Session = scoped_session(sessionmaker(bind=engine))

    t = get_table(table_name)

    try:        
        for result in DR:
            Session.add(t(result))
        Session.commit()
    except Exception as e:
        Session.rollback()
    finally:
        Session.close()


if __name__ == '__main__':
    create('MLP','Svalbard/csv/MLP.csv')
    create('KNN','Svalbard/csv/KNN.csv')