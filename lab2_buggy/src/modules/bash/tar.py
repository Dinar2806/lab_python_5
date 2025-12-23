import os
import tarfile
from typing import List

from modules.valid_and_path_ops import *


class CommandTAR:
    """
    Класс для реализации команды TAR - создания tar.gz архивов.
    
    Attributes:
        args (List[str]): Аргументы команды
        current_dir (str): Текущая рабочая директория
    """
    
    def __init__(self, command: List[str], current_dir: str):
        """
        Инициализация команды TAR.
        
        Args:
            command (List[str]): Полная команда с аргументами
            current_dir (str): Текущая рабочая директория
        """
        self.args = command[1:]
        self.current_dir = current_dir

    def command_tar(self, args: List[str], current_dir: str):
        """
        Создает tar.gz архив из указанной директории.
        
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
            raise ValueError("Недостаточно аргументов. Использование: tar <folder> <archive.tar.gz>")
        
        folder_path = make_path(current_dir=current_dir, path=args[0])
        archive_path = make_path(current_dir=current_dir, path=args[1])
        
        # Проверяем существование папки
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Папка {args[0]} не найдена")
        
        if not os.path.isdir(folder_path):
            raise ValueError(f"{args[0]} не является папкой")
        
        # Проверяем расширение архива, добавляем .tar.gz если нужно
        if not archive_path.endswith('.tar.gz') and not archive_path.endswith('.tgz'):
            archive_path += '.tar.gz'
        
        try:
            # Создаем TAR.GZ архив
            with tarfile.open(archive_path, 'w:gz') as tar:
                tar.add(folder_path, arcname=os.path.basename(folder_path))
            
            return f"TAR.GZ архив создан: {folder_path} -> {archive_path}"
        
        except PermissionError:
            return f"Ошибка: Нет прав доступа для создания архива"
        except Exception as e:
            return f"Ошибка при создании TAR.GZ архива: {e}"


class CommandUNTAR:
    """
    Класс для реализации команды UNTAR - распаковки tar.gz архивов.
    
    Attributes:
        args (List[str]): Аргументы команды
        current_dir (str): Текущая рабочая директория
    """
    
    def __init__(self, command: List[str], current_dir: str):
        """
        Инициализация команды UNTAR.
        
        Args:
            command (List[str]): Полная команда с аргументами
            current_dir (str): Текущая рабочая директория
        """
        self.args = command[1:]
        self.current_dir = current_dir

    def command_untar(self, args: List[str], current_dir: str):
        """
        Распаковывает tar.gz архив в текущую директорию.
        
        Args:
            args (List[str]): Аргументы команды
            current_dir (str): Текущая рабочая директория
            
        Returns:
            str: Сообщение о результате распаковки
            
        Raises:
            ValueError: При недостатке аргументов или если файл не является tar архивом
            FileNotFoundError: Если архив не существует
            PermissionError: Если нет прав доступа
            tarfile.ReadError: Если архив поврежден
        """
        if args[0] == None:
            raise ValueError("Недостаточно аргументов. Использование: untar <archive.tar.gz>")
        
        archive_path = make_path(current_dir=current_dir, path=args[0])
        
        # Проверяем существование архива
        if not os.path.exists(archive_path):
            raise FileNotFoundError(f"Архив {args[0]} не найден")
        
        # Проверяем, что это tar архив
        if not tarfile.is_tarfile(archive_path):
            raise ValueError(f"{args[0]} не является TAR архивом")
        
        try:
            # Распаковываем TAR.GZ архив в текущую директорию
            with tarfile.open(archive_path, 'r:gz') as tar:
                tar.extractall(current_dir)
            
            return f"TAR.GZ архив распакован: {archive_path} -> {current_dir}"
        
        except PermissionError:
            return f"Ошибка: Нет прав доступа для распаковки архива"
        
        except tarfile.ReadError:
            return f"Ошибка: Файл поврежден или не является TAR.GZ архивом"
        
        except Exception as e:
            return f"Ошибка при распаковке TAR.GZ архива: {e}"