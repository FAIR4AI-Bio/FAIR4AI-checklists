# FAIR4AI-Bio Checklist — Rating Rubric

*Companion scoring guide for `DRAFT AI-ready checklist_v20260726.csv`.*

**Started:** 2026-07-25 · **Maintainer:** Eric Sokol

---

## 1. Purpose & scope

The checklist is an **evaluation instrument, not a metadata template** (see
`PROGRESS.md` §1 and `NOTES_AND_FUTURE_DIRECTIONS.md` FD-1). Each of its 96 items poses
one assessable question about a target dataset. This rubric defines **how a reviewer or
the `fair4ai-eval-agent` decides which rating an item receives** — so ratings are
consistent across items, datasets, and runs.

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

An item is rated **`N/A`** when — and only when — its `Use-case scope (Condition)` (CSV
col 8) does not apply to the target dataset. Two triggers:

1. **Scope mismatch** — the item is scoped to a use case the dataset is not an instance
   of. Examples from the checklist:
   - Items scoped `Derived/compiled datasets` (e.g. *Source data DOI*, *Provenance
     Tracking*, *citation of subsumed datasets*) → **`N/A`** for a primary/original dataset.
   - Items scoped `Human/sensitive data` or `Restricted/sensitive data` (e.g. *Data
     Anonymization*, *Restricted Data Access*) → **`N/A`** for a dataset with no personal or
     sensitive content.
   - Items scoped `Experimental data` (*Is it experimental data* follow-up *design
     description*) → **`N/A`** for a purely observational dataset.
2. **Modality mismatch** — the item is scoped to a data modality the dataset does not
   contain. Examples:
   - *Language (for text data - IO)*, scoped `Text/NLP (textual data)` → **`N/A`** for an
     image-only or tabular dataset.
   - *Sensor Metadata (link)* / *resolution information*, scoped to sensor/instrument or
     image/audio/video modalities → **`N/A`** for a dataset with no such captures.

**What does NOT make an item `N/A`:**
- The `Required (core, auto, or recommended)` tier (col 7) never triggers `N/A`. A missing
  *recommended* item that is in scope is `does not meet` (just lower-weight; see below),
  not `N/A`.
- Items scoped `All use cases` are **never `N/A`** — they are always rated `meets` /
  `partial` / `does not meet`.

**Required tier affects weight, not rating.** `core` items that are `does not meet` are
the most consequential gaps; `recommended` items that are `does not meet` are minor gaps.
The tier changes how a low rating rolls up into a score — it does not change which of the
four ratings the item gets. (`auto` items are ones an agent/repository can infer rather
than the publisher stating them; rate them on whether that inference is supportable from
present metadata.)

---

## 4. Grouped guidance by criteria type

The `Criteria: Structural/Scientific/Provenance` column (col 3) tags what *kind* of
readiness each item probes, using canonical tokens (`Structural`, `Scientific`,
`Provenance`) and their `/`-joined blends (e.g. `Structural/Scientific`,
`Provenance/Scientific`). This column drives the **AI-FAIR** assessment (see §6). When an
item lists more than one facet, rate it against **each** applicable facet and take the
**lower** rating as the item's rating (an item that is structurally fine but
scientifically unusable is only `partial`). The definitions in §2 still govern; the
guidance below says what "present / incomplete / absent" concretely look like for each
facet.

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

---

## 5. Worked examples

Grounded in a candidate pilot target (a NEON-style primary occurrence/image dataset such
as *2018 NEON Ethanol-preserved Ground Beetles*). Ratings are illustrative.

| Item (CSV) | Criteria | Scope | Illustrative `status` | Why (evidence) |
|---|---|---|---|---|
| **file format** | Structural | All use cases | **`meets`** | Formats declared (e.g. `image/jpeg`, `text/csv`) and mapped to `sc:encodingFormat` / `cr:FileObject` — machine-actionable. |
| **Bias** | Scientific | All use cases | **`partial`** | Metadata acknowledges collection bias in one prose sentence but does not say which biases, where, or how severe — discernible intent, not actionable. (Note: enumerated-list phrasing in the definition is aspirational; prose that is specific enough still earns `meets`.) |
| **License** | Provenance | All use cases | **`meets`** *(or `partial`)* | An SPDX-identified, machine-readable license (`sc:license`) → `meets`; a bespoke license stated only in prose → `partial` (see *Standardized/Machine-readable?*). |
| **Language (for text data - IO)** | Structural | Text/NLP | **`N/A`** | Dataset contains images + occurrence tables, no textual data — modality mismatch (§3.2). |
| **Source data DOI** | Provenance | Derived/compiled datasets | **`N/A`** | A primary NEON dataset is not derived from other datasets — scope mismatch (§3.1). |

---

## 6. Relationship to the `fair4ai-eval-agent`

The agent (`/evaluate-dataset`) answers each checklist item from a dataset's metadata and
emits, per item, a `status` plus an `evidence` string, `notes`, `recommendation`, and the
`fair4ai_category` / `criteria` / `section` values copied verbatim from the checklist, then
computes a `summary.fair4ai_scores` block. The four `status` values are exactly the rubric
levels in §2 — `meets`, `partial`, `does not meet`, `N/A` — so nothing needs translating:

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
  checklist's `FAIR4AI category` column (the historical `AI-ready` token is ignored here);
  `overall` = equal-weight mean of the non-null dimensions.
- **AI-FAIR** — four categories built from the `Criteria` column (§4) and the **Governance**
  broad category: `ml_ready` (structural), `ai_ready_for_task` (structural + scientific),
  `traceable` (provenance + structural), and `care_compliance` (the governance items — see
  below); `overall` = equal-weight mean of the four.

**Governance / CARE.** The five items in the **Governance** broad category (based on the
CARE Data Governance specification published with IEEE in 2025) are scored as their own
`care_compliance` category via each response's `section` value — so the agent must copy the
Broad category label **verbatim**. This is what makes ethical/CARE readiness a first-class,
separately visible score rather than being absorbed into "reusable". Rate these items with
the same four levels and the §4c provenance guidance; a missing permission/steward/consent
disclosure that is in scope is `does not meet`, not `N/A`.

---

## 7. Maintenance

Update this rubric whenever the checklist's rating semantics change (new scopes that
affect the `N/A` rule, a decision to weight `core`/`recommended` differently, or — per
FD-1 — if/when a controlled vocabulary is ever adopted for a specific item). Keep the four
`status` values and the `N/A` rule stable so scores remain comparable across dataset
evaluations and across gap-analysis re-runs.
