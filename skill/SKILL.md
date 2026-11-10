---
name: fpsot-identity
description: Identity and access rules for FPSOT software. Use when writing or reviewing sign-in, OpenID Connect or OAuth clients, token checks in APIs, sessions and sign-out, authorization calls to a policy engine, representation of another person or business, workload identity, provisioning, identity audit events or identity error responses.
---

# FPSOT identity and access

Summary of the FPSOT identity and access specification. It adds no rules of its own.
The spec text in `spec/` wins on any difference. Each line cites its requirement ID.
The data files are `registry/assurance-levels.yaml` (level mapping) and `registry/problem-types.json` (problem types).

Each line keeps the strength of its rule: "must" and "must not" are MUST and MUST NOT, "should" and "should not" are SHOULD and SHOULD NOT, "may" is MAY.

Rules name standards and capabilities, never products. Products appear only in `spec/en/reference-stack.adoc`, which is informative.

## Assurance levels

- Each service must declare `low`, `substantial` or `high` from a documented harm assessment of confidentiality, integrity and availability, even with no sign-in (IAM-001).
- `acr` must be one of `https://fpsot.org/assurance-levels/{low,substantial,high}`, naming the level, not the method; methods go in `amr` (IAM-002).
- Pick a level at least as strict as the jurisdiction's, through `registry/assurance-levels.yaml`; confirm each mapping marked "to be verified"; meet stricter local details too (IAM-003).
- The identity provider must not state an `acr` above the account's identity verification; record verification and authentication levels separately (should) (IAM-004).

## Authenticators

- `substantial` and `high` must require multifactor authentication; the identity provider must offer a phishing-resistant authenticator, such as a passkey (IAM-010).
- `high` must use a device-bound, non-exportable hardware key; refuse synced passkeys (backup eligibility flag set); synced passkeys may serve the public at `low` and `substantial` (IAM-011).
- Staff must use phishing-resistant MFA; administrators of the identity provider, the authorization engine and their keys must use `high`; an organization may refuse synced passkeys for staff (IAM-012).
- Offer at least two kinds of authenticator per level and let people enroll a backup of the same level (IAM-013).
- Passwords follow NIST SP 800-63B-4: 15 characters alone, 8 in MFA, accept 64 and paste, blocklist; no composition rules, forced change, security questions or hints (IAM-014).
- SMS or voice codes should not be factors except as a chosen fallback, and must not be at `high`; email must not be an authenticator; push needs number matching (IAM-015).
- Recovery must not give a level above what it checked; regaining `substantial` or `high` needs a backup of that level or new identity verification; notify each recovery (IAM-016).
- On suspected compromise: let people report it, notify them, block at once, end sessions, revoke refresh tokens, review and cancel untrusted actions (IAM-017).

## Sign-in flows and clients

- Authorization code flow of OpenID Connect with PKCE `S256` for every client; no implicit, password or token-returning hybrid flow; read the discovery document (IAM-020).
- Browser front ends must use a backend for the front end (RFC 10017); no token in browser code; only a `Secure`, `HttpOnly` cookie, `SameSite=Strict` (should); block cross-site request forgery (IAM-021).
- Exact redirect URI match, `https` only (loopback for native apps); send and check `iss` (RFC 9207) (IAM-022).
- Check issuer, audience, signature, expiry and `nonce` of ID tokens; request `acr_values` and check `acr`; never send an ID token to an API (IAM-023).
- Send `ui_locales` from LOC-005 (should); show that locale; `locale` holds a BCP 47 tag; keep the profile language (IAM-024).
- Confidential clients must use `private_key_jwt` (aud = issuer only, RFC 10070) or mutual TLS; the server must reject other audiences; no shared secrets at `substantial` and `high`, and should not elsewhere (IAM-025).
- At `high`, bind every access token: DPoP for browser front ends and their backend, certificate-bound tokens between services; should do the same at `substantial` (IAM-026).
- At `high`, conform to the FAPI 2.0 Security Profile in full; other confidential web clients should use pushed authorization requests (IAM-027).
- Register each client with redirect URIs, grants, scopes and keys; publish `jwks_uri` (should); rotate keys under SEC-023; publish server metadata (IAM-028).

## Tokens at APIs

- Accept only tokens whose `aud` names this API; clients should use `resource` (RFC 8707) (IAM-030).
- Check JWT access tokens under RFC 9068 (`typ` `at+jwt`, fixed asymmetric algorithms, never `none`, RFC 8725) or introspect opaque ones; check the key proof of bound tokens (IAM-031).
- Access tokens expire within 15 minutes, 5 at `high`; bind or rotate public-client refresh tokens; refresh tokens must not outlive the session; offer revocation (IAM-032).
- Publish protected resource metadata at `/.well-known/oauth-protected-resource` (IAM-033).
- Check `acr` and `auth_time` per operation; on shortfall answer 401 `insufficient_user_authentication` with `acr_values` and `max_age` (IAM-034).
- Scopes are coarse and never replace per-object checks (API-092); FPSOT scopes are kebab-case, FPSOT claims lowerCamelCase, outside names unchanged (IAM-035).
- Tokens carry only needed claims; `sub` is opaque, never a SIN, health number, email or name; pairwise `sub` across organizations (should) (IAM-036).

