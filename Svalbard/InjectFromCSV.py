from Svalbard import db
from Svalbard.models import Dataset, Metadata, Result, Metrics
import csv
from sqlalchemy import Column, MetaData, Table, create_engine, ForeignKey
from sqlalchemy import String, Integer, Float, BigInteger, DateTime

from sqlalchemy.schema import DropTable, CreateTable
from sqlalchemy.orm import scoped_session, sessionmaker
import re

from contextlib import contextmanager

fID = ''


def init_fetch():
    global DR1, DR2, DR3, DR4
    DR1 = csv.DictReader(open('Svalbard/csv/results.csv', 'r'))
    DR2 = csv.DictReader(open('Svalbard/csv/MetaData.csv', 'r'))
    DR3 = csv.DictReader(open('Svalbard/csv/Data.csv', 'r'))
    DR4 = csv.DictReader(open('Svalbard/csv/KNN.csv', 'r'))


def next_from_file1():
    global fID, DR1
    for row in DR1:
        if not(row['fID'] == fID):
            continue
        else:
            yield row


def next_from_file2():
    global fID, DR2
    for row in DR2:
        if not(row['fID'] == fID):
            continue
        else:
            yield row


def next_from_file3():
    global fID, DR3
    for row in DR3:
        fID = row['Metadata']
        yield row


def next_from_file4():
    global fID, DR4
    for row in DR4:
        if not(row['fID'] == fID):
            continue
        else:
            yield row


@contextmanager
def Session(*args, **kwargs):
    Session = scoped_session(sessionmaker(
        bind=create_engine(*args, **kwargs)))

    try:
        session = Session()
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def create_clf_tables():
    DB = 'sqlite:///Svalbard/site.db'
    global clf_list 
    clf_list = ['KNN']
    for clf in clf_list:
        f = open(f'Svalbard/csv/{clf}.csv', 'r')
        DX = csv.DictReader(f)
        dictio = next(DX)
        TABLE_SPEC = [('id', BigInteger), ('ResultId',BigInteger)]+[(k, Float) if re.match(r'^-?\d+(?:\.\d+)?$', v) else (k, String) for (k,v) in dictio.items()]
        TABLE_SPEC = [item for item in TABLE_SPEC if 'ID' not in item[0]]
        print(TABLE_SPEC)
         
        TABLE_NAME = clf_list

        with Session(DB, echo=True) as s:
            for table_x in TABLE_NAME:
                columns = [Column(n, t) for n, t in TABLE_SPEC]
                table = Table(table_x, MetaData(), *columns)
            # this is just here to make the script idempotent
                s.execute('drop table if exists {}'.format(table_x))
                ForeignKey('ResultId')
                table_creation_sql = CreateTable(table)
                s.execute(table_creation_sql)

class Player(object):
    def __init__(self, name, score):
         self.name = name
         self.score = score

def inject_data(x):
    #create_clf_tables()
    init_fetch()
    Entry1 = []
    Entry2 = []
    Entry3 = []
    Entry4 = []
    dataset = []
    for i in range(x):
        Entry1 = next(next_from_file3())
        dataset = Dataset(
            dataset_name=Entry1['Filename'], csv_link=Entry1['csv_url'],
            size=10)
        db.session.add(dataset)
        db.session.commit()

        Entry2 = next(next_from_file1())
        clf_result = Metrics(
            Accuracy=Entry2['Accuracy'], F1_Score=Entry2['F1 Score_1'],
            Precision=Entry2['Precision_1'], Recall=Entry2['Recall_1'],
            Time=Entry2['time'])
        db.session.add(clf_result)
        db.session.commit()

        result = Result(dataset_id=dataset.id,
                        process='Classification', result_id=clf_result.id,
                        task=Entry2['Classifier'].strip(), platform='Python-scikit')
        db.session.add(result)
        db.session.commit()

        #Entry4 = next(next_from_file4())
        #del Entry4['fID']
        #del Entry4['eID']
        #hyperparameter_result = db.Model.KNN(**Entry4)

        row = next(next_from_file2())
        del row['fID']
        row['Dataset_id'] = dataset.id
        Entry3 = Metadata(**row)
        db.session.add(Entry3)
        db.session.commit()

def inject_data2(x):
    #create_clf_tables()
    init_fetch()
    Entry1 = []
    Entry2 = []
    Entry3 = []
    Entry4 = []
    dataset = []
    for i in range(x):
        Entry1 = next(next_from_file3())
        dataset = Dataset(
            dataset_name=Entry1['Filename'], csv_link=Entry1['csv_url'],
            size=10)
        db.session.add(dataset)
        db.session.commit()

        Entry2 = next(next_from_file1())
        clf_result = Metrics(
            Accuracy=Entry2['Accuracy'], F1_Score=Entry2['F1 Score_1'],
            Precision=Entry2['Precision_1'], Recall=Entry2['Recall_1'],
            Time=Entry2['time'])
        db.session.add(clf_result)
        db.session.commit()

        result = Result(dataset_id=dataset.id,
                        process='Classification', result_id=clf_result.id,
                        task=Entry2['Classifier'].strip(), platform='Python-scikit')
        db.session.add(result)
        db.session.commit()

        #Entry4 = next(next_from_file4())
        #del Entry4['fID']
        #del Entry4['eID']
        #hyperparameter_result = db.Model.KNN(**Entry4)

        row = next(next_from_file2())
        del row['fID']
        row['Dataset_id'] = dataset.id
        Entry3 = Metadata(**row)
        db.session.add(Entry3)
        db.session.commit()