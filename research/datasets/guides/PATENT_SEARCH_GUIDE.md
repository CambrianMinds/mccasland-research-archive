# Patent Database Search Strategy & Technical Analysis
**Research Phase:** Post-extended analysis  
**Targeting:** USPTO, WIPO, Google Patents for novel technical integration claims  
**Prepared:** April 19, 2026

---

## Strategic Overview

Based on SOURCE_EXPANSION_EXTENDED.md analysis, patent searches should focus on:

1. **Electret + Plasma Integration** — Not found in IEEE antenna literature
2. **Solid-State Alternator + MHD** — Component pairing not documented
3. **Sintered Ceramic + Plasma Boundary** — Specific materials application
4. **Closed-Cycle Propulsion System** — Integration of known components

**Search Confidence:** Medium  
**Expected Hit Rate:** 5-15% (many components exist separately)  
**Timeline:** 1-2 hours per search domain

---

## Patent Database Resources

### Primary Databases (Free)

**1. Google Patents** (patents.google.com)
- Coverage: USPTO, WIPO, EPO, JP, CN (global)
- Strengths: Full-text search, family grouping, citation analysis
- Export: CSV, PDF, links
- **Best for:** Broad searches, US/international comparison

**2. USPTO (uspto.gov)**
- Coverage: US patents only, most comprehensive
- Strengths: Advanced search operators, classification browsing
- Export: Text, PDF
- **Best for:** Detailed US patent analysis, IPC/CPC classification

**3. WIPO (wipo.int/portal/en/)**
- Coverage: International patents, PCT applications
- Strengths: Global coverage, treaty information
- Export: Links, XML
- **Best for:** International patent strategy, priority dates

**4. espacenet.com** (European Patent Office)
- Coverage: European patents + international family trees
- Strengths: Global database, application status
- Export: PDF, links
- **Best for:** Priority dates, filing history, family patents

### Secondary Databases (Limited Access)

- **IEEE Xplore**: IEEE patent abstracts (limited)
- **ArXiv**: Preprints on plasma physics, propulsion
- **ProQuest Dissertations & Theses**: Academic research (MIT, UCSD, AFIT theses)

---

## Primary Search Terms & Strategies

### Search 1: Electret + Plasma Integration

**Primary Terms:**
- "electret" AND "plasma"
- "electret" AND "propulsion"
- "electret" AND "boundary layer"
- "electret polymer" AND "ionization"
- "electrostatic" AND "plasma" AND "propulsion"

**Classification:**
- IPC: H01L (Semiconductor devices), H05H (Plasma technique)
- CPC: H01L27 (Semiconductor devices with at least two potential barriers), H05H1 (Plasma generation)
- USPC: 315 (Electric apparatus), 250 (Radiant energy)

**Expected Results:** 50-200 patents (many antenna-related, few propulsion-related)

**Novelty Threshold:** Patents combining all three terms with propulsion application

---

### Search 2: Solid-State Alternator + MHD

**Primary Terms:**
- "solid state alternator" AND "magnetohydrodynamic"
- "solid state alternator" AND "MHD"
- "semiconductor" AND "magnetohydrodynamic" AND "power"
- "magneto-hydro-dynamic" AND "solid state"
- "MHD generator" AND "alternator"

**Classification:**
- IPC: F25K (Apparatus for generating cold), H02K (Dynamo-electric machines)
- CPC: F03D (Wind motors), H02K (Dynamo-electric machines)
- USPC: 310 (Electrical generators), 322 (Electricity distribution)

**Expected Results:** 20-100 patents (MHD well-documented, alternator integration less common)

**Novelty Threshold:** Patents combining solid-state semiconductor with MHD generator technology

---

### Search 3: Sintered Ceramics + Plasma Boundary

**Primary Terms:**
- "sintered ceramic" AND "plasma"
- "ceramic" AND "plasma boundary" AND "containment"
- "sintered" AND "plasma" AND "propulsion"
- "refractory ceramic" AND "plasma layer"
- "ceramic matrix" AND "plasma electrode"

**Classification:**
- IPC: C01B (Non-metallic elements), H05H (Plasma techniques)
- CPC: C01B25 (Boron compounds), H05H1 (Plasma generation)
- USPC: 250 (Radiant energy), 423 (Chemistry of non-metallic compounds)

**Expected Results:** 30-150 patents (ceramics documented, plasma boundary application novel)

