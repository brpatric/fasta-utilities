# FASTA Utilities

Three small Python scripts for tidying FASTA files before analysis or submission:

| Script | What it does |
|---|---|
| **ConvertTextToFasta** | Renames FASTA files saved as `.txt` so they end in `.fasta` (or `.fa`, `.fas`, `.fna`), after checking that each one really is FASTA. Only the name changes. |
| **split_major_fastas** | Splits "major" FASTA files (one file per gene, one record per specimen) into one file per gene per specimen, in one folder per specimen. |
| **trim_fasta_trailing_whitespace** | Removes blank lines, spaces and line endings from the end of each FASTA file, leaving no final line ending (or exactly one). |

Each script runs on its own, from the IDLE 3.13 shell or the command line. Together they make a short pipeline: rename, split, trim (see the [worked example](#worked-example-all-files-included)).

**Release 1.1.0** (2026-11-24): all three scripts at version 1.1.0 · Python 3 (standard library only)

**Author:** L. Brian Patrick, Department of Biological Sciences, Dakota Wesleyan University, Mitchell, SD, USA · ORCID [0000-0003-1969-9600](https://orcid.org/0000-0003-1969-9600)

**Cite as:**

> Patrick, L. B. (2026). *FASTA Utilities: helper scripts for renaming, splitting and trimming FASTA files* (Version 1.1.0) [Computer software]. https://github.com/brpatric/fasta-utilities

## Contents

```
fasta-utilities/
├── ConvertTextToFasta_v1.1.0_2026-11-24.py
├── split_major_fastas_v1.1.0_2026-11-24.py
├── trim_fasta_trailing_whitespace_v1.1.0_2026-11-24.py
├── README_ConvertTextToFasta_v1.1.0_2026-11-24.txt              plain-text manual for each script
├── README_split_major_fastas_v1.1.0_2026-11-24.txt
├── README_trim_fasta_trailing_whitespace_v1.1.0_2026-11-24.txt
├── README.md                                                    this page
├── CITATION.cff                                                 citation information
├── LICENSE
└── example/                                                     complete worked example
    ├── input/      13 "major" gene files for two Erigone atra mitogenomes, saved as .txt, and a notes file
    └── output/     the result of each step, and what each script printed
```

Each script has its own version number and date, carried in its file name, its header and its manual, so a script can be updated without changing the others.

## Requirements

| Item | Version or format | Install or notes |
| --- | --- | --- |
| Python | 3.8 or later (written and tested for IDLE 3.13; tested with 3.13.18) | [python.org](https://www.python.org/downloads/). No other packages are needed |
| FASTA files | Plain text, nucleotide or protein, any line length, Windows (CRLF) or Unix (LF) line endings | Each script works on the files in one folder |

The scripts run anywhere Python runs (Windows, macOS, Linux).

## Download

Click **Code → Download ZIP** at the top of this page and unzip it, or clone it:

```
git clone https://github.com/brpatric/fasta-utilities.git
```

---

## Running the scripts

All three scripts can be run the same five ways.

**A. In IDLE, with the SETTINGS block.** Open the script in IDLE, edit the SETTINGS block near the top, save, and press **F5**. For example, in `trim_fasta_trailing_whitespace`:

```python
FOLDER             = r"C:\Users\me\data\genes"   # keep the r before the quote on Windows
KEEP_FINAL_NEWLINE = False
RECURSIVE          = False
DRY_RUN            = False
```

**B. In IDLE, answering a question.** Leave the folder setting as `None` and press **F5**: the script asks for the folder in the shell. You can paste a path copied from Windows Explorer (**Shift + right-click → Copy as path**); quotes around it are removed. `split_major_fastas` asks only if `ASK_FOR_FOLDERS = True`; otherwise it uses the folder it is saved in, as in its first version.

**C. From the IDLE shell prompt.** After one F5 run, `run()` stays available at the `>>>` prompt:

```python
>>> run(r"C:\data\genes", dry_run=True)
```

**D. From the command line** (Windows PowerShell, macOS Terminal, Linux). Use `py -3.13` in place of `python3` on Windows:

```bash
python3 ConvertTextToFasta_v1.1.0_2026-11-24.py my_genes
python3 split_major_fastas_v1.1.0_2026-11-24.py my_genes --out by_specimen
python3 trim_fasta_trailing_whitespace_v1.1.0_2026-11-24.py by_specimen --recursive
```

With no arguments, a script uses its SETTINGS block, as in IDLE. `-h` lists the options and `--version` prints the version.

**E. From your own Python code.** The file names contain dots, so load a script with `runpy`:

```python
import runpy
trim = runpy.run_path("trim_fasta_trailing_whitespace_v1.1.0_2026-11-24.py")
trim["run"]("by_specimen", recursive=True)
```

**Try a dry run first.** Every script has a dry-run setting (`DRY_RUN = True` or `--dry-run`) that prints what it would do and changes nothing. ConvertTextToFasta and trim_fasta_trailing_whitespace change files in place, so work on a copy of anything you cannot replace.

---

## ConvertTextToFasta

Renames each `.txt` file in a folder (`.TXT` too) to the same name with a FASTA extension. The contents are not changed.

Before renaming, the script checks that the file is FASTA: the first line that is not blank must start with `>`, and every other line must be a header or a line of sequence letters (IUPAC codes, gaps `-` `.`, stop `*`). A notes file or other text file in the same folder is skipped. A file is also skipped if the new name is already taken, so nothing is overwritten.

| Setting | Command line | Default | Meaning |
|---|---|---|---|
| `FOLDER` | `FOLDER` (first argument) | ask | folder holding the `.txt` files |
| `NEW_EXTENSION` | `--ext` | `.fasta` | `.fasta`, `.fa`, `.fas` or `.fna` |
| `CHECK_FASTA` | `--no-check` | `True` | rename only files that look like FASTA |
| `DRY_RUN` | `--dry-run` | `False` | list what would be renamed; change nothing |

Messages: `[RENAMED]`, `[WOULD RENAME]` (dry run), `[SKIPPED] … already exists`, `[SKIPPED] … not FASTA (reason)` and `[ERROR]`, then a summary.

## split_major_fastas

Reads every FASTA file (`.fasta`, `.fa`, `.fas`, `.fna`) in the input folder. Each file holds one gene, with one record per specimen. Every record is written to its own file, `<label>/<label>_<gene>.fasta`, in a folder for each specimen.

Each header must have two words, the specimen label and the gene name:

```
>Erigone_atra_male COX1          ->  Erigone_atra_male/Erigone_atra_male_COX1.fasta
>Geolycosa_sp_Africa ATP8        ->  Geolycosa_sp_Africa/Geolycosa_sp_Africa_ATP8.fasta
```

The label is a single word (use underscores, not spaces). Anything after the gene name is ignored. Sequences are copied line for line, whatever their line length. Windows and old Mac line endings and blank lines are handled, and the output files have Unix (LF) line endings.

| Setting | Command line | Default | Meaning |
|---|---|---|---|
| `INPUT_FOLDER` | `INPUT_FOLDER` (first argument) | the script's own folder | folder holding the major FASTA files |
| `OUTPUT_FOLDER` | `--out` | same as the input folder | where the specimen folders are made |
| `ASK_FOR_FOLDERS` | | `False` | `True` = ask for both folders in the shell |
| `DRY_RUN` | `--dry-run` | `False` | list what would be written; write nothing |

The simplest way to use it is the original one: put the script in the folder with the major files, open it in IDLE and press F5.

**Notices.** The script reports and skips a header without a gene name, a record without a sequence, and a second record for the same specimen and gene (the first one is kept). It says how many files replaced files from an earlier run. It stops without writing anything if an output file would overwrite one of the input files.

## trim_fasta_trailing_whitespace

Removes whitespace from the end of each FASTA file in a folder: blank lines, spaces, tabs, carriage returns and line feeds. Nothing else in the file changes, and files that already end cleanly are not rewritten. The file is read and written as raw bytes, so its line endings and encoding stay as they were.

By default the last line is left with no line ending at all, which some programs need. `KEEP_FINAL_NEWLINE = True` (`--keep-newline`) instead leaves exactly one line ending, in the file's own style (CRLF or LF), which is what most Unix tools expect.

| Setting | Command line | Default | Meaning |
|---|---|---|---|
| `FOLDER` | `FOLDER` (first argument) | ask | folder holding the FASTA files |
| `KEEP_FINAL_NEWLINE` | `--keep-newline` | `False` | `True` = end with exactly one line ending |
| `RECURSIVE` | `--recursive` | `False` | also process FASTA files in sub-folders |
| `DRY_RUN` | `--dry-run` | `False` | report what would change; change nothing |

Messages: `[OK] … already clean`, `[MODIFIED] … removed N trailing byte(s)` (or `added a final line ending`), `[WOULD FIX]` (dry run), `[SKIPPED]` and `[ERROR]`, then a summary.

---

## Worked example (all files included)

The example uses the 13 protein-coding genes of the two *Erigone atra* mitogenomes from Patrick and Santos (2025): a male, GenBank [PP726906](https://www.ncbi.nlm.nih.gov/nuccore/PP726906), and a female, GenBank [PP726907](https://www.ncbi.nlm.nih.gov/nuccore/PP726907). The gene sequences were taken from the CDS features of the two records.

[`example/input/`](example/input) holds one "major" file per gene, saved with a `.txt` extension and Windows line endings, as files saved from many Windows programs are. Each holds both specimens:

```
>Erigone_atra_male COX1
TTACTGCGATGAATTTATTCAACTAATCATAAGGACATTGGAAGTTTGTATTTTGTTTTT
...
>Erigone_atra_female COX1
TTACTGCGATGAATTTATTCAACTAATCATAAGGACATTGGAAGTTTGTATTTTGTTTTT
...
```

The folder also holds `Notes_on_specimens.txt`, a plain-text note, to show that ConvertTextToFasta leaves files that are not FASTA alone.

To run the example, copy `example/input` to a working folder named `my_genes`, then run the three scripts in turn from the folder that contains it:

```bash
python3 ConvertTextToFasta_v1.1.0_2026-11-24.py my_genes
python3 split_major_fastas_v1.1.0_2026-11-24.py my_genes --out by_specimen
python3 trim_fasta_trailing_whitespace_v1.1.0_2026-11-24.py by_specimen --recursive
```

(or set the same folders in each script's SETTINGS block and press F5). The result of each step should match [`example/output/`](example/output) exactly.

### Step 1. ConvertTextToFasta

The 13 gene files are renamed to `.fasta`. The notes file is skipped because it is not FASTA. The result is in [`example/output/step1_convert/`](example/output/step1_convert), and the shell output is in [`step1_log.txt`](example/output/step1_log.txt):

```
  [RENAMED] ATP6.txt -> ATP6.fasta
  ...
  [RENAMED] ND6.txt -> ND6.fasta
  [SKIPPED] Notes_on_specimens.txt: not FASTA (first line does not start with '>')

Summary: 13 renamed, 0 skipped (name already used), 1 skipped (not FASTA), 0 error(s).
```

### Step 2. split_major_fastas

The 13 major files become 26 gene files, in one folder per specimen ([`example/output/step2_split/`](example/output/step2_split), [`step2_log.txt`](example/output/step2_log.txt)):

```
  Major FASTA files read : 13
  Specimen folders       : 2
  Gene files written     : 26

  Specimen folders:
    Erigone_atra_female/  (13 genes)
    Erigone_atra_male/  (13 genes)
```

### Step 3. trim_fasta_trailing_whitespace

Each of the 26 gene files loses its final line ending ([`example/output/step3_trim/`](example/output/step3_trim), [`step3_log.txt`](example/output/step3_log.txt)):

```
  [MODIFIED] Erigone_atra_female/Erigone_atra_female_ATP6.fasta - removed 1 trailing byte(s).
  ...
Summary: 26 modified, 0 unchanged, 0 error(s).
```

**Check.** All 26 gene files from steps 2 and 3 were read back and compared with the CDS sequences of PP726906 and PP726907. The sequences and headers matched in every case.

---

## Citing

If you use these scripts, please cite the release as given in [`CITATION.cff`](CITATION.cff) (or with the **Cite this repository** button on this page):

> Patrick, L. B. (2026). *FASTA Utilities: helper scripts for renaming, splitting and trimming FASTA files* (Version 1.1.0) [Computer software]. https://github.com/brpatric/fasta-utilities

If you use the worked example, please also cite Patrick and Santos (2025).

## References

Patrick, L. B., & Santos, S. R. (2025). The complete mitochondrial genome of *Erigone atra* Blackwall, 1833 (Araneae, Linyphiidae). *Mitochondrial DNA Part B*, 10(12), 1243–1248. https://doi.org/10.1080/23802359.2025.2594297 (source of the worked example)

Pearson, W. R., & Lipman, D. J. (1988). Improved tools for biological sequence comparison. *Proceedings of the National Academy of Sciences of the United States of America*, 85(8), 2444–2448. https://doi.org/10.1073/pnas.85.8.2444 (origin of the FASTA format)

Python Software Foundation. (2024). *Python* (Version 3.13) [Computer software]. https://www.python.org/

## Provenance and version history

The first versions were written by the author with the assistance of Claude (Anthropic). Version 1.1.0 of each script was drafted with the assistance of Claude Opus 5.5 (Anthropic) on 2026-11-24, from specifications by the author, and reviewed by the author. Version 1.1.0 of each was tested with Python 3.13.18 on the worked example. Edge cases were also tested: name clashes, empty files, a header with no sequence, duplicate records, headers without a gene name, CRLF and CR line endings, existing output files, dry runs, and each IDLE mode.

| Script | Version | Date | Changes |
|---|---|---|---|
| ConvertTextToFasta | 1.0.0 | (undated) | Original script (`ConvertTextToFasta.py`): renames every `*.txt` in a folder to `*.fasta`; skips a file whose new name already exists. |
| ConvertTextToFasta | 1.1.0 | 2026-11-24 | Checks each file is FASTA before renaming, and skips files that are not. `.txt` matched in any capitalisation. Choice of new extension. Dry run. SETTINGS block, question in the shell, command-line options, `run()`. |
| split_major_fastas | 1.0.0 | (undated) | Original script (`split_major_fastas.py`): splits every `*.fasta` in its own folder into `<label>/<label>_<gene>.fasta`; skips duplicates and records without a gene name or sequence. |
| split_major_fastas | 1.1.0 | 2026-11-24 | Input and output folders can be chosen (the default is still the script's own folder). `.fa`, `.fas` and `.fna` accepted. Stops if an output file would overwrite an input file. Reports files replaced from an earlier run. Dry run. SETTINGS block, optional questions, command-line options, `run()`. |
| trim_fasta_trailing_whitespace | 1.0 | 2026-07-18 | Original script: removes all trailing whitespace from each `.fasta` file in a folder; files already clean are not rewritten. |
| trim_fasta_trailing_whitespace | 1.1.0 | 2026-11-24 | Option to keep exactly one final line ending, in the file's own style. `.fa`, `.fas` and `.fna` accepted. Optional sub-folders. Dry run. SETTINGS block, command-line options, `run()`. |

Each version's file names carry its version number and date. Releases on this page are tagged with the release version.

## License

Released under the MIT License; see [`LICENSE`](LICENSE).
