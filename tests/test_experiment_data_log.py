import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
LOG_PATH = REPO_ROOT / "logs" / "experiment_data.json"

ALLOWED_ACTIONS = {"DEBUG", "FIX", "CODE_ANALYSIS", "CODE_GEN"}
ALLOWED_STATUS = {"SUCCESS", "FAILURE"}

REQUIRED_KEYS = ["id", "timestamp", "agent", "model", "action", "details", "status"]
REQUIRED_DETAIL_KEYS = ["input_prompt", "output_response"]


def test_log_file_exists_and_is_json_array():
    assert LOG_PATH.exists(), f"Missing log file: {LOG_PATH}"
    data = json.loads(LOG_PATH.read_text(encoding="utf-8"))
    assert isinstance(data, list), "logs/experiment_data.json must be a JSON array (list)"


def test_each_entry_respects_minimum_contract():
    data = json.loads(LOG_PATH.read_text(encoding="utf-8"))

    for i, entry in enumerate(data):
        assert isinstance(entry, dict), f"Entry #{i} must be a JSON object"

        for k in REQUIRED_KEYS:
            assert k in entry, f"Entry #{i} missing key: {k}"

        assert isinstance(entry["id"], str) and entry["id"], f"Entry #{i} invalid id"
        assert isinstance(entry["timestamp"], str) and entry["timestamp"], f"Entry #{i} invalid timestamp"
        assert isinstance(entry["agent"], str) and entry["agent"], f"Entry #{i} invalid agent"
        assert isinstance(entry["model"], str) and entry["model"], f"Entry #{i} invalid model"

        assert entry["action"] in ALLOWED_ACTIONS, f"Entry #{i} invalid action: {entry['action']}"
        assert entry["status"] in ALLOWED_STATUS, f"Entry #{i} invalid status: {entry['status']}"

        details = entry["details"]
        assert isinstance(details, dict), f"Entry #{i} details must be an object"
        for dk in REQUIRED_DETAIL_KEYS:
            assert dk in details, f"Entry #{i} details missing: {dk}"
            assert isinstance(details[dk], str), f"Entry #{i} details.{dk} must be a string"


def test_fix_outputs_are_code_only_no_markdown_fences():
    """
    Quality gate: FIX outputs should be raw code, not wrapped in ``` fences.
    (Your sample log showed fences; this test will catch it and force prompt/tool alignment.)
    """
    data = json.loads(LOG_PATH.read_text(encoding="utf-8"))

    for i, entry in enumerate(data):
        if entry.get("action") == "FIX" and entry.get("status") == "SUCCESS":
            out = entry.get("details", {}).get("output_response", "")
            assert "```" not in out, f"Entry #{i} FIX output contains markdown fences"
