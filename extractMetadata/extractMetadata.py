# import json
from pathlib import Path

import Adresse.relateAdresse as relateAdresse
# import Objnr.getObjnr as getObjnr
import Objnr.relateObjnr as relateObjnr
# import extract.extractDatum as extractDatum
import extract.extractText as extractText
import Vorgang.relateVorgang as relateVorgang
import Vorhaben.relateVorhaben as relateVorhaben
import Misc.helpers as helpers
import Datum.relateDatum as relateDatum

print('Tika runs on Docker container, make sure it is activated (on "http://localhost:9998/tika)!')

# Einlesen der Input-Daten
input_file = open(r'extractMetadata\Input\input.txt', "r", encoding='utf-8')
content = input_file.read()
inputdata = content.split("\n")
input_file.close()

datei = inputdata[1]
dateidir = inputdata[3]
ordnerStruktur = inputdata[5] # r"C:\Users\schull\Projekte\KIbarDok\bu\ordnerStrukturTreptow.json"
results_path = Path(inputdata[7])
metadataToExtract = inputdata[9].split(', ')

if ordnerStruktur[0:4] == 'Dict':
    pfad, \
    hoechsterPfad, \
    reversedDictionary, \
    directories = helpers.getDirectory(datei, ordnerStruktur)
else:
    pfad = dateidir
    hoechsterPfad = ordnerStruktur
    ordnerStruktur = []
    


objnr = []
adresse = []
adressen = []
denkmalname = []
sachbegriff = []
objnrMethode = []
behoerde = []
vorhaben = []
vorhabenScore = ''
vorgang = ''
inhalt = ''
daten = []
adrDict = {}

metadata = {pfad: {datei: {'objnr': objnr, 'adresse': adresse, 'denkmalname': denkmalname, 'sachbegriff': sachbegriff, \
                                'objnrMethode': objnrMethode, 'behoerde': behoerde, 'vorhaben': vorhaben, 'vorhabenScore': vorhabenScore, \
                                'vorgang': vorgang, 'daten': daten, 'inhalt': inhalt, 'adrDict': adrDict, 'pfadAktuell': dateidir}}}


parser = 'tika' # 'docx'
for item in metadataToExtract:
    print(item)
    if item == 'inhalt':
        # Inhalt extrahieren
        content: any = extractText.getTextContent(metadata, parser)
        metadata[pfad][datei]['inhalt'] = content
    if item == 'adresse':
        # Adresse identifizieren
        metadata[pfad][datei]['adrDict'], \
        metadata[pfad][datei]['adresse'], adrName = relateAdresse.findAddress(metadata, parser)

    if item == 'objnr':
        # Objektnummer identifizieren
        metadata[pfad][datei]['objnr'], \
        metadata[pfad][datei]['behoerde'], \
        metadata[pfad][datei]['objnrMethode'] = relateObjnr.relateObjnr(metadata, parser)

    if item == 'daten':        
        # Daten identifizieren
        metadata[pfad][datei]['daten'] = relateDatum.datum(metadata, parser)

    if item == 'sachbegriff':
        # Sachbegriffe zum Denkmalobjekt
        metadata[pfad][datei]['sachbegriff'] = relateObjnr.getSachbegriff(metadata, parser)

    if item == 'denkmalname':
        # Denkmalname zum Denkmalobjekt
        metadata[pfad][datei]['denkmalname'] = relateObjnr.getDenkmalname(metadata, parser)

    if item == 'vorhaben':
        # Vorhaben identifizieren
        if ordnerStruktur[0:4] == 'Dict':
            metadata[pfad][datei]['vorhaben'], \
            metadata[pfad][datei]['vorhabenScore'] = relateVorhaben.vorhaben(metadata, directories, ordnerStruktur, parser)
        else:            
            metadata[pfad][datei]['vorhaben'], \
            metadata[pfad][datei]['vorhabenScore'] = relateVorhaben.vorhaben(metadata, hoechsterPfad, ordnerStruktur, parser)

    if item == 'vorgang':
        # Vorgang identifizieren
        metadata[pfad][datei]['vorgang'] = relateVorgang.vorgang(pfad,datei,True,parser,True)[pfad][datei]['vorgang']
        
        

# Save metadata (increments json-file)
helpers.saveMetadata(metadata, results_path)