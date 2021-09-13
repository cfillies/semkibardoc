import requests
from requests.api import request
import os
from pathlib import Path
from pymongo.collection import Collection


def extract_text(file_path, tika_url):
    with open(file_path, 'rb') as d:
        r = requests.put(tika_url + "/tika", data=d)
    r.encoding = r.apparent_encoding
    result = r.text
    return result


def extract_meta(file_path, tika_url):
    file_name = str.split(file_path, '\\')[-1]
    with open(file_path, 'rb') as d:
        response = requests.put(tika_url + "/meta", data=d,
                                headers={"Accept": "application/json"})
    try:
        result = response.json()
    except:  # TODO Except statement too broad
        result = {}
    result['file_name'] = file_name
    return result


def get_all_files_in_dir(directory):
    """ Runs recursively through all files in `directory` and yields their full filepaths. """

    for root, directories, filenames in os.walk(directory):
        for file_ in filenames:
            yield Path(os.path.join(root, file_))


def extract_contents(district: str, filepath: Path, col: Collection,
                     tika_url: str, data_dir: Path):
    # col.delete_many({})
    none_list = ['.xml']
    empty_list = ['.tif', '.tiff', '.bmp', '.jpg', '.jpeg', '.gif', '.png', '.eps']
    if filepath.suffix in none_list:
        txt = None
    elif filepath.suffix in empty_list:
        txt = ""
    else:
        txt = extract_text(filepath, tika_url)
    met = extract_meta(filepath, tika_url)

    try:
        col.find_one_and_update(
            {"path": filepath.relative_to(data_dir), "file": filepath.stem,
             "ext": filepath.suffix},
            {"district": district, "meta": met, "text": txt},
            upsert=True)
    except:  # TODO Exception statement too broad: Raise for now and fix upcoming errors
        print(f"mongoDB Problem: {filepath}")
        raise
