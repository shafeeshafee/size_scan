import os
import sys


def get_entry_sizes(entry):
    if entry.is_file():
        return os.path.getsize(entry.path)
    elif entry.is_dir():
        size = 0
        for sub_entry in os.scandir(entry.path):
            size += get_entry_sizes(sub_entry)
        return size


def get_entry_info(entry):
    entry_size = get_entry_sizes(entry)
    if entry.is_file():
        return (entry.path, entry_size, "File")
    elif entry.is_dir():
        return (entry.path, entry_size, "Directory")


def generate_output_file(folder_path, output_path):
    entries = []
    for entry in os.scandir(folder_path):
        entries.append(get_entry_info(entry))
    entries.sort(key=lambda x: x[1], reverse=True)

    with open(output_path, 'w') as output_file:
        for entry_path, entry_size, entry_type in entries:
            if entry_size >= 1024 * 1024 * 1024:
                size_unit = "GB"
                entry_size /= (1024 * 1024 * 1024)
            else:
                size_unit = "MB"
                entry_size /= (1024 * 1024)
            output_file.write(
                f"{entry_path}  -> {entry_size:.2f} {size_unit} ({entry_type})\n")


if len(sys.argv) > 1:
    folder_path = sys.argv[1]
else:
    folder_path = input("Enter the folder path: ")

output_path = 'output.txt'

generate_output_file(folder_path, output_path)

os.system(f'notepad.exe {output_path}')