**Novelty Threshold:** Patents specifically using sintered ceramics to contain/boundary plasma

---

### Search 4: Closed-Cycle Propulsion System

**Primary Terms:**
- "closed cycle" AND "propulsion"
- "closed loop" AND "plasma propulsion"
- "closed system" AND "electric propulsion"
- "regenerative cycle" AND "propulsion"
- "MHD" AND "closed cycle" AND "propulsion"

**Classification:**
- IPC: B64B (Balloons, dirigibles), F03B (Machines for generating power)
- CPC: B64B1 (Balloons or other non-rigid aircraft), F03B (Power generation)
- USPC: 244 (Aeronautics), 415 (Elevator and hoists)

**Expected Results:** 10-50 patents (closed-cycle propulsion relatively rare)

**Novelty Threshold:** Patents integrating closed-cycle system with plasma/electrostatic propulsion

---

### Search 5: Z-Pinch Propulsion Integration

**Primary Terms:**
- "Z-pinch" AND "propulsion"
- "Z pinch" AND "spacecraft propulsion"
- "magnetic pinch" AND "propulsion"
- "z-axis" AND "plasma pinch" AND "propulsion"
- "theta-z pinch" AND "propulsion"

**Classification:**
- IPC: F03H (Plasma or particle engines)
- CPC: F03H1 (Plasma or particle engines)
- USPC: 244 (Aeronautics)

**Expected Results:** 5-30 patents (Z-pinch well-documented in fusion, propulsion application rare)

**Novelty Threshold:** Patents specifically applying Z-pinch principle to spacecraft propulsion

---

### Search 6: Marx Generator + Plasma Ignition

**Primary Terms:**
- "Marx generator" AND "plasma"
- "Marx" AND "ignition" AND "propulsion"
- "multistage capacitor" AND "plasma generation"
- "Marx circuit" AND "electrostatic propulsion"
- "high voltage pulse" AND "plasma initiation"

**Classification:**
- IPC: H05H (Plasma technique), H02H (Emergency protective devices)
- CPC: H05H1 (Plasma generation), H02H7 (Protective devices)
- USPC: 315 (Electrical apparatus), 307 (Electrical transmission or interconnection)

**Expected Results:** 20-100 patents (Marx well-documented, plasma ignition integration less common)

**Novelty Threshold:** Patents using Marx generator for plasma propulsion system ignition

---

## Advanced Search Operators

### Google Patents Syntax

```
"exact phrase" — Matches exact phrase
term1 OR term2 — Either term
-term — Exclude term
term* — Wildcard
SPEC:(term) — Search specifications only
TITLE:(term) — Search titles only
ASGN:(term) — Search assignee
CPCL:(term) — Search CPC classification
```

### USPTO Advanced Search Operators

```
(term1 AND term2) — Both terms
(term1 OR term2) — Either term
(term1 NOT term2) — First but not second
SPEC/[term] — Full text
TITL/[term] — Title only
ASNM/[term] — Assignee name
IPC/[code] — IPC classification
```

---

## Search Execution Roadmap

### Phase 1: Broad Searches (30 minutes)
1. **Google Patents** — All 6 search domains
2. **Document:** Patent titles, assignees, filing dates
3. **Filter:** Keep only 2015+ (recent technology), non-obvious assignees

### Phase 2: Classification Refinement (30 minutes)
1. **USPTO Classification Search** — Focus on CPC codes
2. **Document:** Classification hits, trending areas
3. **Filter:** Identify clusters, emerging patent categories

### Phase 3: Citation Analysis (30 minutes)
1. **Patent family analysis** — Citations between patents
2. **Document:** Who cites whom, priority dates
3. **Filter:** Identify key patents cited by multiple filers

### Phase 4: Assignee Analysis (30 minutes)
1. **Corporation/institution assignees** — Who files in these domains?
2. **Document:** Assignee distribution, institutional affiliations
3. **Filter:** Cross-reference with AFRL, LLNL, UCSD, MIT affiliations

---

## Key Patent Classifications Reference

### Plasma Techniques (IPC: H05H)
- H05H1 — Plasma generation, ionisation
- H05H3 — Plasma confinement
- H05H5 — Plasma actuation
- H05H7 — Plasma diagnostic devices

### Electrical Generators (IPC: H02K)
- H02K1 — Details of dynamo-electric machines
- H02K3 — Windings
- H02K7 — Structural association
- H02K27 — Electromagnetic couplings

