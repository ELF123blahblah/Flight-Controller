#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys

def run_easyeda2kicad_from_file(input_file, output_dir="./lib/lcsc"):
    input_file = os.path.expanduser(input_file)
    output_dir = os.path.expanduser(output_dir)

    if not os.path.isfile(input_file):
        print(f"Error: Input file not found: {input_file}")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    with open(input_file, "r", encoding="utf-8") as f:
        # Ignore blank lines and comments
        lcsc_ids = [line.strip() for line in f if line.strip() and not line.lstrip().startswith("#")]

    if not lcsc_ids:
        print("No valid LCSC IDs found in file.")
        sys.exit(0)

    print(f"Processing {len(lcsc_ids)} LCSC parts...")

    for lcsc_id in lcsc_ids:
        print(f"\n→ Converting {lcsc_id} ...")
        cmd = [
            "easyeda2kicad",
            "--full",                # symbol + footprint + 3d
            "--lcsc_id", lcsc_id,
            "--output", output_dir,
            "--overwrite"            # optional: avoid manual confirmation
        ]
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error converting {lcsc_id}:")
            print(e.stderr)
            continue

    print("\nDone! Check your output folder:", output_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch convert LCSC parts to KiCad libs using easyeda2kicad")
    parser.add_argument("input_file", nargs="?", default="lcsc.txt",
                        help="Path to text file with LCSC IDs (one per line)")
    parser.add_argument("--output", default="./lib/lcsc",
                        help="Output directory for generated libs")

    args = parser.parse_args()

    run_easyeda2kicad_from_file(args.input_file, args.output)