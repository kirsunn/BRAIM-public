# BRAVO v0.4 Architecture Update

> **Architecture update v0.4:** BRAIM is hosted inside BRAVIUM-Planet. The BRAV container is `IFCA + BAR + BAV + RAG + BAG`. BAV is validated against RAG; BAG records activity and decisions. See [`BRAVO_ARCHITECTURE_V0_4.md`](../architecture/BRAVO_ARCHITECTURE_V0_4.md).

# BRAVO — Critique Response and v0.2 Plan

Version: 0.2
Date: 2026-10-18
Status: Planning document
Purpose: respond to external critique and define the next practical iteration of BRAVO

## 1. What the critiques confirm

Both external reviews support the core direction of BRAVO:

- BAV as a verifiable building entity;
- separation of geometry and semantics;
- identity, traceability and evidence;
- versioned Ruleset Packages;
- human-in-the-loop decision-making;
- a focused MVP.

They also identify the same main risks:

- the term "avatar" may be unclear;
- BAR and VAR may overlap;
- Ruleset Packages need conflict handling and scalable updating;
- users may be overloaded by findings;
- integration with existing systems is a major risk;
- data security, user onboarding and pilot planning are missing.

This document turns those observations into v0.2 decisions.

## 2. BAV versus digital twin

BAV should not be explained as simply a smarter digital twin.

| Question | Digital twin | BAV |
|---|---|---|
| What does it show? | Current or near-real-time building state | Building as an explainable, checkable entity |
| Main focus | Monitoring, simulation, operations | Requirements, evidence, validation, decisions |
| Core question | "How does the building work now?" | "Why is it designed this way, what applies, and what would change mean?" |
| Typical output | Dashboard, sensor data, simulation | Finding, evidence, treatment proposal, decision record |

Working definition:

```text
A digital twin shows how a building behaves.
A BAV explains how a building is organized,
which requirements apply to it,
on what evidence decisions were made,
and what changes would mean.
```

BAV may consume digital-twin data, but it is not defined by sensors or real-time operation.

## 3. BAR and VAR: clear separation

| Component | Question it answers | Contains |
|---|---|---|
| **BAR** | "Which avatars, versions and statuses exist?" | Avatar registry, version history, status, evidence references, rule bindings |
| **VAR** | "How does a specific version look and how is it exchanged?" | Versioned representation, snapshot or delta, manifest, exchange payload |

Short formula:

```text
BAR is the catalog and journal.
VAR is the representation and transport artifact.
```

Example:

```text
BAR says: BAV-001 has version 7, status draft, evidence E1-E5.
VAR defines: what version 7 contains, how it is serialized,
how it is hashed, and how it can be exchanged.
```

## 4. Ruleset Package: scale and conflicts

A Ruleset Package must not silently resolve conflicts.

### Rule statuses

```text
active
conditional
deprecated
superseded
```

### Conflict handling

```text
1. If two rules conflict, both remain visible.
2. The system shows both sources and applicable editions.
3. The system does not choose a winner silently.
4. A human or a defined policy resolves the conflict.
5. The resolution is recorded.
```

### Priority model

```text
1. Mandatory requirement
2. Conditional requirement
3. Recommendation
4. Information
```

Regional or project-specific rules may refine general rules, but must explicitly reference the rule they refine, replace or conflict with.

### Rule updates

Rule updates are proposed by Planet, reviewed, versioned and only then made available. A Local Core pins a specific version; it does not automatically replace the knowledge used for a validation.

## 5. Findings and Treatment UX

BRAVO should not turn every check result into a separate alarm.

### Grouping principle

```text
Not: 12 separate notifications.
But: 1 scenario, for example "evacuation on floor 3".
```

### Finding card

A finding should answer:

```text
What is wrong?
Where is it?
Why does it matter?
Which source applies?
What can be done?
What decision is required?
```

### Treatment flow

```text
Finding
-> Grouped scenario
-> 1-3 treatment options
-> Impact preview
-> Human approval
-> Controlled application
-> Recheck
```

A Treatment Package should usually address one clear problem, not a large batch of unrelated changes.

## 6. Data security and access

Security is a first-class requirement, not a later feature.

### Principles

```text
1. Project data remains under project control.
2. Local Core may work without sending the full model to the cloud.
3. Planet receives only the minimum needed to select applicable rules.
4. Access is role-based.
5. Every important action is recorded.
6. Sensitive project data is not published publicly.
```

