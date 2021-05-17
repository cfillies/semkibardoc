import json
import re
import extractVorgang as eVorgang
import os
#########################
efindVorgang= eVorgang.findVorgang
##########################
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
#print(sys.path[0])
import extractText as eText
##########################
# resultVorgang='resultVorgangAll-NoDocName.json'
# with open(resultVorgang) as f:
#     resultVorgang = json.load(f)
# #########################
def filename_divider(filename):
    fname, fext = os.path.splitext(filename)
    fnameNew = fname.replace(".", " ").replace("_", " ").replace("-", " ").replace("'", " ").replace(","," ")
    return fnameNew

def rep(x):
    return str(x).replace('{','').replace('}','').replace('[','').replace(']','').replace('\"','').replace('\'','')


#########################
#remove manipulating content
def remManContent(inhalt):
    #########################################################################################################stop looking in unnecessary content
    searchAuflage = re.search('Auflage[n]*\sund\sBedingung[en]*|Auflage[n]*[^.]*[:]',inhalt)
    if searchAuflage:
        startInhalt=searchAuflage.span()[1]#[1] damit Auflafe auch im Match berücksichtigt wird.
        inhalt=inhalt[:startInhalt]
    else:
        searchSachverhalt=re.search('Begründung.*Sachverhalt',inhalt)
        if searchSachverhalt:
            startInhalt=searchSachverhalt.span()[0]
            inhalt=inhalt[:startInhalt]
        else:
            searchAusgleich=re.search('Entscheidung\süber\sden\sAusgleich\sin\sGeld',inhalt)
            if searchAusgleich:
                startRemove=searchAusgleich.span()[0]
                inhalt=inhalt[:startRemove]
    #################################################remove "Ausgleich in Geld ist nicht genehmigungsfähig"
    search=re.search('(Ausgleich.+Geld.+gewähren)', inhalt)
    if search:
        startInhalt=search.span()[0]
        stopInhalt=search.span()[1]
        removeInhalt=inhalt[startInhalt:stopInhalt]
        inhalt=inhalt.replace(removeInhalt,'')
    ########################################################################################################
    return inhalt

#reanalyze no matching files
def postProcessNoMatch(noMatchList,matchList):
    #Nicht-Genehmigung means Versagung
    for file,val in list(noMatchList.items()):
        if 'Nicht-Genehmigung' in val.keys():
            matchList[file]={'Versagung': val['Nicht-Genehmigung']}
            del noMatchList[file]
    return noMatchList

#solve uncertain classification
def postProcessMatch(matchList):
    for file,val in  list(matchList.items()):
        if len(val.keys())>1:
            ###Anfrage=question, Nachforderung=claim can contain information about Versagung or Genehmgigung. However, it is still a question or a claim.
            if ('Anfrage' or 'Nachforderung') in val.keys() and len(val.keys())>1:
                for key in list(val.keys()):
                    if key!='Anfrage' and key!='Nachforderung':
                        del matchList[file][key]
            if 'Eingang' in val.keys() and len(val.keys())>1:
                for key in list(val.keys()):
                    if key!='Eingang':
                        del matchList[file][key]
            ###Anhörung includes also Versagung but not reverse
            if len(val.keys())==2 and ('Anhörung' and 'Versagung') in val.keys():
                del matchList[file]['Versagung']
            if len(val.keys())==2 and ('Genehmigung' and 'Versagung') in val.keys():
                del matchList[file]['Genehmigung']
            if len(val.keys())==3 and ('Genehmigung' and 'Versagung' and 'Anhörung') in val.keys():
                del matchList[file]['Genehmigung']
                del matchList[file]['Versagung']
            ###Bauverfahren is relatively uncertain. It appiers mostly with Genehmigung.Genehmigung is more certain
            if 'Bauverfahren' in val.keys():
                del matchList[file]['Bauverfahren']
    return matchList

#give a short summary of the results: amount of each classification, classification of each files
def resultSummary(matchList, noMatchList, wrongFormatList, errorList):
    i=0
    points={'Gesamt-Zuordnung':0,'Informelles-Format':len(wrongFormatList),'Keine-Zuordnung':len(noMatchList.keys()),'Fehler':len(errorList),'Genehmigung':0,'Versagung':0,'Anhörung':0,'Antrag':0,'Anfrage':0,'Nachforderung':0,'Bauverfahren':0,'Eingang':0}
    for k,v in list(matchList.items()):
#         if len(v.keys())>0:
#             i+=1
#             print(i,v,k)
        points['Gesamt-Zuordnung']+=1  
        for key in points.keys():
            if key in v.keys():
                points[key]+=1
    resultDict={}
    resultDict['Ergebnis']=points
    resultDict['Gesamt-Zuordnung']=matchList
    resultDict['Keine-Zuordnung']=noMatchList
    resultDict['Informelles-Format']=wrongFormatList
    resultDict['Fehler']=errorList
    return resultDict

