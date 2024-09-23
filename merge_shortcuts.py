import zipfile
import os
import csv
import re
import xml.etree.ElementTree as ET

files = {"original": "German Standard.afshort",
         "update": "SFX Affinity Photo Pro Shortcuts V2.afshort",
         "new": "SFX Affinity Photo Pro German Shortcuts V2.afshort"
}

items = ("type", "command", "scope", "tool", "functionEnum", "key", "char", "modifierKeys")

header = """<?xml version="1.0" encoding="utf-8"?>
<Workspace>
	<Shortcuts Version="0">\n"""

footer = """	</Shortcuts>
</Workspace>\n"""

def update_file(filename):
    files = {}
    commands = {}

    for file in ("original", "update"):
        commands[file] = {}
        with open(f"./{file}/{filename}", "r", encoding="utf-8") as infile:
            files[file] = infile.readlines()[3:-2] # ignore header and footer

        for line in files[file]:
            xml = ET.fromstring(line).attrib
            if "command" in xml:
                parameters = xml["command"].split(", ")
                xml["command"], xml["scope"] = parameters[:2] # Discard Version, Culture, PublicKeyToken parameters
            commands[file][tuple(xml.get(item) for item in items[:5])] = [xml.get(item) for item in items[5:]] + [line]
    
    new = {}
    differences = {}
    output = []
    seen_commands = set()
    duplicate_commands = []
    update_commands = commands["update"].keys()

    for command, details in commands["original"].items():
        if command in update_commands: # Either: The same command is defined in both files
            up_details = commands["update"][command]
            if details[:3]==up_details[:3]: # key, char, modifiers are identical --> both files are identical
                output.append(details[3]) # keep original line and add it to output
            else:                      # Or: The updated version is different from the original  
                output.append(up_details[3]) # replace line with update and add it to output
                differences[command] = details[:3] + up_details[:3] # document the differences
            del(commands["update"][command]) # Remove this entry from the update list
        else:                          # Or: The command is only found in the original file
            output.append(details[3])  # Then copy that line to the output file
        seen_commands.add(command)
    for command, details in commands["update"].items(): # Whatever remains in update_commands is unique to it
        output.append(details[3])            # so add those lines to the output file
        if command in seen_commands:         # However, it's possible that it uses an already-used key combo
            duplicate_commands.append(command) # so make a note of that
    
    with open(f"./new/{filename}", "w", encoding="utf-8") as outfile:
        outfile.write(header)
        outfile.writelines(output)
        outfile.write(footer)
    
    with open(f"./new/{filename[:-4]}.csv", "w", encoding="utf-8", newline="") as outfile:
        writer = csv.writer(outfile, delimiter=";")
        writer.writerow(("type", "command", "scope", "tool", "functionEnum", "orig_key", "orig_char", "orig_modifierKeys", "new_key", "new_char", "new_modifierKeys"))
        for key, value in differences.items():
            writer.writerow(list(key) + value)
    
    with open(f"./new/{filename[:-4]}.dup", "w", encoding="utf-8", newline="") as outfile:
        writer = csv.writer(outfile, delimiter=";")
        writer.writerow(("key", "char", "modifierKeys"))
        for item in duplicate_commands:
            writer.writerow(item)
    return

    


for file in ("original", "update"):
    path = f"./{file}"
    if not os.path.exists(path):
        os.mkdir(path)
    with zipfile.ZipFile(files[file], mode="r") as zip:
        # Overwrite any files already present in that directory
        zip.extractall(f"./{file}")

if not os.path.exists("./new"):
    os.mkdir("./new")

filenames = os.listdir("./original")

for filename in filenames:
    update_file(filename)
