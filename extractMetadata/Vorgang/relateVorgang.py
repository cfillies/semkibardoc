import sys,os
pathThisFile=sys.path[0]

import json

import Vorgang.getVorgang as gVorgang
findVorgang= gVorgang.findVorgang

def rep(x):
    return str(x).replace('{','').replace('}','').replace('[','').replace(']','').replace('\"','').replace('\'','')

def updatedResult(oldResult,newResult):
    for key in oldResult['Ergebnis']:
        oldResult['Ergebnis'][key]=oldResult['Ergebnis'][key]+newResult['Ergebnis'][key]
    for filePath in newResult['Gesamt-Zuordnung'].keys():
        oldResult['Gesamt-Zuordnung'].setdefault(filePath,{}).update(newResult['Gesamt-Zuordnung'][filePath])
        oldResult['Keine-Zuordnung'].setdefault(filePath,{}).update(newResult['Keine-Zuordnung'][filePath])
        oldResult['Informelles-Format'].setdefault(filePath,[]).extend(newResult['Informelles-Format'][filePath])
        oldResult['Fehler'].setdefault(filePath,[]).extend(newResult['Fehler'][filePath])
    return oldResult

def save(filePath,considerDocName,newResult):
    if considerDocName==True:
        name=pathThisFile+'\\outputResult\\'+'result-docName.json'            
    else:
        name=pathThisFile+'\\outputResult\\'+'result-NodocName.json'    
    ###########################################
    if not os.path.isfile(name):#create json-result file
        with open(name,'w') as fp:
            json.dump(newResult, fp,  indent=4,ensure_ascii=False)
            #print('resultFile0',newResult)
    else:#update the json-result file
        with open(name,'r') as fp:
            resultFile = json.load(fp)
        finalResult=updatedResult(resultFile,newResult)
        with open(name,'w') as f:
            json.dump(finalResult, f,  indent=4,ensure_ascii=False)
            
def allVorgang(file,filePath,considerDocName,methode, docxVorhanden):
    resultAll=findVorgang(file, filePath, considerDocName,methode, docxVorhanden).all
    #print('resultAll:',resultAll)
    save(filePath,considerDocName,resultAll)
    return resultAll

def vorgang(filePath,files,considerDocName,methode,docxVorhanden):
    if type(files)!=list:
        files=[files]
    alle=allVorgang(files,filePath,considerDocName,methode,docxVorhanden)
    zuordnung=alle['Gesamt-Zuordnung']
    keineZuordnung=alle['Keine-Zuordnung']
    informellesFormat=alle['Informelles-Format'] 
    fehler=alle['Fehler']
    ###############################################
    result={}
    result[filePath]={}
    ###############################################
    for f in files:
        result[filePath][f]={}
        if f in zuordnung[filePath].keys():
            vResult=rep(list(zuordnung[filePath][f].keys()))
        elif f in keineZuordnung[filePath].keys():
            vResult='Keine Kategorie gefunden'
        elif f in informellesFormat[filePath]:
            vResult='Informelles Format'
        elif f in fehler[filePath]:
            vResult='Fehler in der Datei'
        else:
            vResult='Fehler in der Datei'
        result[filePath][f]['vorgang']=vResult
    return result
