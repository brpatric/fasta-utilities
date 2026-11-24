#!/usr/bin/env python3
r"""
mito_gene_extractor_v1.6.0_2026-11-24.py

Extracts one FASTA file per gene from a mitogenome FASTA file, using a MITOS2
annotation: either the MITOS2 BED file as downloaded, or a simplified table
(gene, start, end, strand). Minus-strand genes are reverse-complemented, and
genes that cross the origin of the circular genome are joined across it.

  Header   : >BaseName Gene          e.g.  >Pardosa_altamontis_Mt242 COX1
  File name: BaseName_Gene.fasta     e.g.  Pardosa_altamontis_Mt242_COX1.fasta

The gene files are meant as draft gene regions for alignment, from which
the final gene boundaries are decided.

COORDINATES
  Both input formats use the BED convention: the start is counted from 0 and
  the end is exclusive, so a gene at bases 1-65 is written 0  65. These map
  directly onto Python slicing (sequence[start:end]).

PROVENANCE
  Program    : mito_gene_extractor
  Version    : 1.6.0
  Date       : 2026-11-24
  Author     : L. Brian Patrick, Department of Biological Sciences,
               Dakota Wesleyan University, Mitchell, SD, USA
               ORCID 0000-0003-1969-9600
  Development: v1.0-v1.5 written by the author with the assistance of Claude
               (Anthropic), 2026. v1.6.0 drafted with the assistance of Claude
               Opus 5.5 (Anthropic), 2026-11-24, from specifications by the
               author, and reviewed by the author.
  Derived from: mito_gene_extractor_v1_5.py (v1.5, 2026-06-23).
  Tested with: Python 3.13.18, on the worked example in example/extract/
               (Alopecosa albostriata, GenBank PV694306.1, with its MITOS2
               draft annotation).
  Companion  : README_mito_gene_extractor_v1.6.0_2026-11-24.txt
               (README.md on GitHub)
  Version history
    1.0    2026       Initial release.
    1.1    2026       Header format: a space, not an underscore, before the
                      gene name.
    1.2    2026       Coordinates and strand removed from the header; header
                      is ">Species_ID Gene_Name".
    1.3    2026       Start coordinate decremented by 1 (later found wrong).
    1.4    2026       No line ending after the sequence, so concatenated files
                      have no blank lines between records.
    1.5    2026-06-23 Reverted the v1.3 change: MITOS BED starts are 0-based
                      and ends exclusive, so both are used as they are (v1.3
                      added one extra base at the start of every gene).
    1.6.0  2026-11-24 Reads the MITOS2 BED file directly (sequence ID, start,
                      end, name, score, strand) as well as the simplified
                      four-column table; MITOS2 names converted to standard
                      symbols (cox1 -> COX1, nad4l -> ND4L, cob -> CytB,
                      rrnL -> 16S, trnL1(tag) -> trnL1), with gene parts that
                      MITOS2 splits (nad5_0, rrnS_0-b) kept as separate files
                      and reported; genes crossing the origin joined across
                      it; files left from an earlier run replaced (v1.5 added
                      _2, _3 ... to the new file names), with duplicate names
                      within one run still numbered; option for a final line
                      ending; base name can be taken from the FASTA ID;
                      warning if the FASTA holds more than one sequence;
                      clearer summary by gene type; SETTINGS block for IDLE
                      (questions in the shell if it is left empty) and
                      command-line options; run() callable from the IDLE
                      shell.

HOW TO USE (IDLE 3.13)
  1. Open this file in IDLE.
  2. Edit the SETTINGS below (at least FASTA_FILE and ANNOTATION_FILE).
  3. Save, then press F5 (Run > Run Module).
  If FASTA_FILE is left as None, the program asks for the files instead.
  After one F5 run, run() can be called again from the IDLE shell prompt:
    >>> run(r"C:\data\Mt242.fasta", r"C:\data\Mt242.bed", base_name="Pardosa_altamontis_Mt242")

OPTIONAL: COMMAND LINE
  python3 mito_gene_extractor_v1.6.0_2026-11-24.py FASTA ANNOTATION
          [-o OUTPUT_DIR] [-b BASE_NAME | --base-from-fasta] [--keep-names]
          [--keep-newline]
  With no arguments, the SETTINGS below are used.

Only the Python standard library is needed.
"""

