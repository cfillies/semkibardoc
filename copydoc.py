import os
from shutil import copyfile

path = "C:\\Data\\test\\KIbarDok\\Treptow"
doc_path = 'C:\\Data\\test\\KIbarDok\\doc'
i=0

for root, d_names, f_names in os.walk(path):
    for f in f_names:
        if f.endswith(".doc"):
            i=i+1
            if i>0:
                copyfile(os.path.join(root, f), os.path.join(doc_path, f))
