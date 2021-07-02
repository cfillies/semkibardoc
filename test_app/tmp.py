import pymongo
from flask import jsonify
import json
# uri = "mongodb://localhost:27017"

myclient = pymongo.MongoClient(uri)

db = myclient["kibardoc"]
col=db["resolved"]
col.createIndex( { "vorgang": 1 } )
col.createIndex( { "Außenanlagen": 1 } )
col.createIndex( { "Baumaßnahme": 1 } )
col.createIndex( { "vorhaben": "text" } )

res= col.find_one()
# print(res)

def _get_array_param(param):
    if param=='':
        return []
    else:
        # return filter(None, param.split(","))
        return param.split(",")
def _get_group_pipeline(group_by):
    return [
        {
            '$group': {
                '_id': '$' + group_by,
                'count': {'$sum': 1},
            }
        },
        {
            '$project': {
                '_id': 0,
                'value': '$_id',
                'count': 1,
            }
        },
        {
            '$sort': {'count': -1}
        },
        {
            '$limit': 6,
        }
    ]

def resolved2():
    Außenanlagen = []
    Baumaßnahme = []
    Bepflanzungen = []
    Brandschutz = []
    Dach = []
    dir = []
    Diverse = []
    Eingangsbereich = []
    Farbe = []
    Fassade = []
    Gebäude = []
    Gebäudenutzung = ["Gewerbe"]
    Haustechnik = []
    hida = []
    Massnahme = []
    Nutzungsänderung = []
    vorgang = []
    vorhaben = []
    Werbeanlage = []

    match = {}
    if Außenanlagen and len(Außenanlagen)>0:
        match['Außenanlagen'] = {'$in': Außenanlagen}
    if Baumaßnahme and len(Baumaßnahme)>0:
        match['Baumaßnahme'] = {'$in': Baumaßnahme}
    if Bepflanzungen and len(Bepflanzungen)>0:
        match['Bepflanzungen'] = {'$in': Bepflanzungen}
    if Brandschutz and len(Brandschutz)>0:
        match['Brandschutz'] = {'$in': Brandschutz}
    if Dach and len(Dach)>0:
        match['Dach'] = {'$in': Dach}
    if dir and len(dir)>0:
        match['dir'] = {'$in': dir}
    if Diverse and len(Diverse)>0:
        match['Diverse'] = {'$in': Diverse}
    if Eingangsbereich and len(Eingangsbereich)>0:
        match['Eingangsbereich'] = {'$in': Eingangsbereich}
    if Farbe and len(Farbe)>0:
        match['Farbe'] = {'$in': Farbe}
    if Fassade and len(Fassade)>0:
        match['Fassade'] = {'$in': Fassade}
    if Gebäude and len(Gebäude)>0:
        match['Gebäude'] = {'$in': Gebäude}
    if Gebäudenutzung and len(Gebäudenutzung)>0:
        match['Gebäudenutzung'] = {'$in': Gebäudenutzung}
    if Haustechnik and len(Haustechnik)>0:
        match['Gebäudenutzung'] = {'$in': Gebäudenutzung}
    if Massnahme and len(Massnahme)>0:
        match['Massnahme'] = {'$in': Massnahme}
    if Nutzungsänderung and len(Nutzungsänderung)>0:
        match['Nutzungsänderung'] = {'$in': Nutzungsänderung}
    if vorgang and len(vorgang)>0:
        match['vorgang'] = {'$in': vorgang}
    if vorhaben and len(vorhaben)>0:
        match['vorhaben'] = {'$in': vorhaben}
    if Werbeanlage and len(Werbeanlage)>0:
        match['Werbeanlage'] = {'$in': Werbeanlage}

    pipeline = [{
            '$match': match
            }] if match else []

    pipeline += [{
            '$facet': {
                'resolved': [
                    {'$skip': 0},
                    {'$limit': 100}
                ],
                'count': [
                    {'$count': 'total'}
                ],
            }
        }]

    res = list(col.aggregate(pipeline))[0]
    print(res["count"])

    for resolved in res['resolved']: # remove _id, is an ObjectId and is not serializable
        del resolved['_id']

    res['count'] = res['count'][0]['total'] if res['count'] else 0

    print(res)

# resolved2()
def _get_facet_pipeline(facet, match):
    pipeline = []
    if match:
        if facet in match:
            matchc = match.copy();            
            del matchc[facet]
        else:
            matchc = match
        pipeline = [
            {'$match': match}
        ] if match else []
    return pipeline + _get_group_pipeline(facet)

