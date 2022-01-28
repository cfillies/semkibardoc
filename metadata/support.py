from pymongo.collection import Collection

log = []
def resetLog(): 
    global log
    log=[]

def logEntry(entry: any): 
    global log
    log[:0] = [entry]
    if len(log)>100:
        del log[100:]
    print(entry)
    
def getLog(top): 
    global log
    l = {}
    if log==[]:
        return {}
    t = []+log[:top]
    for i in range(0, top):
        l[str(i)]=t[i]
    return l

def initDocumentPattern(col: Collection):
    document_pattern = {}
    d = '[denkmal]*[schutz]*[gerechten]*[geschützen]*[rechtliche[rn]*]*'
    no = '(?<!nicht)\s'
    # Treffer
    g_patList = [d+'\sGenehmigung|[§]\s*11|Paragraph\s*11|Genehmigung|Bescheid|Maßnahme|Instandsetzung|Auflage[n]*[^\w]|keiner\s'+d+'\sGenehmigung|keine\s'+d+'\sGenehmigung.+nötig', 'keiner\s'+d +
                '\sGenehmigung|keine\s'+d+'\sGenehmigung.+nötig|'+no+'[zZ]u[ge]*stim[^ ]*|'+no+'[bB]+estäti[^ ]*|'+no+'erteil[^ ]*|'+no+'angenommen|'+no+'annehmen|'+no+'genehmig[t]*[en]*|'+no+'[zu\s]*gewähr[t]*[en]*']

    document_pattern["Genehmigung"] = {
        "file": ['geneh', 'zustim'],
        "pos": g_patList,
        "neg": ['[kK]eine[n]*\s[dD]+enkmal[en]*[schutz]*[gerechten]*[geschützen]*[rechtliche[n]*]*', 'Anhörung', 'Versagung', '[kK]eine\sGenehmigung', '[kK]eine\sZustimmung', '[kK]eine\s[bB]+estäti[^ ]*', 'versagt', 'versagen', 'abgelehnt', 'ablehnen', 'zurückgewiesen|zurückzuweisen', '§\s28\sVwVfG', '14\sTagen|zwei\sWochen|2\sWochen', 'Baugenehmigungsverfahren', '[Uu]nterlage[n]*[^.]*[nach]*[ein]*[zu]*reichen', 'fehlend[e]*[r]*[n]*\s[Uu]nterlage[n]*', 'nicht\sausreichend[e]*[r]*[n]*\s[Uu]nterlage[n]*', '[Uu]nterlage[n]*[^.]+nicht\sausreichend', 'unvollständig[e]*[r]*[n]*\s[Uu]+nterlage[n]*', 'bauordnungsrechtlich', 'Kein\sRechtsbehelfsbelehrung', 'FORMCHECKBOX', 'Prüfung\smit\sMitzeichnung\sdurch\sLDA']
    }
    document_pattern["Nachforderung"] = {
        "file": [],
        "pos": ['[Uu]nterlage[n]*[^.]*[un]*[nach]*[ein]*[zu]*reich[^.]*|fehlend[e]*[r]*[n]*\s[Uu]nterlage[n]*|unvollständig[e]*[r]*[n]*\s[Uu]nterlage[n]*|nicht\sausreichend[e]*[r]*[n]*\s[Uu]nterlage[n]*|[Uu]nterlage[n]*[^.]+nicht\sausreichend|Ergänz[^.]*[Uu]nterlage[n]*|\sum[^.]*Stellung[nahme]*|[Uu]nterlage[^.]*vervollständ[^ ]*|vervollständ[^.]*[uU]nterlage[n]*'],
        "neg": ['Baugenehmigungsverfahren', '[bB]auordnungsrechtlich', '[kK]ein[e]*\sRechtsbehelfsbelehrung', 'Prüfung\smit\sMitzeichnung\sdurch\sLDA', 'Versagung', 'Anhörung']
    }
    document_pattern["Eingang"] = {
        "file": [],
        "pos": ['bestätig[^.]+Eingang|Eingangsbestätigung'],
        "neg": ['Baugenehmigungsverfahren', '[bB]auordnungsrechtlich', '[kK]ein[e]*\sRechtsbehelfsbelehrung', 'Prüfung\smit\sMitzeichnung\sdurch\sLDA', 'Versagung', 'Anhörung', 'Unterlage[n]*[^.][nach]*[ein]*[zu]*reichen', 'fehlend[e]*[r]*[n]*\sUnterlage[n]*', 'nicht\sausreichend[e]*[r]*[n]*\sUnterlage[n]*', '[Unterlage[n]*]*[^.]+nicht\sausreichend']
    }
    document_pattern["Anhörung"] = {
        "file": ['anhö', 'anhoe', 'anhorung'],
        "pos": ['Anhörung\svor\sVersagung|Anhörung|§\s*28\s*VwVfG|14\sTage|zwei\sWochen|2\sWochen', '14\sTage|zwei\sWochen|2\sWochen|Versagung|Ablehnung|[kK]eine\sZustim[^ ]*|nicht\sgenehmig[^ ]*|nicht\san[ge]*n[^ ]*|nicht\s[zu ]*gewähr[^ ]*|anhören|versag[^ ]*|ab[ge]*lehn[^ ]*|entgegensteh[^ ]*|nicht\serteil[^ ]*|nicht\szu[ge]*stimm[^ ]*'],
        "neg": ['Baugenehmigungsverfahren', '[bB]auordnungsrechtlich', '[kK]ein[e]*\sRechtsbehelfsbelehrung', 'FORMCHECKBOX', 'Prüfung\smit\sMitzeichnung\sdurch\sLDA', 'Anhörung[^.]*vom']
    }
    document_pattern["Versagung"] = {
        "file": ['versag', 'versg', 'negativ'],
        "pos": ['[dD]+enkmal[en]*[schutz]*[gerechten]*[geschützen]*[rechtliche[rn]*]*\sVersagung|Begründung\sder\sVersagung|Versagung|Ablehnung|[kK]eine\sZustim[^ ]*|kein[en]*\s[dD]+enkmal[en]*[schutz]*[gerechten]*[geschützen]*[rechtliche[rn]*]*|nicht\sgenehmig[^ ]*|nicht\szu\sgewähren|Wider[^ ]*[^.]*zurück[^ ]*', 'Wider[^ ]*[^.]*zurück[^ ]*|nicht\sgenehmig[^ ]*|nicht\s[zu ]*gewähren|versag[^ ]*|ab[ge]*lehn[^ ]*|entgegensteh[^ ]*|nicht\serteil[^ ]*|nicht\szugestim[^ ]*|nicht\san[ge]*n[^ ]*'],
        "neg": ['Anhörung(?!\svom)|Anhörung\s[zur]*[der]*[\s]*Versagung(?!\svom)', 'Auflage[n]*[^\w]', '14\sTage|zwei\sWochen|2\sWochen', 'Baugenehmigungsverfahren', 'bauordnungsrechtlich', '[kK]ein\sRechtsbehelfsbelehrung', 'FORMCHECKBOX', 'Prüfung\smit\sMitzeichnung\sdurch\sLDA']
    }
    document_pattern["Bauverfahren"] = {
        "file": [],
        "pos": ['Bau[genehmigungs]*verfahren|Bauvorhaben|Bauvorlage|Bauabnahme|Bauausführung|Bauherr|[bB]auordnungsrechtlich[en]*|Genehmigungsverfahren|Anlage\szur\sBaugenehmigung[sverfahren]*|[kK]ein[e]*\sRechtsbehelfsbelehrung|Anlage\szur\sGenehmigung'],
        "neg": ['Anhörung', '14\sTage|zwei\sWochen|2\sWochen', 'Versagung', 'FORMCHECKBOX', 'Prüfung\smit\sMitzeichnung\sdurch\sLDA']
    }
    document_pattern["Antrag"] = {
        "file": [],
        "pos": ['FORMCHECKBOX|Prüfung\smit\sMitzeichnung\sdurch\sLDA'],
        "neg": ['never_ever']
    }
    document_pattern["Anfrage"] = {
        "file": ["anfr"],
        "pos": ['[Be]*[aA]+ntwort[ung]*[^.]*[fF]+rage|Anfrage|Frage[:]|Antwort[:]'],
        "neg": ['never_ever']
    }
    document_pattern["Stellungnahme"] = {
        "file": ["stellung"],
        "pos": ['never_ever'],
        "neg": ['never_ever']
    }
    document_pattern["Kein Denkmal"] = {
        "file": ["kein denkmal"],
        "pos": ['never_ever'],
        "neg": ['never_ever']
    }
    col.delete_many({})

    plist =[]
    for dt in document_pattern:
       le = document_pattern[dt]
       le["name"]=dt
       plist.append(le)
    col.insert_many(plist)

    return document_pattern;

