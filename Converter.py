import json
import os

def convert_typing_field(pokedex):
    for pokemon, data in pokedex.items():
        if "typing" in data and isinstance(data["typing"], str):
            types_array = [t.strip() for t in data["typing"].split("/")]
            data["typing"] = types_array
    return pokedex

file_names = ["Uber.json", "OU.json", "UU.json"]

for file_name in file_names:
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            data = json.load(f)
        converted_data = convert_typing_field(data)
        # Option 1: Save to a new file with a prefix (so you don't overwrite the originals)
        output_file = f"converted_{file_name}"
        # Option 2: Alternatively, you could overwrite the original file by using file_name directly
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(converted_data, f, indent=2)
        print(f"Converted {file_name} to {output_file}.")
    else:
        print(f"File {file_name} not found.")
