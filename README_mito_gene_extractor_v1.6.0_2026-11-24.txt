README_mito_gene_extractor_v1.6.0_2026-11-24.txt
================================================
Manual for mito_gene_extractor_v1.6.0_2026-11-24.py

mito_gene_extractor, version 1.6.0 (2026-11-24)

Program file: mito_gene_extractor_v1.6.0_2026-11-24.py. Part of FASTA
Utilities (release 1.0.0), https://github.com/brpatric/fasta-utilities

Author: L. Brian Patrick, Department of Biological Sciences, Dakota Wesleyan
University, Mitchell, SD, USA. ORCID 0000-0003-1969-9600

What it does

Writes one FASTA file per annotated gene. Each file holds a header and the
gene sequence on one line:

    >Alopecosa_albostriata_PV694306 COX1        ->  Alopecosa_albostriata_PV694306_COX1.fasta

Minus-strand genes are reverse-complemented. A gene that crosses the origin of
the circular genome is joined across it, whether it is written with its start
larger than its end or with its end past the last base. The gene files are
draft gene regions, meant to be aligned to decide the final gene boundaries.

Annotation formats. The script recognises either format on each line:

  Format                      Columns                                        Example
  --------------------------- ---------------------------------------------- -----------------------------------------------
  MITOS2 BED, as downloaded   sequence ID, start, end, name, score, strand   PV694306.1  1137  2679  cox1  2418098491.5  +
  Simplified table            gene, start, end, strand                       COX1  1137  2679  +

Coordinates. Both formats use the BED convention: the start is counted from 0
and the end is exclusive, so a gene occupying bases 1–65 is written 0  65. In
an edited table, keep the start values exactly as MITOS2 wrote them. Changing
a start of 0 to 1 drops the first base of that gene.

Gene names. MITOS2 names are converted to standard symbols: cox1 → COX1, nad4l
→ ND4L, cob → CytB, rrnL → 16S, rrnS → 12S, and trnL1(tag) → trnL1. Names that
are already standard are left alone. MITOS2 sometimes splits a gene into parts
(nad5_0, nad5_1, rrnS_0-b). Each part is saved as its own file (ND5_0, ND5_1,
12S_0-b) and listed at the end of the run, so you can check them and merge or
rename them in an edited table.

  Setting              Command line        Default     Meaning
  -------------------- ------------------- ----------- ---------------------------------------------------------------
  FASTA_FILE           first argument      ask         mitogenome FASTA (the first sequence is used)
  ANNOTATION_FILE      second argument     ask         MITOS2 .bed or gene/start/end/strand table
  OUTPUT_DIR           -o                  mitogenes   folder for the gene files (made if needed)
  BASE_NAME            -b                  none        text put before each gene name, e.g. Pardosa_altamontis_Mt242
  BASE_FROM_FASTA      --base-from-fasta   False       use the first word of the FASTA header as the base name
  STANDARD_NAMES       --keep-names        True        convert MITOS2 names to standard symbols
  KEEP_FINAL_NEWLINE   --keep-newline      False       end each file with a line ending

Files from an earlier run are replaced. A gene name that appears twice in one
annotation is saved as …_2.fasta. Lines that cannot be read and coordinates
that do not fit the genome are reported and skipped.

Requirements

  Item                                           Version or format                                                                                     Install or notes
  ---------------------------------------------- ----------------------------------------------------------------------------------------------------- ------------------------------------------------------------------
  Python                                         3.8 or later (written and tested for IDLE 3.13; tested with 3.13.18)                                  python.org. No other packages are needed
  FASTA files                                    Plain text, nucleotide or protein, any line length, Windows (CRLF) or Unix (LF) line endings          
  MITOS2 annotation (mito_gene_extractor only)   The BED file from MITOS2 (e.g. run on Galaxy), or a tab-delimited table of gene, start, end, strand   Coordinates in the BED convention (0-based start, exclusive end)

The scripts run anywhere Python runs (Windows, macOS, Linux).

Running it

All five scripts can be run the same five ways.

A. In IDLE, with the SETTINGS block. Open the script in IDLE, edit the
SETTINGS block near the top, save, and press F5. For example, in
trim_fasta_trailing_whitespace:

    FOLDER             = r"C:\Users\me\data\genes"   # keep the r before the quote on Windows
    KEEP_FINAL_NEWLINE = False
    RECURSIVE          = False
    DRY_RUN            = False

B. In IDLE, answering questions. Leave the first file or folder setting as
None and press F5: the script asks for what it needs in the shell. You can
paste a path copied from Windows Explorer (Shift + right-click → Copy as
path); quotes around it are removed. split_major_fastas asks only if
ASK_FOR_FOLDERS = True; otherwise it uses the folder it is saved in, as in its
first version.

C. From the IDLE shell prompt. After one F5 run, run() stays available at
the >>> prompt:

    >>> run(r"C:\data\genes", dry_run=True)

D. From the command line (Windows PowerShell, macOS Terminal, Linux). Use
py -3.13 in place of python3 on Windows. With no arguments, a script uses its
SETTINGS block, as in IDLE. -h lists the options and --version prints the
version. The commands for each script are in the worked examples.

E. From your own Python code. The file names contain dots, so load a script
with runpy:

    import runpy
    trim = runpy.run_path("trim_fasta_trailing_whitespace_v1.1.0_2026-11-24.py")
    trim["run"]("by_specimen", recursive=True)

Try a dry run first. Concatenate_fasta_files, ConvertTextToFasta,
split_major_fastas and trim_fasta_trailing_whitespace have a dry-run setting
(DRY_RUN = True or --dry-run) that prints what would happen and changes
nothing. ConvertTextToFasta and trim_fasta_trailing_whitespace change files in
place, so work on a copy of anything you cannot replace.

