import extract.extractDatum as extractDatum
import extract.extractText as extractText
import Misc.helpers as helpers

def datum(metadata: dict, parser: str):
    
    pfad = next(iter(metadata))
    datei = next(iter(metadata[pfad]))    
    inhalt = metadata[pfad][datei]['inhalt']
    
    if inhalt == '':
        inhalt = extractText.getTextContent(metadata, parser)
        
    datenDateiAll = extractDatum.getDates(inhalt)
    daten = helpers.convertDate(datenDateiAll)
    
    return daten