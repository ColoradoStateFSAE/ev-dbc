import subprocess
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DBC_DIR = ROOT / "dbc"
SRC_DIR = ROOT / "src"

if SRC_DIR.exists():
    for item in SRC_DIR.iterdir():
        if item.name != "can_macros.h":
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()

SRC_DIR.mkdir(parents=True, exist_ok=True)

SRC_DIR.mkdir(parents=True, exist_ok=True)

dbc_files = sorted(DBC_DIR.glob("*.dbc"))
names = []

for dbc_file in dbc_files:
    name = dbc_file.stem
    names.append(name)

    output_dir = SRC_DIR / name
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate C source
    subprocess.run([
        "cantools", "generate_c_source",
        str(dbc_file), "--output-directory", str(output_dir)
    ], check=True)

    # Create lowercase aliases
    header = output_dir / f"{name}.h"
    aliases = output_dir / f"{name}_aliases.h"

    if header.exists():
        with open(aliases, "w") as out:
            out.write("#pragma once\n")
            out.write(f"#include \"{name}.h\"\n\n")

            for line in header.read_text().splitlines():
                if line.startswith("#define"):
                    parts = line.split(maxsplit=2)
                    if len(parts) >= 2:
                        out.write(f"#define {parts[1].lower()} {parts[1]}\n")

# Generate rrcan.h
rrcan_path = SRC_DIR / "rrevcan.h"

with open(rrcan_path, "w") as out:
    out.write("#pragma once\n\n")
    out.write("#include \"can_macros.h\"\n\n")

    for name in names:
        out.write(f"#include \"{name}/{name}.h\"\n")
        out.write(f"#include \"{name}/{name}_aliases.h\"\n\n")

print("rrevcan.h generated")
