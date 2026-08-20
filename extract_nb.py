import json

with open('c:/university/neuroconnect summerschool/project/project_implementation.ipynb', encoding='utf-8') as f:
    nb = json.load(f)

with open('c:/university/neuroconnect summerschool/project/notebook_summary.txt', 'w', encoding='utf-8') as f:
    for i, c in enumerate(nb['cells']):
        f.write(f"--- Cell {i} : {c['cell_type']} ---\n")
        f.write(''.join(c.get('source', [])))
        f.write("\n\n")