# =============================================================================
# SETTINGS  (edit these, save, then press F5 in IDLE)
# =============================================================================

FASTA_FILE         = None        # mitogenome FASTA, e.g. r"C:\data\Mt242.fasta"
                                 # None = ask for the files when the program runs
ANNOTATION_FILE    = None        # MITOS2 .bed file, or a table: gene start end strand
OUTPUT_DIR         = "mitogenes" # folder for the gene files (made if needed)
BASE_NAME          = None        # e.g. "Pardosa_altamontis_Mt242"; put before each
                                 # gene name. None = gene names only
BASE_FROM_FASTA    = False       # True = use the first word of the FASTA header
                                 # as the base name (when BASE_NAME is None)
STANDARD_NAMES     = True        # convert MITOS2 names (cox1, nad5_0, trnL1(tag))
                                 # to standard symbols (COX1, ND5_0, trnL1)
KEEP_FINAL_NEWLINE = False       # False = no line ending after the sequence (as v1.5)

# =============================================================================

import os
import re
import sys

PROGRAM = "mito_gene_extractor"
VERSION = "1.6.0"
DATE = "2026-11-24"

# MITOS2 name (lower case, before any _part suffix) -> standard symbol
STANDARD = {
    "cox1": "COX1", "cox2": "COX2", "cox3": "COX3",
    "atp6": "ATP6", "atp8": "ATP8", "cob": "CytB", "cytb": "CytB",
    "nad1": "ND1", "nad2": "ND2", "nad3": "ND3", "nad4": "ND4",
    "nad4l": "ND4L", "nad5": "ND5", "nad6": "ND6",
    "rrnl": "16S", "rrns": "12S",
    "oh": "OH", "ol": "OL",
}

COMPLEMENT = str.maketrans("ACGTRYSWKMBDHVNacgtryswkmbdhvn",
                           "TGCAYRSWMKVHDBNtgcayrswmkvhdbn")


def reverse_complement(seq):
    return seq.translate(COMPLEMENT)[::-1]


def read_fasta(path):
    """Return (ID, sequence, number of records) for the first record."""
    seq_id, parts, n = None, [], 0
    with open(path, encoding="utf-8-sig") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                n += 1
                if n == 1:
                    seq_id = line[1:].strip()
                continue
            if n == 1:
                parts.append(line)
    return seq_id, re.sub(r"\s", "", "".join(parts)).upper(), n


def standard_name(raw):
    """
    MITOS2 name -> standard symbol, keeping any part suffix:
    'cox1' -> 'COX1', 'nad5_0' -> 'ND5_0', 'rrnS_0-b' -> '12S_0-b',
    'trnL1(tag)' -> 'trnL1'. Names already standard are returned unchanged.
    """
    name = re.sub(r"\(.*?\)", "", raw).strip()
    m = re.match(r"^([A-Za-z0-9]+?)(_[\w\-]+)?$", name)
    if not m:
        return name
    base, suffix = m.group(1), m.group(2) or ""
    if base.lower() in STANDARD:
        return STANDARD[base.lower()] + suffix
    if base.lower().startswith("trn") and len(base) in (4, 5):
        return "trn" + base[3:]
    return name


def gene_type(name):
    n = name.lower()
    if n.startswith("trn"):
        return "tRNA"
    if n.startswith(("16s", "12s", "rrn")):
        return "rRNA"
    if n.startswith(("cox", "atp", "nd", "nad", "cytb", "cob")):
        return "protein-coding"
    if any(k in n for k in ("control", "d-loop", "dloop", "oh", "ol")):
        return "control/origin"
    return "other"


def parse_strand(text):
    t = text.strip().lower()
    if t in ("+", "plus", "forward", "f", "1", "+1"):
        return "+"
    if t in ("-", "minus", "reverse", "r", "-1"):
        return "-"
    return None


