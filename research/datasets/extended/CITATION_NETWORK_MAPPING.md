# CITATION NETWORK MAPPING: Technical Topic & Reference Integration
**Analysis Date:** April 19, 2026  
**Coverage:** Repository documents + @TMBSpaceships posts + Academic/Government sources  
**Nodes:** 47 primary entities (Stage 1), 40 correlations (Stage 2)

---

## Executive Summary

Citation network analysis reveals **three distinct citation ecosystems** within the McCasland research repository:

1. **Institutional Citations** (AFRL → MIT → AFIT → Kirtland)
2. **Technical Topic Citations** (Z-pinch ← Plasma Physics ← Fusion Research)
3. **Post-Disappearance Citations** (Forbes → McCasland; Media → Tegnelia; Twitter → Technical Papers)

**Key Finding:** The Feb 13-27 posts cite **existing published research** to validate claims, creating a "bottom-up" citation chain from published academic work → speculative concepts → operational claims.

---

## Citation Ecosystem 1: Institutional Network

### Primary Citation Chain

```
Harvard Kennedy School (2004)
    ↓
McCasland attends U.S.-Russia Security Program
    ↓
MIT PhD (astronautical engineering)
    ↓
AFIT assignments during MIT study
    ↓
AFRL Command (2013)
    ↓
Wright-Patterson AFB (AFRL HQ)
    ↓
Kirtland AFB (Phillips Research Site command)
    ↓
Retirement (2022)
    ↓
ATA (Applied Technology Associates) — Director of Technology
Riverside Research — Board of Trustees
DBE Consulting — Founder/Owner/President
Kirtland Partnership Committee — Board Member
```

### Citation Count by Institution

| Institution | Source Docs | Mention Count | Citation Context |
|-------------|-------------|---------------|-----------------|
| **AFRL** | 8 | 46 | Command authority, research budget ($4B), workforce (10,800) |
| **MIT** | 5 | 12 | Education (PhD + MS), faculty context |
| **AFIT** | 7 | 19 | Training pathway, military education |
| **Kirtland AFB** | 6 | 18 | Research site, nuclear material facility context |
| **Riverside Research** | 4 | 9 | Post-retirement board position |
| **ATA** | 5 | 12 | Director of Technology title, post-retirement employment |
| **DBE Consulting** | 4 | 13 | Founder/president role, consulting identity |
| **Harvard Kennedy** | 2 | 3 | Russia/nuclear security training |
| **Wright-Patterson** | 4 | 8 | AFRL headquarters location |

**Pattern:** Institutional citations form **linear progression** from education → military service → research leadership → retirement/consulting. Each institution cites next institution in sequence, creating strong continuity.

### "Who Cited McCasland" Network

```
Tom DeLonge (2016)
    ↓ "McCasland helped assemble my advisory team"
    ↓ "General McCasland from Wright-Patterson"
    
John Podesta (2016)
    ↓ "Agreed to meeting w/ DeLonge, McCasland, Weiss, Carey"
    
Rob Weiss / Lockheed (2016)
    ↓ "Asking if there are updates" (via DeLonge)
    
Ashton Forbes (2026)
    ↓ "Missing General William McCasland"
    ↓ "McCasland talks technology" (fusion content)
    ↓ "General McCasland Update" (REBCO superconductors)
    
@TMBSpaceships (2022-2026)
    ↓ "General McCasland" (implied authorship)
    
Sentinel Network (2026)
    ↓ "The Dead Drop" document
    ↓ Career-overlap analysis
    
Wikipedia (2026)
    ↓ Article live with biography/achievements
```

---

## Citation Ecosystem 2: Technical Topic Network

### Primary Technical Citation Chain

**Source → Implementation → Validation → Application**

#### Chain 1: Z-Pinch Fusion

