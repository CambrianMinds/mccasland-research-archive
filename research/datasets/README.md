# Research Datasets

This directory is the generated analysis package for the McCasland archive. It has been reorganized so analysis output, derived data, and follow-up guides stop accumulating flat in one folder.

## Layout

- [`data/`](data): machine-readable outputs from the correlation pipeline
- [`pipeline/`](pipeline): staged reports and verification summaries
- [`extended/`](extended): deeper thematic analyses built on top of the pipeline
- [`guides/`](guides): follow-up execution guides for FOIA and patent work

## Start here

If you want the shortest path through the package:

1. Read [`extended/EXTENDED_ANALYSIS_MASTER_INDEX.md`](extended/EXTENDED_ANALYSIS_MASTER_INDEX.md).
2. Read [`pipeline/FINAL_VERIFICATION_SUMMARY.md`](pipeline/FINAL_VERIFICATION_SUMMARY.md).
3. Use [`guides/FOIA_PATENT_EXECUTION_GUIDE.md`](guides/FOIA_PATENT_EXECUTION_GUIDE.md) only if you are moving into follow-up investigation work.

## Package contents

### Data

- [`data/stage1_primary_entities.json`](data/stage1_primary_entities.json)
- [`data/stage2_correlations.json`](data/stage2_correlations.json)
- [`data/stage3_novelty_status.json`](data/stage3_novelty_status.json)

### Pipeline

- [`pipeline/STAGE_1_REPORT.md`](pipeline/STAGE_1_REPORT.md)
- [`pipeline/STAGE_2_REPORT.md`](pipeline/STAGE_2_REPORT.md)
- [`pipeline/STAGE_3_REPORT.md`](pipeline/STAGE_3_REPORT.md)
- [`pipeline/STAGE_3_WEB_VERIFICATION.md`](pipeline/STAGE_3_WEB_VERIFICATION.md)
- [`pipeline/PIPELINE_SUMMARY.md`](pipeline/PIPELINE_SUMMARY.md)
- [`pipeline/FINAL_VERIFICATION_SUMMARY.md`](pipeline/FINAL_VERIFICATION_SUMMARY.md)

### Extended

- [`extended/TIMELINE_FORENSICS.md`](extended/TIMELINE_FORENSICS.md)
- [`extended/CITATION_NETWORK_MAPPING.md`](extended/CITATION_NETWORK_MAPPING.md)
- [`extended/INSTITUTIONAL_GRAPH_ANALYSIS.md`](extended/INSTITUTIONAL_GRAPH_ANALYSIS.md)
- [`extended/SOURCE_EXPANSION_EXTENDED.md`](extended/SOURCE_EXPANSION_EXTENDED.md)
- [`extended/EXTENDED_ANALYSIS_MASTER_INDEX.md`](extended/EXTENDED_ANALYSIS_MASTER_INDEX.md)

### Guides

- [`guides/FOIA_REQUEST_GUIDE.md`](guides/FOIA_REQUEST_GUIDE.md)
- [`guides/PATENT_SEARCH_GUIDE.md`](guides/PATENT_SEARCH_GUIDE.md)
- [`guides/FOIA_PATENT_EXECUTION_GUIDE.md`](guides/FOIA_PATENT_EXECUTION_GUIDE.md)

## Notes

- These files are generated analysis and follow-up planning outputs, not the canonical research narrative.
- The canonical narrative still lives in [`../findings.md`](../findings.md), [`../trail-analysis.md`](../trail-analysis.md), and [`../../notes/claim-matrix.md`](../../notes/claim-matrix.md).
- The JSON files are useful, but they still need schema cleanup if you want to build automation on top of them.
- Some generated outputs still contain original source-path references from before this repo cleanup pass.
