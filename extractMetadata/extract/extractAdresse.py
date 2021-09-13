#!/usr/bin/env python
# coding: utf-8

import json
import re
import numpy as np
import pandas as pd
# https://pyspellchecker.readthedocs.io/en/latest/
# https://github.com/barrust/pyspellchecker
from spellchecker import SpellChecker

from extractMetadata.Misc import schluesselregex as rex
from extractMetadata.Misc import helpers


def getSpellcheck():
    """
    Instantiates a `Spellchecker` and adds the hida database street names to its vocabulary.
    :return: deutsch: Spellchecker
    """
    deutsch = SpellChecker(language='de')
    hidaStrassenDf = pd.read_csv(r'Dictionaries\hidaData.csv', sep='\t', encoding='utf-8',
                                 usecols=['denkmalStrasse'])
    hidaStrassenSet = set(hidaStrassenDf['denkmalStrasse'].tolist())
    hidaStrassenSet.remove(np.nan)
    hidaStrassen = list(hidaStrassenSet)
    deutsch.word_frequency.load_words(hidaStrassen)
    return deutsch


def getAdresse(textRaw: str):
    """
    Takes a string and tries to find an address in it using regex as defined in schluesselregex.py

    :param str textRaw: The string to be analyzed
    :return:
    """
    # Explode the individual text elements of the string by adding white spaces around them
    textString = re.sub("[a-zA-Z äÄöÖüÜß]+", lambda ele: " " + ele[0] + " ", textRaw)
    # Replace \\, \, _ with whitespaces
    text = textString.replace('\\', ' ').replace('\ ', '').replace('_', ' ')

    # TODO This reads in the hida csv and reinstanciates the spellchecker at every call!
    typoSpellcheck = getSpellcheck()

    text_split = text.split()
    text_corr = []
    for word in text_split:
        text_corr.append(re.sub('str$|str.$|straße$|staße$|stasse$', 'strasse', word).lower())

    text = ' '.join(text_corr)

    text = text.replace('.', ' ').lower()
    adrName = rex.getRegex(text).adresseUnvollstaendig  # Adresse ohne Hausnummer
    adresse = rex.getRegex(text).adresse  # Adresse mit Hausnummer

    adressen = {}

    if adresse and isinstance(adresse, list):
        for adr in adresse:
            try:
                # TODO: "/" und "-" haben in der Adressenangabe unterschiedliche Bedeutungen.
                #   In diesem Skript wird das aber noch nicht berücksichtigt
                # TODO The script does not recognize letters in numbers (e.g. 76a-g)
                adr = adr.replace('/', '-')
                strassenNameOrig = re.findall('([a-zA-Z äÄöÖüÜß-]*)\d*.*', adr)[0].rstrip()
                strassenName = re.sub('str$|str.$|straße$|staße$|stasse$', 'strasse',
                                      strassenNameOrig)
                hausNummer = adr.replace(strassenNameOrig, '').replace(' ', '') \
                    .replace('.', ' ').lstrip()

                strassenName = corrAdresseTypo(strassenName, typoSpellcheck)

                if re.search(r'-\d{1,3}$', hausNummer):
                    # Adresse beinhaltet mehrere Hausnummern: range aufsplitten und auflisten
                    hausNummerRange = hausNummer.rsplit(' ', 1)[-1].rsplit('-', 1)

                    if int(hausNummerRange[1]) - int(hausNummerRange[0]) > 0:
                        # TODO Check if Hausnummern have the correct range with +2 instead of +1
                        nr_range = np.arange(int(hausNummerRange[0]), int(
                            hausNummerRange[1]) + 2)  # WARNINg: +1 probably right
                        hausNummer = [item for item in nr_range.astype(str)]

                elif '-' in hausNummer:
                    indStrich = hausNummer.find('-')
                    hausNummerRange = [hausNummer[:indStrich],
                                       re.findall(r'\d+', hausNummer[indStrich + 1:])[0]]

                    if int(hausNummerRange[1]) - int(hausNummerRange[0]) > 0:
                        nr_range = np.arange(int(hausNummerRange[0]), int(
                            hausNummerRange[1]) + 2)  # WARNINg: +1 probably right
                        hausNummer = [item for item in nr_range.astype(str)]

                hausNummerList = [hausNummer] if isinstance(hausNummer, str) else hausNummer
                hausNummerStr = ''.join(hausNummerList)
                if (strassenName in adressen) and (hausNummerStr in adressen[strassenName]):
                    adressen[strassenName][hausNummerStr]['hausnummer'].extend(hausNummerList)
                else:
                    adressen[strassenName] = {hausNummerStr: {'hausnummer': hausNummerList}}
            except:
                # TODO Exception clause too broad
                pass
                dummy = 99999

    elif (type(adrName) is list) and adrName:
        for adn in adrName:
            if adn not in adressen:
                adressen[adn] = {'none': {'hausnummer': []}}

    for key in adressen.keys():
        for innerKey in adressen[key].keys():
            adressen[key][innerKey]['hausnummer'] = list(
                set(adressen[key][innerKey]['hausnummer']))

    return adressen, adresse, adrName


