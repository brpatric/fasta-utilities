#!/usr/bin/env python3
r"""
ConvertTextToFasta_v1.1.0_2026-11-24.py

Renames FASTA files saved with a .txt extension so that they end in .fasta
(or another FASTA extension). Only the file name changes; the contents are
not touched. Before renaming, each file is checked to be FASTA, so notes or
other text files in the same folder are left alone.

PROVENANCE
  Program    : ConvertTextToFasta
  Version    : 1.1.0
  Date       : 2026-11-24
  Author     : L. Brian Patrick, Department of Biological Sciences,
               Dakota Wesleyan University, Mitchell, SD, USA
               ORCID 0000-0003-1969-9600
  Development: v1.0.0 written by the author with the assistance of Claude
               (Anthropic). v1.1.0 drafted with the assistance of Claude
               Opus 5.5 (Anthropic), 2026-11-24, from specifications by the
               author, and reviewed by the author.
  Derived from: ConvertTextToFasta.py (v1.0.0, the author's original script).
  Tested with: Python 3.13.18, on the worked example in example/ (Erigone
               atra, GenBank PP726906 and PP726907).
  Companion  : README_ConvertTextToFasta_v1.1.0_2026-11-24.txt
               (README.md on GitHub)
  Version history
    1.0.0  (undated)   Original script: renames every *.txt in a folder to
                       *.fasta; skips a file whose .fasta name already exists.
    1.1.0  2026-11-24  Each file is checked to be FASTA before it is renamed
                       (first line starts with '>', the rest are sequence
                       lines); non-FASTA files are skipped with a message.
                       .txt matched in any capitalisation (.TXT); choice of
                       new extension (.fasta, .fa, .fas, .fna); dry run to
                       preview; SETTINGS block for IDLE (questions in the
                       shell if it is left empty) and command-line options;
                       run() callable from the IDLE shell; summary counts.

HOW TO USE (IDLE 3.13)
  1. Open this file in IDLE.
  2. Edit the SETTINGS below (at least FOLDER).
  3. Save, then press F5 (Run > Run Module).
  If FOLDER is left as None, the program asks for the folder instead.
  After one F5 run, run() can be called again from the IDLE shell prompt:
    >>> run(r"C:\data\genes", dry_run=True)

OPTIONAL: COMMAND LINE
  python3 ConvertTextToFasta_v1.1.0_2026-11-24.py FOLDER [--ext .fasta]
          [--no-check] [--dry-run]
  With no arguments, the SETTINGS below are used.

Only the Python standard library is needed.
"""

# =============================================================================
# SETTINGS  (edit these, save, then press F5 in IDLE)
# =============================================================================

FOLDER        = None      # folder holding the .txt files, e.g. r"C:\data\genes"
                          # None = ask for the folder when the program runs
NEW_EXTENSION = ".fasta"  # .fasta, .fa, .fas or .fna
CHECK_FASTA   = True      # rename only files whose contents look like FASTA
DRY_RUN       = False     # True = list what would be renamed, change nothing

# =============================================================================

import os
import re
import sys

PROGRAM = "ConvertTextToFasta"
VERSION = "1.1.0"
DATE = "2026-11-24"

ALLOWED_EXTENSIONS = (".fasta", ".fa", ".fas", ".fna")

# IUPAC nucleotide and amino-acid letters, gaps (-, .) and stop (*)
SEQUENCE_LINE = re.compile(r"^[A-Za-z\-\.\*]+$")


def looks_like_fasta(path, max_lines=2000):
    """
    Return (True, '') if the file looks like FASTA, otherwise (False, reason).
    The first non-blank line must start with '>', and every other non-blank
    line (up to max_lines) must be a header or a line of sequence letters.
    """
    try:
        with open(path, "r", encoding="utf-8-sig", errors="replace") as fh:
            first = None
            n_seq = 0
            for n, raw in enumerate(fh):
                line = raw.strip()
                if not line:
                    continue
                if first is None:
                    first = line
                    if not line.startswith(">"):
                        return False, "first line does not start with '>'"
                    continue
                if line.startswith(">"):
                    continue
                if not SEQUENCE_LINE.match(line.replace(" ", "")):
                    return False, "line {} is not sequence: {!r}".format(
                        n + 1, line[:40])
                n_seq += 1
                if n >= max_lines:
                    break
    except OSError as e:
        return False, "could not be read ({})".format(e)
    if first is None:
        return False, "file is empty"
    if n_seq == 0:
        return False, "no sequence lines after the header"
    return True, ""


