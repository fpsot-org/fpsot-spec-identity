# Terms needed in the FPSOT term base

These entries are not yet in `fpsot-spec-writing/termbase/terms.yaml` (writing v0.2.5).
The pages use them already. Each entry is in the format of `terms.yaml`.

The French terms are the usual Canadian terms, but their GDT and TERMIUM Plus records were not read: the GDT search could not be queried by automated reads and TERMIUM Plus returned 403.
The project lead or the term-base pull request must confirm each French term against the GDT before merge.

```yaml
  - id: access-token
    kind: term
    en: {full: "access token", definition: "A credential that an authorization server issues to a client, so that the client can call an API within set limits."}
    fr: {full: "jeton d'accès", definition: "Justificatif qu'un serveur d'autorisation remet à un client, pour que celui-ci appelle une API dans des limites fixées."}
    source: {name: "IETF RFC 6749 (English); French to be verified in the Grand dictionnaire terminologique", url: "https://www.rfc-editor.org/info/rfc6749", checked: "2026-11-10"}
  - id: authorization-engine
    kind: term
    en: {full: "authorization engine", definition: "A service that decides whether a subject may take an action on a resource, from policies and relationships, and returns the decision to the service that asks."}
    fr: {full: "moteur d'autorisation", definition: "Service qui décide si un sujet peut faire une action sur une ressource, à partir de politiques et de relations, et qui rend la décision au service qui la demande."}
    source: {name: "OpenID AuthZEN Authorization API 1.0 (policy decision point; English); French to be verified in the Grand dictionnaire terminologique", url: "https://openid.net/specs/authorization-api-1_0-final.html", checked: "2026-11-10"}
  - id: identity-provider
    kind: term
    en: {full: "identity provider", definition: "A service that signs people or workloads in and tells other services who they are and how they signed in."}
    fr: {full: "fournisseur d'identité", definition: "Service qui connecte des personnes ou des charges de travail et qui indique aux autres services qui elles sont et comment elles se sont connectées."}
    source: {name: "NIST SP 800-63C-4 (English); French to be verified in the Grand dictionnaire terminologique", url: "https://pages.nist.gov/800-63-4/sp800-63c.html", checked: "2026-11-10"}
```
