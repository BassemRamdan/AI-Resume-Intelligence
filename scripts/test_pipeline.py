import sys
import os
import json
import subprocess
from pathlib import Path

def run_command(cmd, input_data=None):
    print(f"\n> Running: {' '.join(cmd)}")
    try:
        if input_data:
            result = subprocess.run(cmd, input=input_data.encode(), capture_output=True, check=True)
        else:
            result = subprocess.run(cmd, capture_output=True, check=True)
            
        output = result.stdout.decode()
        return output
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e.stderr.decode()}")
        sys.exit(1)

def extract_json_between_markers(text, start_marker, end_marker):
    start_idx = text.find(start_marker)
    end_idx = text.find(end_marker)
    if start_idx == -1 or end_idx == -1:
        return None
    json_str = text[start_idx + len(start_marker):end_idx].strip()
    return json.loads(json_str)

def main(pdf_path):
    if not os.path.exists(pdf_path):
        print(f"Error: {pdf_path} not found.")
        sys.exit(1)
        
    print(f"=== Starting E2E Pipeline Test for {pdf_path} ===")
    
    script_dir = Path(__file__).parent.parent / "lib" / "ai"
    
    # 1. Extraction
    output = run_command([sys.executable, str(script_dir / "extract_resume.py"), pdf_path])
    profile = extract_json_between_markers(output, "===START===", "===END===")
    if not profile:
        print("Failed to extract profile")
        sys.exit(1)
        
    print("\n--- Extracted Profile Snippet ---")
    print(json.dumps({
        "skills_count": len(profile.get("skills", [])),
        "experience_count": len(profile.get("experience", [])),
        "projects_count": len(profile.get("projects", [])),
    }, indent=2))
    
    # Save temp profile
    temp_profile = "temp_test_profile.json"
    with open(temp_profile, "w") as f:
        json.dump(profile, f)
        
    # 2. Career Map
    output = run_command([sys.executable, str(script_dir / "career_engine.py"), temp_profile])
    career_map = extract_json_between_markers(output, "===START===", "===END===")
    
    print("\n--- Career Map Snippet ---")
    print(json.dumps(career_map.get("paths", [])[:2], indent=2))
    
    # Update profile with targets
    if career_map and career_map.get("paths"):
        profile["job_targets"] = [p["title"] for p in career_map["paths"][:3]]
    with open(temp_profile, "w") as f:
        json.dump(profile, f)
        
    # 3. Find Jobs
    output = run_command([sys.executable, str(script_dir / "job_engine.py"), "find", temp_profile])
    jobs_data = extract_json_between_markers(output, "===JOBS_START===", "===JOBS_END===")
    
    print("\n--- Jobs Snippet ---")
    if jobs_data and "error" in jobs_data:
        print(f"Job Engine returned error: {jobs_data['error']}")
    else:
        jobs = jobs_data.get("jobs", []) if isinstance(jobs_data, dict) else jobs_data
        print(f"Found {len(jobs)} matched jobs.")
        if jobs:
            print(json.dumps({
                "top_job_title": jobs[0].get("job_details", {}).get("title"),
                "top_job_score": jobs[0].get("overall_match_score"),
                "matched_skills": len(jobs[0].get("matched_skills", []))
            }, indent=2))
            
    print("\n=== E2E Test Completed Successfully ===")
    os.remove(temp_profile)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_pipeline.py <path_to_pdf>")
        sys.exit(1)
    main(sys.argv[1])