def run(folder, new_extension=".fasta", check_fasta=True, dry_run=False):
    r"""
    Rename the .txt files in folder; return the number renamed. Can be called
    from the IDLE shell after one F5 run, e.g.
        >>> run(r"C:\data\genes", dry_run=True)
    """
    print("{} v{} ({})".format(PROGRAM, VERSION, DATE))
    new_extension = new_extension if new_extension.startswith(".") else "." + new_extension
    if new_extension.lower() not in ALLOWED_EXTENSIONS:
        print("ERROR: the new extension must be one of {}.".format(
            ", ".join(ALLOWED_EXTENSIONS)))
        return 0
    if not os.path.isdir(folder):
        print("ERROR: folder not found: {}".format(folder))
        return 0

    txt_files = sorted(f for f in os.listdir(folder)
                       if f.lower().endswith(".txt")
                       and os.path.isfile(os.path.join(folder, f)))
    print("  folder : {}".format(os.path.abspath(folder)))
    if dry_run:
        print("  DRY RUN: nothing will be renamed.")
    if not txt_files:
        print("  No .txt files found.")
        return 0
    print("  Found {} .txt file(s).\n".format(len(txt_files)))

    renamed = skipped_exists = skipped_not_fasta = errors = 0
    for name in txt_files:
        old_path = os.path.join(folder, name)
        new_name = name[:-4] + new_extension
        new_path = os.path.join(folder, new_name)

        if os.path.exists(new_path):
            print("  [SKIPPED] {}: {} already exists".format(name, new_name))
            skipped_exists += 1
            continue
        if check_fasta:
            ok, reason = looks_like_fasta(old_path)
            if not ok:
                print("  [SKIPPED] {}: not FASTA ({})".format(name, reason))
                skipped_not_fasta += 1
                continue
        if dry_run:
            print("  [WOULD RENAME] {} -> {}".format(name, new_name))
            renamed += 1
            continue
        try:
            os.rename(old_path, new_path)
            print("  [RENAMED] {} -> {}".format(name, new_name))
            renamed += 1
        except OSError as e:
            print("  [ERROR]   {}: {}".format(name, e))
            errors += 1

    print("\nSummary: {} {}, {} skipped (name already used), {} skipped "
          "(not FASTA), {} error(s).".format(
              renamed, "would be renamed" if dry_run else "renamed",
              skipped_exists, skipped_not_fasta, errors))
    return renamed


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv:
        import argparse
        p = argparse.ArgumentParser(
            prog=os.path.basename(sys.argv[0]),
            description="Rename FASTA files saved as .txt to a FASTA extension "
                        "(the contents are not changed).")
        p.add_argument("folder", help="folder holding the .txt files")
        p.add_argument("--ext", default=".fasta",
                       help="new extension: .fasta (default), .fa, .fas or .fna")
        p.add_argument("--no-check", action="store_true",
                       help="rename every .txt file without checking it is FASTA")
        p.add_argument("--dry-run", action="store_true",
                       help="list what would be renamed; change nothing")
        p.add_argument("--version", action="version",
                       version="{} {} ({})".format(PROGRAM, VERSION, DATE))
        a = p.parse_args(argv)
        return run(a.folder, a.ext, not a.no_check, a.dry_run)

    folder = FOLDER
    if folder is None:
        print("{} v{} ({})  -- SETTINGS not filled in.".format(PROGRAM, VERSION, DATE))
        folder = input("Folder holding the .txt files (Enter = current folder): ")
        folder = folder.strip().strip('"').strip("'") or "."
    return run(folder, NEW_EXTENSION, CHECK_FASTA, DRY_RUN)


if __name__ == "__main__":
    main()
