from Svalbard import app, db, InjectFromCSV, sqltables, InjectData, SQLfns

import csv

if __name__ == '__main__':
    # db.drop_all()
    # db.create_all()
    # #InjectFromCSV.inject_data(5)
    # #sqltables.create()
    # DR1 = csv.DictReader(open('Svalbard/csv/results.csv', 'r'))
    # DR2 = csv.DictReader(open('Svalbard/csv/MetaData.csv', 'r'))
    # DR3 = csv.DictReader(open('Svalbard/csv/Data.csv', 'r'))
    # DR4 = csv.DictReader(open('Svalbard/csv/KNN.csv', 'r'))
    # for row in DR3:
    #     Data = {}
    #     Data.update({'csv_link':row['csv_url']})
    #     Data.update({'fID':row['Metadata']})
    #     Data.update({'dataset_name':row['Filename']})
    #     Data.update({'tablename':'dataset'})
    #     InjectData.inject(Data)

    # for row in DR2:
    #     row.update({'tablename': 'metadata'})
    #     row =dict(zip(row.keys(), map(SQLfns.str2sqltype, row.values())))
    #     row.update({'Dataset_id':SQLfns.getdatasetid(row['fID'])})
    #     del row['fID']
    #     InjectData.inject(row)
    
    # clf_list = ['KNN','MLP','RF','QDA','GNB','ABC']
    # #clf_list = ['KNN']
    # for clf in clf_list:
    #     DR = csv.DictReader(open(f'Svalbard/csv/{clf}_results.csv', 'r'))
    #     keys = next(csv.DictReader(open(f'Svalbard/csv/{clf}.csv', 'r'))).keys()
    #     for row in DR:            
    #         data3 = {}
    #         data3.update({'tablename':'metrics'})
    #         data3.update({'Accuracy':row['Accuracy']})
    #         data3.update({'Precision':row['Precision']})
    #         data3.update({'F1_Score':row['F1 Score']})
    #         data3.update({'Recall':row['Recall']})
    #         data3.update({'Time':row['time']})
    #         metricsid = InjectData.inject(data3)
    #         data = {}
    #         data.update({'tablename':'result'})
    #         data.update({'fID':row['fID']})
    #         data.update({'eID':row['eID']})
    #         data.update({'dataset_id':SQLfns.getdatasetid(row['fID'])})
    #         data.update({'task':clf})
    #         data.update({'process':'Classification'})
    #         data.update({'platform':'Python-scikit'})
    #         data.update({'metricsid':metricsid})
    #         resultid = InjectData.inject(data)
    #         data2 = {key:row[key] for key in keys}
    #         data2.update({'tablename':clf+'_py'})
    #         data2.update({'resultid':resultid})
    #         InjectData.inject(data2)

    app.run(debug=True,threaded=False)
