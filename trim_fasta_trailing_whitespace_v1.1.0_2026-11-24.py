#!/usr/bin/env python3
r"""
trim_fasta_trailing_whitespace_v1.1.0_2026-11-24.py

Removes trailing whitespace (blank lines, spaces, tabs, carriage returns and
line feeds) from the end of each FASTA file in a folder. Files that already
end cleanly are left untouched (not rewritten). By default the last line is
left with no line ending at all; KEEP_FINAL_NEWLINE leaves exactly one.

PROVENANCE
  Program    : trim_fasta_trailing_whitespace
  Version    : 1.1.0
  Date       : 2026-11-24
  Author     : L. Brian Patrick, Department of Biological Sciences,
               Dakota Wesleyan University, Mitchell, SD, USA
               ORCID 0000-0003-1969-9600
  Development: v1.0 prepared for the author with the assistance of Claude
               (Anthropic), 2026-07-18. v1.1.0 drafted with the assistance of
               Claude Opus 5.5 (Anthropic), 2026-11-24, from specifications by
               the author, and reviewed by the author.
  Derived from: trim_fasta_trailing_whitespace.py (v1.0, 2026-07-18).
  Tested with: Python 3.13.18, on the worked example in example/ (Erigone
               atra, GenBank PP726906 and PP726907).
  Companion  : README_trim_fasta_trailing_whitespace_v1.1.0_2026-11-24.txt
               (README.md on GitHub)
  Version history
    1.0    2026-07-18  Initial release. Top-level folder only; case-insensitive
                       .fasta matching; binary read/write to keep the bytes
                       exactly; files already clean are not rewritten;
                       per-file status and summary.
    1.1.0  2026-11-24  Option to keep exactly one final line ending (in the
                       file's own style, LF or CRLF); .fa, .fas and .fna
                       accepted as well as .fasta; optional search of
                       sub-folders; dry run to preview; SETTINGS block for
                       IDLE (questions in the shell if it is left empty) and
                       command-line options; run() callable from the IDLE
                       shell. Only the end of each file is changed, as before.

HOW TO USE (IDLE 3.13)
  1. Open this file in IDLE.
  2. Edit the SETTINGS below (at least FOLDER).
  3. Save, then press F5 (Run > Run Module).
  If FOLDER is left as None, the program asks for the folder instead.
  After one F5 run, run() can be called again from the IDLE shell prompt:
    >>> run(r"C:\data\genes", keep_final_newline=True)

OPTIONAL: COMMAND LINE
  python3 trim_fasta_trailing_whitespace_v1.1.0_2026-11-24.py FOLDER
          [--keep-newline] [--recursive] [--dry-run]
  With no arguments, the SETTINGS below are used.

Only the Python standard library is needed.
"""

# =============================================================================
# SETTINGS  (edit these, save, then press F5 in IDLE)
# =============================================================================

FOLDER             = None   # folder holding the FASTA files, e.g. r"C:\data\genes"
                            # None = ask for the folder when the program runs
KEEP_FINAL_NEWLINE = False  # False = no line ending after the last line (as v1.0)
                            # True  = exactly one line ending after the last line
RECURSIVE          = False  # True = also process FASTA files in sub-folders
DRY_RUN            = False  # True = report what would change, change nothing

# =============================================================================

import os
import sys

PROGRAM = "trim_fasta_trailing_whitespace"
VERSION = "1.1.0"
DATE = "2026-11-24"

FASTA_EXTENSIONS = (".fasta", ".fa", ".fas", ".fna")


def find_fasta_files(folder, recursive=False):
    if not recursive:
        return sorted(os.path.join(folder, f) for f in os.listdir(folder)
                      if os.path.isfile(os.path.join(folder, f))
                      and f.lower().endswith(FASTA_EXTENSIONS))
    found = []
    for root, dirs, files in os.walk(folder):
        dirs.sort()
        found += [os.path.join(root, f) for f in sorted(files)
                  if f.lower().endswith(FASTA_EXTENSIONS)]
    return found


def trimmed_bytes(content, keep_final_newline=False):
    """
    Return the file content with trailing whitespace removed. With
    keep_final_newline, end with one line ending in the file's own style.
    """
    body = content.rstrip()          # bytes.rstrip(): space, \t, \n, \r, \v, \f
    if keep_final_newline and body:
        body += b"\r\n" if b"\r\n" in content else b"\n"
    return body


def run(folder, keep_final_newline=False, recursive=False, dry_run=False):
    r"""
    Trim the FASTA files in folder; return the number of files changed. Can be
    called from the IDLE shell after one F5 run, e.g.
        >>> run(r"C:\data\genes", keep_final_newline=True)
    """
    print("{} v{} ({})".format(PROGRAM, VERSION, DATE))
    if not os.path.isdir(folder):
        print("ERROR: '{}' is not a valid folder.".format(folder))
        return 0
    files = find_fasta_files(folder, recursive)
    print("  folder : {}{}".format(os.path.abspath(folder),
                                   "  (and sub-folders)" if recursive else ""))
    print("  ending : {}".format("one final line ending" if keep_final_newline
                                 else "no final line ending"))
    if dry_run:
        print("  DRY RUN: nothing will be changed.")
    if not files:
        print("  No FASTA files (.fasta, .fa, .fas, .fna) found.")
        return 0
    print("  Found {} FASTA file(s).\n".format(len(files)))

    modified = unchanged = errors = 0
    for path in files:
        name = os.path.relpath(path, folder)
        try:
            with open(path, "rb") as fh:
                content = fh.read()
        except OSError as e:
            print("  [SKIPPED]  {} - could not read: {}".format(name, e))
            errors += 1
            continue
        new = trimmed_bytes(content, keep_final_newline)
        if new == content:
            print("  [OK]       {} - already clean, unchanged.".format(name))
            unchanged += 1
            continue
        change = len(content) - len(new)
        what = ("removed {} trailing byte(s)".format(change) if change > 0
                else "added a final line ending")
        if dry_run:
            print("  [WOULD FIX] {} - {}.".format(name, what))
            modified += 1
            continue
        try:
            with open(path, "wb") as fh:
                fh.write(new)
            print("  [MODIFIED] {} - {}.".format(name, what))
            modified += 1
        except OSError as e:
            print("  [ERROR]    {} - could not write: {}".format(name, e))
            errors += 1

    print("\nSummary: {} {}, {} unchanged, {} error(s).".format(
        modified, "would be modified" if dry_run else "modified", unchanged, errors))
    return modified


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv:
        import argparse
        p = argparse.ArgumentParser(
            prog=os.path.basename(sys.argv[0]),
            description="Remove trailing whitespace from the end of FASTA files.")
        p.add_argument("folder", help="folder holding the FASTA files")
        p.add_argument("--keep-newline", action="store_true",
                       help="leave exactly one line ending after the last line")
        p.add_argument("--recursive", action="store_true",
                       help="also process FASTA files in sub-folders")
        p.add_argument("--dry-run", action="store_true",
                       help="report what would change; change nothing")
        p.add_argument("--version", action="version",
                       version="{} {} ({})".format(PROGRAM, VERSION, DATE))
        a = p.parse_args(argv)
        return run(a.folder, a.keep_newline, a.recursive, a.dry_run)

    folder = FOLDER
    if folder is None:
        print("{} v{} ({})  -- SETTINGS not filled in.".format(PROGRAM, VERSION, DATE))
        folder = input("Enter the path to the folder containing the FASTA files: ")
        folder = folder.strip().strip('"').strip("'")
    return run(folder, KEEP_FINAL_NEWLINE, RECURSIVE, DRY_RUN)


if __name__ == "__main__":
    main()
