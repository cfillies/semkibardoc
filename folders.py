import os
import json

# path = "C:\\Data\\test\\KIbarDok\\Treptow"


# for root, d_names, f_names in os.walk(path):
#     ents.append({ 'dir': root, 'files': f_names} )
# s= json.dumps(ents, indent = 4, ensure_ascii = False)
# print(s)
def replacestuff(r: str):
    r = r.replace('\uf022', '')
    r = r.replace('\uf025', '')
    r = r.replace('\uf028', '')
    r = r.replace('\u0301', '')
    r = r.replace('\u0308', '')
    r = r.replace('\u251c', '')
    r = r.replace('\u255d', '')
    r = r.replace('\x80', '')
    r = r.replace('\x88', '')
   # r = r.replace('\u301', '')
    return r


def getFolders(path):
    ents = []
    for root, d_names, f_names in os.walk(path):
        r = replacestuff(root)
        fl = []
        for f in f_names:
            fl.append(replacestuff(f))
        ents.append({'dir': r, 'files': fl})
    return ents

# getFolders("E:\\2_Köpenick", 'C:\\Data\\test\\KIbarDok\\koepnick_files.json')
