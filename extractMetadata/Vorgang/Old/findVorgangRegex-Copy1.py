# coding: utf-8
import re

# Check regex: https://pythex.org/

def compiler(patList,notPatList):
    #########positive matching elements
    pattern='.*$'
    for pat in patList:
        pattern='(?=.*('+pat+'))'+pattern
    #########negativ matching elements'
    temp_notPattern=''
    for pat in notPatList:
        pattern='^(?!.*'+pat+')'+pattern
        temp_notPattern=temp_notPattern+pat+'|'
    notPattern='(?=.*('+temp_notPattern+'kjcebjkw'+'))'+'.*$'
    ########compile
    compiling = re.compile(pattern)
    notCompiling = re.compile(notPattern)
    return compiling,notCompiling

def findAll(patList,txt):
    #########positive matching elements
    find=[]
    for pat in patList:
        match=re.findall(pat,txt)
        if match:
            if type(match[0])==tuple:
                find.extend(list(match))
            else:
                find.append(match[0])
    return list(filter(None,find))
###########################################################
##################################pattern for "Genehmigung"
d='[denkmal]*[schutz]*[gerechten]*[geschützen]*[rechtliche[rn]*]*'
g_patList = ['[dD]+enkmal[en]*[schutz]*[gerechten]*[geschützen]*[rechtliche[rn]*]*|[§]\s*11|Paragraph\s*11|Genehmigung|Bescheid|Maßnahme|Instandsetzung|Auflage|keiner\s'+d+'\sGenehmigung|keine\s'+d+'\sGenehmigung.+nötig','keiner\s'+d+'\sGenehmigung|keine\s'+d+'\sGenehmigung.+nötig|[zZ]u[ge]*stim[^ ]*|bestäti[^ ]*|erteil[^ ]*|angenommen|annehmen|genehmig[^ ]*|gewähr[^ ]*']
g_not_patList=['[kK]eine[n]*\s[dD]+enkmal[en]*[schutz]*[gerechten]*[geschützen]*[rechtliche[n]*]*','Anhörung', 'Versagung', '[kK]eine\sGenehmigung','[kK]eine\sZustimmung','nicht\serteilt','nicht\serteilen','nicht\sgenehmigt','nicht\sangenommen','versagt','versagen','abgelehnt','ablehnen','§\s28\sVwVfG','14\sTagen|zwei\sWochen|2\sWochen','Baugenehmigungsverfahren','Unterlage[n]*[^.][nach]*[ein]*[zu]*reichen','fehlend[e]*[r]*[n]*\sUnterlage[n]*','nicht\sausreichend[e]*[r]*[n]*\sUnterlage[n]*','[Unterlage[n]*]*[^.]+nicht\sausreichend', 'bauordnungsrechtlich','Kein\sRechtsbehelfsbelehrung','FORMCHECKBOX','Prüfung\smit\sMitzeichnung\sdurch\sLDA']
genehmigung=compiler(g_patList,g_not_patList)[0]
notGenehmigung=compiler(g_patList,g_not_patList)[1]
####################################pattern for 'Nachforderung'
n_patList=['Unterlage[n]*[^.][nach]*[ein]*[zu]*reichen|fehlend[e]*[r]*[n]*\sUnterlage[n]*|nicht\sausreichend[e]*[r]*[n]*\sUnterlage[n]*|[Unterlage[n]*]*[^.]+nicht\sausreichend']
n_not_patList=['Baugenehmigungsverfahren','[bB]auordnungsrechtlich','[kK]ein[e]*\sRechtsbehelfsbelehrung','Prüfung\smit\sMitzeichnung\sdurch\sLDA','Versagung', 'Anhörung']
nachforderung=compiler(n_patList,n_not_patList)[0]
notNachforderung=compiler(n_patList,n_not_patList)[1]
####################################pattern for 'Eingangbestaetigung'
e_patList=['bestätig[^.]+Eingang|Eingangsbestätigung']
e_not_patList=['Baugenehmigungsverfahren','[bB]auordnungsrechtlich','[kK]ein[e]*\sRechtsbehelfsbelehrung','Prüfung\smit\sMitzeichnung\sdurch\sLDA','Versagung', 'Anhörung','Unterlage[n]*[^.][nach]*[ein]*[zu]*reichen','fehlend[e]*[r]*[n]*\sUnterlage[n]*','nicht\sausreichend[e]*[r]*[n]*\sUnterlage[n]*','[Unterlage[n]*]*[^.]+nicht\sausreichend']
eingang=compiler(e_patList,e_not_patList)[0]
notEingang=compiler(e_patList,e_not_patList)[1]
####################################pattern for 'Anhoerung'
a_patList=['Anhörung\svor\sVersagung|Anhörung|§\s*28\s*VwVfG|14\sTage|zwei\sWochen|2\sWochen','14\sTage|zwei\sWochen|2\sWochen|Versagung|Ablehnung|[kK]eine\sZustim[^ ]*|nicht\sgenehmig[^ ]*|nicht\san[ge]*n[^ ]*|nicht\s[zu ]*gewähr[^ ]*|anhören|versag[^ ]*|ab[ge]*lehn[^ ]*|entgegensteh[^ ]*|nicht\serteil[^ ]*|nicht\szu[ge]*stimm[^ ]*']
a_not_patList=['Baugenehmigungsverfahren','[bB]auordnungsrechtlich','[kK]ein[e]*\sRechtsbehelfsbelehrung','FORMCHECKBOX','Prüfung\smit\sMitzeichnung\sdurch\sLDA']
anhoerung=compiler(a_patList,a_not_patList)[0]
notAnhoerung=compiler(a_patList,a_not_patList)[1]
####################################pattern for 'Versagung'
v_patList=['[dD]+enkmal[en]*[schutz]*[gerechten]*[geschützen]*[rechtliche[rn]*]*\sVersagung|Begründung\sder\sVersagung|Versagung|Ablehnung|[kK]eine\sZustim[^ ]*|kein[en]*\s[dD]+enkmal[en]*[schutz]*[gerechten]*[geschützen]*[rechtliche[rn]*]*|nicht\sgenehmig[^ ]*|nicht\szu\sgewähren','nicht\sgenehmig[^ ]*|nicht\s[zu ]*gewähren|versag[^ ]*|ab[ge]*lehn[^ ]*|entgegensteh[^ ]*|nicht\serteil[^ ]*|nicht\szugestim[^ ]*|nicht\san[ge]*n[^ ]*']
v_not_patList=['Anhörung','Auflage','14\sTage|zwei\sWochen|2\sWochen','Baugenehmigungsverfahren', 'bauordnungsrechtlich','[kK]ein\sRechtsbehelfsbelehrung','FORMCHECKBOX','Prüfung\smit\sMitzeichnung\sdurch\sLDA']
versagung=compiler(v_patList,v_not_patList)[0]
notVersagung=compiler(v_patList,v_not_patList)[1]
####################################pattern for 'Baugenehmigungsverfahren'
b_patList=['Bau[genehmigungs]*verfahren|Bauvorhaben|Bauvorlage|Bauabnahme|Bauausführung|Bauherr|[bB]auordnungsrechtlich[en]*|Genehmigungsverfahren|Anlage\szur\sBaugenehmigung[sverfahren]*|[kK]ein[e]*\sRechtsbehelfsbelehrung|Anlage\szur\sGenehmigung']
b_not_patList=['Anhörung','14\sTage|zwei\sWochen|2\sWochen','Versagung','FORMCHECKBOX','Prüfung\smit\sMitzeichnung\sdurch\sLDA']
bauverfahren=compiler(b_patList,b_not_patList)[0]
notBauverfahren=compiler(b_patList,b_not_patList)[1]
####################################pattern for Antrag
at_patList=['FORMCHECKBOX|Prüfung\smit\sMitzeichnung\sdurch\sLDA']
at_not_patList=['kwfjdwe']
antrag=compiler(at_patList,at_not_patList)[0]
notAntrag=compiler(at_patList,at_not_patList)[1]
###########################################################

