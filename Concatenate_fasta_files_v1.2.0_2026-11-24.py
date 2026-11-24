#!/usr/bin/env python3
r"""
Concatenate_fasta_files_v1.2.0_2026-11-24.py

Combines all FASTA files in a folder into one multi-FASTA file, in
alphabetical order of file name. Each record keeps its header and sequence;
there are no blank lines between records and, by default, no line ending
after the last record.

Typical use: a folder holding the same gene from many specimens
(Species1_ATP6.fasta, Species2_ATP6.fasta, ...) becomes one file,
ATP6.fasta, ready for alignment.

PROVENANCE
  Program    : Concatenate_fasta_files
  Version    : 1.2.0
  Date       : 2026-11-24
  Author     : L. Brian Patrick, Department of Biological Sciences,
               Dakota Wesleyan University, Mitchell, SD, USA
               ORCID 0000-0003-1969-9600
  Development: v1.0 and v1.1 written for the author with the assistance of
               Claude (Anthropic), 2026-07-18. v1.2.0 drafted with the
               assistance of Claude Opus 5.5 (Anthropic), 2026-11-24, from
               specifications by the author, and reviewed by the author.
  Derived from: Concatenate_fasta_files_v1_1_2026_07_18.py (v1.1).
  Tested with: Python 3.13.18, on the worked example in example/ (Erigone
               atra, GenBank PP726906 and PP726907).
  Companion  : README_Concatenate_fasta_files_v1.2.0_2026-11-24.txt
               (README.md on GitHub)
  Version history
    1.0    2026-07-18  Initial release.
    1.1    2026-07-18  Fixed the line ending after the final record:
                       separators are written between records, not after
                       each one.
    1.2.0  2026-11-24  .fa, .fas and .fna accepted as well as .fasta; each
                       file checked to be FASTA (files that are not are
                       skipped with a message); blank lines inside files
                       removed; a bare output file name is now saved in the
                       input folder (a path is used as given); output always
                       has Unix (LF) line endings; option to end with one
                       line ending; duplicate headers reported; an existing
                       output file is reported as replaced; dry run to
                       preview; SETTINGS block for IDLE (questions in the
                       shell if it is left empty) and command-line options;
                       run() callable from the IDLE shell; errors no longer
                       stop IDLE with a SystemExit.

HOW TO USE (IDLE 3.13)
  1. Open this file in IDLE.
  2. Edit the SETTINGS below (INPUT_FOLDER and OUTPUT_FILE).
  3. Save, then press F5 (Run > Run Module).
  If INPUT_FOLDER or OUTPUT_FILE is left as None, the program asks instead.
  After one F5 run, run() can be called again from the IDLE shell prompt:
    >>> run(r"C:\data\ATP6_files", "ATP6.fasta")

OPTIONAL: COMMAND LINE
  python3 Concatenate_fasta_files_v1.2.0_2026-11-24.py INPUT_FOLDER OUTPUT_FILE
          [--keep-newline] [--no-check] [--dry-run]
  With no arguments, the SETTINGS below are used.

Only the Python standard library is needed.
"""

# =============================================================================
# SETTINGS  (edit these, save, then press F5 in IDLE)
# =============================================================================

INPUT_FOLDER       = None   # folder holding the FASTA files, e.g. r"C:\data\ATP6_files"
OUTPUT_FILE        = None   # e.g. "ATP6.fasta" (saved in INPUT_FOLDER) or a full path
                            # None = ask for either one when the program runs
KEEP_FINAL_NEWLINE = False  # False = no line ending after the last record (as v1.1)
CHECK_FASTA        = True   # skip files that do not look like FASTA
DRY_RUN            = False  # True = report what would be written, write nothing

# =============================================================================

import os
import sys

PROGRAM = "Concatenate_fasta_files"
VERSION = "1.2.0"
DATE = "2026-11-24"

FASTA_EXTENSIONS = (".fasta", ".fa", ".fas", ".fna")


def read_fasta_lines(path):
    """Non-blank lines of a file, stripped, with any line-ending style."""
    with open(path, "r", encoding="utf-8-sig", newline=None) as fh:
        return [line.strip() for line in fh if line.strip()]


