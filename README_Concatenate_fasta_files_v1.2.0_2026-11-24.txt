README_Concatenate_fasta_files_v1.2.0_2026-11-24.txt
====================================================
Manual for Concatenate_fasta_files_v1.2.0_2026-11-24.py

Concatenate_fasta_files, version 1.2.0 (2026-11-24)

Program file: Concatenate_fasta_files_v1.2.0_2026-11-24.py. Part of FASTA
Utilities (release 1.0.0), https://github.com/brpatric/fasta-utilities

Author: L. Brian Patrick, Department of Biological Sciences, Dakota Wesleyan
University, Mitchell, SD, USA. ORCID 0000-0003-1969-9600

What it does

Combines every FASTA file (.fasta, .fa, .fas, .fna) in a folder into one file,
in alphabetical order of file name. Each record keeps its header and sequence.
There are no blank lines between records and, by default, no line ending after
the last record. Files that are empty, or do not start with a > header, are
skipped. A header that appears in two files is reported. The output file is
never read as an input, so the script can be run again safely.

  Setting              Command line      Default   Meaning
  -------------------- ----------------- --------- --------------------------------------------------------------------------------
  INPUT_FOLDER         first argument    ask       folder holding the FASTA files
  OUTPUT_FILE          second argument   ask       a bare name (ATP6.fasta) is saved in the input folder; a path is used as given
  KEEP_FINAL_NEWLINE   --keep-newline    False     end the output with one line ending
  CHECK_FASTA          --no-check        True      skip files that do not start with >
  DRY_RUN              --dry-run         False     report what would be written; write nothing

The output has Unix (LF) line endings.

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

Worked example: Concatenate_fasta_files: COX1 from three specimens

example/concatenate/input/ holds COX1 from A. albostriata (from example 1) and
from the two Erigone atra mitogenomes (from example 3).

    cd example/concatenate
    python3 ../../Concatenate_fasta_files_v1.2.0_2026-11-24.py input output/COX1.fasta

      Found 3 FASTA file(s) to concatenate:
        - Alopecosa_albostriata_PV694306_COX1.fasta  (1 record)
        - Erigone_atra_female_COX1.fasta  (1 record)
        - Erigone_atra_male_COX1.fasta  (1 record)

    Wrote 3 record(s) from 3 file(s) to COX1.fasta.

The result, output/COX1.fasta, is ready for alignment.

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

Version 1.2.0 was drafted with the assistance of Claude Opus 5.5 (Anthropic)
on 2026-11-24, from specifications by the author, and reviewed by the author,
and tested with Python 3.13.18 on the worked examples. The script's header
holds the same provenance.

| Script | Version | What it does | |---|---|---|---| |
Concatenate_fasta_files | 1.0, 1.1 | 2026-07-18 | 1.0 first version; 1.1 no
line ending after the final record. | | Concatenate_fasta_files | 1.2.0 |
2026-11-24 | .fa, .fas, .fna accepted. Non-FASTA files skipped. Blank lines
inside files removed. A bare output name saved in the input folder. Unix line
endings. Option for a final line ending. Duplicate headers and a replaced
output file reported. Dry run. SETTINGS block, questions in the shell,
command-line options, run(). Errors no longer stop IDLE with a SystemExit. |

License

Released under the MIT License; see LICENSE.
