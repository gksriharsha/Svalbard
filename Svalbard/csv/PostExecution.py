import pandas

KNN = pandas.read_csv('KNN.csv')

MLP = pandas.read_csv('MLP.csv')

QDA = pandas.read_csv('QDA.csv')

RF = pandas.read_csv('RF.csv')

GNB = pandas.read_csv('GNB.csv')

ABC = pandas.read_csv('ABC.csv')

results = pandas.read_csv('results.csv')

results1 = pandas.merge(KNN,results,on='eID',how='left')

results2 = pandas.merge(MLP,results,on='eID',how='left')

results3 = pandas.merge(QDA,results,on='eID',how='left')

results4 = pandas.merge(RF,results,on='eID',how='left')

results5 = pandas.merge(GNB,results,on='eID',how='left')

results6 = pandas.merge(ABC,results,on='eID',how='left')

results6.to_csv('ABC_results.csv',index=False)

results5.to_csv('GNB_results.csv',index=False)
results4.to_csv('RF_results.csv',index=False)
results3.to_csv('QDA_results.csv',index=False)
results2.to_csv('MLP_results.csv',index=False)
results1.to_csv('KNN_results.csv',index=False)