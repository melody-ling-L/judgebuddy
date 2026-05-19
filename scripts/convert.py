#!/usr/bin/env python3
"""
convert.py — Normalize external eval platform outputs into JudgeBuddy-compatible CSV.

Supported sources in v0.1:
  - openai-evals   (JSONL format from OpenAI Evals runs)
  - braintrust     (JSON export from Braintrust traces)
  - generic        (your own JSON list with declared field mapping)

Usage:
  python convert.py --from openai-evals --input run.jsonl --output for_judgebuddy.csv
  python convert.py --from braintrust   --input trace.json --output for_judgebuddy.csv
  python convert.py --from generic      --input my.json --output for_judgebuddy.csv \\
                    --field-map '{"input":"resume","reference":"jd","completion":"output"}'

Output format: see README.md → Supported Data Format → Annotated CSV Example.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any


def convert_openai_evals(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """OpenAI Evals JSONL → JudgeBuddy row dicts.

    Expected per-record shape (simplified):
      {
        "sample_id": "...",
        "input": [{"role": "user", "content": "..."}, ...],
        "ideal": "...",          # reference
        "completion": "...",     # model output
        "model_name": "...",
        "scores": {"correctness": 1.0, ...},
        "judge_explanation": "...",
      }
    """
    rows = []
    for r in records:
        # Flatten messages into a single text field
        input_text = "\n".join(
            m.get("content", "") for m in r.get("input", []) if isinstance(m, dict)
        )
        rows.append({
            "Description": f"Case {r.get('sample_id', '?')}",
            "resume": input_text,
            "jd": r.get("ideal", ""),
            "provider_label": r.get("model_name", "Model"),
            "output": r.get("completion", ""),
            "status": "PASS" if r.get("scores", {}).get("overall", 1) >= 0.5 else "FAIL",
            "score": r.get("scores", {}).get("overall", ""),
            "named_scores": json.dumps(r.get("scores", {}), ensure_ascii=False),
            "grader_reason": r.get("judge_explanation", ""),
            "comment": "",
        })
    return rows


def convert_braintrust(payload: dict[str, Any]) -> list[dict[str, Any]]:
    """Braintrust trace JSON → JudgeBuddy row dicts.

    Expected shape (simplified):
      {
        "spans": [
          {
            "id": "...",
            "input": {...},
            "output": "...",
            "scores": {...},
            "metadata": {"model": "..."},
          }
        ]
      }
    """
    rows = []
    for i, span in enumerate(payload.get("spans", [])):
        inp = span.get("input", {})
        if isinstance(inp, dict):
            resume = inp.get("resume", "") or inp.get("source", "") or json.dumps(inp, ensure_ascii=False)
            jd = inp.get("jd", "") or inp.get("reference", "")
        else:
            resume, jd = str(inp), ""
        rows.append({
            "Description": f"Case {span.get('id', i + 1)}",
            "resume": resume,
            "jd": jd,
            "provider_label": span.get("metadata", {}).get("model", "Model"),
            "output": span.get("output", ""),
            "status": "PASS" if (span.get("scores", {}).get("overall", 1)) >= 0.5 else "FAIL",
            "score": span.get("scores", {}).get("overall", ""),
            "named_scores": json.dumps(span.get("scores", {}), ensure_ascii=False),
            "grader_reason": span.get("metadata", {}).get("judge_explanation", ""),
            "comment": "",
        })
    return rows


def convert_generic(payload: list[dict[str, Any]], field_map: dict[str, str]) -> list[dict[str, Any]]:
    """Generic JSON list with caller-supplied field mapping.

    field_map example:
      {"input": "resume", "reference": "jd", "completion": "output"}
    Keys are source field names; values are target field names in the JudgeBuddy row.
    """
    rows = []
    for i, r in enumerate(payload):
        row = {
            "Description": f"Case {r.get('id', i + 1)}",
            "resume": "",
            "jd": "",
            "provider_label": r.get("model", "Model"),
            "output": "",
            "status": "",
            "score": "",
            "named_scores": "",
            "grader_reason": "",
            "comment": "",
        }
        for src, tgt in field_map.items():
            if src in r and tgt in row:
                row[tgt] = r[src] if isinstance(r[src], str) else json.dumps(r[src], ensure_ascii=False)
        rows.append(row)
    return rows


def write_judgebuddy_csv(rows: list[dict[str, Any]], output_path: Path) -> None:
    """Write rows into JudgeBuddy CSV. Groups by case (so each row in output CSV
    represents one case; if multiple providers exist for the same case, they
    become parallel column blocks)."""
    if not rows:
        print("Warning: no rows to write.", file=sys.stderr)
        return

    # Group by Description (case id)
    cases: dict[str, list[dict[str, Any]]] = {}
    for r in rows:
        cases.setdefault(r["Description"], []).append(r)

    # All providers seen across the file (sorted for column stability)
    all_providers = sorted({r["provider_label"] for r in rows})

    # Build header
    header = ["Description", "resume", "jd"]
    for p in all_providers:
        header.extend([
            f"[{p}] output",
            "Status",
            "Score",
            "Named Scores",
            "Grader Reason",
            "Comment",
        ])

    # Write
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)

        for case_id, case_rows in cases.items():
            first = case_rows[0]
            line = [case_id, first.get("resume", ""), first.get("jd", "")]
            # Index providers by label
            by_provider = {r["provider_label"]: r for r in case_rows}
            for p in all_providers:
                r = by_provider.get(p, {})
                line.extend([
                    r.get("output", ""),
                    r.get("status", ""),
                    r.get("score", ""),
                    r.get("named_scores", ""),
                    r.get("grader_reason", ""),
                    r.get("comment", ""),
                ])
            writer.writerow(line)

    print(f"✓ Wrote {len(cases)} cases × {len(all_providers)} providers → {output_path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--from", dest="source", required=True,
                        choices=["openai-evals", "braintrust", "generic"],
                        help="Source platform")
    parser.add_argument("--input", required=True, type=Path, help="Input file")
    parser.add_argument("--output", required=True, type=Path, help="Output CSV")
    parser.add_argument("--field-map", type=str, default="{}",
                        help="(generic only) JSON dict mapping source fields → JudgeBuddy fields")
    args = parser.parse_args()

    if args.source == "openai-evals":
        records = [json.loads(line) for line in args.input.read_text().splitlines() if line.strip()]
        rows = convert_openai_evals(records)
    elif args.source == "braintrust":
        payload = json.loads(args.input.read_text())
        rows = convert_braintrust(payload)
    elif args.source == "generic":
        payload = json.loads(args.input.read_text())
        if not isinstance(payload, list):
            print("generic input must be a JSON list", file=sys.stderr)
            sys.exit(1)
        field_map = json.loads(args.field_map)
        rows = convert_generic(payload, field_map)
    else:
        print(f"Unknown source: {args.source}", file=sys.stderr)
        sys.exit(1)

    write_judgebuddy_csv(rows, args.output)


if __name__ == "__main__":
    main()