def mainProcess(files,filePath,considerDocName,methode):
    wrongFormatList=[]
    matchList={}
    matc
    noMatchList={}
    errorList=[]
    for i in range(0,len(files)):
        try:
            print(i, files[i])
    #         ########################if file already classified
    #         if files[i] in resultVorgang['Gesamt-Zuordnung'].keys():
    #             matchList[files[i]]=resultVorgang['Gesamt-Zuordnung'][files[i]]
    #             continue
    #         elif files[i] in resultVorgang['Keine-Zuordnung'].keys():
    #             noMatchList[files[i]]=resultVorgang['Keine-Zuordnung'][files[i]]
    #             continue
    #         elif files[i] in resultVorgang['Informelles-Format']:
    #             wrongFormatList.append(files[i])
    #             continue
            ##################################################Begin - Analyse the file name
            if considerDocName and files[i].count(' ')<5:
                if 'anfr' in files[i].lower():
                    matchList[files[i]]={'Anfrage':['Dateiname']}
                    continue
                elif ('anhö' or 'anhoe' or 'anhorung') in files[i].lower():
                    matchList[files[i]]={'Anhörung':['Dateiname']}
                    continue
                elif 'versag' in files[i].lower():
                    matchList[files[i]]={'Versagung':['Dateiname']}
                    continue
                elif 'geneh' in files[i].lower():
                    matchList[files[i]]={'Genehmigung':['Dateiname']}
                    continue
                elif 'zustim' in files[i].lower():
                    matchList[files[i]]={'Genehmigung':['Dateiname']}
                    continue
            ##################################################End - Analyse the file name
            ########################load file
            file_extension = files[i][-3:].lower()      
            ########################find amount of pages
            pages=eText.getPageNumber(filePath,files[i],methode)
            print('pages: ', pages)
            ############################################
            if pages<=15:
                inhalt =eText.getInhalt(filePath,files[i],methode)
            else:#if it includes more pages than 15 than --> remove from analyse
                wrongFormatList.append(files[i])
                print("File is too long for Behördendokument:", files[i])
                continue
            ############################################
            if inhalt == None or inhalt =='':
                    print("File does not contain any text data:", files[i])
                    wrongFormatList.append(files[i])
                    continue
            ##################################################remove unecessary spaces
            inhalt = inhalt + ' ' + filename_divider(files[i])
            inhalt = inhalt.replace("\n", " ")
            inhalt=' '.join(inhalt.split())
            ##################################################Begin - look for the required format
            if 'FORMCHECKBOX' in inhalt:
                matchList[files[i]]={'Antrag':['FORMCHECKBOX']}
                continue
            elif 'GeschZ' not in inhalt:
                ############################################
                if pages<=5:
                    matchAnfrage=efindVorgang(inhalt).anfrage
                    if matchAnfrage:#Dokumente die kein GeschZ enthalten, können auch Anfragen sein.
                        matchList[files[i]]={'Anfrage':matchAnfrage}
                    else:
                        #print('File does not corresponed to the required format')
                        wrongFormatList.append(files[i])
                else:
                    #print('File does not corresponed to the required format')
                    wrongFormatList.append(files[i])
                continue
            ##################################################End-look for the required format
            else:
                ###########################remove manipulating content
                inhalt=remManContent(inhalt)
                ###########################
                match=efindVorgang(inhalt).all()
                if match:
                    matchList[files[i]]=match
                    print('match: ',match)
                else:
                    noMatch=efindVorgang(inhalt).negativAllList()
                    noMatchList[files[i]]=noMatch
                    print('noMatch: ', noMatch)
            #print(i, files[i])
        except:
            errorList.append(files[i])
    #end preprocessing
    ##############################################
    matchList = postProcessMatch(matchList)
    noMatchList = postProcessNoMatch(noMatchList,matchList)
    wrongFormatList = wrongFormatList
    errorList = errorList
    ##############################################
    return resultSummary(matchList, noMatchList, wrongFormatList, errorList)

#########################
class findVorgang:
    def __init__(self, files,path,considerDocName,methode):
        if type(files)!=list:
            self.files=[files]
        else:
            self.files=files
        self.filePath=path
        self.considerDocName=considerDocName
        self.methode=methode
        ###############################################
        #self.files=[path+'\\'+self.fileName[i] for i in range(len(self.fileName))]
        ###############################################
        self.all=mainProcess(self.files,self.filePath,self.considerDocName,self.methode)
        self.ergebnis=self.all['Ergebnis']
        self.zuordnung=self.all['Gesamt-Zuordnung']
        self.keineZuordnung=self.all['Keine-Zuordnung']
        self.informellesFormat=self.all['Informelles-Format'] 
        self.fehler=self.all['Fehler']
        ###############################################
        self.result={}
        self.result[self.filePath]={}
        ###############################################
        for f in self.files:
            self.result[self.filePath][f]={}
            if f in self.zuordnung.keys():
                vResult=rep(list(self.zuordnung[f].keys()))
            elif f in self.keineZuordnung.keys():
                vResult='Keine Kategorie gefunden'
            elif f in self.informellesFormat:
                vResult='Informelles Format'
            elif f in self.fehler:
                vResult='Fehler in der Datei'
            else:
                vResult='Fehler in der Datei'
            self.result[self.filePath][f]['Vorgang']=vResult
        #print(f,' --- ',self.result[f])

        