def corrAdresseTypo(strName, typoSpellcheck):
    """
    Corrects typos in street name strings.

    :param strName: A street name (though any string works)
    :param typoSpellcheck: A spellchecker object with hida street names added to its vocabulary
    :return: The corrected street name
    """
    if typoSpellcheck.unknown([strName]):
        strName = typoSpellcheck.correction(strName)
        # print(adrCorr + ' --> ' + corr)
        # print('alle Möglichkeiten:' + str(deutsch.candidates(word)))
    return strName


def getAusHida(denkmalDict):
    with open(denkmalDict) as f:
        denkmale = json.load(f)

    # Denkmalliste mit jeweiligen Adressen versehen
    denkmaleAdresse = list()
    denkmalStrasse = list()
    denkmalHausnr = list()
    denkmalSachbegriff = list()
    denkmaleObjNr = list()
    denkmalName = list()

    for key in denkmale:
        if 'AdresseDict' in denkmale[key].keys():
            adressen = []
            adressenDict = denkmale[key]['AdresseDict']
            for keyAdr in adressenDict:
                hausnummer = adressenDict[keyAdr]
                if not hausnummer:
                    hausnummer = '99999'

                for hnr in hausnummer:
                    if 'Sachbegriff' in denkmale[key].keys():
                        denkmalSachbegriff.append(denkmale[key]['Sachbegriff'])
                    else:
                        denkmalSachbegriff.append(['none'])

                    if 'Denkmalname' in denkmale[key].keys():
                        denkmalName.append(denkmale[key]['Denkmalname'])
                    else:
                        denkmalName.append(['none'])

                    denkmalStrasse.append(keyAdr.replace("ß", "ss").lower())
                    denkmalHausnr.append(hnr)

                    adr = str(keyAdr.lower()) + ' ' + str(hnr)
                    denkmaleAdresse.append(adr)
                    denkmaleObjNr.append(key)

    # Strassennamen aus Denkmalliste entnehmen und in das Wörterbuch einfügen,
    # um Tippfehler in Adressen korrigieren zu können
    strasseSet = list(set(denkmalStrasse))

    d = {'denkmalObjnr': denkmaleObjNr, 'denkmalAdresse': denkmaleAdresse,
         'denkmalStrasse': denkmalStrasse, \
         'denkmalHausnr': denkmalHausnr, 'denkmalName': denkmalName,
         'denkmalSachbegriff': denkmalSachbegriff}
    df = pd.DataFrame(data=d)
    df.to_csv('hidaData.csv', sep='\t', encoding='utf-8', index=False)

    return (denkmale, denkmaleAdresse, denkmalStrasse, denkmalHausnr, denkmalSachbegriff,
            denkmaleObjNr, denkmalName, strasseSet)


def getBehoerde():
    # Dictionary mit allen Denkmalschutzbehörden erstellen
    # aus:
    # https://www.berlin.de/sen/kulteu/denkmal/organisation-des-denkmalschutzes/untere-denkmalschutzbehoerden/
    # https://www.berlin.de/sen/kulteu/denkmal/organisation-des-denkmalschutzes/landesdenkmalrat/
    # https://www.berlin.de/landesdenkmalamt/

    # Form ist Bezirk:Adresse
    dict_behoerden = {
        'Charlottenburg-Wilmersdorf': 'Hohenzollerndamm 174',
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
    return dict_behoerden