### Minimum v0.2 security model

```text
- Local / server deployment option
- Role-based access: owner, editor, reviewer, viewer
- Audit log for validation, approval and publication
- Explicit separation of public specifications and private project data
- No automatic upload of full BAV to Planet
```

## 7. User onboarding

BRAVO must be understandable without a long manual.

### Onboarding principles

```text
1. Start with one question, not with the full architecture.
2. Show a simple building fragment first.
3. Explain every finding in plain language.
4. Always show the source of a rule.
5. Make the first successful check reachable in minutes.
```

### First-user scenario

```text
1. Open a small residential floor.
2. Ask: "Are evacuation paths compliant?"
3. See one grouped finding.
4. Open evidence.
5. See treatment options.
6. Approve or reject.
7. See the recheck result.
```

### Learning model

```text
- Guided first scenario
- Plain-language explanations
- Glossary available in context
- Examples for each rule type
- Progressive disclosure of advanced features
```

## 8. Integration strategy

Integration should be incremental, not a big-bang replacement.

| Stage | Integration target | Approach |
|---|---|---|
| 1 | IFC / IFC5 files | Import and map to BAV |
| 2 | CDE | Reference artifacts, do not replace CDE |
| 3 | BCF | Exchange findings and issues |
| 4 | Design tools | Read/write through connectors |
| 5 | Calculation tools | Consume results as evidence, not as approvals |

Integration rule:

```text
BRAVO connects to existing systems.
It does not require replacing them on day one.
```

## 9. Pilot plan

The pilot should prove one complete chain on a real or realistic project.

### Pilot scope

```text
1. One residential building or fragment
2. One floor or limited set of spaces
3. 3-5 rules
4. One Ruleset Package
5. One user role: project reviewer
6. One grouped finding scenario
7. One treatment proposal
8. One approval and recheck
```

### Pilot success criteria

```text
1. A reviewer understands a finding without help.
2. Every finding has evidence.
3. The used ruleset version is recorded.
4. A treatment can be reviewed and approved.
5. A recheck shows the result of the decision.
6. No project data is published without explicit control.
```

## 10. Narrow MVP for v0.2

```text
1. One building type: residential
2. One floor or small fragment
3. 3-5 rules
4. One ruleset package
5. Simple checks: width, existence, classification
6. One evidence source per rule
7. One grouped finding scenario
8. One treatment proposal
9. One human approval
10. One recheck
```

The MVP succeeds if a reviewer can see:

```text
Here is a problem.
Here is why it matters.
Here is the official source.
Here is the affected BAV element.
Here are possible solutions.
Here is the impact.
Here is the human decision.
Here is the recheck result.
```

## 11. v0.2 roadmap

| Step | Result |
|---|---|
| 1 | BAV Core Schema v0.1: entities, IDs, classifications, properties, relations |
| 2 | BAR Registry Model v0.1: avatars, versions, statuses, evidence links |
| 3 | VAR Representation Model v0.1: snapshot, manifest, hash, delta concept |
| 4 | Ruleset Package conflict and update policy v0.1 |
| 5 | Finding grouping and severity model v0.1 |
| 6 | Treatment Package UX flow v0.1 |
| 7 | Security and access model v0.1 |
| 8 | Onboarding scenario v0.1 |
| 9 | MVP pilot scenario: residential floor, 3-5 rules |
| 10 | Review and simplification pass |

## 12. Success metrics

| Metric | Target |
|---|---|
| Time to understand a finding | Under 1 minute for a non-author |
| Evidence traceability | Every finding has a source link |
| Rule version pinning | Every validation records package version |
| Treatment clarity | Each treatment shows impact before approval |
| Human control | No change is applied without approval |
| Data control | No full BAV upload without explicit user action |
| Pilot demonstration | One complete finding-to-recheck chain |

## 13. What we will not do in v0.2

```text
No full normative coverage
No autonomous design
No automatic publication
No replacement of CDE
No replacement of calculation software
No black-box AI decisions
No silent conflict resolution
No mandatory cloud upload of project data
```

## 14. Main v0.2 formula

```text
One building fragment.
A few clear rules.
One evidence chain.
One understandable finding.
One reviewable treatment.
One human decision.
One recheck.
One secure, local-first deployment.
```

> The goal of v0.2 is not to build everything.
> The goal is to make one real scenario understandable, traceable, secure and useful.