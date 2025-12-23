import os
from typing import *
from modules.valid_and_path_ops import *

class CommandCAT:
    """
    Класс для реализации команды CAT (concatenate) - вывода содержимого файла.
    
    Команда выводит содержимое указанного файла в стандартный вывод.
    Поддерживает обработку текстовых файлов с кодировкой UTF-8.
    
    Attributes:
        args (List[str]): Аргументы команды (пути к файлам)
        current_dir (str): Текущая рабочая директория
    """
    
    def __init__(self, command: List[str], current_dir: str):
        """
        Инициализация команды CAT.
        
        Args:
            command (List[str]): Полная команда с аргументами
            current_dir (str): Текущая рабочая директория
        """
        self.args = command[1:]
        self.current_dir = current_dir

    def print_file_content(self, path: str, current_dir: str) -> str:
        """
        Чтение и возврат содержимого файла.
        
        Args:
            path (str): Путь к файлу (абсолютный или относительный)
            current_dir (str): Текущая рабочая директория для разрешения относительных путей
            
        Returns:
            str: Содержимое файла или сообщение об ошибке
            
        Raises:
            ValueError: Если путь указывает на директорию, а не файл
            FileNotFoundError: Если файл не существует
            PermissionError: Если нет прав доступа к файлу
            UnicodeDecodeError: Если файл имеет некорректную кодировку
        """
        path = make_path(current_dir=current_dir, path=path)
        if os.path.isdir(path):
            raise ValueError(f"Путь {path} является директорией")

        try:
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
                return content
            
        except FileNotFoundError:
            return f"Ошибка: Файл '{path}' не найден"
        except PermissionError:
            return f"Ошибка: Нет прав доступа к файлу '{path}'"
        except UnicodeDecodeError:
            return f"Ошибка: Не удается декодировать файл '{path}'"
        except Exception as e:
            return f"Неизвестная ошибка: {e}"