def run(input_folder, output_file, keep_final_newline=False, check_fasta=True,
        dry_run=False):
    r"""
    Concatenate the FASTA files in input_folder into output_file; return the
    number of records written. Can be called from the IDLE shell after one F5
    run, e.g.
        >>> run(r"C:\data\ATP6_files", "ATP6.fasta")
    """
    print("{} v{} ({})".format(PROGRAM, VERSION, DATE))
    if not os.path.isdir(input_folder):
        print("ERROR: '{}' is not a valid folder.".format(input_folder))
        return 0
    if not os.path.dirname(output_file):          # bare name -> input folder
        output_file = os.path.join(input_folder, output_file)
    if not output_file.lower().endswith(FASTA_EXTENSIONS):
        print("  NOTE: the output name does not end in .fasta/.fa/.fas/.fna, so a "
              "later run would not recognise it as FASTA.")
    out_abs = os.path.abspath(output_file)
    print("  input  : {}".format(os.path.abspath(input_folder)))
    print("  output : {}".format(out_abs))
    if dry_run:
        print("  DRY RUN: nothing will be written.")

    files = sorted(f for f in os.listdir(input_folder)
                   if f.lower().endswith(FASTA_EXTENSIONS)
                   and os.path.isfile(os.path.join(input_folder, f))
                   and os.path.abspath(os.path.join(input_folder, f)) != out_abs)
    if not files:
        print("ERROR: no FASTA files (.fasta, .fa, .fas, .fna) found.")
        return 0
    print("\n  Found {} FASTA file(s) to concatenate:".format(len(files)))

    blocks, n_records, headers, notices = [], 0, {}, []
    for name in files:
        lines = read_fasta_lines(os.path.join(input_folder, name))
        if not lines:
            notices.append("{} is empty; skipped.".format(name))
            print("    - {}  (empty, skipped)".format(name))
            continue
        if check_fasta and not lines[0].startswith(">"):
            notices.append("{} does not start with a '>' header; skipped "
                           "(not FASTA).".format(name))
            print("    - {}  (not FASTA, skipped)".format(name))
            continue
        recs = [l for l in lines if l.startswith(">")]
        for h in recs:
            if h in headers:
                notices.append("header {} appears in both {} and {}".format(
                    h, headers[h], name))
            else:
                headers[h] = name
        n_records += len(recs)
        blocks.append("\n".join(lines))
        print("    - {}  ({} record{})".format(name, len(recs), "" if len(recs) == 1 else "s"))

    if not blocks:
        print("ERROR: no usable FASTA files. Nothing written.")
        return 0

    combined = "\n".join(blocks) + ("\n" if keep_final_newline else "")
    replaced = os.path.exists(output_file)
    if not dry_run:
        out_dir = os.path.dirname(out_abs)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        with open(output_file, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(combined)

    if notices:
        print("\n  Notices ({}):".format(len(notices)))
        for w in notices:
            print("    - " + w)
    print("\n{} {} record(s) from {} file(s) to {}{}.".format(
        "Would write" if dry_run else "Wrote", n_records, len(blocks),
        os.path.basename(output_file),
        " (replacing the existing file)" if replaced else ""))
    return n_records


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv:
        import argparse
        p = argparse.ArgumentParser(
            prog=os.path.basename(sys.argv[0]),
            description="Concatenate all FASTA files in a folder into one FASTA file.")
        p.add_argument("input_folder", help="folder holding the FASTA files")
        p.add_argument("output_file",
                       help="output file; a bare name is saved in the input folder")
        p.add_argument("--keep-newline", action="store_true",
                       help="end the output with one line ending")
        p.add_argument("--no-check", action="store_true",
                       help="include files without checking they start with '>'")
        p.add_argument("--dry-run", action="store_true",
                       help="report what would be written; write nothing")
        p.add_argument("--version", action="version",
                       version="{} {} ({})".format(PROGRAM, VERSION, DATE))
        a = p.parse_args(argv)
        return run(a.input_folder, a.output_file, a.keep_newline,
                   not a.no_check, a.dry_run)

    inp, out = INPUT_FOLDER, OUTPUT_FILE
    if inp is None or out is None:
        print("{} v{} ({})  -- SETTINGS not filled in.".format(PROGRAM, VERSION, DATE))
    if inp is None:
        inp = input("Folder holding the FASTA files: ").strip().strip('"').strip("'")
    if out is None:
        out = input("Output file name (e.g. ATP6.fasta): ").strip().strip('"').strip("'")
    if not inp or not out:
        print("ERROR: both the folder and the output file name are needed.")
        return 0
    return run(inp, out, KEEP_FINAL_NEWLINE, CHECK_FASTA, DRY_RUN)


if __name__ == "__main__":
    main()
