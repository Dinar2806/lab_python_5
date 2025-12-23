import os
import stat


from typing import *
from modules.valid_and_path_ops import *

from datetime import datetime


class CommandLS:
    """
    Класс для реализации команды LS (list) - вывода содержимого директории.
    
    Поддерживает:
    - Простой вывод списка файлов
    - Детальный вывод с правами доступа и метаданными с опцией -l
    - Цветовое выделение директорий
    
    Attributes:
        args (List[str]): Аргументы команды
        current_dir (str): Текущая рабочая директория
    """
    
    def __init__(self, command: List[str], current_dir: str):
        """
        Инициализация команды LS.
        
        Args:
            command (List[str]): Полная команда с аргументами
            current_dir (str): Текущая рабочая директория
        """
        self.args = command[1:]
        self.current_dir = current_dir

    
    def ls_with_rights(self, path:str, current_dir: str):
        """
        Выводит содержимое директории с детальной информацией о правах доступа.
        
        Args:
            path (str): Путь к директории
            current_dir (str): Текущая рабочая директория
            
        Returns:
            str: Форматированный вывод с правами доступа и метаданными
        """
        directory = make_path(current_dir=current_dir, path=path)
    
        def get_file_type(mode):
            if stat.S_ISDIR(mode):
                return 'd'
            elif stat.S_ISREG(mode):
                return '-'
            elif stat.S_ISLNK(mode):
                return 'l'
            else:
                return '?'
        
        def get_permissions(mode):
            perm_str = ''
            for type in "USR", "GRP", "OTH":
                for perms in "R", "W", "X":
                    if mode & getattr(stat, f"S_I{perms}{type}"):
                        perm_str += perms.lower()
                    else:
                        perm_str += '-'
            return perm_str
        
        try:
            items = os.listdir(directory)
            items.sort()
            
            result = []
            for item in items:
                item_path = os.path.join(directory, item)
                
                try:
                    stat_info = os.stat(item_path)
                    
                    file_type = get_file_type(stat_info.st_mode)
                    permissions = get_permissions(stat_info.st_mode)
                    nlink = stat_info.st_nlink
                    size = stat_info.st_size
                    mtime = datetime.fromtimestamp(stat_info.st_mtime).strftime("%b %d %H:%M")
                    
                    # Для симлинков
                    display_name = item
                    if file_type == 'l':
                        try:
                            target = os.readlink(item_path)
                            display_name = f"{item} -> {target}"
                        except OSError:
                            display_name = f"{item} -> [broken]"
                    
                    line = f"{file_type}{permissions} {nlink:>2} {stat_info.st_uid:>5} {stat_info.st_gid:>5} {size:>8} {mtime} {display_name}"
                    result.append(line)
                    
                except PermissionError:
                    result.append(f"?????????? ? ? ? ? ? ??? ?? ???? {item} (Permission denied)")
                except OSError as e:
                    result.append(f"?????????? ? ? ? ? ? ??? ?? ???? {item} (Error: {e})")
            
            return "\n".join(result)
            
        except Exception as e:
            return f"Error: {e}"

        
    
    def ls_without_rgihts(self, path: str, current_dir: str):
        """
        Выводит простое содержимое директории без детальной информации.
        
        Args:
            path (str): Путь к директории
            current_dir (str): Текущая рабочая директория
            
        Returns:
            List[str]: Список файлов и директорий
            
        Raises:
            FileNotFoundError: Если директория не существует
            ValueError: Если путь не является директорией
        """
        if path == None:
            return os.listdir(current_dir)
        else:
            res_path = make_path(current_dir, path)
            if not os.path.exists(res_path):
                raise FileNotFoundError(f"Несуществующая директория {res_path}")
            elif not os.path.isdir(res_path):
                raise ValueError(f"{res_path} не является директорией")
            else:
                return os.listdir(res_path)
            


    def command_ls(self, args: List[str]) -> str:
        """
        Выполняет команду LS с учетом переданных аргументов.
        
        Args:
            args (List[str]): Аргументы команды
            
        Returns:
            str: Результат выполнения команды
        """
        str = ""
        if args[0] == "-l":
            return self.ls_with_rights(path=args[1], current_dir=self.current_dir)
        else:
            dir_path = make_path(self.current_dir, args[0])
            output = self.ls_without_rgihts(path=args[0],current_dir=self.current_dir)
            for obj_dir in colorize_dirs(output, dir_path):
                str += f"{obj_dir}  "
            logging.info(output)
            return str