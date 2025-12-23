import os
from typing import *
from modules.valid_and_path_ops import *
import shutil


class CommandRM:
    """
    Класс для реализации команды RM (remove) - удаления файлов и директорий.
    
    Поддерживает:
    - Удаление файлов
    - Рекурсивное удаление директорий с опцией -r
    
    Attributes:
        args (List[str]): Аргументы команды
        current_dir (str): Текущая рабочая директория
    """
    
    def __init__(self, command: List[str], current_dir: str):
        """
        Инициализация команды RM.
        
        Args:
            command (List[str]): Полная команда с аргументами
            current_dir (str): Текущая рабочая директория
        """
        self.args = command[1:]
        self.current_dir = current_dir

    def command_rm(self, args: List[str], current_dir: str) -> str:
        """
        Выполняет удаление файлов или директорий.
        
        Args:
            args (List[str]): Аргументы команды
            current_dir (str): Текущая рабочая директория
            
        Returns:
            str: Сообщение о результате удаления
            
        Raises:
            ValueError: При попытке удалить корневую или родительскую директорию
            FileNotFoundError: Если путь не существует
            ValueError: При попытке удалить директорию без опции -r
        """
        path_to_remove: str
        if args[0] == "-r":
            path_to_remove = args[1]
            if path_to_remove == "/" or path_to_remove == "..":
                raise ValueError("Нельзя удалять корневой или родительский каталог")
            else:
                path = make_path(current_dir=current_dir, path=path_to_remove)
                print(f"Вы уверены что хотите удалить директорию {path} со всем ее содержимым? [Y/n]\n")
                ans = input("Ваш ответ: ")
                if ans == "Y":
                    try:
                        if os.path.exists(path):
                            shutil.rmtree(path)
                            return f"Директория '{path}' и все её содержимое удалены"
                            
                        else:
                            return f"Директория '{path}' не существует"
                            
                    except Exception as e:
                        print(f"Ошибка при удалении '{path}': {e}")
                        return False
                
                elif ans == "n":
                    return f""
        else:
            path_to_remove = args[0]
            path = make_path(path=path_to_remove, current_dir=self.args)  # ОШИБКА 3 <- перепутанные аргументы
            if os.path.isdir(path):
                raise ValueError(f"{path} является директорией(используйте ключ -r для рекурсивного удаления директории и ее содержимого)")


            elif not os.path.exists(path=path):
                raise FileNotFoundError(f"Пути {path} не существует")

            else:
                os.remove(path)
                return f"Файл {path} успешно удален"