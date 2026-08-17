
import os
import subprocess
import sys

notebooks = [
    "05_FineTuning.ipynb",
    "06_Embeddings_Similarity.ipynb"
]

for nb in notebooks:
    print(f"Starting {nb}...", flush=True)
    try:
        subprocess.run(["python", "-m", "jupyter", "nbconvert", "--to", "notebook", "--execute", "--inplace", f"notebooks/{nb}"], check=True)
        print(f"Successfully finished {nb}", flush=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing {nb}: {e}", file=sys.stderr, flush=True)
        # Continuing to the next notebook even if one fails

