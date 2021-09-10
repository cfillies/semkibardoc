from typing import Dict

from extractMetadata.extract.extractAdresse import getAdresse
from extractMetadata.extract.extractText import getTextContent


def findAddress(metadata: Dict, parser: str):
    pfad = next(iter(metadata))
    datei = next(iter(metadata[pfad]))
    inhalt = metadata[pfad][datei]['inhalt']

    # Pfad
    # TODO pass getAdresse only the filepath starting at the data parent dir, not C:\\users\\...
    #   to shorten regex search time
    adressen, adresse, adrName = getAdresse(pfad)
    # Dateiname
    if not adressen:
        adressen, adresse, adrName = getAdresse(datei)
    # Inhalt
    if not adressen:
        if inhalt == '':
            inhalt = getTextContent(metadata, parser)

        adressen, adresse, adrName = getAdresse(inhalt)  # inhalt = inhalt.split('§')[0]
    return adressen, adresse, adrName
