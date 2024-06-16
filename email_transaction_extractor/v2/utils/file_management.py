import json
from datetime import datetime
from logging import getLogger
import socket
from functools import partial
from os.path import join
from pathlib import Path


def get_dir_from_home(*args) -> Path:
    return Path(join(str(Path.home()), *args))


get_log_folder = partial(get_dir_from_home, 'logs')
get_report_folder = partial(get_dir_from_home, 'reports')


def make_folder(path: Path) -> str:
    path.mkdir(parents=True, exist_ok=True)
    return str(path)


def create_logs_folder(name: str) -> str:
    return make_folder(get_log_folder(name))


def create_reports_folder(name: str) -> str:
    return make_folder(get_report_folder(name))


def get_timestamp_name(name: str, extension: str) -> str:
    return f'{name}_{datetime.now().strftime("%Y%B%dT%H_%M_%S_%f")[:-3]}.{extension}'


def dump_data_to_file(name: str, path: Path, data: dict) -> str:
    try:
        folder_path = str(path) if path.exists() else make_folder(path)
        name = get_timestamp_name(name, 'json')
        file_path = Path(join(folder_path, name))
        with file_path.open('w') as file:
            file.write(json.dumps(data, indent=4))
        return file_path
    except Exception as e:
        print(e)
