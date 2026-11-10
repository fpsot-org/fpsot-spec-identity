#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check registry/problem-types.json against the specification text.

Checks:
  - the file parses, and each entry has a name, a type URI, a status and titles;
  - each type URI is unique, and equals the base URI followed by the name;
  - each entry has a non-empty title in English and in French;
  - every problem type URI that a page under spec/ or docs/ cites exists in the file;
  - every name in the problem type table of spec/<lang>/errors.adoc exists in the file.

Usage: check-problem-types.py [REPO_ROOT]. Exit code 1 on any finding.
Uses only the Python standard library.
"""
import json
import pathlib
import re
import sys

BASE = "https://fpsot.org/problems/identity/"
NAME = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")
CITED = re.compile(r"https://fpsot\.org/(?:fr/)?problems/identity/([A-Za-z0-9-]+)")
TABLE_ROW = re.compile(r"^\|`([a-z0-9-]+)` \|[0-9]{3} \|")


def check(root: pathlib.Path) -> list[str]:
    out: list[str] = []
    path = root / "registry" / "problem-types.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        return [f"{path}: cannot read: {e}"]
    if data.get("base") != BASE:
        out.append(f"{path}: base must be {BASE}")
    entries = data.get("types")
    if not isinstance(entries, list) or not entries:
        return out + [f"{path}: 'types' must be a non-empty list"]
    seen_uri: set[str] = set()
    names: set[str] = set()
    for i, e in enumerate(entries):
        where = f"{path}: types[{i}]"
        name, uri = e.get("name", ""), e.get("type", "")
        if not NAME.match(name):
            out.append(f"{where}: name {name!r} is not kebab-case")
        if uri != BASE + name:
            out.append(f"{where}: type {uri!r} must be {BASE + name!r}")
        if uri in seen_uri:
            out.append(f"{where}: duplicate type {uri}")
        seen_uri.add(uri)
        names.add(name)
        if not isinstance(e.get("status"), int) or not 400 <= e["status"] <= 599:
            out.append(f"{where}: status must be a 4xx or 5xx integer")
        title = e.get("title") or {}
        for lang in ("en", "fr"):
            if not str(title.get(lang, "")).strip():
                out.append(f"{where}: title.{lang} is missing")
    for sub in ("spec", "docs"):
        for page in sorted((root / sub).rglob("*.adoc")):
            for n, line in enumerate(page.read_text(encoding="utf-8").splitlines(), 1):
                for m in CITED.finditer(line):
                    if m.group(1) not in names:
                        out.append(f"{page}:{n}: problem type {m.group(1)!r} is not in {path.name}")
    for lang in ("en", "fr"):
        page = root / "spec" / lang / "errors.adoc"
        if not page.exists():
            out.append(f"{page}: missing")
            continue
        rows = [m.group(1) for line in page.read_text(encoding="utf-8").splitlines()
                if (m := TABLE_ROW.match(line))]
        if not rows:
            out.append(f"{page}: no problem type table found")
        for r in rows:
            if r not in names:
                out.append(f"{page}: table row {r!r} is not in {path.name}")
        for missing in sorted(names - set(rows)):
            out.append(f"{page}: {missing!r} is in {path.name} but not in the table")
    return out


def main() -> int:
    root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    findings = check(root)
    for f in findings:
        print(f)
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
