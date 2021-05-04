import json
import os

filename = "taxonomy.txt"
with open(filename, encoding='utf-8') as f:
    content = f.readlines()
# content = [x.strip() for x in content]
tlist = []

level = 0
plevel = 0
pobj = ""
stack = []
sid = "     ID"
sdn = "     DN"
svb = "     VB"
sbs = "     BS"
t = {}
slist = []
for l in content:
    if l.startswith(sid):
        t["ID"] = l[len(sid)+1:].strip()
        slist = []
    elif l.startswith(sdn):
        t["DN"] = l[len(sdn)+1:].strip()
    elif l.startswith(svb):
        t["VB"] = l[len(svb)+1:].strip()
    elif l.startswith(sbs):
        slist.append(l[len(sbs)+1:].strip())
        t["BS"] = slist
    if l[0] != " ":
        b = l.find(" ")
        nlevel = int(l[0:b])
        cobj = l[b+1:].strip()
        t = {}
        if nlevel == 0:
            pobj = cobj
            t = {'topic': cobj}
          #  tlist.append(t)
        elif nlevel != level:
            if nlevel > level:
                stack.append(pobj)
                t = {'topic': cobj, 'parent': pobj}
                # print(str(nlevel) + " " + cobj + "->" + pobj)
                level = nlevel
                pobj = cobj
            else:
                if level-nlevel>1:
                    print(cobj)
                for x in range(0, level-nlevel):
                    stack.pop()
                pobj = stack[len(stack)-1]
                t = {'topic': cobj, 'parent': pobj}
                # print(str(nlevel) + " " + cobj + "->" + pobj)
                level = nlevel
                pobj = cobj
        else:
            ppobj = stack[len(stack)-1]
            t = {'topic': cobj, 'parent': ppobj}
            # print(str(nlevel) + " " + cobj + "->" + ppobj)
            pobj = cobj
        try:
            if len(t)>0:
                json.dumps(t)
                tlist.append(t)
        except:
            pass

with open('C:\\Data\\test\\taxo.json', 'w', encoding='utf-8') as json_file:
    json.dump(tlist, json_file, indent=4, ensure_ascii=False)