def read_annotations(path):
    """
    Read a MITOS2 BED file (seqid start end name score strand) or a simple
    table (gene start end strand). Return (list of dicts, format name, notes).
    """
    rows, notes, fmt = [], [], None
    with open(path, encoding="utf-8-sig") as fh:
        for n, line in enumerate(fh, 1):
            line = line.strip()
            if not line or line.startswith(("#", "track", "browser")):
                continue
            f = line.split("\t")
            if len(f) < 4:
                f = line.split()
            f = [x.strip() for x in f]

            def is_int(x):
                return re.fullmatch(r"-?\d+", x) is not None

            if len(f) >= 6 and is_int(f[1]) and is_int(f[2]) and parse_strand(f[5]):
                kind, name, start, end, strand = "MITOS2 BED", f[3], int(f[1]), int(f[2]), f[5]
            elif len(f) >= 4 and is_int(f[1]) and is_int(f[2]):
                kind, name, start, end, strand = "gene/start/end/strand table", f[0], int(f[1]), int(f[2]), f[3]
            else:
                notes.append("line {}: not a BED or gene/start/end/strand line; skipped".format(n))
                continue
            fmt = fmt or kind
            s = parse_strand(strand)
            if s is None:
                notes.append("line {} ({}): strand '{}' not understood; skipped".format(n, name, strand))
                continue
            rows.append({"line": n, "raw": name, "start": start, "end": end, "strand": s})
    return rows, fmt, notes


def extract(seq, start, end, strand):
    """BED-style 0-based start / exclusive end; start > end or end > length crosses the origin."""
    L = len(seq)
    if start > end:                       # written across the origin: start ... end
        piece = seq[start:] + seq[:end]
    elif end > L:                         # end past the last base: continue from base 1
        piece = seq[start:] + seq[:end - L]
    else:
        piece = seq[start:end]
    return reverse_complement(piece) if strand == "-" else piece


