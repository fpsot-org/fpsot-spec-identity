#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Check the registry files against the specification text.

Problem types (IAM-101), in registry/problem-types.json:
  - the file parses, and each entry has a name, a type URI, a status and titles;
  - each type URI is unique, and equals the base URI followed by the name;
  - each entry has a non-empty title in English and in French;
  - every problem type URI that a page under spec/ or docs/ cites exists in the file;
  - every name in the problem type table of spec/<lang>/errors.adoc exists in the file,
    with the same status and the same OAuth error ("None" or "Aucune" for none).

Event schemas (IAM-094), in registry/events/<type>.schema.json:
  - every event type that a page under spec/ or docs/ names is in the catalog table of
    spec/<lang>/events.adoc, and has a schema file;
  - every schema file belongs to a type of the catalog table;
  - each schema parses, declares JSON Schema 2020-12, and has a unique $id.

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
TABLE_ROW = re.compile(r"^\|`([a-z0-9-]+)` \|([0-9]{3}) \|(?:`([a-z_]+)`|(None|Aucune)) \|")
EVENT = re.compile(r"\borg\.fpsot\.identity\.[a-z][a-z0-9-]*\.[a-z][a-z0-9-]*\b")
EVENT_ROW = re.compile(r"^\|`(org\.fpsot\.identity\.[a-z0-9.-]+)` \|")
DRAFT = "https://json-schema.org/draft/2020-12/schema"


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
    by_name: dict[str, dict] = {}
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
        by_name[name] = e
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
        matches = [m for line in page.read_text(encoding="utf-8").splitlines()
                   if (m := TABLE_ROW.match(line))]
        rows = [m.group(1) for m in matches]
        if not rows:
            out.append(f"{page}: no problem type table found")
        for m in matches:
            r = m.group(1)
            if r not in names:
                out.append(f"{page}: table row {r!r} is not in {path.name}")
                continue
            e = by_name[r]
            if e.get("status") != int(m.group(2)):
                out.append(f"{page}: table row {r!r} has status {m.group(2)}, "
                           f"but {path.name} has {e.get('status')!r}")
            if e.get("oauthError") != m.group(3):
                out.append(f"{page}: table row {r!r} has OAuth error {m.group(3) or m.group(4)!r}, "
                           f"but {path.name} has {e.get('oauthError')!r}")
        for missing in sorted(names - set(rows)):
            out.append(f"{page}: {missing!r} is in {path.name} but not in the table")
    return out + check_events(root)


def check_events(root: pathlib.Path) -> list[str]:
    out: list[str] = []
    folder = root / "registry" / "events"
    catalog: set[str] = set()
    for lang in ("en", "fr"):
        page = root / "spec" / lang / "events.adoc"
        if not page.exists():
            out.append(f"{page}: missing")
            continue
        rows = {m.group(1) for line in page.read_text(encoding="utf-8").splitlines()
                if (m := EVENT_ROW.match(line))}
        if not rows:
            out.append(f"{page}: no event catalog table found")
        if catalog and rows != catalog:
            out.append(f"{page}: the event catalog differs from the English one")
        catalog |= rows
    for sub in ("spec", "docs"):
        for page in sorted((root / sub).rglob("*.adoc")):
            for n, line in enumerate(page.read_text(encoding="utf-8").splitlines(), 1):
                for m in EVENT.finditer(line):
                    if m.group(0) not in catalog:
                        out.append(f"{page}:{n}: event type {m.group(0)!r} is not in the catalog table")
    ids: dict[str, str] = {}
    files = {p.name: p for p in folder.glob("*.schema.json")} if folder.is_dir() else {}
    for t in sorted(catalog):
        if t + ".schema.json" not in files:
            out.append(f"{folder}: event type {t!r} has no schema {t}.schema.json")
    for name, p in sorted(files.items()):
        t = name[: -len(".schema.json")]
        if t not in catalog:
            out.append(f"{p}: {t!r} is not an event type of the catalog table")
        try:
            schema = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            out.append(f"{p}: cannot read: {e}")
            continue
        if not isinstance(schema, dict):
            out.append(f"{p}: the schema must be a JSON object")
            continue
        if schema.get("$schema") != DRAFT:
            out.append(f"{p}: $schema must be {DRAFT}")
        sid = schema.get("$id")
        if not isinstance(sid, str) or not sid:
            out.append(f"{p}: $id is missing")
        elif sid in ids:
            out.append(f"{p}: $id {sid} is also the $id of {ids[sid]}")
        else:
            ids[sid] = name
    return out


def main() -> int:
    root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    findings = check(root)
    for f in findings:
        print(f)
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