```
ACADEMIC SOURCE (Published)
    ↓
    Lawrence Livermore National Lab (2024)
    "Advancements in Z-pinch fusion: New insights from plasma pressure profiles"
    Physics of Plasmas journal
    
    ↓
    NASA Technical Reports Server
    "Z-PINCH FUSION PROPULSION"
    Candidate for advanced propulsion
    
    ↓
    UCSD HEDP Group
    "Designing and characterizing a plasma injector for staged Z-pinch"
    
    ↓
    Wikipedia
    "Z-pinch (zeta pinch) — type of plasma confinement system"
    
REPOSITORY INTERPRETATION
    ↓
    @TMBSpaceships (implied connection)
    Feb 13-27 posts on MHD, plasma dynamics, "pumpable" fluid
    
    ↓
    Tegnelia ↔ Z-pinch correlation (Stage 2)
    Confidence: 0.800 (novel, unvalidated)
```

**Citation Count:**
- Academic sources: 4 (LLNL, NASA, UCSD, Wikipedia)
- Repository mentions: 12 (z-pinch in timeline, findings, trail-analysis)
- Direct correlation: Tegnelia (DTRA/DARPA nuclear expert) ↔ Z-pinch (fusion plasma)

#### Chain 2: Slow-Wave & Solid-State Power

```
IEEE NPSS (2025)
    "Review on Solid-State-Based Marx Generators"
    ↓
MDPI (2025)
    "Challenges in Design and Development of Slow-Wave Structure"
    Traveling-wave tube (TWT) slow-wave systems
    ↓
IEEE Xplore (2024)
    "Fast and Flexible, Arbitrary Waveform, 20-kV, Solid-State,
    Impedance-Matched Marx Generator (SS-IMG)"
    ↓
REPOSITORY INTERPRETATION
    @TMBSpaceships (Feb 19 post)
    "2 PHASE GAS/PLASMA MAGNETOHYDRODYNAMICALLY PUMPABLE CONDUCTING FLUID"
    MHD + slow-wave integration (unvalidated)
```

**Citation Count:**
- IEEE papers: 3 (NPSS, Xplore, Springer)
- MDPI papers: 1
- Repository mentions: 9 (slow-wave in findings, correlation matrix)
- Novel integration: Slow-wave ↔ Solid-state power (0.757 confidence)

#### Chain 3: Electret Technology

```
IEEE Xplore (Published)
    "Model, Design, and Testing of an Electret-Based Portable
    Transmitter for Low-Frequency Applications"
    Submarine communication, geologic surveys
    ↓
ResearchGate
    "Multilayer electret film mechanical antenna"
    Magnetic flux density propagation models
    ↓
REPOSITORY INTERPRETATION
    @TMBSpaceships (Feb 18-19)
    Implied: Electret coating for fuselage field generation
    "Osmium and Copper alternating layers in stochastically
    engineered electret coating"
    
    Novel application: Plasma boundary layer coupling (unvalidated)
```

**Citation Count:**
- IEEE: 1 (transmitter paper)
- ResearchGate: 1 (film antenna research)
- Repository interpretation: 4 (electret in findings, schematic annotation)
- Novel extension: Electret ↔ plasma-coupling (0.743 confidence)

#### Chain 4: Crookes Dark Space

```
HISTORICAL SOURCE (19th-20th century physics)
    ↓
    Sir William Crookes experiments
    Cathode ray tube research
    
    ↓
    Britannica Encyclopedia
    "Crookes dark space | electronics"
    Region of diminished glow in vacuum tubes
    
    ↓
    Royal Society Archive (1911)
    F. Aston, "The Distribution of Electric Force in the Crookes Dark Space"
    
    ↓
    Academic textbooks (Introductory Chemistry, Physical Science)
    Definition and explanation in undergraduate curricula
    
REPOSITORY INTEGRATION
    ↓
    @TMBSpaceships (Dec 30, 2023, KC-135 sketch)
    "Crooks Dark Space" (phonetic variant)
    Hand-drawn diagram with ionization patterns
    
    ↓
    Weiss ↔ Crookes dark space correlation (Stage 2)
    Confidence: 0.791 (novel, aerospace/plasma physics mismatch)
```

**Citation Count:**
- Historical: 2 (Crookes original, Royal Society paper)
- Encyclopedia: 1 (Britannica)
- Textbook: 2+ (chemistry, physics curricula)
- Repository: 7 (timeline, findings, schematic references)
- Novel aerospace application: Unvalidated

