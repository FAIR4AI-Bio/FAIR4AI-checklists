# FAIR4AI-Bio Checklist — Rating Rubric

*Companion scoring guide for `CHECKLIST.csv`.*

**Started:** 2026-07-25 · **Maintainer:** Eric Sokol

---

## 1. Purpose & scope

The checklist is an **evaluation instrument, not a metadata template** (see
`PROGRESS.md` §1 and `NOTES_AND_FUTURE_DIRECTIONS.md` FD-1). Each of its 89 items poses
one assessable question about a target dataset. This rubric defines **how a reviewer or
the `fair4ai-eval-agent` decides which rating an item receives** — so ratings are
consistent across items, datasets, and runs.

**Where the guidance lives.** Judge each item against its `Requirement Definition` in the
checklist (what the item asks the dataset to disclose), and use **this rubric as the
authoritative, overarching framework** for deciding which rating that item earns: the four
rating levels (§2), the N/A rule (§3), the facet-level guidance that says what "present /
incomplete / absent" concretely look like for each kind of readiness (§4), the evidence
requirement, and the scoring math (§6). There are no per-item `Scoring: Meets / Partial /
Does Not Meet` cells — the rubric's section-level guidance is what makes ratings consistent
across items, datasets, and runs. The one item-specific cell that remains is **`Scoring:
NA`**, which is authoritative **for the `N/A` decision only** (§3): it states, per item, the
condition under which that item does not apply.

What it rates: the **Data** vertex of the Question–Data–Model triangle — whether a
dataset *communicates* the information an AI/ML user would need. It rates **what the
metadata discloses**, not whether the dataset conforms to any fixed vocabulary. A dataset
does **not** have to use a controlled enumeration to score well; it only has to make the
relevant information present and locatable. (This preserves the FD-1 stance: *enable, do
not enforce*.)

This rubric is also intended to be publishable as an interim community standard: it tells
publishers what would raise a dataset's AI-readiness score tomorrow, without mandating a
schema today (FD-1, future direction 4).

Read alongside: `CHECKLIST_OVERVIEW.md` (the 9 sections), `NOTES_workflow.md` (the Q–D–M
frame), and FD-1 (why vocabularies are deferred).

---

## 2. The four rating levels (general definitions)

Every item is rated with exactly one of these four `status` values. These are the same
strings the `fair4ai-eval-agent` emits and the scoring script reads — there is **no
separate rubric vocabulary to translate**. They apply to all items regardless of section.

| `status` | Definition |
|---|---|
| **`meets`** | The information the item asks for is **clearly present and evidence-locatable** in the dataset's metadata. A reviewer or agent can point to the specific place it lives (a field, a mapped element, a linked resource that actually resolves) and cite it. |
| **`partial`** | The information is **present but incomplete, ambiguous, buried in free text, or not machine-locatable**. The intent is discernible but a user could not rely on it without extra interpretation, or it covers only some of what the item asks (e.g. some variables but not all; a link that resolves but lacks the required detail). |
| **`does not meet`** | The item **applies to this dataset but the information is absent or not findable** in the metadata. Includes dangling pointers to resources that do not resolve. |
| **`N/A`** | The item **does not apply to this dataset** — its use-case scope or modality is not present (see §3). `N/A` is *not* a penalty; it removes the item from this dataset's denominator. |

**Evidence is required for `meets` and `partial`.** A rating of `meets` or `partial`
must be backed by a concrete `evidence` citation (the metadata text, field, or resolvable
link that justifies it). If no evidence can be cited, the correct rating is `does not
meet`, not `meets`. This matches the `fair4ai-eval-agent`'s per-item `status` + `evidence`
contract (§6).

---

## 3. The N/A rule (when an item is not applicable)

An item is rated **`N/A`** when — and only when — the condition in its **`Scoring: NA`**
column applies to the target dataset. That cell states, per item, the specific situation in
which the item does not apply. Two recurring shapes of that condition:

1. **Scope mismatch** — the item's `Scoring: NA` cell names a use case the dataset is not an
   instance of. Examples from the checklist:
   - Derived/compiled-only items (e.g. *Upstream Source Attribution and DOIs*, *Source Data
     Cryptographic Checksums*) → **`N/A`** for a primary/original dataset.
   - Conditional-disclosure items whose `Scoring: NA` cell describes the absence of the
     condition (e.g. *Sensitive Data Handling and Obfuscation* → `N/A` when the dataset has
     no PII or sensitive localities; *Access Restriction Justification* / *Secure Access
     Procedure* → `N/A` when the dataset is fully open).
   - Experimental-design items (*Experimental Factor Specification*) → **`N/A`** for a purely
     observational dataset.
