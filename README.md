# FASTA Utilities

Five small Python scripts for preparing mitogenome FASTA files for alignment, from a raw mitogenome to tidy gene files:

| Script | Version | What it does |
|---|---|---|
| **mito_gene_extractor** | 1.6.0 | Extracts one FASTA file per gene from a mitogenome, using its MITOS2 annotation (the BED file as downloaded, or a simplified gene/start/end/strand table). |
| **Concatenate_fasta_files** | 1.2.0 | Combines all FASTA files in a folder (e.g. the same gene from many specimens) into one multi-FASTA file. |
| **ConvertTextToFasta** | 1.1.0 | Renames FASTA files saved as `.txt` so they end in `.fasta` (or `.fa`, `.fas`, `.fna`), after checking that each one really is FASTA. Only the name changes. |
| **split_major_fastas** | 1.1.0 | Splits "major" FASTA files (one file per gene, one record per specimen) into one file per gene per specimen, in one folder per specimen. |
| **trim_fasta_trailing_whitespace** | 1.1.0 | Removes blank lines, spaces and line endings from the end of each FASTA file, leaving no final line ending (or exactly one). |

Each script runs on its own, from the IDLE 3.13 shell or the command line.

**Release 1.0.0** (2026-11-24) · Python 3 (standard library only)