### Magnetohydrodynamic Effects
- CPC: F03D — Wind motors (also applies to MHD)
- IPC: F03B — Machines for generating power from heat
- USPC: 310 — Electrical generators

### Propulsion Systems (IPC: B64)
- B64B — Balloons, airships, aircraft
- F03H — Plasma or particle engines (new classification, modern focus)

---

## Expected Patent Landscape Results

### Likely to Find
✓ **Individual Component Patents:**
- Plasma generation patents (thousands)
- Ceramic materials patents (thousands)
- Alternator designs (thousands)
- Solid-state switch patents (hundreds)

✓ **Related Integration Patents:**
- Plasma containment with specific materials
- High-voltage switching circuits
- Multi-stage power generation systems

### Unlikely to Find
✗ **Complete System Patents:**
- Closed-cycle propulsion integrating all components
- Z-pinch applied specifically to spacecraft propulsion
- Electret-plasma boundary layer in propulsion application

✗ **Recent Patents (2024-2026):**
- Novel integration unlikely to have published patents yet
- If filed in Feb 2026, would be pending, not published (18-month rule)

---

## Interpretation Guide

### Patent Filing & Publication Timeline
- **Filing Date** → Invention date (earliest priority)
- **Publication Date** → 18 months after filing (public disclosure)
- **Grant Date** → Typically 2-4 years after filing
- **If filed Feb 2026** → Would publish ~Aug 2027 (not yet visible)

### What Patent Absence Means

**If no patents found for integration claim:**

1. **Integration is genuinely novel** (no prior art)
   - Supports claim of original research
   - Suggests recent development (post-2024)
   
2. **Patents are pending/unpublished** (filed but not public)
   - Filed post-2024, publish timeline: 2025-2026
   - If classified, never published (government patents)
   
3. **Integration considered unpatentable** 
   - Obvious combination of known components
   - Research-stage only, not commercialization-ready
   
4. **Patents filed under different terminology**
   - Similar innovation with different keyword terminology
   - Requires citation analysis to discover

---

## Search Results Documentation Template

### For Each Search Domain:

**Search Term:** [electret + plasma integration]  
**Database:** Google Patents / USPTO / WIPO  
**Date Range:** 2015-2026  
**Results Found:** [number]

**Top 5 Patents:**
1. Patent Title | Assignee | Filing Date | Status
2. Patent Title | Assignee | Filing Date | Status
3. Patent Title | Assignee | Filing Date | Status
4. Patent Title | Assignee | Filing Date | Status
5. Patent Title | Assignee | Filing Date | Status

**Relevance Assessment:**
- Strong match (directly relevant): [X]
- Moderate match (partial relevance): [X]
- Weak match (tangentially related): [X]
- No match (unrelated): [X]

**Citations Found:**
- [Patent A] cites [Patent B] | Relevance: [link type]
- [Patent C] cites [Patent D] | Relevance: [link type]

**Assignee Analysis:**
- University institutions: [X]
- Government agencies: [X]
- Private corporations: [X]
- Individuals: [X]

**Novelty Conclusion:** [Integration appears novel / Prior art exists / Requires further analysis]

---

## Institutional Assignment Cross-Reference

### AFRL-Connected Patents
**Search for:**
- "Air Force Research Lab" as assignee
- Patent portfolios by AFRL researchers (2010-2026)
- AFRL licensing agreements

**Key Patent Assignees to Track:**
- AFRL (direct government patents)
- Contractors: Lockheed Martin, GD-LS, Boeing, Raytheon
- Partners: MIT, UCSD, Stanford, Caltech

### LLNL-Connected Patents
**Search for:**
- "Lawrence Livermore" as assignee
- Z-pinch related patents (LLNL focus area)
- Fusion research patents (2015-2026)

### Academic Institution Patents
**Search for:**
- MIT Lincoln Lab patents
- UCSD/Scripps patents
- AFIT thesis publications (not patents, but prior art)

---

## Next Steps

1. **Start with Google Patents** (easiest interface)
2. **Execute all 6 searches** (30 minutes total)
3. **Document top 5-10 results** per search domain
4. **Analyze assignees** — Cross-reference with research network
5. **Check patent families** — International filings (WIPO/EPO)
6. **Identify gaps** — Absence of patents in novel integration areas

**Expected Outcome:** 10-30 highly relevant patents, 100-500 tangentially related, clear map of existing patent landscape in these technical domains.

