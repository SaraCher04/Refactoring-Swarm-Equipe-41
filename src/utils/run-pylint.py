# =========================================================
# run-pylint(target-dir: str) -> dirct
# =========================================================
import subprocess
import sys
from src.list_python_files.py import list_python_files

def run_pylint(target_dir: str) -> dict:
    py_files = list_python_files(target_dir)
    messages = []
    scores = []

    for file_path in py_files:
        print(f"🔍 Running pylint on '{file_path}'")
        result = subprocess.run(
            [sys.executable, "-m", "pylint", file_path,
             "--score=y", "--disable=R,C", "--enable=E,F,W"],
            capture_output=True,
            text=True
        )
        messages.append(result.stdout)

        for line in result.stdout.splitlines():
            if "rated at" in line:
                try:
                    score = float(line.split("rated at")[1].split("/")[0])
                    scores.append(score)
                except Exception:
                    pass

    avg_score = round(sum(scores)/len(scores), 2) if scores else 0.0
    print(f"✅ Average pylint score: {avg_score}")
    return {"score": avg_score, "messages": messages}
