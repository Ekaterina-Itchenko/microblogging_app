import os
import sys

from main import populate_db

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
AVAILABLE_FLAGS = ("-n",)

if __name__ == "__main__":
    config_list = sys.argv
    for ind in range(1, len(config_list), 2):
        flag = config_list[ind]
        if flag not in AVAILABLE_FLAGS:
            raise ValueError('Invalid flag. Available flags: "-n".')
        elif flag == "-n":
            num_data = config_list[ind + 1]
    if not num_data.isalnum():
        raise ValueError('Number of generated data after flag "-n" must be ' "integer.")
    generate_number = int(num_data)
    populate_db(num=generate_number)
