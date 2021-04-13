import os
import json

path = "C:\\Data\\test\\KIbarDok\\Treptow"

ents = []

# for root, d_names, f_names in os.walk(path):
#     ents.append({ 'dir': root, 'files': f_names} )
# s= json.dumps(ents, indent = 4, ensure_ascii = False)
# print(s)
with open('C:\\Data\\test\\KIbarDok\\files.json', 'w') as fp:
    for root, d_names, f_names in os.walk(path):
       r =  root.replace('\uf028','').replace('\uf022','')
       fl = []
       for f in f_names:
           fl.append(f.replace('\uf025',''))
       ents.append({ 'dir': r, 'files': fl} )
    json.dump(ents, fp, indent = 4, ensure_ascii = False)
