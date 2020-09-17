from flask import render_template, url_for, flash, redirect, request, jsonify
from Svalbard import app, db
from Svalbard.forms import SearchForm
from Svalbard.models import Result, Dataset, Metadata
from sqlalchemy.orm import scoped_session, sessionmaker
from scipy import stats

import numpy as np


import io
import base64
import math

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt


from .model.Insight import Insight

results = []


@app.route("/")
def index():
    platform = [ str(r.platform)
                               for r in db.session.query(Result.platform).distinct()]
    process = [ str(r.process)
                              for r in db.session.query(Result.process).distinct()]
    task = [ str(r.task)
                           for r in db.session.query(Result.task).distinct()]
    dataset = [(r.dataset_id, str(Dataset.query.filter_by(id=r.dataset_id).first()
                                                 .dataset_name)) for r in db.session.query(Result.dataset_id).distinct()]
    return render_template("index.html",platforms=platform,datasets=dataset,tasks=task,processes=process)


@app.route("/analytics")
def analytics():
    fixed_hp_resultids = [result.resultid for result in \
        db.session.query(db.metadata.tables['KNN_py'])\
            .filter_by(K=3)
            .filter_by(weights='uniform')
            .filter_by(algorithm='auto')]
    global iterable_list
    iterable_list = []
    metric_list = []
    Accuracies = {result.dataset_id:result.details.Accuracy for result in Result.query.filter(Result.id.in_(fixed_hp_resultids))}
    F1_Score = {result.dataset_id:result.details.F1_Score for result in Result.query.filter(Result.id.in_(fixed_hp_resultids))}
    Metadata_values=  [item.__dict__ for item in
                     Metadata.query.filter(
                         Metadata.Dataset_id.in_(
                             [result.dataset_id for result in
                              Result.query.filter(
                                  Result.id.in_(fixed_hp_resultids))]))]
    for item in Metadata_values:
        iterable_list.append((item,Accuracies[item['Dataset_id']],F1_Score[item['Dataset_id']]))
    for col in Metadata_values[0]:
        if col[0] != '_' and not('id' in col.lower()):
            try:
                correlation_acc = stats.pearsonr([val[1] for val in iterable_list],[val[0][col] for val in iterable_list])[0]
                correlation_f1 = stats.pearsonr([val[2] for val in iterable_list],[val[0][col] for val in iterable_list])[0]
                if not(math.isnan(correlation_acc) or math.isnan(correlation_f1)):
                    metric_list.append(Insight(col,'Correlation',correlation_acc,correlation_f1))
            except:
                continue
        metric_list.sort(key=lambda x: abs(x.value_acc), reverse=True)
        # cols = [(table, col, [val[0] for (val) in db.session.query(colobj).distinct().all()])for (table, tblobj) in list(
        #         db.metadata.tables.items()) if '_py' in table for (col, colobj) in tblobj.columns.items()]
    return render_template('insights.html',list=metric_list,selected_clf='KNN')

@app.route("/analytics-sweep")
def sweep():
    fixed_hp_resultids = [(result.resultid,result.K) for result in \
        db.session.query(db.metadata.tables['KNN_py'])\
            .filter_by(weights='uniform')
            .filter_by(algorithm='auto')]
    global iterable_list
    iterable_list = []
    metric_list = []
    Accuracies = {result.dataset_id:result.details.Accuracy for result in Result.query.filter(Result.id.in_([i[1] for i in fixed_hp_resultids ]))}
    F1_Score = {result.dataset_id:result.details.F1_Score for result in Result.query.filter(Result.id.in_([i[1] for i in fixed_hp_resultids ]))}
    Metadata_values=  [item.__dict__ for item in
                     Metadata.query.filter(
                         Metadata.Dataset_id.in_(
                             [result.dataset_id for result in
                              Result.query.filter(
                                  Result.id.in_([i[1] for i in fixed_hp_resultids ]))]))]
    
    

# @app.route("/analytics-hp", methods=['POST'])
# def analytics_hp():
#     global iterable_list
#     fixed_hp_resultids = []
#     flag = False
#     session = scoped_session(sessionmaker(bind=db.get_engine()))()
#     #tblobj = db.metadata.tables[str(request.form.get('clf')).strip()+'_py']
#     tblobj = db.metadata.tables['KNN_py']
#     data = request.form.get('form_data').split(';')
#     param_dictionary = {}
#     for condition in data:
#         if not 'csrf' in condition:
#             if 'true' in condition:
#                 [_, hp_val] = condition.split(',')
#                 [param, val] = hp_val.split(':')
#                 param = param.replace('select', '')
#                 if fixed_hp_resultids:
#                     fixed_hp_resultids = list(set(fixed_hp_resultids).intersection(set([result.resultid for result in \
#                     db.session.query(db.metadata.tables['KNN_py'])\
#                         .filter_by(**{param:val})])))
#                 param_dictionary.update({param:val})

