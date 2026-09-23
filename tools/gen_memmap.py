#!/usr/bin/env python3
"""Genera firmware/include/memory_map.h y docs/mapa_memoria.md desde memory_map.yml.

Uso:
  python3 tools/gen_memmap.py            # regenera los archivos
  python3 tools/gen_memmap.py --check    # falla si los generados no están al día
"""
import argparse
import sys
from pathlib import Path
import memmap

ROOT = memmap.ROOT
HDR = ROOT / "firmware" / "include" / "memory_map.h"
DOC = ROOT / "docs" / "mapa_memoria.md"
BANNER = "GENERADO por tools/gen_memmap.py desde interfaces/memory_map.yml. NO EDITAR."


def gen_header(m):
    L = ["/* " + BANNER + " */", "#ifndef MEMORY_MAP_H", "#define MEMORY_MAP_H", ""]
    for n, r in m["regions"].items():
        N = n.upper()
        L += [f"#define {N}_BASE  0x{r['origin']:08X}u", f"#define {N}_SIZE  0x{r['size']:08X}u"]
    L.append("")
    for p in m.get("peripherals", []):
        N = p["name"].upper()
        L += [f"/* {p['name']} (equipo: {p['owner']}) */",
              f"#define {N}_BASE  0x{p['base']:08X}u",
              f"#define {N}_SIZE  0x{p['size']:08X}u"]
        for r in p.get("registers", []):
            L.append(f"#define {N}_{r['name'].upper()}_OFFSET  0x{r['offset']:02X}u")
        L.append("")
    L += ["#endif /* MEMORY_MAP_H */", ""]
    return "\n".join(L)


def gen_doc(m):
    L = ["# Mapa de memoria", "",
         f"> {BANNER}", "",
         "## Regiones del SoC", "",
         "| Región | Origen | Tamaño | Descripción |", "|---|---|---|---|"]
    for n, r in m["regions"].items():
        L.append(f"| `{n}` | `0x{r['origin']:08X}` | `0x{r['size']:X}` | {r['desc']} |")
    w = m["periph_window"]
    L += ["", "## Ventana de periféricos del curso", "",
          f"Origen `0x{w['origin']:08X}`, tamaño `0x{w['size']:X}`. "
          "Cada periférico usa una ventana alineada a su tamaño.", "",
          "| Periférico | Base | Tamaño | Equipo | Puertos extra |", "|---|---|---|---|---|"]
    for p in m.get("peripherals", []):
        ports = ", ".join(f"`{q['name']}` ({q['dir']}, {q['width']}b → `{q['connect']}`)"
                          for q in p.get("ports", [])) or "—"
        L.append(f"| `{p['name']}` | `0x{p['base']:08X}` | `0x{p['size']:X}` | {p['owner']} | {ports} |")
    for p in m.get("peripherals", []):
        L += ["", f"### `{p['name']}`", "",
              "| Offset | Registro | Acceso | Descripción |", "|---|---|---|---|"]
        for r in p.get("registers", []):
            L.append(f"| `0x{r['offset']:02X}` | `{r['name']}` | {r['access']} | {r['desc']} |")
    L.append("")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    m = memmap.load()
    memmap.die_on_errors(m)
    outs = {HDR: gen_header(m), DOC: gen_doc(m)}
    bad = []
    for path, text in outs.items():
        if a.check:
            if not path.exists() or path.read_text(encoding="utf-8") != text:
                bad.append(path.relative_to(ROOT))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
            print("escrito", path.relative_to(ROOT))
    if bad:
        print("Desactualizados (ejecute tools/gen_memmap.py):", *map(str, bad), sep="\n  - ")
        sys.exit(1)
    if a.check:
        print("OK: archivos generados al día")


if __name__ == "__main__":
    main()
