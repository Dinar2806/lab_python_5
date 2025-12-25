import os

from typing import List

from modules.valid_and_path_ops import *

class CommandHISTORY:
    def __init__(self, command: List[str], current_dir: str):
        self.args = command[1:]
        self.current_dir = current_dir
        self.history_file = HISTORY_FILE

    def command_history(self, args: List[str], current_dir: str):
        self.history_file = HISTORY_FILE

        if args[0] == None:
            raise ValueError("Напишите конечное количество строк вывода для истории. Ожидаемый формат history <число комманд(int)>")
        
        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w', encoding='utf-8') as f:
                pass
            return "История команд пуста"
        
        
        with open(self.history_file, 'r', encoding='utf-8') as f:
            commands = [line.strip() for line in f.readlines() if line.strip()]
        
        
        if not commands:
            return "История команд пуста"
        
        if args:
            try:
                n = int(args[0])
                if n <= 0:
                    return "Количество команд должно быть положительным числом"
                
                commands = commands[-n:]

            except ValueError:
                return f"Некорректный аргумент: {args[0]}. Ожидается число"
        else:
            n = len(commands)
        

        
        result = []

        # ОШИБКА 5 <- неверное логическое условие в цикле
        for i in range(len(commands)):
            if i > n and i > 0:  # ← условие всегда True при n > 0 и i > 0
                result.append(f"{commands[i]}")

        # for cmd in commands[-n:]:
        #     result.append(f"{cmd}")
        
        return "\n".join(result)


