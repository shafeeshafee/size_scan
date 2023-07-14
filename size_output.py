import os
import sys
import json


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


if len(sys.argv) > 1:
    folder_path = sys.argv[1]
else:
    folder_path = input("Enter the folder path: ")

folder_path = os.path.abspath(folder_path)

output_path = 'output.json'

generate_output(folder_path, output_path)

os.system(f'notepad.exe {output_path}')

os.remove(output_path)
