from flask import render_template, url_for, flash, redirect, request, jsonify
from Svalbard import app, db
from Svalbard.forms import SearchForm
from Svalbard.models import Result, Dataset
from sqlalchemy.orm import scoped_session, sessionmaker


import numpy as np


import io
import base64

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt

results = []


@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    results = Result.query.order_by(
        Result.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', results=results)


@app.route("/bg_process", methods=['POST'])
def hp():
    global results
    flag = False
    session = scoped_session(sessionmaker(bind=db.get_engine()))()
    ids = set([result.id for result in results])
    tblobj = db.metadata.tables[str(request.form.get('clf')).strip()+'_py']
    data = request.form.get('form_data').split(';')
    for condition in data:
        if not 'csrf' in condition:
            if 'true' in condition:
                [_, hp_val] = condition.split(',')
                [param, val] = hp_val.split(':')
                param = param.replace('select', '')
                ids = set(ids).intersection(
                    set(i[1] for i in session.query(tblobj).filter_by(**{param: val}).all()))
    ids1 = ids
    if(len(ids) > 100):
        ids1 = set(list(ids)[0:98])
        flag = True
    results1 = results.filter(Result.id.in_(ids1))
    return jsonify(data=render_template('response.html', results=results1, flag=flag))


@app.route("/search", methods=['GET', 'POST'])
def search():
    global results
    page = request.args.get('page', 1, type=int)
    search = SearchForm()
    search.Process.choices = [(r.process, str(r.process))
                              for r in db.session.query(Result.process).distinct()]
    search.Task.choices = [(r.task, str(r.task))
                           for r in db.session.query(Result.task).distinct()]
    search.Platform.choices = [(r.platform, str(r.platform))
                               for r in db.session.query(Result.platform).distinct()]
    search.Dataset.choices = [(r.dataset_id, str(Dataset.query.filter_by(id=r.dataset_id).first()
                                                 .dataset_name)) for r in db.session.query(Result.dataset_id).distinct()]
    if search.is_submitted():
        cols = []
        results = Result.query
        hp_list = []
        if search.ProcessCheck.data:
            results = results.filter_by(process=search.Process.data)
        if search.PlatformCheck.data:
            results = results.filter_by(platform=search.Platform.data)
        if search.DatasetCheck.data:
            results = results.filter_by(dataset_id=search.Dataset.data)
        if search.TaskCheck.data:
            results = results.filter_by(task=search.Task.data)

            #cols = [table for table in db.metadata.tables if '_py' in table]
            #values_list = [val for (val,_) in db.session.query(list(t1.columns)[4]).distinct().all()]
            #cols = [(table,column['name'],db.session.query(list(tblobj.columns)[1]).distinct().all()) for (table,tblobj) in db.metadata.tables.items() if '_py' in table for column in inspector.get_columns(table)]
            cols = [(table, col, [val[0] for (val) in db.session.query(colobj).distinct().all()])for (table, tblobj) in list(
                db.metadata.tables.items()) if '_py' in table for (col, colobj) in tblobj.columns.items()]
            hp_list = [col for (_, col, _) in cols]
        tbl_dct = dict(db.metadata.tables)
        zipped = []
        for result in results:
            tblobj = tbl_dct[str(result.task)+'_py']
            hp_config = db.session.query(tblobj).filter_by(
                resultid=result.id).first()
            col_names = [desc['name']
                         for desc in db.session.query(tblobj).column_descriptions]

            zipped.append(dict(zip(col_names, hp_config)))

        if results.count() > 300:
            results1 = results.limit(300)
            flag = True
        else:
            results1 = results
            flag = False

        return render_template('search.html', title='Results', flag=flag, results=results1, form=search, cols=cols, hp_list=hp_list, res_zip=zipped)

    return render_template('search.html', title='Search Space', form=search, hp_list=[], cols={})


@app.route("/task/<string:task>")
def ML_task(task):
    page = request.args.get('page', 1, type=int)
    results = Result.query.filter_by(task=task).order_by(
        Result.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('task.html', title='Task', task=task, results=results)


@app.route("/process/<string:process>")
def process(process):
    page = request.args.get('page', 1, type=int)
    results = Result.query.filter_by(process=process).order_by(
        Result.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('process.html', title='Process', process=process, results=results)


@app.route("/platform/<string:platform>")
def ML_platform(platform):
    page = request.args.get('page', 1, type=int)
    results = Result.query.filter_by(platform=platform).order_by(
        Result.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('platform.html', title='Language', platform=platform, results=results)


@app.route("/dataset/<string:dataset>")
def ML_dataset(dataset):
    page = request.args.get('page', 1, type=int)
    results = Result.query.filter_by(dataset_id=dataset).order_by(
        Result.date_posted.desc())
    results_paginated = results.paginate(page=page, per_page=5)
    dataset = Dataset.query.filter_by(
        id=dataset).first_or_404()

    def getdatasetAnalytics():
        Analytics = {}
        Analytics['Accuracy'] = {}
        Analytics['Accuracy']['Mean'] = np.mean(
            [result.details.Accuracy for result in results])
        Analytics['Accuracy']['Median'] = np.median(
            [result.details.Accuracy for result in results])
        Analytics['Accuracy']['Std'] = np.std(
            [result.details.Accuracy for result in results])
        Analytics['Accuracy']['Q1'] = np.quantile(
            [result.details.Accuracy for result in results], 0.25)
        Analytics['Accuracy']['Q3'] = np.quantile(
            [result.details.Accuracy for result in results], 0.75)
        Analytics['F1 Score'] = {}
        Analytics['F1 Score']['Mean'] = np.mean(
            [result.details.F1_Score for result in results])
        Analytics['F1 Score']['Median'] = np.median(
            [result.details.F1_Score for result in results])
        Analytics['F1 Score']['Std'] = np.std(
            [result.details.F1_Score for result in results])
        Analytics['F1 Score']['Q1'] = np.quantile(
            [result.details.F1_Score for result in results], 0.25)
        Analytics['F1 Score']['Q3'] = np.quantile(
            [result.details.F1_Score for result in results], 0.75)

        Tasks = [r.task for r in db.session.query(Result.task).distinct()]
        for task in Tasks:
            Analytics[str(task)] = {}
            results1 = results.filter_by(task=task)
            Analytics[str(task)]['Accuracy'] = np.mean(
                [result.details.Accuracy for result in results1])
            Analytics[str(task)]['F1 Score'] = np.mean(
                [result.details.F1_Score for result in results1])
        return Analytics

    Analytics = getdatasetAnalytics()

    return render_template('dataset.html', title='Language', dataset=dataset, results=results_paginated, dataset_id=dataset, analytics=Analytics)


@app.route("/datagraph", methods=["GET"])
def plotView():
    data = []
    dataset = request.args.get('dataset',1,type=int)
    results = Result.query.filter_by(dataset_id=dataset)
    Tasks = [r.task for r in db.session.query(Result.task).distinct()]
    for task in Tasks:
        results1 = results.filter_by(task=task)
        data.append([result.details.Accuracy*100 for result in results1])
    fig,axis1 = plt.subplots()
    axis1.set_title('Task wise results')
    axis1.set_ylabel('Accuracy')
    axis1.set_xticklabels(Tasks)
    axis1.boxplot(data)
    plt.show()