vorgang_type = {
  "Genehmigung"           : genehmigung,
  "Anhörung"              : anhoerung,
  "Versagung"             : versagung,
  "Bauverfahren"          : bauverfahren,
  "Antrag"                : antrag,
  "Nachforderung"         : nachforderung,
  "Eingang"               : eingang
}

not_vorgang_type = {
    'Nicht-Genehmigung'   : notGenehmigung,
    'Nicht-Anhörung'      : notAnhoerung,
    'Nicht-Versagung'     : notVersagung,
    'Nicht-Bauverfahren'  : notBauverfahren,
    'Nicht-Antrag'        : notAntrag,
    "Nicht-Nachforderung" : notNachforderung,
    "Nicht-Eingang"       : notEingang
}
    
class findVorgang:
    def __init__(self, text=""):
        #######################################remove unecessary spaces
        text = text.replace("\n", " ")
        text=' '.join(text.split())
        self.text = text
        #######################################
        self.genehmigung=genehmigung.findall(self.text)
        self.allGenehmigung=findAll(g_patList,self.text)
        self.notGenehmigung=notGenehmigung.findall(self.text)
        self.allNotGenehmigung=findAll(g_not_patList,self.text)
        #######################################
        self.anhoerung=anhoerung.findall(self.text)
        self.allAnhoerung=findAll(a_patList,self.text)
        self.notAnhoerung=notAnhoerung.findall(self.text)
        self.allNotAnhoerung=findAll(a_not_patList,self.text)
        #######################################
        self.versagung=versagung.findall(self.text)
        self.allVersagung=findAll(v_patList,self.text)
        self.notVersagung=notVersagung.findall(self.text)
        self.allNotVersagung=findAll(v_not_patList,self.text)
        #######################################
        self.bauverfahren=bauverfahren.findall(self.text)
        self.allBauverfahren=findAll(b_patList,self.text)
        self.notBauverfahren=notBauverfahren.findall(self.text)
        self.allNotBauverfahren=findAll(b_not_patList,self.text)
        #######################################
        self.antrag=antrag.findall(self.text)
        self.allAntrag=findAll(at_patList,self.text)
        self.notAntrag=notAntrag.findall(self.text)
        self.allNotAntrag=findAll(at_not_patList,self.text)
        #######################################
        self.nachforderung=nachforderung.findall(self.text)
        self.allNachforderung=findAll(n_patList,self.text)
        self.notNachforderung=notNachforderung.findall(self.text)
        self.allNotNachforderung=findAll(n_not_patList,self.text)
        #######################################
        self.eingang=eingang.findall(self.text)
        self.allEingang=findAll(e_patList,self.text)
        self.notEingang=notEingang.findall(self.text)
        self.allNotEingang=findAll(e_not_patList,self.text)
        #######################################
        self.allList={
            'Genehmigung':self.allGenehmigung,
            'Anhoerung':self.allAnhoerung,
            'Versagung':self.allVersagung,
            'Bauverfahren':self.allBauverfahren,
            'Antrag':self.allAntrag,
            'Nachforderung':self.allNachforderung,
            'Eingang':self.allEingang
        }
        #######################################
        self.allNotList={
            'Nicht-Genehmigung':self.allNotGenehmigung,
            'Nicht-Anhoerung':self.allNotAnhoerung,
            'Nicht-Versagung':self.allNotVersagung,
            'Nicht-Bauverfahren':self.allNotBauverfahren,
            'Nicht-Antrag':self.allNotAntrag,
            'Nicht-Nachforderung':self.allNotNachforderung,
            'Nicht-Eingang':self.allNotEingang
        }
    #######################################
    def all(self):
        self.all = {}
        for k, v in list(vorgang_type.items()):
            match=v.findall(self.text)
            if match:
                if type(match[0])==tuple:
                    self.all[k]=list(filter(None, list(match[0])))
                else:
                    self.all[k]=[match[0]]
        return self.all
    #######################################
    def negativAll(self):
        self.negativAll = {}
        for k, v in list(not_vorgang_type.items()):
            match=v.findall(self.text)
            if match:
                if type(match[0])==tuple:
                    self.negativAll[k]=list(filter(None, list(match[0])))
                else:
                    self.negativAll[k]=[match[0]]
        return self.negativAll
    
    #######################################
    def posAllList(self):
        self.posAllList = {'all':[]}
        for k,v in list(self.allList.items()):
            if v:
                self.posAllList[k]=v
                self.posAllList['all'].extend(v)
        self.posAllList['all']=list(set(list(self.posAllList['all'])))
        return self.posAllList
    ######################################
    def negativAllList(self):
        self.negativAllList = {'all':[]}
        for k,v in list(self.allNotList.items()):
            if v:
                self.negativAllList[k]=v
                self.negativAllList['all'].extend(v)
        self.negativAllList['all']=list(set(list(self.negativAllList['all'])))
        return self.negativAllList
    #######################################