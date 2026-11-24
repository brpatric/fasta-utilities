#!/usr/bin/env python3
r"""
split_major_fastas_v1.1.0_2026-11-24.py

Splits "major" FASTA files (one file per gene, each holding one record per
specimen) into individual per-gene FASTA files, organised into one folder
per specimen.

  Input : COX1.fasta holding  >Erigone_atra_male COX1
                              >Erigone_atra_female COX1   ...
  Output: Erigone_atra_male/Erigone_atra_male_COX1.fasta
          Erigone_atra_female/Erigone_atra_female_COX1.fasta   ...

Each header must have two words: the specimen label (Genus_species_identifier,
no spaces) and the gene name, e.g.  >Geolycosa_sp_Africa ATP8

PROVENANCE
  Program    : split_major_fastas
  Version    : 1.1.0
  Date       : 2026-11-24
  Author     : L. Brian Patrick, Department of Biological Sciences,
               Dakota Wesleyan University, Mitchell, SD, USA
               ORCID 0000-0003-1969-9600
  Development: v1.0.0 written by the author with the assistance of Claude
               (Anthropic). v1.1.0 drafted with the assistance of Claude
               Opus 5.5 (Anthropic), 2026-11-24, from specifications by the
               author, and reviewed by the author.
  Derived from: split_major_fastas.py (v1.0.0, the author's original script).
  Tested with: Python 3.13.18, on the worked example in example/ (Erigone
               atra, GenBank PP726906 and PP726907).
  Companion  : README_split_major_fastas_v1.1.0_2026-11-24.txt
               (README.md on GitHub)
  Version history
    1.0.0  (undated)   Original script: reads every *.fasta in the folder the
                       script is saved in and writes <label>/<label>_<gene>.fasta
                       beside them; skips duplicates and records without a
                       gene name or sequence.
    1.1.0  2026-11-24  Input and output folders can be chosen (the default is
                       still the script's own folder); .fasta, .fa, .fas and
                       .fna accepted in any capitalisation; the run stops if
                       an output file name would clash with an input file;
                       files left from an earlier run are reported as
                       overwritten; dry run to preview; SETTINGS block for
                       IDLE (questions in the shell if asked for) and
                       command-line options; run() callable from the IDLE
                       shell.

HOW TO USE (IDLE 3.13)
  Simplest (as in v1.0.0): put this file in the folder with your major FASTA
  files, open it in IDLE and press F5.
  Otherwise, edit the SETTINGS below, save, and press F5. With
  ASK_FOR_FOLDERS = True the program asks for the folders in the shell.
  After one F5 run, run() can be called again from the IDLE shell prompt:
    >>> run(r"C:\data\major_fastas", output_folder=r"C:\data\by_specimen")

OPTIONAL: COMMAND LINE
  python3 split_major_fastas_v1.1.0_2026-11-24.py [INPUT_FOLDER]
          [--out OUTPUT_FOLDER] [--dry-run]
  With no arguments, the SETTINGS below are used.

Only the Python standard library is needed.
"""

# =============================================================================
# SETTINGS  (edit these, save, then press F5 in IDLE)
# =============================================================================

INPUT_FOLDER    = None    # folder holding the major FASTA files
                          # None = the folder this script is saved in
OUTPUT_FOLDER   = None    # where the specimen folders are made
                          # None = the same as INPUT_FOLDER
ASK_FOR_FOLDERS = False   # True = ask for both folders in the shell
DRY_RUN         = False   # True = list what would be written, write nothing

# =============================================================================

import os
import sys

PROGRAM = "split_major_fastas"
VERSION = "1.1.0"
DATE = "2026-11-24"

FASTA_EXTENSIONS = (".fasta", ".fa", ".fas", ".fna")

# Prefer the folder this script is saved in. If the code is instead pasted
# straight into the IDLE shell (no __file__), fall back to the current folder.
try:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    SCRIPT_DIR = os.getcwd()


def safe_name(text):
    """Guard against characters that are not allowed in folder/file names."""
    for ch in '/\\:*?"<>|':
        text = text.replace(ch, "_")
    return text


def read_records(path):
    """
    Read one major FASTA file and return a list of (header, [seq_lines]).
    Handles Windows (CRLF) and old Mac (CR) line endings, blank lines, and
    sequences wrapped across several lines.
    """
    records, header, seq_lines = [], None, []
    with open(path, "r", encoding="utf-8-sig", newline=None) as fh:
        for raw in fh:
            line = raw.strip()
            if not line:
                continue
            if line.startswith(">"):
                if header is not None:
                    records.append((header, seq_lines))
                header, seq_lines = line, []
            else:
                seq_lines.append(line)
        if header is not None:
            records.append((header, seq_lines))
    return records


def parse_header(header):
    """'>Geolycosa_sp_Africa ATP8' -> ('Geolycosa_sp_Africa', 'ATP8'); (None, None) if not two words."""
    tokens = header[1:].split()
    if len(tokens) < 2:
        return None, None
    return tokens[0], tokens[1]


