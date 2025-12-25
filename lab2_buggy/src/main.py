import os
import sys
import logging



from modules.bash.ls import CommandLS
from modules.valid_and_path_ops import *
from modules.full_cycle import FullCycle
from consts import *





def main():
    current_directory: str = HOME_CATALOG
    history_file = HISTORY_FILE
    command_counter = read_last_command_number(history_file)

    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logging.info("Запуск")

    while (True):
        try:
            input_command = input(f"{current_directory} $ ")
            if input_command == "exit()":
                sys.exit()
            if not input_command:
                continue
            if input_command.isspace():
                continue

            command_counter += 1
            write_to_history(history_file, command_counter, input_command)
            
            full_cycle = FullCycle(input_command=input_command, current_directory=current_directory)
            result = full_cycle.full_cycle(full_cycle.input_command, full_cycle.current_directory)
            output = result[0]
            new_directory = result[1]
            del(input_command)
            current_directory = new_directory
            if output != None and output != "":
                print(output)
                logging.info(output)
                
        except KeyboardInterrupt:
            print("\nВыполнение прервано")
            logging.info("Выполнение прервано")
            sys.exit()
        
        except ValueError as e:
            error_message = str(e)
            print(error_message)
            logging.error(error_message)

        except PermissionError as e:
            error_message = str(e)
            print(error_message)
            logging.error(error_message)

        except FileNotFoundError as e:
            error_message = str(e)
            print(error_message)
            logging.error(error_message)

        except TypeError as e:
            error_message = str(e)
            print(error_message)
            logging.error(error_message)

        

        
        
                
    
    
if __name__ == "__main__":
    main()

