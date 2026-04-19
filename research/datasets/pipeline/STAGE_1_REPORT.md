# STAGE 1 REPORT: Primary Entity Extraction
**Generated:** April 19, 2026  
**Agent:** Research Correlation Discovery  
**Threshold:** Primary entities (2+ mentions across documents)

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| **Files Scanned** | 57 |
| **Total Entities Extracted** | 53 |
| **Primary Entities (2+ mentions)** | 47 |
| **Highest-Mention Entity** | @tmbspaceships (146 mentions) |

## Entity Distribution by Type

| Entity Type | Count | Examples |
|-------------|-------|----------|
| **People** | 11 | Neil McCasland, Ashton Forbes, Tom DeLonge, John Podesta, Susan Wilkerson |
| **Organizations** | 14 | AFRL, Riverside Research, Kirtland AFB, MIT, Lockheed Skunk Works |
| **Technical Topics** | 11 | Plasma physics, MHD, Z-pinch, Electret, Slow wave |
| **Dates/Events** | 5 | February 27 2026, January 2016, November 2024 |
| **Accounts/Handles** | 6 | @TMBSpaceships (multiple variants) |

---

## Top 20 Primary Entities (Ranked by Mention Count)

| Rank | Entity | Type | Mentions | Key Indicator |
|------|--------|------|----------|---------------|
| 1 | @tmbspaceships / @TMBSpaceships | Account | 146-88 | Core subject of analysis |
| 2 | Riverside Research | Organization | 73 | McCasland's board affiliation |
| 3 | Wright-Patterson AFB | Organization | 61 | AFRL command location |
| 4 | Ashton Forbes | Person | 64 | Public amplifier of McCasland connection |
| 5 | AFRL | Organization | 46 | McCasland's former command |
| 6 | Plasma Physics | Technical Topic | 40 | Core technical theme |
| 7 | Neil McCasland | Person | 40 | Central subject |
| 8 | neilmcc79 | Account | 49 | McCasland's email handle |
| 9 | Kirtland AFB | Organization | 36 | Albuquerque location |
| 10 | Kirtland Partnership Committee | Organization | 33 | McCasland board role |

---

## Network Positions (Initial Mapping)

### People-to-Organization Connections (Primary Entities)

**William Neil McCasland:**
- Riverside Research (Board)
- Applied Technology Associates (Director of Technology)
- DBE Consulting LLC (Founder/Owner)
- Kirtland Partnership Committee (Board)
- AFRL (Former Commander)
- Air Force Academy (Commissioning)
- MIT (Degrees)

**Tom DeLonge:**
- Podesta meeting network (WikiLeaks 2016)
- Lockheed Skunk Works connection (Rob Weiss)

**Ashton Forbes:**
- @TMBSpaceships amplification (post-disappearance)
- Public podcast/livestream commentary

**John Podesta:**
- Email network (WikiLeaks)
- DeLonge meeting coordination (2016)

### Technology-to-Account Connection

**@TMBSpaceships account content themes:**
- Plasma physics
- MHD (magnetohydrodynamics)
- Electret materials
- Slow wave propagation
- Z-pinch plasma
- Thermal plasma systems
- Advanced propulsion concepts

---

## Co-Reference Patterns (High-Signal Pairings)

**Most Densely Connected Pairs:**

1. **@TMBSpaceships ↔ McCasland**
   - 146+ account mentions across research documents
   - 40 mentions of McCasland as central figure
   - 81+ @tmbspaceships handle variations documented

2. **Ashton Forbes ↔ @TMBSpaceships**
   - 64 Forbes mentions primarily in correlation-to-account analysis
   - Forbes publicly connects McCasland to @TMBSpaceships

3. **McCasland ↔ AFRL**
   - 46 AFRL mentions
   - Documented former command relationship
   - Public career record

4. **McCasland ↔ Riverside Research**
   - 73 Riverside Research mentions
   - Board affiliation post-AFRL
   - Technology director role at ATA

5. **DeLonge ↔ Podesta**
   - 30 Podesta mentions
   - 20 DeLonge mentions
   - 2016 email network documented in WikiLeaks corpus

---

## Key Dates (Primary Temporal Entities)

| Date | Significance | Mention Count |
|------|--------------|--------------|
| **February 27, 2026** | McCasland disappearance | 12 |
| **November 2024** | Schematic sent to Ashton Forbes | Multiple |
| **January 2016** | Podesta/DeLonge meeting, McCasland participation | Multiple |
| **February 13-27, 2026** | Final @TMBSpaceships post window | Multiple |

---

## Source Document Concentration

**Documents with highest primary entity density:**

1. **research/findings.md** — 31 primary entities
2. **notes/claim-matrix.md** — 28 primary entities
3. **research/trail-analysis.md** — 25 primary entities
4. **sources/context/ashton-forbes-podcast-transcript.md** — 18 primary entities
5. **sources/primary/wikileaks-emailid-*.html** — 12+ entities each

---

## Gaps & Low-Signal Entities

**Entities appearing only once (excluded from primary dataset):**
- Robert Weiss (Rob Weiss from Lockheed mentioned once)
- James Tegnelia (once)
- Susan McCasland Wilkerson variants (consolidated into primary)
- Location names (Albuquerque, Quail Run Court, Pagosa Springs)
- Technical terms appearing in single documents

---

## STAGE 1 DELIVERABLES

✓ **stage1_primary_entities.json** — Machine-parseable dataset with full metadata  
✓ **STAGE_1_REPORT.md** — This human-readable summary  

**Total Primary Entities Ready for Stage 2:** 47 entities across 5 categories

---

## Ready for Stage 2: Correlation Analysis

Next phase will:
- Compute co-occurrence metrics across primary entities
- Build correlation confidence scores (0.0–1.0)
- Surface timeline-based and document-based patterns
- Identify high-confidence correlations (0.65+)
- Filter to novel and significant findings

**Stage 1 Status:** COMPLETE ✓