def run(fasta_file, annotation_file, output_dir="mitogenes", base_name=None,
        base_from_fasta=False, standard_names=True, keep_final_newline=False):
    r"""
    Write one FASTA file per annotated gene; return the number of files
    written. Can be called from the IDLE shell after one F5 run, e.g.
        >>> run(r"C:\data\Mt242.fasta", r"C:\data\Mt242.bed", base_name="Mt242")
    """
    print("{} v{} ({})".format(PROGRAM, VERSION, DATE))
    for p in (fasta_file, annotation_file):
        if not os.path.isfile(p):
            print("ERROR: file not found: {}".format(p))
            return 0

    seq_id, seq, n_rec = read_fasta(fasta_file)
    if not seq:
        print("ERROR: no sequence found in {}".format(fasta_file))
        return 0
    print("  FASTA      : {}".format(fasta_file))
    print("               {}  ({:,} bp)".format(seq_id, len(seq)))
    if n_rec > 1:
        print("  WARNING: the FASTA holds {} sequences; only the first is used.".format(n_rec))
    if base_name is None and base_from_fasta:
        base_name = seq_id.split()[0]
    if base_name and re.search(r"\s", base_name):
        print("ERROR: the base name '{}' contains spaces; use underscores.".format(base_name))
        return 0

    rows, fmt, notes = read_annotations(annotation_file)
    print("  Annotation : {}".format(annotation_file))
    print("               {} feature(s), read as a {}".format(len(rows), fmt or "?"))
    print("  Output     : {}{}".format(os.path.abspath(output_dir),
          "   (base name: {})".format(base_name) if base_name else ""))
    if not rows:
        print("ERROR: no usable annotation lines.")
        return 0

    os.makedirs(output_dir, exist_ok=True)
    used, counts, replaced, written, parts = {}, {}, 0, 0, []
    print()
    for r in rows:
        name = standard_name(r["raw"]) if standard_names else r["raw"]
        name = name.replace("/", "_").replace("\\", "_").replace(" ", "_")
        start, end, strand = r["start"], r["end"], r["strand"]
        L = len(seq)
        if start < 0 or start >= L or end < 0 or end > 2 * L or start == end:
            notes.append("line {} ({}): coordinates {}-{} do not fit a {} bp genome; "
                         "skipped".format(r["line"], r["raw"], start, end, L))
            continue
        gene_seq = extract(seq, start, end, strand)
        crosses = start > end or end > L

        stem = "{}_{}".format(base_name, name) if base_name else name
        used[stem] = used.get(stem, 0) + 1
        if used[stem] > 1:                       # same name twice in this run
            notes.append("{} appears {} times; this copy saved as {}_{}.fasta".format(
                name, used[stem], stem, used[stem]))
            stem = "{}_{}".format(stem, used[stem])
        if re.search(r"_\d+(-[ab])?$", name) and standard_names:
            parts.append(name)
        out = os.path.join(output_dir, stem + ".fasta")
        if os.path.exists(out):
            replaced += 1
        header = ">{} {}".format(base_name, name) if base_name else ">{}".format(name)
        with open(out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(header + "\n" + gene_seq + ("\n" if keep_final_newline else ""))
        written += 1
        t = gene_type(name)
        counts[t] = counts.get(t, 0) + 1
        label = name if name == r["raw"] else "{} ({})".format(name, r["raw"])
        print("  {:<24} {:>6} bp  {}  {}-{}{}  -> {}".format(
            label, len(gene_seq), strand, start, end,
            "  (crosses the origin)" if crosses else "", os.path.basename(out)))

    print("\n=== Summary ===")
    print("  Gene files written: {}".format(written))
    for t in ("protein-coding", "tRNA", "rRNA", "control/origin", "other"):
        if t in counts:
            print("    {:<15} {}".format(t, counts[t]))
    if replaced:
        print("  ({} replaced files from an earlier run)".format(replaced))
    if parts:
        notes.append("MITOS2 split these genes into parts, each saved as its own "
                     "file: {}. Check them, and merge or rename parts in an edited "
                     "annotation file if needed.".format(", ".join(parts)))
    if notes:
        print("\n  Notices ({}):".format(len(notes)))
        for w in notes:
            print("    - " + w)
    print("\nDone. Output folder: {}".format(os.path.abspath(output_dir)))
    return written


def _ask_file(prompt):
    while True:
        p = input(prompt).strip().strip('"').strip("'")
        if p and os.path.isfile(p):
            return p
        print("  File not found: {}".format(p) if p else "  Please enter a file path.")


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv:
        import argparse
        p = argparse.ArgumentParser(
            prog=os.path.basename(sys.argv[0]),
            description="Extract one FASTA file per gene from a mitogenome, using a "
                        "MITOS2 BED file or a gene/start/end/strand table "
                        "(0-based start, exclusive end).")
        p.add_argument("fasta_file", help="mitogenome FASTA")
        p.add_argument("annotation_file", help="MITOS2 .bed, or a gene/start/end/strand table")
        p.add_argument("-o", "--output-dir", "--output_dir", default="mitogenes",
                       help="output folder (default: mitogenes)")
        g = p.add_mutually_exclusive_group()
        g.add_argument("-b", "--base-name", "--base_name",
                       help='put before each gene name, e.g. "Pardosa_altamontis_Mt242"')
        g.add_argument("--base-from-fasta", action="store_true",
                       help="use the first word of the FASTA header as the base name")
        p.add_argument("--keep-names", action="store_true",
                       help="keep the gene names exactly as in the annotation file")
        p.add_argument("--keep-newline", action="store_true",
                       help="end each file with a line ending")
        p.add_argument("--version", action="version",
                       version="{} {} ({})".format(PROGRAM, VERSION, DATE))
        a = p.parse_args(argv)
        return run(a.fasta_file, a.annotation_file, a.output_dir, a.base_name,
                   a.base_from_fasta, not a.keep_names, a.keep_newline)

    if FASTA_FILE is None:
        print("{} v{} ({})  -- SETTINGS not filled in.".format(PROGRAM, VERSION, DATE))
        print("Coordinates follow the BED convention: 0-based start, exclusive end.\n")
        fasta = _ask_file("Mitogenome FASTA file: ")
        ann = _ask_file("MITOS2 .bed file or gene/start/end/strand table: ")
        out = input("Output folder (Enter = mitogenes): ").strip().strip('"') or "mitogenes"
        base = input("Base name before each gene name (Enter = gene names only): ").strip() or None
        return run(fasta, ann, out, base, False, STANDARD_NAMES, KEEP_FINAL_NEWLINE)
    return run(FASTA_FILE, ANNOTATION_FILE, OUTPUT_DIR, BASE_NAME, BASE_FROM_FASTA,
               STANDARD_NAMES, KEEP_FINAL_NEWLINE)


if __name__ == "__main__":
    main()
