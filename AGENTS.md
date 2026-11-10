# Instructions for agents

This repository holds the FPSOT identity and access specification: assurance levels and their mapping, authenticators and passkeys, OpenID Connect and OAuth 2.0 clients, tokens at APIs, sessions and sign-out, authorization through OpenID AuthZEN, representation and delegation, workload identity, accounts and federation, identity and access events, and problem types.

- The normative text is in `spec/en/` and `spec/fr/`. Every rule has an ID such as `IAM-001`.
- Follow `skill/SKILL.md` when you write or review sign-in, token, session, authorization or identity event code in any FPSOT project. The spec text wins on any difference.
- `registry/problem-types.json` lists every problem type. Add a type there and in the table of `spec/<lang>/errors.adoc` in the same commit, then run `python3 -I scripts/check-problem-types.py .`.
- `registry/assurance-levels.yaml` maps the levels. Keep `verified: false` until a primary source confirms a mapping.
- Every page exists in English and in French, with the same file name and the same IDs.
- Terms and abbreviations come from the term base of `fpsot-spec-writing`. Add a missing term there first; `TERMS-NEEDED.md` lists the pending ones.
- This is a layer 1 specification. It may refer to the layer 0 specifications, to data types, vocabularies, data models, api-restful, testing and security. It refers to the observability specification by topic only, and never to the registry, code or capability specifications, except by topic.
- Do not name a product in a rule. Name the standard or the capability; products appear only on the informative reference stack page.
- Never put a real token, key, password or personal information in an example, a test or an event.
- Do not copy text from NIST, OpenID, IETF, W3C, OWASP or the governments. Summarize in your own words and cite the exact version.
- Do not state a legal point as a rule. Points that need a lawyer go on the page Questions for counsel.
- Commits follow Conventional Commits and are signed. Pull requests are squash-merged.
