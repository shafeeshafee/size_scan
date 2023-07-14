import os
import sys
import json
from datetime import datetime
import shutil
import random
import string


def get_entry_sizes(entry):
    if entry.is_file():
        return os.path.getsize(entry.path)
    elif entry.is_dir():
        size = 0
        for sub_entry in os.scandir(entry.path):
            size += get_entry_sizes(sub_entry)
        return size


def format_size(size):
    unit = "MB"
    if size >= 1024 * 1024 * 1024:
        size /= (1024 * 1024 * 1024)
        unit = "GB"
    else:
        size /= (1024 * 1024)
    return f"{size:.2f} {unit}"


def get_entry_info(entry):
    entry_size = get_entry_sizes(entry)
    return {
        "path": entry.path,
        "size": format_size(entry_size),
        "type": "File" if entry.is_file() else "Directory"
    }


def convert_size_to_bytes(size):
    value, unit = size.split(" ")
    units = {"MB": 1, "GB": 1024}
    return float(value) * units[unit]


def generate_output(folder_path, output_path):
    entries = [get_entry_info(entry) for entry in os.scandir(folder_path)]
    sorted_entries = sorted(
        entries, key=lambda x: convert_size_to_bytes(x["size"]), reverse=True)

    with open(output_path, 'w') as output_file:
        json.dump(sorted_entries, output_file, indent=4)


def get_output_directory_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, "output")


def get_unique_filename():
    random_string = ''.join(random.choices(
        string.ascii_letters + string.digits, k=8))
    current_time = datetime.now().strftime("%I%M%S%p-%b%d%Y")
    return f"output-{random_string}-{current_time}.json"


def get_output_file_path(output_directory):
    filename = get_unique_filename()
    return os.path.join(output_directory, filename)


if len(sys.argv) > 1:
    folder_path = sys.argv[1]
else:
    folder_path = input("Enter the folder path: ")

folder_path = os.path.abspath(folder_path)
output_directory = get_output_directory_path()
output_file_path = get_output_file_path(output_directory)

generate_output(folder_path, output_file_path)

os.system(f'notepad.exe {output_file_path}')

file_name = os.path.basename(output_file_path)
print(f"Successfully generated and saved. Results stored in: '{file_name}'")