def _get_group_pipeline(group_by):
    return [
        {
            '$group': {
                '_id': '$' + group_by,
                'count': {'$sum': 1},
            }
        },
        {
            '$project': {
                '_id': 0,
                'value': '$_id',
                'count': 1,
            }
        },
        {
            '$sort': {'count': -1}
        },
        {
            '$limit': 6,
        }
    ]

def resolved2_facets():
    # filters
    Außenanlagen = []
    Baumaßnahme = []
    Bepflanzungen = []
    Brandschutz = []
    Dach = []
    dir = []
    Diverse = []
    Eingangsbereich = []
    Farbe = []
    Fassade = []
    Gebäude = []
    Gebäudenutzung = ["Gewerbe"]
    Haustechnik = []
    hida = []
    Massnahme = []
    Nutzungsänderung = []
    vorgang = []
    vorhaben = []
    Werbeanlage = []

    match = {}
    
    if Außenanlagen and len(Außenanlagen)>0:
        match['Außenanlagen'] = {'$in': Außenanlagen}
    if Baumaßnahme and len(Baumaßnahme)>0:
        match['Baumaßnahme'] = {'$in': Baumaßnahme}
    if Bepflanzungen and len(Bepflanzungen)>0:
        match['Bepflanzungen'] = {'$in': Bepflanzungen}
    if Brandschutz and len(Brandschutz)>0:
        match['Brandschutz'] = {'$in': Brandschutz}
    if Dach and len(Dach)>0:
        match['Dach'] = {'$in': Dach}
    if dir and len(dir)>0:
        match['dir'] = {'$in': dir}
    if Diverse and len(Diverse)>0:
        match['Diverse'] = {'$in': Diverse}
    if Eingangsbereich and len(Eingangsbereich)>0:
        match['Eingangsbereich'] = {'$in': Eingangsbereich}
    if Farbe and len(Farbe)>0:
        match['Farbe'] = {'$in': Farbe}
    if Fassade and len(Fassade)>0:
        match['Fassade'] = {'$in': Fassade}
    if Gebäude and len(Gebäude)>0:
        match['Gebäude'] = {'$in': Gebäude}
    if Gebäudenutzung and len(Gebäudenutzung)>0:
        match['Gebäudenutzung'] = {'$in': Gebäudenutzung}
    if Haustechnik and len(Haustechnik)>0:
        match['Gebäudenutzung'] = {'$in': Gebäudenutzung}
    if Massnahme and len(Massnahme)>0:
        match['Massnahme'] = {'$in': Massnahme}
    if Nutzungsänderung and len(Nutzungsänderung)>0:
        match['Nutzungsänderung'] = {'$in': Nutzungsänderung}
    if vorgang and len(vorgang)>0:
        match['vorgang'] = {'$in': vorgang}
    if vorhaben and len(vorhaben)>0:
        match['vorhaben'] = {'$in': vorhaben}
    if Werbeanlage and len(Werbeanlage)>0:
        match['Werbeanlage'] = {'$in': Werbeanlage}


    pipeline = []
    pipeline += [{
        '$facet': {
            'vorgang': _get_facet_pipeline('vorgang', match),
            'vorhaben':  _get_facet_pipeline('vorhaben', match),
            'Außenanlagen':  _get_facet_pipeline('Außenanlagen', match),
            'Baumaßnahme':  _get_facet_pipeline('Baumaßnahme', match),
            'Bepflanzungen':  _get_facet_pipeline('Bepflanzungen', match),
            'Brandschutz':  _get_facet_pipeline('Brandschutz', match),
            'Dach':  _get_facet_pipeline('AußenanDachagen', match),
            'Diverse':  _get_facet_pipeline('Diverse', match),
            'Eingangsbereich':  _get_facet_pipeline('Eingangsbereich', match),
            'Farbe':  _get_facet_pipeline('Farbe', match),
            'Fassade':  _get_facet_pipeline('Fassade', match),
            'Gebäude':  _get_facet_pipeline('Gebäude', match),
            'Gebäudenutzung':  _get_facet_pipeline('Gebäudenutzung', match),
            'Haustechnik':  _get_facet_pipeline('Haustechnik', match),
            'Massnahme':  _get_facet_pipeline('Massnahme', match),
            'Nutzungsänderung':  _get_facet_pipeline('Nutzungsänderung', match),
            'Werbeanlage':  _get_facet_pipeline('Werbeanlage', match),
          # 'zipcode': _get_facet_zipcode_pipeline(boroughs, cuisines),
        }
    }]
    res = list(col.aggregate(pipeline))[0]
    print(res)

resolved2_facets()