# NEON Beetles Landing Page Retrieval Notes

**Landing Page URL:** https://data.neonscience.org/data-products/DP1.10022.001

**Retrieval Status:** Limited (JavaScript-rendered page)

## Retrieved Content
The landing page appears to be JavaScript-rendered and returned only a minimal page fragment:
- Page title: "NEON | Data Product"
- No structured metadata, JSON-LD, or schema.org markup was accessible via WebFetch

## Expected Content (not retrieved)
The landing page typically contains:
- DOI: 10.48443/q9ne-6b77 (for RELEASE-2026)
- Product title: "Ground beetles sampled from pitfall traps"
- Abstract/description
- Keywords
- Science team information
- Data package formats (basic/expanded; bet_* tables)
- Methods documentation links:
  - Protocol: NEON.DOC.014050
  - Science design: NEON.DOC.000909
  - User guide: NEON_beetle_userGuide_vG
  - Quick Start Guide: NEON.QSG.DP1.10022.001v2
  - DQ ATBD: NEON.DOC.005424
- Citation information
- Biorepository/DarwinCore archive links

## Workaround
All essential metadata was successfully retrieved from the NEON API endpoints:
- Product API: https://data.neonscience.org/api/v0/products/DP1.10022.001
- Release API: https://data.neonscience.org/api/v0/products/DP1.10022.001/RELEASE-2026

## Limitation Note for Evaluations
JavaScript-rendered landing pages may not be fully accessible to automated retrieval tools. The NEON API endpoints provide comprehensive machine-readable metadata as an alternative access method.