def getDistricts():
    treptow = { "name": "Treptow", 
                "collection": "treptow", 
                "district": "Treptow-Köpenick",
                "folder": "C:\\Data\\test\\KIbarDok\\Treptow\\1_Treptow",
                "folders": "folders",
                "startindex": 0 }
    koepenick = { "name": "Köpenick", 
                "collection": "koepenick", 
                "district": "Treptow-Köpenick",
                "folder": "E:\\2_Köpenick",
                "folders": "koepenick_folders",
                "startindex": 100000 }
    pankow = { "name": "Pankow", 
                "collection": "pankow", 
                "district": "Pankow",
                "folder": "E:\\3_Pankow",
                "folders": "pankow_folders",
                "startindex": 200000 }
    return { "treptow": treptow,
             "koepenick": koepenick,
             "pankow": pankow
             }


def getAuthorities():
    # Dictionary mit allen Denkmalschutzbehörden erstellen
    # aus:
    # https://www.berlin.de/sen/kulteu/denkmal/organisation-des-denkmalschutzes/untere-denkmalschutzbehoerden/
    # https://www.berlin.de/sen/kulteu/denkmal/organisation-des-denkmalschutzes/landesdenkmalrat/
    # https://www.berlin.de/landesdenkmalamt/

    # Form ist Bezirk:Adresse
    return {'Charlottenburg-Wilmersdorf': 'Hohenzollerndamm 174',
            'Friedrichshain-Kreuzberg': 'Yorckstrasse 4',
            'Lichtenberg': 'Alt-Friedrichsfelde 60',
            'Marzahn-Hellersdorf': 'Helene-Weigel-Platz 8',
            'Mitte': 'Müllerstrasse 146',
            'Neukölln': 'Karl-Marx-Strasse 83',
            'Pankow': 'Storkower Strasse 97',
            'Reinickendorf': 'Eichborndamm 215',
            'Spandau': 'Carl-Schurz-Strasse 2',
            'Steglitz-Zehlendorf': 'Kirchstrasse 1',
            'Tempelhof-Schöneberg': 'John-F-Kennedy-Platz',
            'Treptow-Köpenick': 'Alt-Köpenick 21',
            'Oberste Denkmalschutzbehörde': 'Brunnenstrasse 188-190',
            'Oberste Denkmalschutzbehörde': 'Behrenstrasse 42',
            'Landesdenkmalamt': 'Klosterstrasse 47',
            'Senatsverwaltung für Stadtentwicklung und Wohnen': 'Württembergische Strasse 6'
            }

def initSupport(col: Collection, hida_col: Collection, district, streetnames: str):

    # streets = pd.read_csv(r'hidaData.csv', sep='\t', encoding='utf-8', usecols=['denkmalStrasse'])
    # streetsset = set(streets['denkmalStrasse'].tolist())
    # streetsset.remove(np.nan)
    # item = col.find()
    # if not item:
        hidal = hida_col.find({ "Bezirk": district })
        streets = set([])
        for hida in hidal:
            if "AdresseDict" in hida:
                adlist = hida["AdresseDict"]
                streets.update(set(adlist.keys()))
        item = { streetnames: list(streets),
                "authorities": getAuthorities(),
                "districts": getDistricts(),
                "adcache": {}}
        col.delete_many({})
        col.insert_one(item)
