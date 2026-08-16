import os
import sys
import glob
import random
import subprocess
import json
from pathlib import Path

def extract_json_between_markers(text, start_marker, end_marker):
    start_idx = text.find(start_marker)
    end_idx = text.find(end_marker)
    if start_idx == -1 or end_idx == -1:
        return None
    json_str = text[start_idx + len(start_marker):end_idx].strip()
    try:
        return json.loads(json_str)
    except:
        return None

def main():
    data_dir = r"C:\NTI 2026\NTI-HCI\data\data"
    all_pdfs = glob.glob(os.path.join(data_dir, "**", "*.pdf"), recursive=True)
    if not all_pdfs:
        print("No PDFs found in dataset.")
        sys.exit(1)
        
    random.seed(42) # For reproducible "random" selection
    selected_pdfs = random.sample(all_pdfs, 3)
    
    script_dir = Path(r"C:\NTI 2026\NTI-HCI\AI-Resume-Intelligence\lib\ai")
    results = []
    
    for pdf in selected_pdfs:
        print(f"Testing {pdf}...")
        
        # Run extraction
        try:
            result = subprocess.run([sys.executable, str(script_dir / "extract_resume.py"), pdf], capture_output=True, check=True, text=True)
            profile = extract_json_between_markers(result.stdout, "===START===", "===END===")
        except Exception as e:
            profile = {"error": str(e)}
            
        results.append({
            "pdf": os.path.basename(pdf),
            "category": os.path.basename(os.path.dirname(pdf)),
            "skills": profile.get("skills", []) if profile else [],
            "experience": profile.get("experience", []) if profile else [],
            "projects": profile.get("projects", []) if profile else []
        })
        
    with open("forensic_results.json", "w") as f:
        json.dump(results, f, indent=2)
        
    print("Forensic test complete.")

if __name__ == "__main__":
    main()