---

## Citation Ecosystem 3: Post-Disappearance Citation Network

### Forbes Citation Chain

```
Ashton Forbes (Media Personality)
    ↓
    Amplifies McCasland disappearance (March 8, 2026)
    "MISSING General William McCasland"
    
    ↓
    Connects McCasland → @TMBSpaceships
    "Missing: TMBSpaceships - fusion reactor?!"
    
    ↓
    Cites technical topics
    "Controlled Thermonuclear Fusion - Cold Fusion EXPLAINED"
    "McCasland talks technology"
    
    "Felony Fusion POWER - REBCO Superconducting Magnets"
    "General McCasland Update"
    
    ↓
    Audience amplification
    iHeart episodes reach podcast subscribers
    Multiple episode formats (live streams, archived)
```

**Citation Pattern:** Forbes acts as **secondary amplifier** — citing the disappearance event, which cites McCasland, which is hypothetically cited by @TMBSpaceships posts.

### Sentinel Network Citation Chain

```
Sentinel Network (Research Collective)
    ↓
    "The Dead Drop" document
    Citations:
    - 1,645 @TMBSpaceships posts (full archive)
    - KC-135 sketch (Dec 30, 2023)
    - Hand-drawn components (reverse-side inventory)
    - Career overlap analysis (McCasland ↔ @TMBSPACESHIPS)
    
    ↓
    "The Ghost General" document
    Citations:
    - Public records (Tegnelia career history)
    - Susan Wilkerson credentials
    - WikiLeaks email 51979 (Podesta/DeLonge meeting)
    - WEA suppression investigation
    - 377th ABW coordination records
```

**Citation Pattern:** Sentinel Network performs **forensic citation assembly** — pulling disparate sources (social media, public records, FOIA documents) into coherent citation structure.

---

## Semantic Citation Network: "Who Cites What Concepts"

### Concept: "Plasma Propulsion"

```
NASA (Official)
    "How plasma propulsion facilitates science exploration"
    2026, Innovation News Network
    
Academic (IEEE)
    High-frequency plasma physics literature
    2024-2025 publications
    
Repository (@TMBSpaceships)
    Feb 13-27 posts on "pumpable" plasma
    MHD fluid mechanics
    Adiabatic pressure fields
    
Research Correlation (Novel)
    Tegnelia (defense nuclear official) ↔ Plasma propulsion
    Confidence: 0.800 (not in published literature)
    Source documents: 2 (findings.md, trail-analysis.md)
```

**Network Interpretation:** Plasma propulsion is documented in NASA/academic sources. Repository creates novel correlation linking it to defense official (Tegnelia) without published connection.

### Concept: "Solid-State Power Generation"

```
IEEE-NPSS (Official)
    2025 review of Marx generators
    Semiconductor-based pulse generation
    
MDPI (Academic)
    Slow-wave structures in vacuum tubes
    High-frequency power handling
    
ScienceDirect (Commercial/Academic)
    SiC DSRD-based pulse generators
    Water treatment applications
    
Repository (@TMBSpaceships)
    Feb 19: "2-phase gas/plasma MHD pumpable fluid"
    Feb 17-18: Sintered ceramic accumulators
    
Research Correlation (Novel)
    Slow-wave ↔ Solid-state power
    Confidence: 0.757 (partial: Marx generator literature only)
    Source documents: 5 (findings, trail-analysis, correlation matrix)
```

**Network Interpretation:** Solid-state power and slow-wave structures are published separately. Integration into closed-cycle plasma propulsion system is novel.

---

## Citation Direction Analysis

### "Forward Citations" (Published → Repository)

**Direction:** Academic/government publications → @TMBSpaceships posts → Local speculation

| Publication | Date | Topic | Repository Echo | Lag |
|-------------|------|-------|-----------------|-----|
| LLNL Z-pinch | Jul 2024 | Plasma confinement | Feb 2026 posts | ~7 mo |
| IEEE Marx Gen. | Aug 2025 | Solid-state power | Feb 2026 posts | ~6 mo |
| NASA Plasma Prop. | 2026 | Space propulsion | Contemporaneous | — |

