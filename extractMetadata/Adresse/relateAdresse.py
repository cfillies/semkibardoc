import extract.extractAdresse as extractAdresse
import extract.extractText as extractText
from typing import Dict

def findAddress(metadata: Dict, parser: str):

    pfad = next(iter(metadata))
    datei = next(iter(metadata[pfad]))
    inhalt = metadata[pfad][datei]['inhalt']
    
    # Pfad
    # TODO pass getAdresse only the filepath starting at the data parent dir, not C:\\users\\...
    #   to shorten regex search time
    adressen, adresse, adrName = extractAdresse.getAddress(pfad)
    # Dateiname
    if not adressen:
        adressen, adresse, adrName = extractAdresse.getAddress(datei)
    # Inhalt
    if not adressen:
        if inhalt == '':
            inhalt = extractText.getTextContent(metadata, parser)

        adressen, adresse, adrName = extractAdresse.getAddress(inhalt) #inhalt = inhalt.split('§')[0]
    return adressen, adresse, adrName