2. **Modality mismatch** — the item's `Scoring: NA` cell names a data modality the dataset
   does not contain. Examples:
   - *Natural Language Specification* → **`N/A`** for a dataset with no textual features.
   - *Sensor and Instrument Metadata* / *Quantitative Resolution Metrics* → **`N/A`** for a
     dataset with no sensor/instrument captures or continuous resolution dimensions.

**What does NOT make an item `N/A`:**
- Items whose `Scoring: NA` cell reads **"Never NA …"** are always rated `meets` /
  `partial` / `does not meet`, never `N/A`.
- A conditional-disclosure item is `N/A` when the condition is **absent**, `meets` when the
  condition is present **and** documented — never `does not meet` for a clean dataset with
  nothing to disclose (that polarity error wrongly drags the score down).

`N/A` removes the item from this dataset's denominator (§6); it is not a penalty.

---

## 4. Grouped guidance by criteria type

This section is the **authoritative rating guidance** (see §1): it explains what the AI-FAIR
facets mean and, for each facet, what `meets` / `partial` / `does not meet` concretely look
like, so ratings stay consistent across items and the score is interpretable. Apply the facet
guidance below together with the item's `Requirement Definition`.

The `AI FAIR Criteria: Structural | Scientific | Provenance | Governance` column tags what *kind*
of readiness each item probes, using canonical tokens (`Structural`, `Scientific`, `Provenance`,
`Governance`) and their ` | `-joined blends (e.g. `Structural | Scientific`, `Scientific |
Provenance`, `Provenance | Governance`). This column drives the **AI-FAIR** assessment (see §6):
the first three tokens are scoring facets; `Governance` routes the item to the `care_compliance`
category. When an item lists more than one facet, rate it against **each** applicable facet and
take the **lower** rating as the item's rating (an item that is structurally fine but
scientifically unusable is only `partial`). The definitions in §2 still govern; the guidance below
says what "present / incomplete / absent" concretely look like for each facet.

### 4a. Structural criteria
*Machine-readability, formats, schema, organization, resolvable mappings.* Ask: **could a
pipeline ingest this without a human interpreting prose?**

- **`meets`** — format/structure is explicit and machine-actionable: open/known file
  formats declared, schema or data dictionary present, records/files/assets and their
  relationships documented, and the relevant standard mapping (EML/DataCite/SOSO/
  Croissant) resolves to real content.
- **`partial`** — structure is described only in narrative prose, partially
  specified (some files/variables documented, others not), or a mapping exists but is
  incomplete or proprietary-format-only.
- **`does not meet`** — no structural description; format unknown or unstated; mapped
  element or link does not resolve.

### 4b. Scientific criteria
*Sampling semantics, taxonomy, fitness-for-question, biases/limitations, intended use.*
Ask: **can a user judge whether the data are scientifically fit for their question?**

- **`meets`** — the scientific context needed to judge fitness is disclosed: collection
  method/design, effort/resolution where relevant, taxonomy/units, and known
  biases/limitations/intended-uses stated clearly enough to act on (structured **or**
  well-organized prose both qualify — no enum required).
- **`partial`** — the information is gestured at but not specific enough to act on
  (e.g. bias acknowledged in one vague sentence; "labeled" stated without saying what was
  labeled or by whom; resolution implied but not quantified).
- **`does not meet`** — the scientific context the item asks for is absent, leaving the
  user unable to assess fitness-for-use.

### 4c. Provenance criteria
*Source chain, attribution, licensing, identifiers, governance/CARE.* Ask: **can origin,
rights, and responsibility be established and trusted?**

- **`meets`** — origin and responsibility are traceable and citable: creators/contacts,
  persistent identifiers (DOI/ORCID), a machine-readable license, and — for derived data —
  a resolvable link back to sources; governance/CARE conditions disclosed where relevant.
- **`partial`** — provenance is partial: attribution present but no persistent ID; a
  license stated in prose but not machine-readable/SPDX; sources named but not linked; a
  derived dataset naming sources without checksums or DOIs.
- **`does not meet`** — origin, license, or responsible party cannot be established from the
  metadata.

### 4d. Governance criteria (CARE)
*Consent, permissions, stewardship, and responsible-party disclosure for governed / CARE /
Indigenous or community data.* Ask: **are the ethical/CARE conditions for using these data
disclosed and honorable?** (Based on the CARE Data Governance specification published with IEEE
in 2025.) This facet feeds the `care_compliance` category (§6).

- **`meets`** — the governance conditions the item asks for are disclosed: permission-to-collect,
  the agent granting permission, the people/communities stewarding the observations, and the
  actions/provenance that led to a data point are stated clearly enough to honor.
