import spacy
model = None
def init():
    global model
    model = spacy.load("C:\\Data\\test\\kibartmp\\msg_modelle\\adressen\\spacy_address_model_human_validation_50_1000" )

def show( text : str or float ) -> None:
    
    """
    This function uses Displacy from Spacy to display the found addresses.
    
    PARAMETERS
    ----------
        text : str
             the text to be analyzed
    """
    
    if type( text ) != str:
        
        print( "Leerer Text" )
        
    else:
        
        doc = model( text )
        
        spacy.displacy.render( doc, style = "ent" )

text = 'Offene Vorhaben – Dauerbrenner\n\nAlt-Treptow:\n\n· Hoffmannstr. 11, ehem. Kinderheim\n\n· Kiehnwerderallee Gaststätte Eierhäuschen\nBaumschulenweg:\n\n· Südostallee 134, Kinderheim Makarenko\n\nNiederschöneweide:\n\n· Schnellerstr.137 Brauerei Bärenquell\n\n· Adlergestell, Bahnbetriebswerk Schöneweide\n\nJohannisthal:\n\n· Segelfliegerdamm 1/45 Flugzeugfabrik der Luftverkehrsgesellschaft\n\nAdlershof:\n\n· Adlergestell 327, Fabrik Bärensiegel\n\nGrünau:\n\n· Regattastraße 161/167 – Riviera / Gesellschaftshaus\n\n· Regattastraße 10\n\n\n· Regattastraße 273-277\n\n· Richterstraße 3, 4, 5 – Bahnhäuser\n\nSchmöckwitz:\n\n· Wernsdorfer Straße 27 – Jagdhaus Schmöckwitz\n\n· Alt-Schmöckwitz 15 und 9\n\nRahnsdorf: \n\n· Fürstenwalder Damm 838 - Strandbad Müggelsee\n\n· Dorfstraße 20/21 in Rahnsdorf\n\n· Hessenwinkel – Dämmeritzsee Villa\n\nFriedrichshagen:\n\n· Bölschestraße 130\n\n· Bölschestraße – Kampfhunde\n\n· Müggelseedamm 8-10 - Garten – Hirschgarten Villa\n\nKöpenick:\n\n· Friedrichshagener Straße 9-11\n\n· Müggelturm\n\n· Wendenschlossstrasse 254 – Bolle-Villa-Grundstück\n\n· Altstadt \n\n\n· Laurenstraße 1/1a\n\n· Freiheit 17\n\n· Kirchstraße\n\n· Kietzerstraße 6\n\n· Bahnhofstraße 65/64/63 – Ötting-Villa\n\n· Elsengrund – Haustüren\n\n· Uhlenhorsterstraße 29 – Anbau\n\n· Lindenhof\n\n· Ottomar-Geschke-Straße - Spindlersfeld Ringbau\n\nOberschöneweide: \n\n· Wilhelminenhofstraße Oberschöneweide – zahlreiche Industriehallen\n\n· Wilhelminenhofstraße 66/67 – Klubhaus\n\n· Rummelsburger Landstraße - Altes Kraftwerk Rummelsburg\n\n· Nalepastraße 10-50 – Sheddachhalle\n\nAußerdem muss geprüft werden:\n\n· Späthstr. 80-85, 86-88,  Baumschule Späth\n\n· Adlergestell 250/254, Wohnhäuser für die Bahnarbeiter\n'
# print( text )

# show( text )

# res = "Offene Vorhaben – DauerbrennerAlt-Treptow:· Hoffmannstr. 11 ADDRESS , ehem. Kinderheim· Kiehnwerderallee Gaststätte EierhäuschenBaumschulenweg:· Südostallee 134 ADDRESS , Kinderheim MakarenkoNiederschöneweide:· Schnellerstr.137 Brauerei Bärenquell· Adlergestell, Bahnbetriebswerk SchöneweideJohannisthal:· Segelfliegerdamm 1/45 ADDRESS Flugzeugfabrik der LuftverkehrsgesellschaftAdlershof:· Adlergestell 327 ADDRESS , Fabrik BärensiegelGrünau:· Regattastraße 161/167 ADDRESS – Riviera / Gesellschaftshaus· Regattastraße 10 ADDRESS · Regattastraße 273-277 ADDRESS · Richterstraße 3, 4, 5 ADDRESS – BahnhäuserSchmöckwitz:· Wernsdorfer Straße 27 ADDRESS – Jagdhaus Schmöckwitz· Alt-Schmöckwitz 15 und 9 ADDRESS Rahnsdorf: · Fürstenwalder Damm 838 ADDRESS - Strandbad Müggelsee· Dorfstraße 20/21 ADDRESS in Rahnsdorf· Hessenwinkel – Dämmeritzsee VillaFriedrichshagen:· Bölschestraße 130 ADDRESS · Bölschestraße – Kampfhunde· Müggelseedamm 8-10 - Garten – Hirschgarten VillaKöpenick:· Friedrichshagener Straße 9-11 ADDRESS · Müggelturm· Wendenschlossstrasse 254 ADDRESS – Bolle-Villa-Grundstück· Altstadt · Laurenstraße 1/1a ADDRESS · Freiheit 17 ADDRESS · Kirchstraße· Kietzerstraße 6 ADDRESS · Bahnhofstraße 65/64/63 ADDRESS – Ötting-Villa· Elsengrund – Haustüren· Uhlenhorsterstraße 29 ADDRESS – Anbau· Lindenhof· Ottomar-Geschke-Straße - Spindlersfeld RingbauOberschöneweide: · Wilhelminenhofstraße Oberschöneweide – zahlreiche Industriehallen· Wilhelminenhofstraße 66/67 ADDRESS – Klubhaus· Rummelsburger Landstraße - Altes Kraftwerk Rummelsburg· Nalepastraße 10-50 ADDRESS – SheddachhalleAußerdem muss geprüft werden:· Späthstr. 80-85, 86-88 ADDRESS , Baumschule Späth· Adlergestell 250/254, Wohnhäuser für die Bahnarbeiter"