Worked example: mito_gene_extractor: Alopecosa albostriata

example/extract/input/ holds the mitogenome of the wolf spider Alopecosa
albostriata, GenBank PV694306.1 (14,397 bp; the GenBank record is marked
UNVERIFIED). It also holds two annotations. The annotation is an uncurated
MITOS2 draft, used here only to show the program: it is not a final annotation
of this genome.

  File                         Content
  ---------------------------- -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  PV694306.fasta               the mitogenome
  PV694306_MITOS2.bed          the MITOS2 BED file as downloaded from Galaxy (38 features)
  PV694306_MITOS2_edited.txt   the same annotation edited by hand into a gene/start/end/strand table: names cleaned up, the three rrnS parts merged into 12S, and MITOS2's nad5_1 relabelled as trnY (36 features)

In the author's working copy of the edited table, trnM began at 1. It is 0
here, as in the BED file (see Coordinates above).

    cd example/extract
    python3 ../../mito_gene_extractor_v1.6.0_2026-11-24.py input/PV694306.fasta input/PV694306_MITOS2.bed -o output/from_MITOS2_bed -b Alopecosa_albostriata_PV694306
    python3 ../../mito_gene_extractor_v1.6.0_2026-11-24.py input/PV694306.fasta input/PV694306_MITOS2_edited.txt -o output/from_edited_table -b Alopecosa_albostriata_PV694306

From the BED file, 38 gene files (output/from_MITOS2_bed/; log), with the
MITOS2 names converted and the split genes listed:

      trnM (trnM(cat))             65 bp  +  0-65  -> Alopecosa_albostriata_PV694306_trnM.fasta
      ND2 (nad2)                  966 bp  +  46-1012  -> Alopecosa_albostriata_PV694306_ND2.fasta
      ND5_1 (nad5_1)               78 bp  +  977-1055  -> Alopecosa_albostriata_PV694306_ND5_1.fasta
      ...
      Notices (1):
        - MITOS2 split these genes into parts, each saved as its own file: ND5_1, ND5_0, 12S_0-b, 12S_0-a, 12S_1. ...

From the edited table, 36 gene files: 13 protein-coding, 21 tRNA and 2 rRNA
(output/from_edited_table/; log).

Checks. On the edited table, version 1.6.0 writes files byte-for-byte
identical to those of version 1.5. COX1, CytB and ND4 translate under the
invertebrate mitochondrial code with no internal stop codons. To test genes
that cross the origin, the genome was rotated so that genes on both strands
crossed it. All 144 extractions, made with both ways of writing such a gene,
matched the unrotated genes.

Citing

If you use these scripts, please cite the release as given in CITATION.cff (or
with the Cite this repository button on this page):

  Patrick, L. B. (2026). FASTA Utilities: scripts for extracting, combining,
  renaming, splitting and trimming mitogenome FASTA files (Version 1.0.0)
  [Computer software]. https://github.com/brpatric/fasta-utilities

If you use MITOS2 annotations, please cite MITOS2 (Donath et al., 2019). If
you use the worked examples, please also cite the sources of their data
(Patrick & Santos, 2025; GenBank PV694306).

References

Donath, A., Jühling, F., Al-Arab, M., Bernhart, S. H., Reinhardt, F., Stadler,
P. F., Middendorf, M., & Bernt, M. (2019). Improved annotation of
protein-coding genes boundaries in metazoan mitochondrial genomes. Nucleic
Acids Research, 47(20), 10543–10552. https://doi.org/10.1093/nar/gkz833
(MITOS2)

Patrick, L. B., & Santos, S. R. (2025). The complete mitochondrial genome of
Erigone atra Blackwall, 1833 (Araneae, Linyphiidae). Mitochondrial DNA Part B,
10(12), 1243–1248. https://doi.org/10.1080/23802359.2025.2594297 (source of
worked example 3)

Pearson, W. R., & Lipman, D. J. (1988). Improved tools for biological sequence
comparison. Proceedings of the National Academy of Sciences of the United
States of America, 85(8), 2444–2448. https://doi.org/10.1073/pnas.85.8.2444
(origin of the FASTA format)

Python Software Foundation. (2024). Python (Version 3.13) [Computer software].
https://www.python.org/

Provenance and version history

Version 1.6.0 was drafted with the assistance of Claude Opus 5.5 (Anthropic)
on 2026-11-24, from specifications by the author, and reviewed by the author,
and tested with Python 3.13.18 on the worked examples. The script's header
holds the same provenance.

| Script | Version | What it does | |---|---|---|---| | mito_gene_extractor |
1.0–1.5 | 2026 (1.5: 2026-06-23) | 1.0 first version; 1.1 space before the
gene name in the header; 1.2 header reduced to >Species_ID Gene_Name; 1.3
start decremented by 1 (later found wrong); 1.4 no line ending after the
sequence; 1.5 BED starts used as they are, reverting 1.3. | |
mito_gene_extractor | 1.6.0 | 2026-11-24 | Reads the MITOS2 BED file directly
as well as the simplified table. MITOS2 names converted to standard symbols,
with split gene parts kept and reported. Genes crossing the origin joined
across it. Files from an earlier run replaced (1.5 added _2, _3 … to new
names). Option for a final line ending; base name from the FASTA ID; warning
for multi-sequence FASTA; summary by gene type. SETTINGS block, questions in
the shell, command-line options, run(). |

License

Released under the MIT License; see LICENSE.