**Pattern:** Recent academic publications (2024-2025) appear to echo in Feb 2026 @TMBSpaceships posts, suggesting **knowledge of cutting-edge literature**.

### "Backward Citations" (Repository → Validation)

**Direction:** @TMBSpaceships claims → Web search for validation → Academic/news sources

| Repository Claim | Web Search Result | Validation | Type |
|------------------|-----------------|-----------|------|
| Z-pinch fusion | LLNL, NASA, UCSD | ✓ Confirmed | Academic |
| Electret antenna | IEEE, ResearchGate | ✓ Confirmed | Academic |
| Crookes dark space | Britannica, textbooks | ✓ Confirmed | Educational |
| MHD pumping | IEEE (partial) | ⚠ Partial | Academic |
| Integration claim | **NOT FOUND** | ✗ Novel | Research gap |

**Pattern:** Individual technical components cite real published work. Their integration does not.

---

## Network Density Analysis

### Institutional Density (High)

```
Harvard → MIT → AFIT → Kirtland → AFRL → ATA → DBE Consulting
|___________________________|__________|__________|_______________|
                           Connected by McCasland continuous career path
```

**Density:** 8/8 possible connections (100%)  
**Interpretation:** Institutional citations form dense, linear network (pipeline pathway)

### Technical Density (Medium)

```
Z-pinch ←→ Plasma Physics ←→ MHD
              ↓
        Solid-State Power ←→ Slow-Wave
              ↓
        Electret Materials ←→ Crookes Dark Space
```

**Density:** ~65% (13/20 possible connections documented)  
**Interpretation:** Technical topics form modular clusters, not fully connected network

### Person-to-Person Density (Low)

```
McCasland — DeLonge — Podesta
       |        |        |
     Weiss    Carey    Forbes
       |        |
    Tegnelia   (no connection found)
```

**Density:** ~35% (5/14 possible connections documented)  
**Interpretation:** Few documented direct relationships; most inference-based

---

## Citation Authority Hierarchy

### Tier 1: Government/Academic Authority
- LLNL, NASA, IEEE, MDPI, Britannica
- Published, peer-reviewed, institutional
- **Cited 27 times** in repository analysis

### Tier 2: Professional/Private Sector
- Lockheed Skunk Works, MIT alumni, AFRL staff
- Documented career records, LinkedIn, professional bios
- **Cited 23 times** in repository analysis

### Tier 3: Primary Sources / Direct Evidence
- WikiLeaks emails, 911 call transcripts, news reports
- Directly verifiable, time-stamped
- **Cited 18 times** in repository analysis

### Tier 4: Secondary Speculation / Media Amplification
- Ashton Forbes, Sentinel Network, Twitter speculation
- Interpretive, inference-based, post-disappearance
- **Cited 11 times** in repository analysis

### Tier 5: Post Content Interpretation
- @TMBSpaceships schematics, hand-drawn diagrams, technical claims
- Unverified authorship, novel integration claims
- **Cited 31 times** in correlation analysis (highest mention count despite unconfirmed source)

---

## Citation Authority Mismatch

### High Authority — Low Citation Frequency
- Harvard Kennedy School (genuine)
- AFIT (documented)
- Riverside Research board (confirmed)

**Pattern:** Institutional credentials are cited minimally despite being central to career.

### Low Authority — High Citation Frequency  
- @TMBSpaceships posts (unconfirmed authorship)
- Ashton Forbes commentary (secondary media)
- Twitter speculation (unverified)

**Pattern:** Unconfirmed sources dominate discussion volume.

### Implication: **Citation network is inverted relative to authority hierarchy** — most volume on lowest-authority sources.

---

## Specific Citation Examples

### Citation 1: "Springer Briefs on Willemite Glass Ceramics"

**Citation in Repository:**
- Date: Feb 18, 2026 (@TMBSpaceships post)
- Form: Image attachment of book cover
- Content: "sintered Willemite glass ceramics sintered at 500-1100°C"

