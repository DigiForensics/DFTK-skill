#!/usr/bin/env python3
"""Validate answers/answer_slots.json against the DFTK question-workspace spec.

This is a self-check tool bundled with the question-workspace template so an Agent
can verify its answer sheet before handing it off for scoring / audit.

Usage:
    python tools/validate_answers.py [path/to/answer_slots.json]

Default path: answers/answer_slots.json resolved from the current directory, then
from this script's own workspace root (templates/question-workspace/).

Exit code: 0 = pass (warnings allowed), 1 = structural errors found.
"""
import json
import os
import re
import sys

VALID_STATUS = {"VERIFIED", "SUPPORTED", "CANDIDATE", "UNRESOLVED", "UNSUPPORTED"}


def main() -> int:
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        cwd_path = os.path.join(os.getcwd(), "answers", "answer_slots.json")
        if os.path.exists(cwd_path):
            path = cwd_path
        else:
            root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            path = os.path.join(root, "answers", "answer_slots.json")

    if not os.path.exists(path):
        print(f"ERROR: answer_slots.json not found: {path}")
        return 1

    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON in {path}: {exc}")
        return 1

    if not isinstance(data, dict) or not data:
        print("ERROR: top level must be a non-empty JSON object keyed by question id")
        return 1

    errors: list[str] = []
    warnings: list[str] = []
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(path)))

    for qid, slot in data.items():
        if not isinstance(slot, dict):
            errors.append(f"{qid}: slot must be an object")
            continue

        question = slot.get("question")
        if not isinstance(question, str) or not question.strip():
            errors.append(f"{qid}: missing 'question' (string)")

        if "answer" not in slot:
            errors.append(f"{qid}: missing 'answer' field (use null if unresolved)")

        status = slot.get("status")
        if status not in VALID_STATUS:
            errors.append(f"{qid}: status {status!r} not in {sorted(VALID_STATUS)}")
            continue

        evidence = slot.get("evidence")
        if status == "VERIFIED":
            if not isinstance(evidence, list) or len(evidence) == 0:
                errors.append(f"{qid}: VERIFIED requires non-empty 'evidence'")
            else:
                for i, item in enumerate(evidence):
                    if not isinstance(item, dict):
                        errors.append(f"{qid}.evidence[{i}] must be an object")
                        continue
                    rel = item.get("path")
                    if rel:
                        abs_path = os.path.join(workspace_root, rel)
                        if not os.path.exists(abs_path):
                            warnings.append(
                                f"{qid}.evidence[{i}].path {rel!r} not found in workspace "
                                f"(check spelling or produce the derived file under work/)"
                            )

        if status != "VERIFIED" and not slot.get("need_verify"):
            warnings.append(
                f"{qid}: status {status} should carry 'need_verify' explaining what is missing"
            )

    qmd = os.path.join(workspace_root, "question.md")
    if os.path.exists(qmd):
        with open(qmd, encoding="utf-8") as fh:
            nums = set(re.findall(r"^Q\d+", fh.read(), re.M))
        for n in nums:
            if n not in data:
                warnings.append(f"question.md has {n} but answer_slots.json is missing it")
        for k in data:
            if k not in nums:
                warnings.append(f"answer_slots.json has {k} but question.md is missing it")

    if errors:
        print(f"FAIL: {len(errors)} error(s) in {path}")
        for e in errors:
            print("  -", e)
        return 1

    if warnings:
        print(f"OK (with {len(warnings)} warning(s)): {path}")
        for w in warnings:
            print("  !", w)
    else:
        print(f"OK: {path} ({len(data)} slot(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