#     for {k,v} in param_dictionary:
#         fixed_hp_resultids = [result.resultid for result in \
#                     db.session.query(db.metadata.tables['KNN_py'])\
#                         .filter_by(**{param:val})]
#     Accuracies = {result.dataset_id:result.details.Accuracy for result in Result.query.filter(Result.id.in_(fixed_hp_resultids))}
#     F1_Score = {result.dataset_id:result.details.F1_Score for result in Result.query.filter(Result.id.in_(fixed_hp_resultids))}
#     for col in Metadata_values[0]:
#         if col[0] != '_' and not('id' in col.lower()):
#             try:
#                 correlation_acc = stats.pearsonr([val[1] for val in iterable_list],[val[0][col] for val in iterable_list])[0]
#                 correlation_f1 = stats.pearsonr([val[2] for val in iterable_list],[val[0][col] for val in iterable_list])[0]
#                 if not(math.isnan(correlation_acc) or math.isnan(correlation_f1)):
#                     metric_list.append(Insight(col,'Correlation',correlation_acc,correlation_f1))
#             except:
#                 continue
#         metric_list.sort(key=lambda x: abs(x.value_acc), reverse=True)
#         cols = [(table, col, [val[0] for (val) in db.session.query(colobj).distinct().all()])for (table, tblobj) in list(
#                 db.metadata.tables.items()) if '_py' in table for (col, colobj) in tblobj.columns.items()]
#         return jsonify(data=render_template('insight-response.html',list=metric_list, cols=cols,selected_clf='KNN'))

@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    results = Result.query.order_by(
        Result.date_posted.desc()).paginate(page=page, per_page=4)
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


@app.route("/dropdown-list/process", methods=['GET','POST'])
def searchlist_process():
    process = request.form.get('selected_process')
    data = request.form.get('selected_data')
    print(data)
    search = SearchForm()
    search.Process.choices = [(r.process, str(r.process))
                              for r in db.session.query(Result.process).distinct()]
    search.Task.choices = [(r.task, str(r.task))
                           for r in db.session.query(Result.task).filter_by(process=process).distinct()]
    search.Platform.choices = [(r.platform, str(r.platform))
                               for r in db.session.query(Result.platform).filter_by(process=process).distinct()]
    search.Dataset.choices = [(r.dataset_id, str(Dataset.query.filter_by(id=r.dataset_id).first()
                                                 .dataset_name)) for r in db.session.query(Result.dataset_id).filter_by(process=process).distinct()]
    search.Process.default = process

    search.process()
    return jsonify(data=render_template('dynamic-search.html',form=search))

@app.route("/dropdown-list/platform")
def searchlist_platform():
    platform = request.form.get('platform')
    search = SearchForm()
    search.Platform.choices = [(r.platform, str(r.platform))
                               for r in db.session.query(Result.platform).distinct()]
    search.Task.choices = [(r.task, str(r.task))
                           for r in db.session.query(Result.task).filter_by(platform=platform).distinct()]
    search.Process.choices = [(r.process, str(r.process))
                              for r in db.session.query(Result.process).filter_by(platform=platform).distinct()]
    search.Dataset.choices = [(r.dataset_id, str(Dataset.query.filter_by(id=r.dataset_id).first()
                                                 .dataset_name)) for r in db.session.query(Result.dataset_id).filter_by(platform=platform).distinct()]
    return jsonify(data=render_template('dynamic-search.html',form=search))

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
        Result.date_posted.desc())
    results1 = results.paginate(page=page, per_page=4)
    count = results.count()

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

        return Analytics

    Analytics = getdatasetAnalytics()

    return render_template('task.html', title='Task', task=task, results=results1, count=count, analytics=Analytics)


@app.route("/process/<string:process>")
def process(process):
    page = request.args.get('page', 1, type=int)
    results = Result.query.filter_by(process=process).order_by(
        Result.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template('process.html', title='Process', process=process, results=results)


@app.route("/platform/<string:platform>")
def ML_platform(platform):
    page = request.args.get('page', 1, type=int)
    results = Result.query.filter_by(platform=platform).order_by(
        Result.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template('platform.html', title='Language', platform=platform, results=results)


@app.route("/dataset/<string:dataset>")
def ML_dataset(dataset):
    page = request.args.get('page', 1, type=int)
    results = Result.query.filter_by(dataset_id=dataset).order_by(
        Result.date_posted.desc())
    results_paginated = results.paginate(page=page, per_page=4)
    dataset = Dataset.query.filter_by(
        id=dataset).first_or_404()
    results_count = results.count()

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

    return render_template('dataset.html', title='Language', dataset=dataset, results=results_paginated, analytics=Analytics, count=results_count)


@app.route("/datagraph", methods=["GET"])
def plotView():
    data = []
    dataset = request.args.get('dataset', 1, type=int)
    results = Result.query.filter_by(dataset_id=dataset)
    Tasks = [r.task for r in db.session.query(Result.task).distinct()]
    for task in Tasks:
        results1 = results.filter_by(task=task)
        data.append([result.details.Accuracy*100 for result in results1])
    fig, axis1 = plt.subplots()
    axis1.set_title('Task wise results')
    axis1.set_ylabel('Accuracy')
    axis1.set_xticklabels(Tasks)
    axis1.boxplot(data)
    plt.show()
    return {'status': 200}
