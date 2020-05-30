from Svalbard.models import Dataset, Result

def getdatasetid(fID):
    return Dataset.query.filter_by(fID=fID).first().id

def str2sqltype(n):
    try:
        a = eval(n)
        return a
    except :
        return n

def getresultid(eID):
    return Result.query.filter_by(eID=eID).first().id
