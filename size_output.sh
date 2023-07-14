#!/bin/bash

get_entry_sizes() {
    local entry="$1"
    if [[ -f "$entry" ]]; then
        stat -c%s "$entry"
    elif [[ -d "$entry" ]]; then
        local size=0
        while IFS= read -r -d '' sub_entry; do
            size=$((size + $(get_entry_sizes "$sub_entry")))
        done < <(find "$entry" -mindepth 1 -print0)
        echo "$size"
    fi
}

format_size() {
    local size="$1"
    local unit="MB"
    if ((size >= 1024 * 1024 * 1024)); then
        size=$(awk "BEGIN { printf \"%.2f\", $size / (1024 * 1024 * 1024) }")
        unit="GB"
    else
        size=$(awk "BEGIN { printf \"%.2f\", $size / (1024 * 1024) }")
    fi
    echo "$size $unit"
}

generate_output() {
    local folder_path="$1"
    local entries=()
    while IFS= read -r -d '' entry; do
        local size=$(get_entry_sizes "$entry")
        entries+=("$size $entry")
    done < <(find "$folder_path" -mindepth 1 -print0)
    IFS=$'\n' sorted_entries=($(printf '%s\n' "${entries[@]}" | sort -rn))
    for entry in "${sorted_entries[@]}"; do
        local size=$(cut -d " " -f 1 <<< "$entry")
        local file=$(cut -d " " -f 2- <<< "$entry")
        local formatted_size=$(format_size "$size")
        echo "$(basename "$file") - $formatted_size"
    done
}

folder_path="${1:-}"
if [[ -z "$folder_path" ]]; then
    read -r -p "Enter the folder path: " folder_path
fi

folder_path=$(realpath "$folder_path")

generate_output "$folder_path"
