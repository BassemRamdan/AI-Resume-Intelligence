import os
import json
import re
import glob

def clean_notebook(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    new_cells = []
    for cell in nb.get('cells', []):
        if cell['cell_type'] == 'markdown':
            # Keep only simple markdown, e.g., headers or very short sentences.
            # Let's keep only lines that start with # or are very short
            new_source = []
            for line in cell['source']:
                if line.startswith('#'):
                    new_source.append(line)
            
            if not new_source and cell['source']:
                # If no headers, just keep the first line truncated if it's too long
                first_line = cell['source'][0][:50].strip()
                if first_line:
                    new_source.append(first_line + "\n")
            
            if new_source:
                cell['source'] = new_source
                new_cells.append(cell)
                
        elif cell['cell_type'] == 'code':
            new_source = []
            for line in cell['source']:
                # Strip full-line comments, but keep inline comments to avoid breaking code that might rely on formatting
                stripped = line.lstrip()
                if stripped.startswith('#') and not stripped.startswith('# TODO'):
                    continue
                new_source.append(line)
            
            if new_source: # Only keep code cells that aren't empty after cleaning
                cell['source'] = new_source
                
            # Keep all code cells, even empty ones if they had logic (though they shouldn't be empty)
            new_cells.append(cell)
            
    nb['cells'] = new_cells
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)

if __name__ == "__main__":
    notebooks = glob.glob("notebooks/*.ipynb")
    for nb in notebooks:
        print(f"Cleaning {nb}...")
        clean_notebook(nb)
    print("Notebooks cleaned successfully.")
