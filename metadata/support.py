from pymongo.collection import Collection

def getAuthorities():
    # Dictionary mit allen Denkmalschutzbehörden erstellen
    # aus:
    # https://www.berlin.de/sen/kulteu/denkmal/organisation-des-denkmalschutzes/untere-denkmalschutzbehoerden/
    # https://www.berlin.de/sen/kulteu/denkmal/organisation-des-denkmalschutzes/landesdenkmalrat/
    # https://www.berlin.de/landesdenkmalamt/

    # Form ist Bezirk:Adresse
    return {'Charlottenburg-Wilmersdorf': 'Hohenzollerndamm 174',
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

def initSupport(col: Collection, hida_col: Collection):

    # streets = pd.read_csv(r'hidaData.csv', sep='\t', encoding='utf-8', usecols=['denkmalStrasse'])
    # streetsset = set(streets['denkmalStrasse'].tolist())
    # streetsset.remove(np.nan)
    # item = col.find()
    # if not item:
        hidal = hida_col.find()
        streets = set([])
        for hida in hidal:
            if "AdresseDict" in hida:
                adlist = hida["AdresseDict"]
                streets.update(set(adlist.keys()))
        item = {"streetnames": list(streets),
                "authorities": getAuthorities(),
                "adcache": {}}
        col.delete_many({})
        col.insert_one(item)
