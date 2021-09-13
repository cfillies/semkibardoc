import json
import os
from pathlib import Path


def create_folder_structure_json_abs():
    path = "C:\\Data\\test\\KIbarDok\\Treptow"
    ents = []
    # for root, d_names, f_names in os.walk(path):
    #     ents.append({ 'dir': root, 'files': f_names} )
    # s= json.dumps(ents, indent = 4, ensure_ascii = False)
    # print(s)
    with open('C:\\Data\\test\\KIbarDok\\files.json', 'w') as fp:
        for root, d_names, f_names in os.walk(path):
            r = root.replace('\uf028', '').replace('\uf022', '')
            fl = []
            for f in f_names:
                fl.append(f.replace('\uf025', ''))
            ents.append({'dir': r, 'files': fl})
        json.dump(ents, fp, indent=4, ensure_ascii=False)


def create_folder_structure_json_rel(dir_data_, output_filepath):
    """
    Creates a folder structure file `output_filepath` that contains the folder and structure
    contained in `dir_data`. The output json contains folder paths RELATIVE TO `dir_data`.

    :param Path dir_data_: A directory
    :param Path output_filepath: The output filepath for saving the json
    """
    # Clean filepaths; if filepaths are clean, these operations have no effect
    dir_data_ = Path(dir_data_)
    output_filepath = Path(output_filepath).with_suffix('.json')

    folder_structure = []
    for root, dirs, files in os.walk(dir_data_):
        dic = {'dir': str(Path(root).relative_to(dir_data_)),
               'files': files}
        folder_structure.append(dic)
    with open(output_filepath, 'w', encoding='utf-8') as outfile:
        json.dump(folder_structure, outfile, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    cwd = Path().cwd()
    daten_folder = 'Test'
    # Change this path to your data folder
    dir_data = Path(r'C:\Users\koenij\Projekte\KIbarDok\Daten') / daten_folder
    path_ordner_struktur_json = cwd / 'static' / f'folder_struc_{daten_folder}.json'
    create_folder_structure_json_rel(dir_data, path_ordner_struktur_json)
