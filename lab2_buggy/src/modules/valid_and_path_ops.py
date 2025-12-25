from typing import *
import os
import shlex
import logging
import zipfile
import tarfile

from consts import *
# LOG_FILE = "/var/log/python-lab-2/shell.log"
# LOGGING_LEVEL: int = logging.DEBUG

# logger = logging.getLogger('my_app')
# logger.setLevel(LOGGING_LEVEL)


# file_handler = logging.FileHandler(LOG_FILE)
# file_handler.setLevel(logging.DEBUG)


# formatter = logging.Formatter(
#     '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     datefmt='%Y-%m-%d %H:%M:%S'
# )
# file_handler.setFormatter(formatter)

# logger.addHandler(file_handler)




# def path_to_arr(self, path: str) -> List[str]:
#     return path.split("/")  

commands_list = ["ls", "cd", "cat", "cp", "mv", "rm", "zip", "unzip", "tar", "untar", "grep", "history", "undo"]

options_list = ["-l", "-r", "-i"]


def write_to_history(history_file: str, command_number: int, command: str):
    """
    Записывает команду в файл истории в формате: <номер> <команда>
    
    Args:
        history_file (str): Путь к файлу истории
        command_number (int): Номер команды
        command (str): Введенная команда
    """
    try:
        with open(history_file, 'a', encoding='utf-8') as f:
            f.write(f"{command_number} {command}\n")
    except Exception as e:
        logging.error(f"Ошибка записи в историю: {e}")


def read_last_command_number(history_file: str) -> int:
    """
    Читает последний номер команды из файла истории.
    
    Args:
        history_file (str): Путь к файлу истории
        
    Returns:
        int: Последний номер команды (0 если файл не существует или пуст)
    """
    if not os.path.exists(history_file):
        return 0
    
    try:
        with open(history_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if not lines:
                return 0
            
            # Берем последнюю строку и извлекаем номер
            last_line = lines[-1].strip()
            if last_line:
                parts = last_line.split(' ', 1)
                if parts and parts[0].isdigit():
                    return int(parts[0])
        return 0
    except Exception:
        return 0


def parent_path(current_dir: str) -> str:
    if current_dir is HOME_CATALOG: 
        return current_dir
    else:
        splitted_path = current_dir.split("/")
        result_dir = ""
        for i in range(1, len(splitted_path)): # ОШИБКА 4 <- ошибка границы цикла (правильно for i in range(1, len(splitted_path) - 1))
            result_dir += f"/{splitted_path[i]}"
        
        return result_dir

def make_path(current_dir: str, path: str) -> str:
    if path == None:
        return current_dir
    
    elif not path.__contains__("/home"):
        return f"{current_dir}/{path}"
    else:
        return path

def shlex_tokenization(input: str) -> List[str]:
    full_arr = [None] * 4
    splitted = shlex.split(input)
    for index_of_command in range(len(splitted)):
        full_arr[index_of_command] = splitted[index_of_command]
        
    return full_arr



def colorize_dirs(list_of_objects: List[str], current_dir):
    res_arr: List[str] = []
    for obj in list_of_objects:
        path = make_path(current_dir=current_dir, path=obj)
        if os.path.isdir(path):
            res_arr.append(f"\033[34m{obj}\033[0m")
        elif zipfile.is_zipfile(path) or tarfile.is_tarfile(path):
            res_arr.append(f"\033[31m{obj}\033[0m")
        elif os.path.isfile(path):
            res_arr.append(obj)
        else:
            ValueError("Ошибка при получении данных")
    return res_arr

def path_exists(path: str) -> bool:
    return os.path.exists(path=path)
    




