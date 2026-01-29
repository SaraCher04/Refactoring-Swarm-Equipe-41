import argparse
import os
from dotenv import load_dotenv
from src.agents.auditor import analyze_code
from src.agents.fixer import fix_code
from src.agents.judge import run_tests
from src.utils.logger import log_experiment, ActionType

# Load environment variables from .env file
load_dotenv()

# Get the API key from the .env file
API_KEY = os.getenv("GEMINI_API_KEY")

# Ensure the API key is loaded
if not API_KEY:
    print("❌ API_KEY not found in the environment variables. Please ensure it's set in the .env file.")
    exit(1)

def process_file(file_path: str, api_key: str):
    """Process a single file through auditing, fixing, and testing."""
    print(f"🚀 Starting analysis for: {file_path}")
    
    # Step 1: Auditor - Analyze the code
    refactoring_feedback = analyze_code(file_path, api_key)
    if not refactoring_feedback:
        print(f"❌ No issues found for {file_path}. Skipping.")
        return

    # Step 2: Fixer - Apply fixes based on the analysis
    fixed_file_path = fix_code(file_path, refactoring_feedback, api_key)
    
    # Step 3: Judge - Run tests on the fixed code
    module_name = os.path.splitext(os.path.basename(file_path))[0]  # Extract module name from file name
    run_tests(fixed_file_path, api_key, module_name)  # Pass the module_name here

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target_dir", type=str, required=True, help="Directory containing Python files to refactor")
    args = parser.parse_args()

    target_dir = args.target_dir
    
    if not os.path.exists(target_dir):
        print(f"❌ Directory {target_dir} not found.")
        exit(1)

    # Process each Python file in the directory
    for filename in os.listdir(target_dir):
        file_path = os.path.join(target_dir, filename)
        if os.path.isfile(file_path) and filename.endswith(".py"):  # Only process Python files
            process_file(file_path, API_KEY)

    print("✅ Mission Complete")

if __name__ == "__main__":
    main()
