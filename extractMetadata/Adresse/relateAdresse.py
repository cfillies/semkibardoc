import  extract.extractAdresse as extractAdresse
import  extract.extractText as extractText

def findAdresse(metadata, einleseMethode):
    
    pfad = next(iter(metadata))
    datei = next(iter(metadata[pfad]))
    inhalt = metadata[pfad][datei]['inhalt']
    
    # Pfad   
    adressen, adresse, adrName = extractAdresse.getAdresse(pfad)  
    # Dateiname
    if not adressen:
        adressen, adresse, adrName = extractAdresse.getAdresse(datei)
    # Inhalt
    if not adressen:
        if inhalt == '':
            inhalt = extractText.getInhalt(metadata, einleseMethode)

        adressen, adresse, adrName = extractAdresse.getAdresse(inhalt) #inhalt = inhalt.split('§')[0]
    return adressen, adresse, adrName