**Author:** L. Brian Patrick, Department of Biological Sciences, Dakota Wesleyan University, Mitchell, SD, USA · ORCID [0000-0003-1969-9600](https://orcid.org/0000-0003-1969-9600)

**Cite as:**

> Patrick, L. B. (2026). *FASTA Utilities: scripts for extracting, combining, renaming, splitting and trimming mitogenome FASTA files* (Version 1.0.0) [Computer software]. https://github.com/brpatric/fasta-utilities

## Contents

```
fasta-utilities/
├── mito_gene_extractor_v1.6.0_2026-11-24.py
├── Concatenate_fasta_files_v1.2.0_2026-11-24.py
├── ConvertTextToFasta_v1.1.0_2026-11-24.py
├── split_major_fastas_v1.1.0_2026-11-24.py
├── trim_fasta_trailing_whitespace_v1.1.0_2026-11-24.py
├── README_<script>_<version>_<date>.txt     plain-text manual for each script (five files)
├── README.md                                this page
├── CITATION.cff                             citation information
├── LICENSE
└── example/                                 complete worked examples
    ├── extract/              a MITOS2-annotated mitogenome (Alopecosa albostriata) and its gene files
    ├── concatenate/          COX1 from three specimens, combined into one file
    └── convert_split_trim/   13 "major" gene files for two Erigone atra mitogenomes, renamed, split and trimmed
```

Each script has its own version number and date, carried in its file name, its header and its manual, so one script can be updated without changing the others. Releases of the repository have their own number.

## Requirements

| Item | Version or format | Install or notes |
| --- | --- | --- |
| Python | 3.8 or later (written and tested for IDLE 3.13; tested with 3.13.18) | [python.org](https://www.python.org/downloads/). No other packages are needed |
| FASTA files | Plain text, nucleotide or protein, any line length, Windows (CRLF) or Unix (LF) line endings | |
| MITOS2 annotation (mito_gene_extractor only) | The BED file from [MITOS2](http://mitos2.bioinf.uni-leipzig.de/) (e.g. run on Galaxy), or a tab-delimited table of gene, start, end, strand | Coordinates in the BED convention (0-based start, exclusive end) |

The scripts run anywhere Python runs (Windows, macOS, Linux).

## Download

Click **Code → Download ZIP** at the top of this page and unzip it, or clone it:

```
git clone https://github.com/brpatric/fasta-utilities.git
```

---

## Running the scripts

All five scripts can be run the same five ways.

**A. In IDLE, with the SETTINGS block.** Open the script in IDLE, edit the SETTINGS block near the top, save, and press **F5**. For example, in `trim_fasta_trailing_whitespace`:

```python
FOLDER             = r"C:\Users\me\data\genes"   # keep the r before the quote on Windows
KEEP_FINAL_NEWLINE = False
RECURSIVE          = False
DRY_RUN            = False
```

**B. In IDLE, answering questions.** Leave the first file or folder setting as `None` and press **F5**: the script asks for what it needs in the shell. You can paste a path copied from Windows Explorer (**Shift + right-click → Copy as path**); quotes around it are removed. `split_major_fastas` asks only if `ASK_FOR_FOLDERS = True`; otherwise it uses the folder it is saved in, as in its first version.

**C. From the IDLE shell prompt.** After one F5 run, `run()` stays available at the `>>>` prompt:

```python
>>> run(r"C:\data\genes", dry_run=True)
```

**D. From the command line** (Windows PowerShell, macOS Terminal, Linux). Use `py -3.13` in place of `python3` on Windows. With no arguments, a script uses its SETTINGS block, as in IDLE. `-h` lists the options and `--version` prints the version. The commands for each script are in the worked examples.

**E. From your own Python code.** The file names contain dots, so load a script with `runpy`:

```python
import runpy
trim = runpy.run_path("trim_fasta_trailing_whitespace_v1.1.0_2026-11-24.py")
trim["run"]("by_specimen", recursive=True)
```

**Try a dry run first.** Concatenate_fasta_files, ConvertTextToFasta, split_major_fastas and trim_fasta_trailing_whitespace have a dry-run setting (`DRY_RUN = True` or `--dry-run`) that prints what would happen and changes nothing. ConvertTextToFasta and trim_fasta_trailing_whitespace change files in place, so work on a copy of anything you cannot replace.

---

## mito_gene_extractor

Writes one FASTA file per annotated gene. Each file holds a header and the gene sequence on one line:

```
>Alopecosa_albostriata_PV694306 COX1        ->  Alopecosa_albostriata_PV694306_COX1.fasta
```

Minus-strand genes are reverse-complemented. A gene that crosses the origin of the circular genome is joined across it, whether it is written with its start larger than its end or with its end past the last base. The gene files are draft gene regions, meant to be aligned to decide the final gene boundaries.

**Annotation formats.** The script recognises either format on each line:

| Format | Columns | Example |
|---|---|---|
| MITOS2 BED, as downloaded | sequence ID, start, end, name, score, strand | `PV694306.1  1137  2679  cox1  2418098491.5  +` |
| Simplified table | gene, start, end, strand | `COX1  1137  2679  +` |

**Coordinates.** Both formats use the BED convention: the start is counted from 0 and the end is exclusive, so a gene occupying bases 1–65 is written `0  65`. In an edited table, keep the start values exactly as MITOS2 wrote them. Changing a start of 0 to 1 drops the first base of that gene.

**Gene names.** MITOS2 names are converted to standard symbols: `cox1` → `COX1`, `nad4l` → `ND4L`, `cob` → `CytB`, `rrnL` → `16S`, `rrnS` → `12S`, and `trnL1(tag)` → `trnL1`. Names that are already standard are left alone. MITOS2 sometimes splits a gene into parts (`nad5_0`, `nad5_1`, `rrnS_0-b`). Each part is saved as its own file (`ND5_0`, `ND5_1`, `12S_0-b`) and listed at the end of the run, so you can check them and merge or rename them in an edited table.

| Setting | Command line | Default | Meaning |
|---|---|---|---|
| `FASTA_FILE` | first argument | ask | mitogenome FASTA (the first sequence is used) |
| `ANNOTATION_FILE` | second argument | ask | MITOS2 `.bed` or gene/start/end/strand table |
| `OUTPUT_DIR` | `-o` | `mitogenes` | folder for the gene files (made if needed) |
| `BASE_NAME` | `-b` | none | text put before each gene name, e.g. `Pardosa_altamontis_Mt242` |
| `BASE_FROM_FASTA` | `--base-from-fasta` | `False` | use the first word of the FASTA header as the base name |
| `STANDARD_NAMES` | `--keep-names` | `True` | convert MITOS2 names to standard symbols |
| `KEEP_FINAL_NEWLINE` | `--keep-newline` | `False` | end each file with a line ending |

Files from an earlier run are replaced. A gene name that appears twice in one annotation is saved as `…_2.fasta`. Lines that cannot be read and coordinates that do not fit the genome are reported and skipped.

## Concatenate_fasta_files

Combines every FASTA file (`.fasta`, `.fa`, `.fas`, `.fna`) in a folder into one file, in alphabetical order of file name. Each record keeps its header and sequence. There are no blank lines between records and, by default, no line ending after the last record. Files that are empty, or do not start with a `>` header, are skipped. A header that appears in two files is reported. The output file is never read as an input, so the script can be run again safely.

| Setting | Command line | Default | Meaning |
|---|---|---|---|
| `INPUT_FOLDER` | first argument | ask | folder holding the FASTA files |
| `OUTPUT_FILE` | second argument | ask | a bare name (`ATP6.fasta`) is saved in the input folder; a path is used as given |
| `KEEP_FINAL_NEWLINE` | `--keep-newline` | `False` | end the output with one line ending |
| `CHECK_FASTA` | `--no-check` | `True` | skip files that do not start with `>` |
| `DRY_RUN` | `--dry-run` | `False` | report what would be written; write nothing |

The output has Unix (LF) line endings.

## ConvertTextToFasta

Renames each `.txt` file in a folder (`.TXT` too) to the same name with a FASTA extension. The contents are not changed.

Before renaming, the script checks that the file is FASTA: the first line that is not blank must start with `>`, and every other line must be a header or a line of sequence letters (IUPAC codes, gaps `-` `.`, stop `*`). A notes file or other text file in the same folder is skipped. A file is also skipped if the new name is already taken, so nothing is overwritten.

| Setting | Command line | Default | Meaning |
|---|---|---|---|
| `FOLDER` | first argument | ask | folder holding the `.txt` files |
| `NEW_EXTENSION` | `--ext` | `.fasta` | `.fasta`, `.fa`, `.fas` or `.fna` |
| `CHECK_FASTA` | `--no-check` | `True` | rename only files that look like FASTA |
| `DRY_RUN` | `--dry-run` | `False` | list what would be renamed; change nothing |

## split_major_fastas

Reads every FASTA file in the input folder. Each file holds one gene, with one record per specimen. Every record is written to its own file, `<label>/<label>_<gene>.fasta`, in a folder for each specimen. Each header must have two words, the specimen label (one word, with underscores) and the gene name:

```
>Erigone_atra_male COX1          ->  Erigone_atra_male/Erigone_atra_male_COX1.fasta
```

Sequences are copied line for line. Windows and old Mac line endings and blank lines are handled, and the output files have Unix (LF) line endings. A header without a gene name, a record without a sequence, and a second record for the same specimen and gene are reported and skipped. The script stops without writing anything if an output file would overwrite one of the input files.

| Setting | Command line | Default | Meaning |
|---|---|---|---|
| `INPUT_FOLDER` | first argument | the script's own folder | folder holding the major FASTA files |
| `OUTPUT_FOLDER` | `--out` | same as the input folder | where the specimen folders are made |
| `ASK_FOR_FOLDERS` | | `False` | `True` = ask for both folders in the shell |
| `DRY_RUN` | `--dry-run` | `False` | list what would be written; write nothing |

## trim_fasta_trailing_whitespace

Removes whitespace from the end of each FASTA file in a folder: blank lines, spaces, tabs, carriage returns and line feeds. Nothing else in the file changes, and files that already end cleanly are not rewritten. The file is read and written as raw bytes, so its line endings and encoding stay as they were. By default the last line is left with no line ending at all. `KEEP_FINAL_NEWLINE = True` instead leaves exactly one, in the file's own style (CRLF or LF).

| Setting | Command line | Default | Meaning |
|---|---|---|---|
| `FOLDER` | first argument | ask | folder holding the FASTA files |
| `KEEP_FINAL_NEWLINE` | `--keep-newline` | `False` | end with exactly one line ending |
| `RECURSIVE` | `--recursive` | `False` | also process FASTA files in sub-folders |
| `DRY_RUN` | `--dry-run` | `False` | report what would change; change nothing |

---

## Worked examples (all files included)

Run each example from its own folder in `example/`. The results should match that folder's `output/` exactly.

### 1. mito_gene_extractor: *Alopecosa albostriata*

[`example/extract/input/`](example/extract/input) holds the mitogenome of the wolf spider *Alopecosa albostriata*, GenBank [PV694306.1](https://www.ncbi.nlm.nih.gov/nuccore/PV694306) (14,397 bp; the GenBank record is marked UNVERIFIED). It also holds two annotations. The annotation is an uncurated MITOS2 draft, used here only to show the program: it is not a final annotation of this genome.

| File | Content |
|---|---|
| `PV694306.fasta` | the mitogenome |
| `PV694306_MITOS2.bed` | the MITOS2 BED file as downloaded from Galaxy (38 features) |
| `PV694306_MITOS2_edited.txt` | the same annotation edited by hand into a gene/start/end/strand table: names cleaned up, the three `rrnS` parts merged into 12S, and MITOS2's `nad5_1` relabelled as trnY (36 features) |

```bash
cd example/extract
python3 ../../mito_gene_extractor_v1.6.0_2026-11-24.py input/PV694306.fasta input/PV694306_MITOS2.bed -o output/from_MITOS2_bed -b Alopecosa_albostriata_PV694306
python3 ../../mito_gene_extractor_v1.6.0_2026-11-24.py input/PV694306.fasta input/PV694306_MITOS2_edited.txt -o output/from_edited_table -b Alopecosa_albostriata_PV694306
```

From the BED file, 38 gene files ([`output/from_MITOS2_bed/`](example/extract/output/from_MITOS2_bed); [log](example/extract/output/from_MITOS2_bed_log.txt)), with the MITOS2 names converted and the split genes listed:

```
  trnM (trnM(cat))             65 bp  +  0-65  -> Alopecosa_albostriata_PV694306_trnM.fasta
  ND2 (nad2)                  966 bp  +  46-1012  -> Alopecosa_albostriata_PV694306_ND2.fasta
  ND5_1 (nad5_1)               78 bp  +  977-1055  -> Alopecosa_albostriata_PV694306_ND5_1.fasta
  ...
  Notices (1):
    - MITOS2 split these genes into parts, each saved as its own file: ND5_1, ND5_0, 12S_0-b, 12S_0-a, 12S_1. ...
```

From the edited table, 36 gene files: 13 protein-coding, 21 tRNA and 2 rRNA ([`output/from_edited_table/`](example/extract/output/from_edited_table); [log](example/extract/output/from_edited_table_log.txt)).

**Checks.** On the edited table, version 1.6.0 writes files byte-for-byte identical to those of version 1.5. COX1, CytB and ND4 translate under the invertebrate mitochondrial code with no internal stop codons. To test genes that cross the origin, the genome was rotated so that genes on both strands crossed it. All 144 extractions, made with both ways of writing such a gene, matched the unrotated genes.

### 2. Concatenate_fasta_files: COX1 from three specimens

[`example/concatenate/input/`](example/concatenate/input) holds COX1 from *A. albostriata* (from example 1) and from the two *Erigone atra* mitogenomes (from example 3).

```bash
cd example/concatenate
python3 ../../Concatenate_fasta_files_v1.2.0_2026-11-24.py input output/COX1.fasta
```

```
  Found 3 FASTA file(s) to concatenate:
    - Alopecosa_albostriata_PV694306_COX1.fasta  (1 record)
    - Erigone_atra_female_COX1.fasta  (1 record)
    - Erigone_atra_male_COX1.fasta  (1 record)

Wrote 3 record(s) from 3 file(s) to COX1.fasta.
```

The result, [`output/COX1.fasta`](example/concatenate/output/COX1.fasta), is ready for alignment.

### 3. ConvertTextToFasta → split_major_fastas → trim_fasta_trailing_whitespace: *Erigone atra*

This example uses the 13 protein-coding genes of the two *Erigone atra* mitogenomes from Patrick and Santos (2025): a male, GenBank [PP726906](https://www.ncbi.nlm.nih.gov/nuccore/PP726906), and a female, GenBank [PP726907](https://www.ncbi.nlm.nih.gov/nuccore/PP726907), taken from the CDS features of the two records. [`example/convert_split_trim/input/`](example/convert_split_trim/input) holds one "major" file per gene, holding both specimens and saved with a `.txt` extension and Windows line endings, as files saved from many Windows programs are. It also holds `Notes_on_specimens.txt`, a plain-text note.

ConvertTextToFasta and trim_fasta_trailing_whitespace change files in place, so copy `input` to a working folder named `my_genes` first:

```bash
cd example/convert_split_trim
cp -r input my_genes          # Windows: copy the folder in Explorer
python3 ../../ConvertTextToFasta_v1.1.0_2026-11-24.py my_genes
python3 ../../split_major_fastas_v1.1.0_2026-11-24.py my_genes --out by_specimen
python3 ../../trim_fasta_trailing_whitespace_v1.1.0_2026-11-24.py by_specimen --recursive
```

**Step 1. ConvertTextToFasta.** The 13 gene files are renamed to `.fasta`. The notes file is skipped because it is not FASTA ([`output/step1_convert/`](example/convert_split_trim/output/step1_convert); [log](example/convert_split_trim/output/step1_log.txt)):

```
  [RENAMED] ATP6.txt -> ATP6.fasta
  ...
  [SKIPPED] Notes_on_specimens.txt: not FASTA (first line does not start with '>')

Summary: 13 renamed, 0 skipped (name already used), 1 skipped (not FASTA), 0 error(s).
```

**Step 2. split_major_fastas.** The 13 major files become 26 gene files, 13 in each specimen's folder ([`output/step2_split/`](example/convert_split_trim/output/step2_split); [log](example/convert_split_trim/output/step2_log.txt)).

**Step 3. trim_fasta_trailing_whitespace.** Each of the 26 gene files loses its final line ending ([`output/step3_trim/`](example/convert_split_trim/output/step3_trim); [log](example/convert_split_trim/output/step3_log.txt)).

**Check.** All 26 gene files from steps 2 and 3 were read back and compared with the CDS sequences of PP726906 and PP726907. The sequences and headers matched in every case.

---

## Citing

If you use these scripts, please cite the release as given in [`CITATION.cff`](CITATION.cff) (or with the **Cite this repository** button on this page):

> Patrick, L. B. (2026). *FASTA Utilities: scripts for extracting, combining, renaming, splitting and trimming mitogenome FASTA files* (Version 1.0.0) [Computer software]. https://github.com/brpatric/fasta-utilities

If you use MITOS2 annotations, please cite MITOS2 (Donath et al., 2019). If you use the worked examples, please also cite the sources of their data (Patrick & Santos, 2025; GenBank PV694306).

## References

Donath, A., Jühling, F., Al-Arab, M., Bernhart, S. H., Reinhardt, F., Stadler, P. F., Middendorf, M., & Bernt, M. (2019). Improved annotation of protein-coding genes boundaries in metazoan mitochondrial genomes. *Nucleic Acids Research*, 47(20), 10543–10552. https://doi.org/10.1093/nar/gkz833 (MITOS2)

Patrick, L. B., & Santos, S. R. (2025). The complete mitochondrial genome of *Erigone atra* Blackwall, 1833 (Araneae, Linyphiidae). *Mitochondrial DNA Part B*, 10(12), 1243–1248. https://doi.org/10.1080/23802359.2025.2594297 (source of worked example 3)

Pearson, W. R., & Lipman, D. J. (1988). Improved tools for biological sequence comparison. *Proceedings of the National Academy of Sciences of the United States of America*, 85(8), 2444–2448. https://doi.org/10.1073/pnas.85.8.2444 (origin of the FASTA format)

Python Software Foundation. (2024). *Python* (Version 3.13) [Computer software]. https://www.python.org/

## Provenance and version history

The earlier versions of each script were written by the author with the assistance of Claude (Anthropic). The versions in this release were drafted with the assistance of Claude Opus 5.5 (Anthropic) on 2026-11-24, from specifications by the author, and reviewed by the author. Each was tested with Python 3.13.18 on the worked examples. Edge cases were also tested: name clashes, empty and non-FASTA files, headers without a gene name or sequence, duplicate records and headers, CRLF and CR line endings, existing output files, unreadable annotation lines, coordinates outside the genome, genes crossing the origin on both strands, dry runs, and each IDLE mode.

| Script | Version | Date | Changes |
|---|---|---|---|
| mito_gene_extractor | 1.0–1.5 | 2026 (1.5: 2026-06-23) | 1.0 first version; 1.1 space before the gene name in the header; 1.2 header reduced to `>Species_ID Gene_Name`; 1.3 start decremented by 1 (later found wrong); 1.4 no line ending after the sequence; 1.5 BED starts used as they are, reverting 1.3. |
| mito_gene_extractor | 1.6.0 | 2026-11-24 | Reads the MITOS2 BED file directly as well as the simplified table. MITOS2 names converted to standard symbols, with split gene parts kept and reported. Genes crossing the origin joined across it. Files from an earlier run replaced (1.5 added `_2`, `_3` … to new names). Option for a final line ending; base name from the FASTA ID; warning for multi-sequence FASTA; summary by gene type. SETTINGS block, questions in the shell, command-line options, `run()`. |
| Concatenate_fasta_files | 1.0, 1.1 | 2026-07-18 | 1.0 first version; 1.1 no line ending after the final record. |
| Concatenate_fasta_files | 1.2.0 | 2026-11-24 | `.fa`, `.fas`, `.fna` accepted. Non-FASTA files skipped. Blank lines inside files removed. A bare output name saved in the input folder. Unix line endings. Option for a final line ending. Duplicate headers and a replaced output file reported. Dry run. SETTINGS block, questions in the shell, command-line options, `run()`. Errors no longer stop IDLE with a SystemExit. |
| ConvertTextToFasta | 1.0.0 | (undated) | First version: renames every `*.txt` in a folder to `*.fasta`; skips a file whose new name already exists. |
| ConvertTextToFasta | 1.1.0 | 2026-11-24 | Checks each file is FASTA before renaming. `.txt` matched in any capitalisation. Choice of new extension. Dry run. SETTINGS block, question in the shell, command-line options, `run()`. |
| split_major_fastas | 1.0.0 | (undated) | First version: splits every `*.fasta` in its own folder into `<label>/<label>_<gene>.fasta`; skips duplicates and records without a gene name or sequence. |
| split_major_fastas | 1.1.0 | 2026-11-24 | Input and output folders can be chosen (the default is still the script's own folder). `.fa`, `.fas`, `.fna` accepted. Stops if an output file would overwrite an input file. Reports files replaced from an earlier run. Dry run. SETTINGS block, optional questions, command-line options, `run()`. |
| trim_fasta_trailing_whitespace | 1.0 | 2026-07-18 | First version: removes all trailing whitespace from each `.fasta` file in a folder; files already clean are not rewritten. |
| trim_fasta_trailing_whitespace | 1.1.0 | 2026-11-24 | Option to keep exactly one final line ending, in the file's own style. `.fa`, `.fas`, `.fna` accepted. Optional sub-folders. Dry run. SETTINGS block, command-line options, `run()`. |

| Release | Date | Script versions |
|---|---|---|
| 1.0.0 | 2026-11-24 | mito_gene_extractor 1.6.0, Concatenate_fasta_files 1.2.0, ConvertTextToFasta 1.1.0, split_major_fastas 1.1.0, trim_fasta_trailing_whitespace 1.1.0 |

## License

Released under the MIT License; see [`LICENSE`](LICENSE).