def run(input_folder=None, output_folder=None, dry_run=False):
    r"""
    Split every major FASTA file in input_folder; return the number of gene
    files written. Can be called from the IDLE shell after one F5 run, e.g.
        >>> run(r"C:\data\major_fastas", output_folder=r"C:\data\by_specimen")
    """
    print("{} v{} ({})".format(PROGRAM, VERSION, DATE))
    input_folder = os.path.abspath(input_folder or SCRIPT_DIR)
    output_folder = os.path.abspath(output_folder or input_folder)
    print("  input  : {}".format(input_folder))
    print("  output : {}".format(output_folder))
    if dry_run:
        print("  DRY RUN: nothing will be written.")
    if not os.path.isdir(input_folder):
        print("ERROR: input folder not found.")
        return 0

    major_files = sorted(
        os.path.join(input_folder, f) for f in os.listdir(input_folder)
        if f.lower().endswith(FASTA_EXTENSIONS)
        and os.path.isfile(os.path.join(input_folder, f)))
    if not major_files:
        print("  No FASTA files (.fasta, .fa, .fas, .fna) found. Nothing to do.")
        return 0

    # Read everything and plan the output first, so nothing is written if a
    # problem would stop the run part-way.
    written = {}            # (label, gene) -> source file name
    plan = []               # (out_path, label, gene, seq_lines)
    notices = []
    for path in major_files:
        fname = os.path.basename(path)
        for header, seq_lines in read_records(path):
            label, gene = parse_header(header)
            if label is None:
                notices.append("{}: skipped a header without a gene name -> {!r}"
                               .format(fname, header))
                continue
            if not seq_lines:
                notices.append("{}: '{}' has no sequence; skipped.".format(fname, header))
                continue
            label, gene = safe_name(label), safe_name(gene)
            key = (label, gene)
            if key in written:
                notices.append("Duplicate {} for '{}' (already taken from {}); kept "
                               "the first, skipped the copy in {}.".format(
                                   gene, label, written[key], fname))
                continue
            written[key] = fname
            out_path = os.path.join(output_folder, label,
                                    "{}_{}.fasta".format(label, gene))
            plan.append((out_path, label, gene, seq_lines))

    clashes = [p for p, *_ in plan if os.path.abspath(p) in map(os.path.abspath, major_files)]
    if clashes:
        print("ERROR: these output files would overwrite input files: {}. "
              "Choose a different OUTPUT_FOLDER.".format(", ".join(clashes)))
        return 0

    overwritten = 0
    for out_path, label, gene, seq_lines in plan:
        if os.path.exists(out_path):
            overwritten += 1
        if dry_run:
            continue
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8", newline="\n") as out:
            out.write(">{} {}\n".format(label, gene))
            for s in seq_lines:
                out.write(s + "\n")

    labels = sorted({lbl for _, lbl, _, _ in plan})
    verb = "would be written" if dry_run else "written"
    print("\n  Major FASTA files read : {}".format(len(major_files)))
    print("  Specimen folders       : {}".format(len(labels)))
    print("  Gene files {}{}: {}".format(verb, " " * max(0, 12 - len(verb)), len(plan)))
    if overwritten:
        print("  ({} of them {} files from an earlier run)".format(
            overwritten, "would replace" if dry_run else "replaced"))
    if labels:
        print("\n  Specimen folders:")
        for lbl in labels:
            n = sum(1 for _, l, _, _ in plan if l == lbl)
            print("    {}/  ({} gene{})".format(lbl, n, "" if n == 1 else "s"))
    if notices:
        print("\n  Notices ({}):".format(len(notices)))
        for w in notices:
            print("    - " + w)
    print("\nDone.")
    return len(plan)


def _ask(prompt, default):
    ans = input(prompt).strip().strip('"').strip("'")
    return ans or default


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv:
        import argparse
        p = argparse.ArgumentParser(
            prog=os.path.basename(sys.argv[0]),
            description="Split major FASTA files (one per gene, one record per "
                        "specimen) into per-gene files, one folder per specimen.")
        p.add_argument("input_folder", nargs="?",
                       help="folder holding the major FASTA files (default: this script's folder)")
        p.add_argument("--out", help="output folder (default: the input folder)")
        p.add_argument("--dry-run", action="store_true",
                       help="list what would be written; write nothing")
        p.add_argument("--version", action="version",
                       version="{} {} ({})".format(PROGRAM, VERSION, DATE))
        a = p.parse_args(argv)
        return run(a.input_folder, a.out, a.dry_run)

    inp, out = INPUT_FOLDER, OUTPUT_FOLDER
    if ASK_FOR_FOLDERS:
        inp = _ask("Folder holding the major FASTA files (Enter = {}): ".format(
            inp or SCRIPT_DIR), inp)
        out = _ask("Output folder (Enter = same as input): ", out)
    return run(inp, out, DRY_RUN)


if __name__ == "__main__":
    main()
