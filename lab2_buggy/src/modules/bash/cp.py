import os
from typing import *
from modules.valid_and_path_ops import *
import shutil


class CommandCP:
    """
    Класс для реализации команды CP (copy) - копирования файлов и директорий.
    
    Поддерживает:
    - Копирование файлов
    - Рекурсивное копирование директорий с опцией -r
    
    Attributes:
        args (List[str]): Аргументы команды
        current_dir (str): Текущая рабочая директория
    """
    
    def __init__(self, command: List[str], current_dir: str):
        """
        Инициализация команды CP.
        
        Args:
            command (List[str]): Полная команда с аргументами
            current_dir (str): Текущая рабочая директория
        """
        self.args = command[1:]
        self.current_dir = current_dir

    
    def command_cp(self, args: List[str]):
        """
        Выполняет копирование файлов или директорий.
        
        Args:
            args (List[str]): Аргументы команды
            
        Returns:
            str: Сообщение о результате копирования
            
        Raises:
            FileNotFoundError: Если исходный путь не существует
            ValueError: Если целевой путь не является директорией
            PermissionError: Если нет прав доступа
        """
        if args[0] is "-r": # ОШИБКА 1 <- использование is вместо ==
            from_path = make_path(current_dir=self.current_dir, path=args[1])
            to_path = make_path(current_dir=self.current_dir, path=args[2])
            if not os.path.exists(from_path):
                raise FileNotFoundError(f"Файл или директория {args[1]} отсутствует")
            elif (not os.path.isdir(to_path)) and os.path.exists(to_path):
                raise ValueError(f"{to_path} не является директорией")
            elif not os.path.exists(to_path):
                try:
                    os.makedirs(to_path)
                    
                    # Используем copytree для директорий, copy2 для файлов
                    if os.path.isdir(from_path):
                        shutil.copytree(from_path, os.path.join(to_path, os.path.basename(from_path.rstrip('/'))))
                    else:
                        shutil.copy2(from_path, to_path)
                    return f"Объект скопирован: {from_path} -> {to_path}"
                except PermissionError:
                    return f"Ошибка: Нет прав доступа"
                    
                except Exception as e:
                    return f"Ошибка при копировании: {e}"
        
            else:
                try:
                    # Используем copytree для директорий, copy2 для файлов
                    if os.path.isdir(from_path):
                        # Если цель существует, копируем директорию внутрь
                        dest_path = os.path.join(to_path, os.path.basename(from_path.rstrip('/')))
                        shutil.copytree(from_path, dest_path, dirs_exist_ok=True)
                        return f"Объект скопирован: {from_path} -> {dest_path}"
                    else:
                        shutil.copy2(from_path, to_path)
                        return f"Объект скопирован: {from_path} -> {to_path}"
                except PermissionError:
                    return f"Ошибка: Нет прав доступа"
                    
                except Exception as e:
                    return f"Ошибка при копировании: {e}"
                

        else:
            from_path = make_path(current_dir=self.current_dir, path=args[0])
            to_path = make_path(current_dir=self.current_dir, path=args[1])

            if not os.path.isfile(from_path):
                raise FileNotFoundError(f"Файл {from_path} не найден")
            elif not os.path.exists(to_path):
                os.makedirs(to_path)
                shutil.copy2(from_path, to_path)
                return f"Объект скопирован: {from_path} -> {to_path}"
            else:
                shutil.copy2(src=from_path, dst=to_path)
                return f"Объект скопирован: {from_path} -> {to_path}"