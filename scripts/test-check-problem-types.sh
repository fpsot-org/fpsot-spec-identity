#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Tests scripts/check-problem-types.py: the repository passes, and each broken copy fails.
# The checker covers the problem types (IAM-101) and the event schemas (IAM-094).
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
case_fails status-mismatch 'import json;p="registry/problem-types.json";d=json.load(open(p));d["types"][0]["status"]=403;json.dump(d,open(p,"w"))'
case_fails oauth-error-mismatch 'import json;p="registry/problem-types.json";d=json.load(open(p));d["types"][0]["oauthError"]="invalid_request";json.dump(d,open(p,"w"))'
case_fails oauth-error-none-mismatch 'import json;p="registry/problem-types.json";d=json.load(open(p));d["types"][-1]["oauthError"]="invalid_token";json.dump(d,open(p,"w"))'
case_fails event-schema-missing 'import os;os.remove("registry/events/org.fpsot.identity.access.evaluated.schema.json")'
case_fails event-schema-unparsable 'open("registry/events/org.fpsot.identity.session.ended.schema.json","w").write("{ not json")'
case_fails event-schema-duplicate-id 'import json;a="registry/events/org.fpsot.identity.session.ended.schema.json";b="registry/events/org.fpsot.identity.account.created.schema.json";d=json.load(open(b));d["$id"]=json.load(open(a))["$id"];json.dump(d,open(b,"w"))'
case_fails event-type-not-in-table 'open("spec/en/events.adoc","a").write("\nSee `org.fpsot.identity.no.such`.\n")'
case_fails event-schema-wrong-draft 'import json;p="registry/events/org.fpsot.identity.token.exchanged.schema.json";d=json.load(open(p));d["$schema"]="http://json-schema.org/draft-07/schema#";json.dump(d,open(p,"w"))'
exit $fail
