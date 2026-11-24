README_trim_fasta_trailing_whitespace_v1.1.0_2026-11-24.txt
===========================================================
Manual for trim_fasta_trailing_whitespace_v1.1.0_2026-11-24.py

trim_fasta_trailing_whitespace, version 1.1.0 (2026-11-24)

Program file: trim_fasta_trailing_whitespace_v1.1.0_2026-11-24.py. Part of
FASTA Utilities (release 1.0.0), https://github.com/brpatric/fasta-utilities

Author: L. Brian Patrick, Department of Biological Sciences, Dakota Wesleyan
University, Mitchell, SD, USA. ORCID 0000-0003-1969-9600

What it does

Removes whitespace from the end of each FASTA file in a folder: blank lines,
spaces, tabs, carriage returns and line feeds. Nothing else in the file
changes, and files that already end cleanly are not rewritten. The file is
read and written as raw bytes, so its line endings and encoding stay as they
were. By default the last line is left with no line ending at all.
KEEP_FINAL_NEWLINE = True instead leaves exactly one, in the file's own style
(CRLF or LF).

  Setting              Command line     Default   Meaning
  -------------------- ---------------- --------- ------------------------------------------
  FOLDER               first argument   ask       folder holding the FASTA files
  KEEP_FINAL_NEWLINE   --keep-newline   False     end with exactly one line ending
  RECURSIVE            --recursive      False     also process FASTA files in sub-folders
  DRY_RUN              --dry-run        False     report what would change; change nothing

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

Worked example: ConvertTextToFasta → split_major_fastas → trim_fasta_trailing_whitespace: Erigone atra

This example uses the 13 protein-coding genes of the two Erigone atra
mitogenomes from Patrick and Santos (2025): a male, GenBank PP726906, and a
female, GenBank PP726907, taken from the CDS features of the two records.
example/convert_split_trim/input/ holds one "major" file per gene, holding
both specimens and saved with a .txt extension and Windows line endings, as
files saved from many Windows programs are. It also holds
Notes_on_specimens.txt, a plain-text note.

ConvertTextToFasta and trim_fasta_trailing_whitespace change files in place,
so copy input to a working folder named my_genes first:

    cd example/convert_split_trim
    cp -r input my_genes          # Windows: copy the folder in Explorer
    python3 ../../ConvertTextToFasta_v1.1.0_2026-11-24.py my_genes
    python3 ../../split_major_fastas_v1.1.0_2026-11-24.py my_genes --out by_specimen
    python3 ../../trim_fasta_trailing_whitespace_v1.1.0_2026-11-24.py by_specimen --recursive

Step 1. ConvertTextToFasta. The 13 gene files are renamed to .fasta. The notes
file is skipped because it is not FASTA (output/step1_convert/; log):

      [RENAMED] ATP6.txt -> ATP6.fasta
      ...
      [SKIPPED] Notes_on_specimens.txt: not FASTA (first line does not start with '>')

    Summary: 13 renamed, 0 skipped (name already used), 1 skipped (not FASTA), 0 error(s).

Step 2. split_major_fastas. The 13 major files become 26 gene files, 13 in
each specimen's folder (output/step2_split/; log).

Step 3. trim_fasta_trailing_whitespace. Each of the 26 gene files loses its
final line ending (output/step3_trim/; log).

Check. All 26 gene files from steps 2 and 3 were read back and compared with
the CDS sequences of PP726906 and PP726907. The sequences and headers matched
in every case.

Citing

If you use these scripts, please cite the release as given in CITATION.cff (or
with the Cite this repository button on this page):

  Patrick, L. B. (2026). FASTA Utilities: scripts for extracting, combining,
  renaming, splitting and trimming mitogenome FASTA files (Version 1.0.0)
  [Computer software]. Zenodo. https://doi.org/10.5281/zenodo.24510362

The release is archived on Zenodo. If you use MITOS2 annotations, please cite
MITOS2 (Donath et al., 2019). If you use the worked examples, please also cite
the sources of their data (Patrick & Santos, 2025; GenBank PV694306).

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

Version 1.1.0 was drafted with the assistance of Claude Opus 5.5 (Anthropic)
on 2026-11-24, from specifications by the author, and reviewed by the author,
and tested with Python 3.13.18 on the worked examples. The script's header
holds the same provenance.

| Script | Version | What it does | |---|---|---|---| |
trim_fasta_trailing_whitespace | 1.0 | 2026-07-18 | First version: removes all
trailing whitespace from each .fasta file in a folder; files already clean are
not rewritten. | | trim_fasta_trailing_whitespace | 1.1.0 | 2026-11-24 |
Option to keep exactly one final line ending, in the file's own style. .fa,
.fas, .fna accepted. Optional sub-folders. Dry run. SETTINGS block,
command-line options, run(). |

License

Released under the MIT License; see LICENSE.
