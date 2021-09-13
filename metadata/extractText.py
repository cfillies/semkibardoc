import requests
from requests.api import request
import os
from pathlib import Path
from pymongo.collection import Collection


def extract_text(file_path, tika_url):
    with open(file_path, 'rb') as d:
        response = requests.put(tika_url + "/tika", data=d)
    response.encoding = response.apparent_encoding
    result = response.text
    return result


def extract_meta(file_path, tika_url):
    file_name = Path(file_path).name
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


def extract_contents(filepath: Path, tika_url: str):
    # col.delete_many({})
    none_list = ['.xml']
    empty_list = ['.tif', '.tiff', '.bmp', '.jpg', '.jpeg', '.gif', '.png', '.eps']
    if filepath.suffix in none_list:
        txt = None
    elif filepath.suffix in empty_list:
        txt = ""
    else:
        txt = extract_text(filepath, tika_url)
    metadata = extract_meta(filepath, tika_url)
    return txt, metadata
