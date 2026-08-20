import json

with open('c:/university/neuroconnect summerschool/project/project_implementation.ipynb', encoding='utf-8') as f:
    nb = json.load(f)

with open('c:/university/neuroconnect summerschool/project/md_only.txt', 'w', encoding='utf-8') as f:
    for i, c in enumerate(nb['cells']):
        if c['cell_type'] == 'markdown':
            f.write(f"--- Cell {i} : markdown ---\n")
            f.write(''.join(c.get('source', [])))
            f.write("\n\n")
