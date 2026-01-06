import argparse
import sys
import os
from dotenv import load_dotenv
from src.agents.auditor import analyze_code
from src.agents.fixer import fix_code
from src.agents.judge import run_tests

# Load environment variables from .env file
load_dotenv()

# Get the API key from the .env file
API_KEY = os.getenv("GOOGLE_API_KEY")

# Ensure the API key is loaded
if not API_KEY:
    print("❌ API_KEY not found in the environment variables. Please ensure it's set in the .env file.")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target_dir", type=str, required=True)
    args = parser.parse_args()

    if not os.path.exists(args.target_dir):
        print(f"❌ Directory {args.target_dir} not found.")
        sys.exit(1)

    print(f"🚀 Starting on: {args.target_dir}")

    # Step 1: Auditor - Analyze the code
    issues = analyze_code(os.path.join(args.target_dir, "example.py"), API_KEY)

    # Step 2: Fixer - Apply fixes based on the analysis
    fixed_file_path = fix_code(os.path.join(args.target_dir, "example.py"), issues, API_KEY)

    # Step 3: Judge - Run tests on the fixed code
    run_tests(fixed_file_path, API_KEY)

    print("✅ Mission Complete")

if __name__ == "__main__":
    main()
