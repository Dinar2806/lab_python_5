import os
import re
from typing import List

from modules.valid_and_path_ops import *


class CommandGREP:
    """
    Класс для реализации команды GREP - поиска текста в файлах по шаблону.
    
    Поддерживает:
    - Регулярные выражения
    - Рекурсивный поиск с опцией -r
    - Поиск без учета регистра с опцией -i
    
    Attributes:
        args (List[str]): Аргументы команды
        current_dir (str): Текущая рабочая директория
    """
    
    def __init__(self, command: List[str], current_dir: str):
        """
        Инициализация команды GREP.
        
        Args:
            command (List[str]): Полная команда с аргументами
            current_dir (str): Текущая рабочая директория
        """
        self.args = command[1:]
        self.current_dir = current_dir

    def command_grep(self, args: List[str], current_dir: str):
        """
        Выполняет поиск текста в файлах по шаблону.
        
        Args:
            args (List[str]): Аргументы команды
            current_dir (str): Текущая рабочая директория
            
        Returns:
            str: Результаты поиска в формате "файл | номер строки | содержимое"
            
        Raises:
            ValueError: При недостатке аргументов или ошибке в регулярном выражении
            FileNotFoundError: Если путь поиска не существует
            PermissionError: Если нет прав доступа к файлу
            IOError: При ошибках чтения файла
        """
        if args[1] == None:
            raise ValueError("Недостаточно аргументов. Использование: grep [-r] [-i] <pattern> <path>")
        
        recursive = False
        ignore_case = False
        pattern_index = 0
        path_index = 1
        
        i = 0
        while i < len(args) and args[i].startswith('-'):
            if args[i] == '-r':
                recursive = True
                pattern_index += 1
                path_index += 1
            elif args[i] == '-i':
                ignore_case = True
                pattern_index += 1
                path_index += 1
            elif args[i] == '-ri' or args[i] == '-ir':
                recursive = True
                ignore_case = True
                pattern_index += 1
                path_index += 1
            else:
                raise ValueError(f"Неизвестная опция {args[i]}")
            i += 1
        
        if len(args) - i < 2:
            raise ValueError("Недостаточно аргументов. Использование: grep [-r] [-i] <pattern> <path>")
        
        pattern = args[pattern_index]
        path_arg = args[path_index]
        
        search_path = make_path(current_dir=current_dir, path=path_arg)
        
        if not os.path.exists(search_path):
            raise FileNotFoundError(f"Путь {search_path} не существует")
        
        flags = re.IGNORECASE if ignore_case else 0
        try:
            regex = re.compile(pattern, flags)
        except re.error as e:
            raise ValueError(f"Ошибка в регулярном выражении: {e}")
        
        results = self._search_files(regex, search_path, recursive)
        if not results:
            return "Совпадений не найдено"
        
        output = []
        for file_path, line_num, line_content in results:
            rel_path = os.path.relpath(file_path, current_dir)
            output.append(f"{rel_path} | {line_num} line | {line_content.strip()}")
        
        return "\n".join(output)

    def _search_files(self, regex: re.Pattern, search_path: str, recursive: bool) -> List[tuple]:
        """
        Рекурсивно ищет совпадения в файлах.
        
        Args:
            regex (re.Pattern): Скомпилированное регулярное выражение
            search_path (str): Путь для поиска
            recursive (bool): Флаг рекурсивного поиска
            
        Returns:
            List[tuple]: Список кортежей (путь_к_файлу, номер_строки, содержимое_строки)
        """
        results = []
        
        if os.path.isfile(search_path):
            results.extend(self._search_in_file(regex, search_path))
        elif os.path.isdir(search_path):
            if recursive:
                for root, dirs, files in os.walk(search_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        if self._is_text_file(file_path):
                            results.extend(self._search_in_file(regex, file_path))
            else:
                for item in os.listdir(search_path):
                    item_path = os.path.join(search_path, item)
                    if os.path.isfile(item_path) and self._is_text_file(item_path):
                        results.extend(self._search_in_file(regex, item_path))
        else:
            raise ValueError(f"Путь {search_path} не является файлом или директорией")
        
        return results

    def _search_in_file(self, regex: re.Pattern, file_path: str) -> List[tuple]:
        """
        Ищет совпадения в одном файле.
        
        Args:
            regex (re.Pattern): Скомпилированное регулярное выражение
            file_path (str): Путь к файлу
            
        Returns:
            List[tuple]: Список найденных совпадений в файле
        """
        results = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    if regex.search(line):
                        results.append((file_path, line_num, line))
        except PermissionError:
            raise PermissionError(f"Нет прав доступа к файлу {file_path}")
        except IOError as e:
            raise IOError(f"Ошибка чтения файла {file_path}: {e}")
        
        return results

    def _is_text_file(self, file_path: str) -> bool:
        """
        Проверяет, является ли файл текстовым по расширению.
        
        Args:
            file_path (str): Путь к файлу
            
        Returns:
            bool: True если файл считается текстовым
        """
        text_extensions = {'.txt', '.py', '.js', '.html', '.css', '.json', '.xml', 
                          '.md', '.csv', '.log', '.conf', '.cfg', '.ini', '.sh', 
                          '.bat', '.c', '.cpp', '.h', '.java', '.php', '.rb', 
                          '.go', '.rs', '.ts', '.yml', '.yaml'}
        
        _, ext = os.path.splitext(file_path)
        return ext.lower() in text_extensions or ext == ''