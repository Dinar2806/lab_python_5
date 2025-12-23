import os
from typing import *

from modules.valid_and_path_ops import *
import shutil


class CommandMV:
    """
    Класс для реализации команды MV (move) - перемещения файлов и директорий.
    
    Attributes:
        args (List[str]): Аргументы команды
        current_dir (str): Текущая рабочая директория
    """
    
    def __init__(self, command: List[str], current_dir: str):
        """
        Инициализация команды MV.
        
        Args:
            command (List[str]): Полная команда с аргументами
            current_dir (str): Текущая рабочая директория
        """
        self.args = command[1:]
        self.current_dir = current_dir

    def command_mv(self, args: List[str], current_dir: str):
        """
        Выполняет перемещение файла или директории.
        
        Args:
            args (List[str]): Аргументы команды
            current_dir (str): Текущая рабочая директория
            
        Returns:
            str: Сообщение о результате перемещения
            
        Raises:
            FileNotFoundError: Если исходный путь не существует
            PermissionError: Если нет прав доступа
        """
        from_path = make_path(current_dir=current_dir, path=args[0])
        to_path = make_path(current_dir=current_dir, path=args[1])
        try:
            if not os.path.exists(from_path):
                raise FileNotFoundError(f"Пути {from_path} не существует")
            else:
                os.makedirs(to_path, exist_ok=True)

                shutil.move(from_path, to_path)
                return f"Файл перемещен: {from_path} -> {to_path}"
        except PermissionError:
            return f"Ошибка: Нет прав доступа"
        except Exception as e:
            return f"Ошибка при перемещении: {e}"