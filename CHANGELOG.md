# Changelog

All notable changes to this specification are listed here.
The format follows [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/),
and versions follow [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-11-10

### Added

- Assurance level rules IAM-001 to IAM-004: three FPSOT levels, `low`, `substantial` and `high`, chosen per service from a documented harm assessment; `acr` URIs under `https://fpsot.org/assurance-levels/`; the mapping file `registry/assurance-levels.yaml` to Québec, Canada, the Pan-Canadian Trust Framework, eIDAS and NIST SP 800-63-4, with unconfirmed mappings marked "to be verified".
- Authenticator rules IAM-010 to IAM-017: multifactor authentication at `substantial` and `high` with a phishing-resistant option on offer; device-bound hardware keys and no synced passkeys at `high`; phishing-resistant MFA for staff; a choice of authenticators and backups; NIST SP 800-63B-4 password rules; limits on SMS, voice, email and push; recovery that keeps the level; the response to a suspected compromise.
- Client rules IAM-020 to IAM-028: the authorization code flow with PKCE `S256` for every client; a backend for each browser front end under RFC 10017; exact redirect matching and `iss` checks; ID token checks with `acr_values`; `ui_locales` and `locale`; `private_key_jwt` with the issuer as the only audience under RFC 10070, or mutual TLS; DPoP and certificate-bound tokens at `high`; the FAPI 2.0 Security Profile at `high`; client registration.
- API rules IAM-030 to IAM-036: audience restriction, JWT access token checks, lifetimes of 15 and 5 minutes, protected resource metadata, step-up under RFC 9470, coarse scopes and their names, and minimal claims with an opaque `sub`.
- Session rules IAM-040 to IAM-044: federal limits for staff and NIST limits for the public, new session identifiers, RP-Initiated and Back-Channel Logout, sessions that keep their level, and a list of active sessions.
- Authorization rules IAM-050 to IAM-057: one authorization engine called over OpenID AuthZEN Authorization API 1.0, deny by default and on failure, coarse access only in the identity provider, policies as tested code with a version in each decision, plain Rego, exportable relationships, and opaque identifiers in decision requests.
- Representation rules IAM-060 to IAM-065: one person per account, representation as relationships with scope, period and proof of capacity, the `Party` model, grants by a business representative, an explicit choice of the represented party, and token exchange within one organization only.
- Workload rules IAM-070 to IAM-074: a cryptographic identity per workload, mutual TLS or bound tokens, no forwarding of user tokens, calls between organizations that authorize the organization, and short-lived keys in an inventory.
- Account rules IAM-080 to IAM-086: SCIM 2.0 provisioning, deprovisioning within 1 hour, an account register, renewal of identity evidence, access reviews, and conditions on outside identity providers and their assertions.
- Event rules IAM-090 to IAM-095: a catalog of 16 identity and access event types, their common content with a session identifier that is never the cookie value, decision events with a keyed hash of the context, minimization of personal information, schemas and reason codes. The FPSOT observability specification sets how the events are recorded and kept, the names of record attributes and the minimization of network addresses.
- Event schemas `registry/events/<type>.schema.json`, one JSON Schema 2020-12 for each of the 16 event types (IAM-094, API-103).
- Error rules IAM-100 to IAM-103 and the registry `registry/problem-types.json` of 11 problem types under `https://fpsot.org/problems/identity/`, with English and French titles.
- A check of the problem type registry (with the status and OAuth error of each table row) and of the event schemas against the text, with its tests, run in the CI job `registry`.
- An informative reference stack page and an informative page of questions for counsel.
- Comparison data with Canada and Québec rows.
- How-to guide that secures a new service.

### Notes

- The Québec column of the level mapping departs from the research report. The report mapped `substantial` to ID2 with AU2 or AU3, and `high` to ID3 or ID4 with AU4. This version maps `substantial` to ID2 with AU2 or ID3 with AU3, and `high` to ID4 with AU4 only. AU4 is the only Québec level that requires a hardware cryptographic device, which IAM-011 requires at `high`. The details of ID3 (no one-time codes by text message and similar channels, renewal every 18 months) appear in the table of IAM-003. The link from the level élevé of IA-SI-2022-001-OP to ID3 is inferred.

[Unreleased]: https://github.com/fpsot-org/fpsot-spec-identity/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/fpsot-org/fpsot-spec-identity/releases/tag/v0.1.0
