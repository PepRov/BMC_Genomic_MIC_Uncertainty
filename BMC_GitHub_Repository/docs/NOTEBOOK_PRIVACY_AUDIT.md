# Public notebook privacy audit — 14 November 2026

**Archive:** BMC GitHub repository v1.1 (privacy-reviewed edition).

## Scope and method

We inspected the actual contents of the 14 Jupyter notebook (`.ipynb`) files included in the archive: all source cells, notebook metadata, execution counts, saved outputs and attachments. Source text was screened for personal machine/home paths, email addresses, publicly recognised secret/API-key formats, passwords and credentials, private-key blocks, IP addresses, personal names and identifiers. Files containing embedded data were inspected after decoding. We also scanned repository documentation and the schema of the packaged data files.

## Findings

- **14/14 notebooks:** no stored execution outputs or cell attachments, and no exposed passwords, API keys, access tokens, private keys, email addresses, personal computer account paths or private IP addresses were found.
- Notebooks 39–55 and Figure02 use generic `BMC_PROJECT_ROOT` and/or Google Colab example paths. These are **not** individual users' home directories. Notebook 53 links to the publicly available EUCAST breakpoint source.
- **Figure04 v0.4 previously embedded the entire NB55 dataset, including NCBI BioSample accession identifiers and record-level MIC/prediction data.** It has been replaced in this archive with **Figure04 v0.5**, which embeds only **60 aggregated plotting rows** and contains no BioSample identifiers or record-level observations.
- Figure04 v0.5 was independently executed from an empty working directory. Its generated Figure 4 PNG is **pixel-identical** to the output of the original v0.4 figure notebook, and its 95% Wilson intervals agree with the source summary.

## Scope limits

The **separate CSV/CSV.GZ scientific datasets** intentionally retain NCBI-style BioSample accessions and MIC observations for traceability. Those accession identifiers are **scientific sample references**, not directly identifying human contact details; nonetheless, this screening does **not** establish provenance, original consent terms, licensing or legal rights to redistribute each dataset. Confirm the original sources and redistribution conditions before public release.

Automated and manual content checks substantially reduce exposure risk, but cannot guarantee that arbitrary private information never appears in undocumented source records.

No frozen source analysis notebooks (NB39–55 or Figure02) were modified during this privacy revision. Only the standalone Figure04 notebook and the packaging documentation were updated.