## Sessions

- Staff: 12 h overall, 30 min idle (15 min at `high`); public: 24 h and 1 h, or 12 h and 15 min at `high`; organizations may set shorter limits (IAM-040).
- At the end of a session, sign in again at the service level; drop backend tokens; revoke refresh tokens; new random session ID (128 bits) at each sign-in and step up (IAM-041).
- Sign-out ends local and identity provider sessions (RP-Initiated Logout) and reaches every other application (Back-Channel Logout); CAEP events (should) (IAM-042).
- A session must keep the service level; when it falls, end the session, or require a step up before the next action (may) (IAM-043).
- Show each person their active sessions and let them end any (should) (IAM-044).

## Authorization

- Ask the authorization engine on every request through OpenID AuthZEN 1.0 evaluation over HTTPS; metadata at `/.well-known/authzen-configuration` (should); batch and search (may); authenticate to the engine (IAM-050).
- Deny by default and on any engine error, timeout or unreadable answer; check each function and object on the server; cache an allow for at most 60 s and drop it on a policy version change (may) (IAM-051).
- The identity provider decides only coarse access; roles and groups stay coarse; business rules live in the engine (IAM-052).
- Policies as code in version control, reviewed under SEC-010, tested through the evaluation interface (TST-005); each decision carries the policy version (IAM-053).
- Policies in plain Rego, with no engine-specific built-in or plug-in (IAM-054).
- Export every relationship as object#relation@subject, and the type model, at any time, loadable into another engine (IAM-055).
- Use roles for coarse rights, attributes for context, relationships for ownership, cases, membership and representation (should) (IAM-056).
- Name subjects and resources by opaque IDs; context holds only what the policy reads (IAM-057).

## Representation and delegation

- One person per account, no shared accounts (IAM-060).
- Each representation is an engine relationship with kind, scope, start, end, a reference to the proof of capacity and who checked it (IAM-061).
- The represented party is a `Party` (DMO-040); keep representations as `PartyRelationship` (DMO-044) and derive engine relationships from them (should) (IAM-062).
- A verified business representative must be able to grant and revoke access; grants must not exceed the grantor's scope and are their own relationships (IAM-063).
- The person must choose whom they act for; show it on every page; pass it to the engine; deny without a valid relationship (IAM-064).
- Token exchange (RFC 8693) may happen within one organization only: narrower audience and scopes, `sub` names the person, `act` names the service; no token without `act`; never between organizations in this version (IAM-065).

## Workloads

- Each workload has its own cryptographic identity (SPIFFE or registered client key); no sharing; test and production differ; least audiences and scopes (IAM-070).
- Service calls use mutual TLS or a key-bound token; client credentials with `private_key_jwt` or mutual TLS (IAM-071).
- Never pass a person's access token to another API; exchange it under IAM-065 (IAM-072).
- Calls between organizations authorize the organization and system, not a person, under a written agreement (IAM-073).
- Workload keys have an owner and expiry and rotate (SEC-023); credentials should last 24 h or less; private keys in a secret store or hardware (SEC-020); keep an inventory (IAM-074).

## Accounts and federation

- Read accounts only from tokens, or accept SCIM 2.0 provisioning for a local copy; cursor pagination (should) (IAM-080).
- On departure or suspension, disable at once, end sessions, revoke refresh tokens; local copies updated within 1 hour; send through SCIM or Shared Signals (should) (IAM-081).
- Keep an account register (creation, suspension, recovery, maintenance, revocation, renewal), reviewed yearly (IAM-082).
- Renew identity evidence every 36 months at `substantial` and 12 at `high`, or sooner where the jurisdiction says (IAM-083).
- Review staff roles and relationships yearly, administrators every 90 days (should) (IAM-084).
- Outside identity providers only under a written agreement and a prior risk analysis with a privacy impact assessment, imposing the service level (IAM-085).
- Outside assertions: signed, one audience, replay-resistant, no personal information in identifiers; linking a weaker identity must not raise the level (IAM-086).

## Events

- Emit the catalog events `org.fpsot.identity.*`; record them as the FPSOT observability specification sets (IAM-090).
- Each event holds time, type, outcome, opaque actor, client and session IDs, trace ID, level, the represented party and the `act` chain (IAM-091).
- `access.evaluated` holds subject, action, resource, decision, policy version, engine ID and a hash of the context, for every decision (IAM-092).
- Never log secrets, tokens, cookies, keys, names, emails, birth dates or identifying numbers; truncate IP addresses to /24 and /48, except failed sign-in and suspension events (may) (IAM-093).
- Publish a JSON Schema per type (API-103); lowerCamelCase fields; code list values with English and French labels (IAM-094).
- Use the fixed reasons for `session.ended` and `authentication.failed` (IAM-095).

## Errors

- Send the OAuth `WWW-Authenticate` header and a problem details body that does not replace or contradict it (IAM-100).
- Use the types under `https://fpsot.org/problems/identity/` from `registry/problem-types.json` when one fits, else the shared types of API-032; `acrValues` and `maxAge` for step up (IAM-101).
- Never reveal the policy, rule or relationship behind a denial, whether a resource or account exists, or which factor failed (IAM-102).
- Authorization and token endpoints keep OAuth and OpenID Connect error responses (IAM-103).
