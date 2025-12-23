from typing import *

import logging

from modules.bash.ls import CommandLS
from modules.bash.cd import CommandCD
from modules.bash.cp import CommandCP
from modules.bash.mv import CommandMV
from modules.bash.rm import CommandRM
from modules.bash.cat import CommandCAT

from modules.bash.grep import CommandGREP
from modules.bash.history import CommandHISTORY
from modules.bash.tar import CommandTAR, CommandUNTAR
from modules.bash.zip import CommandUNZIP, CommandZIP
from modules.bash.undo import CommandUNDO

from modules.valid_and_path_ops import *


# logger = logging.getLogger("my_app")
# logger.setLevel(logging.DEBUG)

# file_handler = logging.FileHandler("")

# formatter = logging.Formatter(
#     '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     datefmt='%Y-%m-%d %H:%M:%S'
# )
# file_handler.setFormatter(formatter)

class FullCycle:

    def __init__(self, input_command: str, current_directory: str):
        self.input_command: str = input_command
        self.current_directory: str = current_directory

        # self.tokenized_command: List[str] = shlex_tokenization(input_command)
        
    
    def full_cycle(self, input_command: str, current_directory: str) -> List[str]:
        
        
        output: List[str]

        console_output: str
        new_directory: str
        
        tokenized_command: List[str] = shlex_tokenization(input=input_command)
        command_name: str = tokenized_command[0]
        arguments: List[str] = tokenized_command[2:] # ОШИБКА 2 <- неправильное разбиение входных данных (нужно tokenized_command[1:])

        if not commands_list.__contains__(command_name):
            raise ValueError(f"127: Команда: \"{command_name}\" не найдена")
        
        
            
        
        match command_name:
            case "ls":
                ls = CommandLS(command=tokenized_command, current_dir=current_directory)
                res = ls.command_ls(args=ls.args)
                new_dir = current_directory
                output = [res, new_dir]
                return output
            case "cd":
                cd = CommandCD(command=tokenized_command, current_dir=current_directory)
                res = None
                new_dir = cd.command_cd(args=cd.args, current_dir=current_directory)
                output = [res, new_dir]
                logging.info(f"directory changed to {new_dir}")
                return output

            case "cat":
                cat = CommandCAT(command=tokenized_command, current_dir=current_directory)
                res = cat.print_file_content(path=cat.args[0], current_dir=current_directory)
                new_dir = current_directory
                output = [res, new_dir]
                logging.info(res)
                return output

            case "cp":
                cp = CommandCP(command=tokenized_command, current_dir=current_directory)
                res = cp.command_cp(args=cp.args)
                new_dir = current_directory
                output = [res, new_dir]
                logging.info(res)
                return output
            case "mv":
                mv = CommandMV(command=tokenized_command, current_dir=current_directory)
                res = mv.command_mv(args=mv.args, current_dir=current_directory)
                new_dir = current_directory
                output = [res, new_dir]
                logging.info(res)
                return output

            case "rm":
                rm = CommandRM(command=tokenized_command, current_dir=current_directory)
                res = rm.command_rm(args=rm.args, current_dir=self.current_directory)
                new_dir = current_directory
                output = [res, new_dir]
                logging.info(res)
                return output

            case "zip":
                zip = CommandZIP(command=tokenized_command, current_dir=current_directory)
                res = zip.command_zip(args=zip.args, current_dir=zip.current_dir)
                new_dir = current_directory
                output = [res, new_dir]
                logging.info(res)
                return output

            case "unzip":
                unzip = CommandUNZIP(command=tokenized_command, current_dir=current_directory)
                res = unzip.command_unzip(args=unzip.args, current_dir=unzip.current_dir)
                new_dir = current_directory
                output = [res, new_dir]
                logging.info(res)
                return output

            case "tar":
                tar = CommandTAR(command=tokenized_command, current_dir=current_directory)
                res = tar.command_tar(args=tar.args, current_dir=tar.current_dir)
                new_dir = current_directory
                output = [res, new_dir]
                logging.info(res)
                return output

            case "untar":
                untar = CommandUNTAR(command=tokenized_command, current_dir=current_directory)
                res = untar.command_untar(args=untar.args, current_dir=untar.current_dir)
                new_dir = current_directory
                output = [res, new_dir]
                logging.info(res)
                return output

            case "grep":
                grep = CommandGREP(command=tokenized_command, current_dir=current_directory)
                res = grep.command_grep(args=grep.args, current_dir=grep.current_dir)
                new_dir = current_directory
                output = [res, new_dir]
                logging.info(res)
                return output

            case "undo":
                pass

            case "history":
                history = CommandHISTORY(command=tokenized_command, current_dir=current_directory)
                res = history.command_history(args=history.args, current_dir=history.current_dir)
                new_dir = current_directory
                output = [res, new_dir]
                logging.info("Success history output")
                return output