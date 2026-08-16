import json

with open('notebooks/06_Embeddings_Similarity.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = cell['source']
        for i in range(len(source)):
            if "clean = re.sub(r'[\\r\\n" in source[i]:
                source[i] = "    clean = re.sub(r'[\\r\\n]+', '\\n', text)\n"
            elif "]+', '\\n', text)" in source[i]:
                source[i] = ""
            if "from lib.ai.extract_resume" in source[i]:
                source[i] = "import sys, os\nsys.path.append(os.path.abspath('..'))\nfrom lib.resume import split_into_sections\n"
            if "from lib.ai.skill_ontology" in source[i]:
                source[i] = "import sys, os\nsys.path.append(os.path.abspath('..'))\nfrom lib.skill_ontology import normalize_skill\n"

with open('notebooks/06_Embeddings_Similarity.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
