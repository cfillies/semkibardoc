import json
from Vorgang.getVorgang import findVorgang


def rep(x):
    x = str(x)
    for r in (('{', ''), ('}', ''), ('[', ''), (']', ''), ('\"', ''), ('\'', '')):
        x.replace(*r)
    return x


def updatedResult(oldResult, newResult):
    for key in oldResult['Ergebnis']:
        oldResult['Ergebnis'][key] = oldResult['Ergebnis'][key] + newResult['Ergebnis'][key]
    for filePath in newResult['Gesamt-Zuordnung'].keys():
        oldResult['Gesamt-Zuordnung'].setdefault(filePath, {}).update(
            newResult['Gesamt-Zuordnung'][filePath])
        oldResult['Keine-Zuordnung'].setdefault(filePath, {}).update(
            newResult['Keine-Zuordnung'][filePath])
        oldResult['Informelles-Format'].setdefault(filePath, []).extend(
            newResult['Informelles-Format'][filePath])
        oldResult['Fehler'].setdefault(filePath, []).extend(newResult['Fehler'][filePath])
    return oldResult


def save(output_dir, consider_doc_name, new_result):
    filename = 'result-docName.json' if consider_doc_name else 'result-NodocName.json'
    output_filepath = output_dir / filename
    try:  # Versuche, existierenden resultFile zu updaten
        with open(output_filepath, 'r', encoding='utf8') as f:
            result_file = json.load(f)
        final_result = updatedResult(result_file, new_result)
    except (FileNotFoundError, json.decoder.JSONDecodeError):  # Keine Datei oder leere Datei
        final_result = new_result
    with open(output_filepath, 'w', encoding='utf8') as f:
        json.dump(final_result, f, indent=4, ensure_ascii=False)


def allVorgang(file, filePath, output_dir, considerDocName, methode, docxVorhanden):
    resultAll = findVorgang(file, filePath, considerDocName, methode, docxVorhanden).all
    # print('resultAll:',resultAll)
    save(output_dir, considerDocName, resultAll)
    return resultAll


def vorgang(file_path, files, output_dir, considerDocName, methode, docxVorhanden):
    if not isinstance(files, list):
        files = [files]
    alle = allVorgang(files, file_path, output_dir, considerDocName, methode, docxVorhanden)
    zuordnung = alle['Gesamt-Zuordnung']
    keineZuordnung = alle['Keine-Zuordnung']
    informellesFormat = alle['Informelles-Format']
    fehler = alle['Fehler']
    ###############################################
    result = {}
    result[file_path] = {}
    ###############################################
    for f in files:
        result[file_path][f] = {}
        if f in zuordnung[file_path].keys():
            vResult = rep(list(zuordnung[file_path][f].keys()))
        elif f in keineZuordnung[file_path].keys():
            vResult = 'Keine Kategorie gefunden'
        elif f in informellesFormat[file_path]:
            vResult = 'Informelles Format'
        elif f in fehler[file_path]:
            vResult = 'Fehler in der Datei'
        else:
            vResult = 'Fehler in der Datei'
        result[file_path][f]['vorgang'] = vResult
    return result
