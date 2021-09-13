import json
from pathlib import Path

import Adresse.relateAdresse as relateAdresse
import Objnr.getObjnr as getObjnr
import Objnr.relateObjnr as relateObjnr
import extract.extractDatum as extractDatum
import extract.extractText as extractText
import Vorgang.relateVorgang as relateVorgang
import Vorhaben.relateVorhaben as relateVorhaben
import Datum.relateDatum as relateDatum
from extractMetadata.Misc import helpers

print('Tika runs on Docker container, make sure it is activated (on "http://localhost:9998/tika")')

# Einlesen der Input-Daten
with open(r'Input\input.txt', "r", encoding='utf-8') as input_file:
    content = input_file.read()
    inputdata = content.split("\n")

datei = inputdata[1]
dateidir = inputdata[3]
ordnerStruktur = inputdata[5]  # r"C:\Users\schull\Projekte\KIbarDok\bu\ordnerStrukturTreptow.json"
results_path = Path(inputdata[7])
metadataToExtract = inputdata[9].split(', ')

einleseMethode = 'tika'  # 'docx'

cwd = Path().cwd()
daten_folder = 'Test'
datei = "Geb.A 19_Zustimmg.auf denkmalrechtl.Genehmig..doc"
dir_proj_root = cwd.parent
dir_data = Path(r'C:\Users\koenij\Projekte\KIbarDok\Daten') / daten_folder
path_ordner_struktur_json = cwd / 'Dictionaries' / f'ordnerStruktur{daten_folder}.json'
path_out_vorgang = cwd / 'outputResult'
# Note: If needed, create a rel. folder structure file with helpers.create_folder_structure_json()

with open(path_ordner_struktur_json, encoding='utf-8') as f:
    dict_ordner_struktur_rel = json.load(f)
# Replace relative file paths with absolute ones (because the script needs them)
dict_ordner_struktur_abs = []
for dic in dict_ordner_struktur_rel:
    temp_dict = {'dir': str(dir_data / Path(dic['dir'])),
                 'files': dic['files']}
    dict_ordner_struktur_abs.append(temp_dict)

pfad_, hoechsterPfad, reversedDictionary, \
    directories = helpers.getDirectory(datei, dict_ordner_struktur_abs)

# TODO Better to retrieve the path from a reversedDictionary that has been created before like this
try:
    pfad = reversedDictionary[datei]
except KeyError:  # If not found, the main data dir becomes the directory
    pfad = dir_data
# The output result is the same, but it avoids re-reading the ordnerStruktur file
assert pfad == pfad_

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

# TODO Why pass the full metadata dict around? This gets unwieldy for a lot of files to analyze
metadata = {pfad: {datei: {'objnr': objnr,
                           'adresse': adresse,
                           'denkmalname': denkmalname,
                           'sachbegriff': sachbegriff,
                           'objnrMethode': objnrMethode,
                           'behoerde': behoerde,
                           'vorhaben': vorhaben,
                           'vorhabenScore': vorhabenScore,
                           'vorgang': vorgang,
                           'daten': daten,
                           'inhalt': inhalt,
                           'adrDict': adrDict,
                           'pfadAktuell': str(dir_data)}}}  # TODO Remove pfadAktuell

parser = 'tika'  # 'docx'
for item in metadataToExtract:
    if item == 'inhalt':
        # Inhalt extrahieren
        content: any = extractText.getTextContent(metadata, parser)
        metadata[pfad][datei]['inhalt'] = content
    if item == 'adresse':
        # Adresse identifizieren
        metadata[pfad][datei]['adrDict'], \
            metadata[pfad][datei]['adresse'], adrName \
            = relateAdresse.findAddress(metadata, parser)

    if item == 'objnr':
        # Objektnummer identifizieren
        metadata[pfad][datei]['objnr'], \
            metadata[pfad][datei]['behoerde'], \
            metadata[pfad][datei]['objnrMethode'] \
            = relateObjnr.relateObjnr(metadata, parser)

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
                metadata[pfad][datei]['vorhabenScore'] \
                = relateVorhaben.vorhaben(metadata, directories, ordnerStruktur, parser)
        else:
            metadata[pfad][datei]['vorhaben'], \
                metadata[pfad][datei]['vorhabenScore']\
                = relateVorhaben.vorhaben(metadata, hoechsterPfad, ordnerStruktur, parser)

    if item == 'vorgang':
        # Vorgang identifizieren
        metadata[pfad][datei]['vorgang']\
            = relateVorgang.vorgang(pfad, datei, path_out_vorgang,
                                    considerDocName=True,
                                    methode=parser,
                                    docxVorhanden=True)[pfad][datei]['vorgang']

# Save metadata (increments json-file)
helpers.save_metadata(metadata, results_path)