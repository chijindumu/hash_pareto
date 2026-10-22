#!/usr/bin/env python3
import json

nb_path = 'notebook/hashpareto.ipynb'
nb = json.load(open(nb_path))

# Fix cell 26 - uncomment the display lines
c26 = nb['cells'][26]
src = ''.join(c26['source'])
lines = src.split('\n')

new_lines = []
for line in lines:
    stripped = line.strip()
    # Check if this line is a comment that contains display(Image
    if stripped.startswith('#') and 'display(' in stripped:
        # Remove the # comment prefix but keep the rest
        new_line = stripped[1:].lstrip()  # removes '#' and leading space
        # Preserve original leading whitespace
        leading = line[:len(line) - len(line.lstrip())]
        new_lines.append(leading + new_line)
    else:
        new_lines.append(line)

c26['source'] = new_lines

with open(nb_path, 'w') as f:
    json.dump(nb, f, indent=1)

print('Fixed cell 26 - uncommented display lines')