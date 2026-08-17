import os
import json
import traceback

# Enable debug extraction mode for tests
os.environ["DEBUG_EXTRACTION"] = "1"

try:
    from resume import extract_resume
except ImportError:
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from resume import extract_resume

def assert_equal(actual, expected, msg=""):
    if actual != expected:
        raise AssertionError(f"{msg} - Expected {expected}, got {actual}")

def assert_true(condition, msg=""):
    if not condition:
        raise AssertionError(msg)

def run_tests():
    print("====================================")
    print("RUNNING EXTRACTION REGRESSION TESTS")
    print("====================================")

    # Test Case 1: Student Resume (No explicit projects/experience)
    text1 = """
KHALED AHMED MOHAMED ERFAN
Computer Science Student
Intelligent Systems
Alexandria, Egypt
khaled@gmail.com
linkedin.com/in/khaled
    """
    print("\n--- TEST CASE 1: Student Header Only ---")
    p1 = extract_resume(None, text_input=text1)
    
    assert_equal(len(p1["projects"]), 0, "Should extract 0 projects from header")
    assert_equal(len(p1["experience"]), 0, "Should extract 0 experience from header")
    assert_true(len(p1["education"]) > 0, "Should extract education/degree from header")
    edu_text = str(p1["education"]).lower()
    assert_true("computer science" in edu_text or "student" in edu_text or p1["education"][0]["degree"] != "UNKNOWN", "Should capture student/CS info")
    print("PASS Test Case 1")

    # Test Case 2: Resume with 4 distinct projects
    text2 = """
SUMMARY
Software engineer with passion for AI.
PROJECTS
Movie Recommendation System
Built a recommendation system using Python, Pandas and Scikit-learn.
Heart Disease Prediction
Developed a machine learning model using Random Forest.
E-commerce Platform
Built a full-stack platform with React and Node.js.
Chatbot AI
Created a chatbot using LLMs and LangChain.
    """
    print("\n--- TEST CASE 2: Four Projects ---")
    p2 = extract_resume(None, text_input=text2)
    assert_equal(len(p2["projects"]), 4, "Should extract exactly 4 projects")
    proj_names = [p["title"] for p in p2["projects"]]
    assert_true("Movie Recommendation System" in proj_names or "Heart Disease Prediction" in proj_names, "Should find explicit project names")
    print("PASS Test Case 2")

    # Test Case 3: Resume with 1 internship + 3 projects
    text3 = """
EXPERIENCE
Machine Learning Intern
XYZ Company
June 2025 to August 2025
Developed computer vision models.
PROJECTS
Autonomous Self-Driving Car Agent
Built a reinforcement learning based agent in Unity.
Developer Personal Portfolio
Built a full-stack platform with Next.js.
Stock Market Predictor System
Developed a machine learning model using LSTMs to predict stock prices.
    """
    print("\n--- TEST CASE 3: 1 Experience + 3 Projects ---")
    p3 = extract_resume(None, text_input=text3)
    assert_equal(len(p3["experience"]), 1, "Should extract exactly 1 experience")
    assert_equal(len(p3["projects"]), 3, "Should extract exactly 3 projects")
    print("PASS Test Case 3")

    # Test Case 4: Resume with no projects
    text4 = """
SUMMARY
Experienced professional.
EXPERIENCE
Senior Developer
Google
Worked on core search.
EDUCATION
Bachelor of Science
    """
    print("\n--- TEST CASE 4: No Projects ---")
    p4 = extract_resume(None, text_input=text4)
    assert_equal(len(p4["projects"]), 0, "Should not fabricate any projects")
    print("PASS Test Case 4")
    
    print("\nALL TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    try:
        run_tests()
    except AssertionError as e:
        import sys
        print(f"\nTEST FAILED: {str(e)}")
        sys.exit(1)
    except Exception as e:
        import sys
        print(f"\nUNEXPECTED ERROR:")
        traceback.print_exc()
        sys.exit(1)
