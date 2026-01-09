import os
import sys
import subprocess
from src.utils.logger import log_experiment, ActionType


def run_tests(target_dir: str, iteration: int = 0, timeout: int = 120) -> dict:
    """
    Judge agent: runs pytest in target_dir and returns structured results.

    Returns:
        {
          "passed": bool,
          "issues": list[str],   # ready to feed Fixer if needed
          "stdout": str,
          "stderr": str,
          "returncode": int
        }
    """
    if not target_dir or not os.path.isdir(target_dir):
        raise ValueError(f"Invalid target_dir: {target_dir}")

    # Use the current interpreter to guarantee pytest runs inside venv
    cmd = [sys.executable, "-m", "pytest", "-q"]
    cmd_str = " ".join(cmd)

    try:
        completed = subprocess.run(
            cmd,
            cwd=target_dir,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        stdout = completed.stdout or ""
        stderr = completed.stderr or ""
        rc = completed.returncode
    except subprocess.TimeoutExpired as e:
        stdout = (e.stdout or "") if isinstance(e.stdout, str) else ""
        stderr = (e.stderr or "") if isinstance(e.stderr, str) else ""
        rc = 124
        stderr = (stderr + "\n[Judge] pytest timed out").strip()

    passed = (rc == 0)
    combined = (stdout + "\n" + stderr).strip()

    # Convert pytest output into "issues" list for Fixer
    issues = []
    if not passed:
        issues = [line.strip() for line in combined.splitlines() if line.strip()]
        # Avoid prompt overload if this is passed to Fixer later
        if len(issues) > 120:
            issues = ["[Judge] pytest output truncated (last 120 lines):"] + issues[-120:]

    # Logging protocol: include input_prompt + output_response (mandatory fields)
    log_experiment(
        agent_name="JudgeAgent",
        model_used="local-pytest",
        action=ActionType.DEBUG,
        details={
            "input_prompt": f"Run tests: {cmd_str} (cwd={target_dir})",
            "output_response": combined,
            "target_dir": target_dir,
            "iteration": iteration,
            "returncode": rc,
            "issues_for_fixer_count": len(issues),
        },
        status="SUCCESS" if passed else "FAILURE",
    )

    return {
        "passed": passed,
        "issues": issues,
        "stdout": stdout,
        "stderr": stderr,
        "returncode": rc,
    }
