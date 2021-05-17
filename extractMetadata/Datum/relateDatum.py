import extract.extractDatum as extractDatum
import extract.extractText as extractText
import Misc.helpers as helpers

def datum(metadata, einleseMethode):
    
    pfad = next(iter(metadata))
    datei = next(iter(metadata[pfad]))    
    inhalt = metadata[pfad][datei]['inhalt']
    
    if inhalt == '':
        inhalt = extractText.getInhalt(metadata, einleseMethode)
        
    datenDateiAll = extractDatum.getDates(inhalt)
    daten = helpers.convertDate(datenDateiAll)
    
    return daten