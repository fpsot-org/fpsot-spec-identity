#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Tests scripts/check-problem-types.py: the repository passes, and each broken copy fails.
set -uo pipefail
here=$(cd "$(dirname "$0")/.." && pwd)
check="$here/scripts/check-problem-types.py"
fail=0
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

if ! python3 -I "$check" "$here"; then
  echo "FAIL: the repository itself does not pass"; fail=1
fi

# Each case copies the repository files the checker reads, breaks one thing, and expects a failure.
case_fails() {
  local name=$1 script=$2 dir="$tmp/$1"
  mkdir -p "$dir"
  cp -r "$here/registry" "$here/spec" "$dir/"
  [ -d "$here/docs" ] && cp -r "$here/docs" "$dir/"
  (cd "$dir" && python3 -I -c "$script")
  if python3 -I "$check" "$dir" >/dev/null; then
    echo "FAIL: case $name passed but should fail"; fail=1
  else
    echo "ok: case $name fails"
  fi
}

case_fails duplicate-uri 'import json;p="registry/problem-types.json";d=json.load(open(p));d["types"].append(dict(d["types"][0]));json.dump(d,open(p,"w"))'
case_fails missing-french-title 'import json;p="registry/problem-types.json";d=json.load(open(p));d["types"][0]["title"]["fr"]="";json.dump(d,open(p,"w"))'
case_fails missing-english-title 'import json;p="registry/problem-types.json";d=json.load(open(p));del d["types"][1]["title"]["en"];json.dump(d,open(p,"w"))'
case_fails uri-not-in-registry 'open("spec/en/errors.adoc","a").write("\nSee https://fpsot.org/problems/identity/no-such-type.\n")'
case_fails wrong-uri 'import json;p="registry/problem-types.json";d=json.load(open(p));d["types"][0]["type"]="https://fpsot.org/problems/other";json.dump(d,open(p,"w"))'
case_fails table-row-missing 'import json;p="registry/problem-types.json";d=json.load(open(p));d["types"].pop();json.dump(d,open(p,"w"))'
exit $fail