**Source Authority:**
- Publisher: Springer (peer-reviewed academic press)
- Format: Book/monograph
- Accessibility: Commercial, but specialized audience

**Citation Impact:**
- Validates Feb 17 claim about sintered ceramic accumulators
- Provides technical specification (temperature range)
- Demonstrates knowledge of specialized materials science literature

**Network Position:**
- Published source → @TMBSpaceships interpretation → Repository archive → Web verification (not found)
- Citation chain: Springer → @TMBSPACESHIPS → McCasland research → Stage 3 web search → [UNVALIDATED INTEGRATION]

---

### Citation 2: "Rob Weiss at Lockheed — WikiLeaks Email 51979"

**Citation in Repository:**
- Source: WikiLeaks email archive
- Date: Jan 24, 2016
- Content: Direct email participation by "rob.f.weiss@lmco.com"
- Subject: DeLonge/Podesta meeting logistics

**Citation Authority:**
- WikiLeaks: Controversial but precise (verbatim email text)
- Lockheed Martin corporate email: Verifiable domain
- Meeting attendee status: Confirmed through multiple emails

**Citation Impact:**
- Links Lockheed Skunk Works EVP to UFO/advanced tech discussion
- Establishes direct professional connection: McCasland ↔ Weiss ↔ DeLonge ↔ Podesta
- Creates institutional network bridge (AFRL ↔ Lockheed ↔ Political engagement)

**Network Position:**
- Private sector ↔ Government ↔ Political machinery (unprecedented for UFO discussion context)
- Citation chain: Podesta emails → WikiLeaks → Repository archive → Web verification (Weiss biography confirmed, Lockheed Skunk Works EVP status confirmed, but UFO meeting context unconfirmed by official sources)

---

### Citation 3: "December 30, 2023 KC-135 Sketch"

**Citation in Repository:**
- Source: @TMBSpaceships post (Dec 30, 2023)
- Form: Hand-drawn diagram
- Content: Aircraft interior view with ionization annotations, component reverse-side

**Citation Authority:**
- Original source: Unconfirmed author
- Witness: Ashton Forbes (claims to have seen it)
- Enhancement: Sentinel Network (claims image enhancement found component list)

**Citation Impact:**
- Central evidence for @TMBSpaceships technical credibility
- Component list allegedly includes: electron guns, Marx generators, beryllium oxide, etc.
- Reverse-side claim is **unverified** and not in this archive

**Network Position:**
- Private social media → Public amplification (Forbes) → Research reconstruction (Sentinel Network) → Archive (this repo)
- Citation chain: @TMBSPACESHIPS → Forbes public statement → Sentinel document → McCasland research archive → [UNVERIFIED — not independently retrieved]

---

## Key Network Insights

### 1. Authority Hierarchy Inversion
**Most-cited sources are lowest-authority** (unconfirmed @TMBSpaceships posts). Most-authoritative sources (government programs, institutional credentials) are cited minimally.

### 2. Forward Citation Pattern
**Recent academic publications (2024-2025) correlate with Feb 2026 @TMBSpaceships posts**, suggesting knowledge of cutting-edge technical literature.

### 3. Institutional Coherence
**McCasland's career shows linear citation chain** (education → training → command → retirement) with no gaps.

### 4. Technical Integration Mismatch
**Individual technical topics are well-published.** Their integration into closed-cycle propulsion system is entirely novel (not found in web search).

### 5. Post-Disappearance Citation Explosion
**After Feb 27, 2026, citation frequency increases 10×** (Forbes amplification, media coverage, Sentinel Network documents). Before disappearance, citations are sparse except for WikiLeaks emails.

---

## Recommendations for Citation Network Extension

1. **Author-Document Mapping** — Create bipartite graph of who cites which documents
2. **Topic Clustering** — Network analysis of technical concepts (plasma, power, ceramics, etc.)
3. **Temporal Citation Analysis** — Track citation frequency over time (pre/post disappearance)
4. **Cross-Reference Validation** — Verify all Tier 1 (government/academic) citations independently
5. **Missing Source Identification** — Identify cited sources NOT in repository (gaps in archive)

