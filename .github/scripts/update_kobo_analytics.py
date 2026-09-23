#!/usr/bin/env python3
import json
import os
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ASSET_UID = "aErF75hMg62Y4nCBoJXQbP"
API_URL = f"https://eu.kobotoolbox.org/api/v2/assets/{ASSET_UID}/data/?format=json"
TOKEN = os.environ.get("KOBO_TOKEN", "").strip()
OUTPUT = Path("analytics.json")

CORRECT = {
    "q1": "b", "q2": "c", "q3": "a", "q4": "a", "q5": "b",
    "q6": "b", "q7": "a", "q8": "a", "q9": "a", "q10": "c",
}


def field(record, name, default=None):
    if name in record:
        return record[name]
    suffix = "/" + name
    for key, value in record.items():
        if key.endswith(suffix):
            return value
    return default


def fetch_all():
    if not TOKEN:
        raise RuntimeError("KOBO_TOKEN is not configured")
    url = API_URL
    records = []
    while url:
        request = urllib.request.Request(
            url,
            headers={"Authorization": f"Token {TOKEN}", "Accept": "application/json"},
        )
        with urllib.request.urlopen(request, timeout=60) as response:
            payload = json.load(response)
        if isinstance(payload, list):
            records.extend(payload)
            break
        records.extend(payload.get("results", []))
        url = payload.get("next")
    return records


def numeric_score(record):
    stored = field(record, "total_score")
    try:
        return int(float(stored))
    except (TypeError, ValueError):
        return sum(1 for question, answer in CORRECT.items() if str(field(record, question, "")) == answer)


def build_summary(records):
    scores = [numeric_score(record) for record in records]
    question_rows = []
    for question, correct_answer in CORRECT.items():
        answered = [str(field(record, question, "")) for record in records if field(record, question, "") not in (None, "")]
        correct_count = sum(answer == correct_answer for answer in answered)
        question_rows.append({
            "question": question,
            "answered": len(answered),
            "correct": correct_count,
            "correct_percent": round((correct_count / len(answered) * 100) if answered else 0, 1),
        })

    return {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "asset_uid": ASSET_UID,
        "participants": len(records),
        "average_score": round(sum(scores) / len(scores), 2) if scores else 0,
        "highest_score": max(scores) if scores else 0,
        "lowest_score": min(scores) if scores else 0,
        "levels": {
            "foundation": sum(score <= 4 for score in scores),
            "intermediate": sum(5 <= score <= 7 for score in scores),
            "good": sum(score >= 8 for score in scores),
        },
        "questions": question_rows,
    }


if __name__ == "__main__":
    summary = build_summary(fetch_all())
    OUTPUT.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Updated {OUTPUT} with {summary['participants']} submissions")
