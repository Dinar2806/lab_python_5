import os
import zipfile
import os
from typing import List

from modules.valid_and_path_ops import *


class CommandZIP:
    """
    Класс для реализации команды ZIP - создания zip архивов.
    
    Attributes:
        args (List[str]): Аргументы команды
        current_dir (str): Текущая рабочая директория
    """
    
    def __init__(self, command: List[str], current_dir: str):
        """
        Инициализация команды ZIP.
        
        Args:
            command (List[str]): Полная команда с аргументами
            current_dir (str): Текущая рабочая директория
        """
        self.args = command[1:]
        self.current_dir = current_dir

    def command_zip(self, args: List[str], current_dir):
        """
        Создает zip архив из указанной директории.
        
        Args:
            args (List[str]): Аргументы команды
            current_dir (str): Текущая рабочая директория
            
        Returns:
            str: Сообщение о результате создания архива
            
        Raises:
            ValueError: При недостатке аргументов или если путь не является директорией
            FileNotFoundError: Если директория не существует
            PermissionError: Если нет прав доступа
        """
        if args[1] == None:
            raise ValueError("Недостаточно аргументов. Использование: zip <folder> <archive.zip>")
        
        folder_path = make_path(current_dir=current_dir, path=args[0])
        archive_path = make_path(current_dir=current_dir, path=args[1])
        
        # Проверяем существование папки
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Папка {args[0]} не найдена")
        
        if not os.path.isdir(folder_path):
            raise ValueError(f"{args[0]} не является папкой")
        
        # Проверяем расширение архива
        if not archive_path.endswith('.zip'):
            archive_path += '.zip'
        
        try:
            # Создаем ZIP архив
            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # Создаем относительный путь для архива
                        arcname = os.path.relpath(file_path, os.path.dirname(folder_path))
                        zipf.write(file_path, arcname)
            
            return f"Архив создан: {folder_path} -> {archive_path}"
        
        except PermissionError:
            return f"Ошибка: Нет прав доступа для создания архива"
        except Exception as e:
            return f"Ошибка при создании архива: {e}"


class CommandUNZIP:
    """
    Класс для реализации команды UNZIP - распаковки zip архивов.
    
    Attributes:
        args (List[str]): Аргументы команды
        current_dir (str): Текущая рабочая директория
    """
    
    def __init__(self, command: List[str], current_dir: str):
        """
        Инициализация команды UNZIP.
        
        Args:
            command (List[str]): Полная команда с аргументами
            current_dir (str): Текущая рабочая директория
        """
        self.args = command[1:]
        self.current_dir = current_dir

    def command_unzip(self, args: List[str], current_dir):
        """
        Распаковывает zip архив в текущую директорию.
        
        Args:
            args (List[str]): Аргументы команды
            current_dir (str): Текущая рабочая директория
            
        Returns:
            str: Сообщение о результате распаковки
            
        Raises:
            ValueError: При недостатке аргументов или если файл не является zip архивом
            FileNotFoundError: Если архив не существует
            PermissionError: Если нет прав доступа
            zipfile.BadZipFile: Если архив поврежден
        """
        if args[0] == None:
            raise ValueError("Недостаточно аргументов. Использование: unzip <archive.zip>")
        
        archive_path = make_path(current_dir=current_dir, path=args[0])
        
        # Проверяем существование архива
        if not os.path.exists(archive_path):
            raise FileNotFoundError(f"Архив {args[0]} не найден")
        
        if not zipfile.is_zipfile(archive_path):
            raise ValueError(f"{args[0]} не является ZIP архивом")
        
        try:
            # Распаковываем архив в текущую директорию
            with zipfile.ZipFile(archive_path, 'r') as zipf:
                zipf.extractall(self.current_dir)
            
            return f"Архив распакован: {archive_path} -> {self.current_dir}"
        
        except PermissionError:
            return f"Ошибка: Нет прав доступа для распаковки архива"
        except zipfile.BadZipFile:
            return f"Ошибка: Файл поврежден или не является ZIP архивом"
        except Exception as e:
            return f"Ошибка при распаковке архива: {e}"