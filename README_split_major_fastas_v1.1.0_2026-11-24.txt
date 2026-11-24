README_split_major_fastas_v1.1.0_2026-11-24.txt
===============================================
Manual for split_major_fastas_v1.1.0_2026-11-24.py

split_major_fastas, version 1.1.0 (2026-11-24)

Program file: split_major_fastas_v1.1.0_2026-11-24.py. Part of FASTA
Utilities, https://github.com/brpatric/fasta-utilities

Author: L. Brian Patrick, Department of Biological Sciences, Dakota Wesleyan
University, Mitchell, SD, USA. ORCID 0000-0003-1969-9600

What it does

Reads every FASTA file (.fasta, .fa, .fas, .fna) in the input folder. Each
file holds one gene, with one record per specimen. Every record is written to
its own file, <label>/<label>_<gene>.fasta, in a folder for each specimen.

Each header must have two words, the specimen label and the gene name:

    >Erigone_atra_male COX1          ->  Erigone_atra_male/Erigone_atra_male_COX1.fasta
    >Geolycosa_sp_Africa ATP8        ->  Geolycosa_sp_Africa/Geolycosa_sp_Africa_ATP8.fasta

The label is a single word (use underscores, not spaces). Anything after the
gene name is ignored. Sequences are copied line for line, whatever their line
length. Windows and old Mac line endings and blank lines are handled, and the
output files have Unix (LF) line endings.

  Setting           Command line                    Default                    Meaning
  ----------------- ------------------------------- -------------------------- -------------------------------------------
  INPUT_FOLDER      INPUT_FOLDER (first argument)   the script's own folder    folder holding the major FASTA files
  OUTPUT_FOLDER     --out                           same as the input folder   where the specimen folders are made
  ASK_FOR_FOLDERS                                   False                      True = ask for both folders in the shell
  DRY_RUN           --dry-run                       False                      list what would be written; write nothing

The simplest way to use it is the original one: put the script in the folder
with the major files, open it in IDLE and press F5.

Notices. The script reports and skips a header without a gene name, a record
without a sequence, and a second record for the same specimen and gene (the
first one is kept). It says how many files replaced files from an earlier run.
It stops without writing anything if an output file would overwrite one of the
input files.

Requirements

  Item          Version or format                                                                              Install or notes
  ------------- ---------------------------------------------------------------------------------------------- ----------------------------------------------
  Python        3.8 or later (written and tested for IDLE 3.13; tested with 3.13.18)                           python.org. No other packages are needed
  FASTA files   Plain text, nucleotide or protein, any line length, Windows (CRLF) or Unix (LF) line endings   Each script works on the files in one folder

The scripts run anywhere Python runs (Windows, macOS, Linux).

Running it

All three scripts can be run the same five ways.

A. In IDLE, with the SETTINGS block. Open the script in IDLE, edit the
SETTINGS block near the top, save, and press F5. For example, in
trim_fasta_trailing_whitespace:

    FOLDER             = r"C:\Users\me\data\genes"   # keep the r before the quote on Windows
    KEEP_FINAL_NEWLINE = False
    RECURSIVE          = False
    DRY_RUN            = False

B. In IDLE, answering a question. Leave the folder setting as None and press
F5: the script asks for the folder in the shell. You can paste a path copied
from Windows Explorer (Shift + right-click → Copy as path); quotes around it
are removed. split_major_fastas asks only if ASK_FOR_FOLDERS = True; otherwise
it uses the folder it is saved in, as in its first version.

C. From the IDLE shell prompt. After one F5 run, run() stays available at
the >>> prompt:

    >>> run(r"C:\data\genes", dry_run=True)

D. From the command line (Windows PowerShell, macOS Terminal, Linux). Use
py -3.13 in place of python3 on Windows:

    python3 ConvertTextToFasta_v1.1.0_2026-11-24.py my_genes
    python3 split_major_fastas_v1.1.0_2026-11-24.py my_genes --out by_specimen
    python3 trim_fasta_trailing_whitespace_v1.1.0_2026-11-24.py by_specimen --recursive

With no arguments, a script uses its SETTINGS block, as in IDLE. -h lists the
options and --version prints the version.

E. From your own Python code. The file names contain dots, so load a script
with runpy:

    import runpy
    trim = runpy.run_path("trim_fasta_trailing_whitespace_v1.1.0_2026-11-24.py")
    trim["run"]("by_specimen", recursive=True)

Try a dry run first. Every script has a dry-run setting (DRY_RUN = True or
--dry-run) that prints what it would do and changes nothing.
ConvertTextToFasta and trim_fasta_trailing_whitespace change files in place,
so work on a copy of anything you cannot replace.

Worked example

The example in example/ uses the 13 protein-coding genes of the two Erigone
atra mitogenomes (GenBank PP726906 and PP726907; Patrick & Santos, 2025): one
"major" file per gene, holding both specimens, saved as .txt. The three
scripts are run in turn (see README.md for the full example). This script is
step 2:

The 13 major files become 26 gene files, in one folder per specimen
(example/output/step2_split/, step2_log.txt):

      Major FASTA files read : 13
      Specimen folders       : 2
      Gene files written     : 26

      Specimen folders:
        Erigone_atra_female/  (13 genes)
        Erigone_atra_male/  (13 genes)

Citing

If you use these scripts, please cite the release as given in CITATION.cff (or
with the Cite this repository button on this page):

  Patrick, L. B. (2026). FASTA Utilities: helper scripts for renaming,
  splitting and trimming FASTA files (Version 1.1.0) [Computer software].
  https://github.com/brpatric/fasta-utilities

If you use the worked example, please also cite Patrick and Santos (2025).

References

Patrick, L. B., & Santos, S. R. (2025). The complete mitochondrial genome of
Erigone atra Blackwall, 1833 (Araneae, Linyphiidae). Mitochondrial DNA Part B,
10(12), 1243–1248. https://doi.org/10.1080/23802359.2025.2594297 (source of
the worked example)

Pearson, W. R., & Lipman, D. J. (1988). Improved tools for biological sequence
comparison. Proceedings of the National Academy of Sciences of the United
States of America, 85(8), 2444–2448. https://doi.org/10.1073/pnas.85.8.2444
(origin of the FASTA format)

Python Software Foundation. (2024). Python (Version 3.13) [Computer software].
https://www.python.org/

Provenance and version history

Version 1.1.0 was drafted with the assistance of Claude Opus 5.5 (Anthropic)
on 2026-11-24, from specifications by the author, and reviewed by the author.
It was tested with Python 3.13.18 on the worked example. The script's header
holds the same provenance.

  ---                  ---     ---          ---
  -------------------- ------- ------------ --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  split_major_fastas   1.0.0   (undated)    Original script (split_major_fastas.py): splits every *.fasta in its own folder into <label>/<label>_<gene>.fasta; skips duplicates and records without a gene name or sequence.
  split_major_fastas   1.1.0   2026-11-24   Input and output folders can be chosen (the default is still the script's own folder). .fa, .fas and .fna accepted. Stops if an output file would overwrite an input file. Reports files replaced from an earlier run. Dry run. SETTINGS block, optional questions, command-line options, run().

License

Released under the MIT License; see LICENSE.