- **`partial`** — governance is gestured at but incomplete (e.g. a community named without the
  permission/stewardship terms; consent implied but not documented).
- **`does not meet`** — a governance/CARE disclosure that is **in scope** (governed / CARE /
  Indigenous or community data) is absent. Note: for data with no such governance dimension the
  correct rating is `N/A` (scope mismatch, §3), **not** `does not meet`.

---

## 5. Worked examples

Grounded in a candidate pilot target (a NEON-style primary occurrence/image dataset such
as *2018 NEON Ethanol-preserved Ground Beetles*). Ratings are illustrative.

| Item (CSV) | Criteria | Illustrative `status` | Why (evidence) |
|---|---|---|---|
| **Standardized File Formats** | Structural | **`meets`** | Formats declared (e.g. `image/jpeg`, `text/csv`) and mapped to `sc:encodingFormat` / `cr:FileObject` — machine-actionable. |
| **Known Dataset Biases** | Scientific | **`partial`** | Metadata acknowledges collection bias in one prose sentence but does not say which biases, where, or how severe — discernible intent, not actionable. (Note: enumerated-list phrasing in the definition is aspirational; prose that is specific enough still earns `meets`.) |
| **Dataset License Specification** | Provenance \| Governance | **`meets`** *(or `partial`)* | An SPDX-identified, machine-readable license (`sc:license`) → `meets`; a bespoke license stated only in prose → `partial`. |
| **Natural Language Specification** | Structural | **`N/A`** | Dataset contains images + occurrence tables, no textual data — its `Scoring: NA` cell (no textual features) applies (§3.2). |
| **Upstream Source Attribution and DOIs** | Provenance | **`N/A`** | A primary NEON dataset is not derived from other datasets — its `Scoring: NA` cell (primary-only data) applies (§3.1). |

---

## 6. Relationship to the `fair4ai-eval-agent`

The agent (`/evaluate-dataset`) answers each checklist item from a dataset's metadata and
emits, per item, the `item` label and `requirement_definition` copied from the checklist, a
`status`, an `evidence` string, `notes`, `recommendation`, and the `fair_category` /
`ai_fair_criteria` values copied verbatim from the checklist, then computes a
`summary.fair4ai_scores` block. (Older evaluations used the field names `criteria` plus
`section`/`sub_section`; the scorer still accepts them for backward compatibility.) The four
`status` values are exactly the rubric levels in §2 — `meets`, `partial`, `does not meet`,
`N/A` — so nothing needs translating:

| `status` | Evidence expectation |
|---|---|
| `meets` | `evidence` required — cite the field/element/link |
| `partial` | `evidence` required — cite what is present |
| `does not meet` | `notes` may say where it was expected |
| `N/A` | `notes` should name the scope/modality that is absent |

The scores are computed deterministically from these four `status` values by the
**`fair4ai-scoring`** skill (`scripts/compute_fair4ai_scores.py`): `meets → 1`,
`partial → 0.5`, `does not meet → 0`, `N/A`/blank → excluded. The script produces **two
complementary assessments**, both in 0–1 (1 = most FAIR4AI):

- **Traditional FAIR** — findable / accessible / interoperable / reusable, keyed off the
  checklist's `FAIR category` column;
  `overall` = equal-weight mean of the non-null dimensions.
- **AI-FAIR** — four categories built from the `AI FAIR Criteria …` column (§4): `ml_ready`
  (structural), `ai_ready_for_task` (structural + scientific), `traceable` (provenance +
  structural), and `care_compliance` (the `Governance` facet — see below); `overall` =
  equal-weight mean of the four.

**Governance / CARE.** The governance items (based on the CARE Data Governance specification
published with IEEE in 2025) carry a `Governance` token in their `AI FAIR Criteria …` column and
are scored as their own `care_compliance` category. This is what makes ethical/CARE readiness a
first-class, separately visible score rather than being absorbed into "reusable". Governance is
now a criteria facet across **11 items**; **5 of those also sit in the Governance broad category**.
The scorer detects governance from the item's `ai_fair_criteria` value (an older evaluation's
`section = Governance` still works as a backward-compatible fallback). Rate these items with the
same four levels and the §4d governance guidance; a missing permission/steward/consent disclosure
that is in scope is `does not meet`, while data with no governance dimension at all is `N/A`.

---

## 7. Maintenance

Update this rubric whenever the checklist's rating semantics change (new scopes that
affect the `N/A` rule, a decision to weight `core`/`recommended` differently, or — per
FD-1 — if/when a controlled vocabulary is ever adopted for a specific item). Keep the four
`status` values and the `N/A` rule stable so scores remain comparable across dataset
evaluations and across gap-analysis re-runs.
