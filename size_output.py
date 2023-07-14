import os
import sys
import json
from datetime import datetime
import shutil


def get_entry_sizes(entry):
    if entry.is_file():
        return os.path.getsize(entry.path)
    elif entry.is_dir():
        size = 0
        for sub_entry in os.scandir(entry.path):
            size += get_entry_sizes(sub_entry)
        return size


def format_size(size):
    if size >= 1024 * 1024 * 1024:
        size = size / (1024 * 1024 * 1024)
        unit = "GB"
    else:
        size = size / (1024 * 1024)
        unit = "MB"
    return f"{size:.2f} {unit}"


def get_entry_info(entry):
    entry_size = get_entry_sizes(entry)
    if entry.is_file():
        return {"path": entry.path, "size": format_size(entry_size), "type": "File"}
    elif entry.is_dir():
        return {"path": entry.path, "size": format_size(entry_size), "type": "Directory"}


def convert_size_to_bytes(size):
    value, unit = size.split(" ")
    units = {"MB": 1, "GB": 1024}
    return float(value) * units[unit]


def generate_output(folder_path, output_path):
    entries = []
    for entry in os.scandir(folder_path):
        entries.append(get_entry_info(entry))

    sorted_entries = sorted(
        entries, key=lambda x: convert_size_to_bytes(x["size"]), reverse=True)

    with open(output_path, 'w') as output_file:
        json.dump(sorted_entries, output_file, indent=4)


def get_output_directory_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_directory = os.path.join(script_dir, "output")
    os.makedirs(output_directory, exist_ok=True)
    return output_directory


def get_output_file_path():
    current_time = datetime.now().strftime("%I%M%S%p-%b%d%Y")
    return os.path.join(get_output_directory_path(), f"output-{current_time}.json")


if len(sys.argv) > 1:
    folder_path = sys.argv[1]
else:
    folder_path = input("Enter the folder path: ")

folder_path = os.path.abspath(folder_path)

output_file_path = get_output_file_path()

generate_output(folder_path, output_file_path)

os.system(f'notepad.exe {output_file_path}')

save_file = input("Do you want to save the file? (y/n): ")

if save_file.lower() == "y":
    save_path = input("Enter the file path to save the JSON file: ")
    save_path = os.path.abspath(save_path)
    shutil.copy2(output_file_path, save_path)

os.remove(output_file_path)
