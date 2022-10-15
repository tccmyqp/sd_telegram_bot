# import importlib
# from fnmatch import fnmatch
import json
import os
import pathlib
import re

from app.config import ROOT_DIR

# from dacite import from_dict
# from app.classes import poll_list, str_data


# strings.py directory
# ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(ROOT_DIR,'polls')


# print(os.getcwd())
# path = 'app\polls'
# content = os.listdir(path)
dirs = [i.name for i in os.scandir(path) if i.is_dir() and re.match(r'[^__]', i.name)]
# print(dirs)

data_polls = {}
for name in dirs:
    # загружаем данные из json
    str_path = os.path.join(path, name, 'poll_strings.json')
    with open(str_path, encoding='utf-8') as f:
            data = json.load(f)
            data_polls[name] = data
            
    # сохраним данные в json
    # with open(os.path.join(path, name, 'poll_strings.json'), 'w', encoding='utf-8') as f:
    #json.dump(module.data, f, indent=2, ensure_ascii=False)


# сохраняем strings.json
# with open('strings.json', 'w', encoding='utf-8') as f:
#json.dump(data, f, indent=2, ensure_ascii=False)

# читаем strings.json
str_path = os.path.join(ROOT_DIR, 'strings.json')
with open(str_path, encoding='utf-8') as f:
        data_strings = json.load(f)

