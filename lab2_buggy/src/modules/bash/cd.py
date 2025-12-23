import os
from typing import *
from modules.valid_and_path_ops import *


class CommandCD:
    """
    Класс для реализации команды CD (change directory) - смены текущей директории.
    
    Поддерживает переходы:
    - '..' - на уровень выше
    - '~' - в домашнюю директорию
    - относительные и абсолютные пути
    
    Attributes:
        args (List[str]): Аргументы команды
        current_dir (str): Текущая рабочая директория
    """
    
    def __init__(self, command: List[str], current_dir: str):
        """
        Инициализация команды CD.
        
        Args:
            command (List[str]): Полная команда с аргументами
            current_dir (str): Текущая рабочая директория
        """
        self.args: List[str] = command[1:]
        self.current_dir: str = current_dir

    
    def command_cd(self, args: List[str], current_dir: str) -> str:
        """
        Выполняет смену текущей директории.
        
        Args:
            args (List[str]): Аргументы команды
            current_dir (str): Текущая рабочая директория
            
        Returns:
            str: Новый путь к директории
            
        Raises:
            ValueError: Если указанная директория не существует
        """
        new_dir = args[0]
        if new_dir == "..":
            return parent_path(current_dir)
        elif new_dir == "~":
            return HOME_CATALOG
        else:
            res_path = make_path(current_dir=current_dir, path=new_dir)
            if path_exists(res_path):
                return res_path
            else:
                raise ValueError("Несуществующая директория")