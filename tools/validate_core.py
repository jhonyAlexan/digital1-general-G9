#!/usr/bin/env python3
"""Valida la estructura, la interfaz y la simulación de uno o más periféricos.

  python3 tools/validate_core.py cores/uart              # un core
  python3 tools/validate_core.py --all                   # todos (cores/ y template/cores/)
  python3 tools/validate_core.py cores/uart --registered # exige estar en memory_map.yml
  python3 tools/validate_core.py --all --no-sim          # solo estructura

Comprueba:
  1. Estructura: diagramas/, rtl/{Makefile,módulo,TB,gtkw}, firmware/{.c,.h}
  2. Interfaz estándar en la cabecera del módulo (clk, rst, d_in, cs, addr, rd, wr, d_out)
  3. Simulación: `make sim` termina con PASS y sin FAIL/ERROR (requiere iverilog)
  4. (--registered) el core está declarado en interfaces/memory_map.yml
"""
import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

import memmap

ROOT = memmap.ROOT
STD_PORTS = ["clk", "rst", "d_in", "cs", "addr", "rd", "wr", "d_out"]


def check_core(core: Path, sim=True, registered=False, require_sim=False):
    errs, warns = [], []
    rtl, fw, dg = core / "rtl", core / "firmware", core / "diagramas"

    for d in (dg, rtl, fw):
        if not d.is_dir():
            errs.append(f"falta el directorio {d.relative_to(core)}/")
    if errs:
        return errs, warns

    if not any(dg.iterdir()):
        errs.append("diagramas/ está vacío")
    if not (rtl / "Makefile").is_file():
        errs.append("falta rtl/Makefile")
    mods = [f for f in rtl.glob("*.v") if not f.stem.endswith("_TB")]
    tbs = list(rtl.glob("*_TB.v"))
    if len(mods) != 1:
        errs.append(f"se esperaba 1 módulo RTL (*.v sin _TB) en rtl/, hay {len(mods)}")
    if not tbs:
        errs.append("falta el testbench rtl/<modulo>_TB.v")
    if not (list(rtl.glob("*_TB.gtkw")) or list(rtl.glob("*_sim.gtkw"))):
        errs.append("falta el archivo GTKWave (*_TB.gtkw o *_sim.gtkw)")
    if not list(fw.glob("*.c")) or not list(fw.glob("*.h")):
        errs.append("firmware/ debe tener al menos un .c y un .h (driver)")
    if errs:
        return errs, warns

    mod_file = mods[0]
    text = mod_file.read_text(encoding="utf-8")
    m = re.search(r"\bmodule\s+(\w+)\s*(?:#\s*\(.*?\))?\s*\((.*?)\)\s*;", text, re.S)
    if not m:
        errs.append(f"{mod_file.name}: no se pudo leer la cabecera del módulo")
    else:
        header = m.group(2)
        for p in STD_PORTS:
            if not re.search(rf"\b{p}\b", header):
                errs.append(f"{mod_file.name}: falta el puerto estándar '{p}'")
        if m.group(1) != mod_file.stem:
            warns.append(f"el módulo '{m.group(1)}' no se llama como su archivo '{mod_file.stem}'")

    if registered:
        mm = memmap.load()
        if not any(p["core"] == core.name for p in mm.get("peripherals", [])):
            errs.append(f"'{core.name}' no está declarado en interfaces/memory_map.yml")

    if sim:
        if not shutil.which("iverilog"):
            (errs if require_sim else warns).append("iverilog no instalado: simulación omitida")
        else:
            r = subprocess.run(["make", "sim"], cwd=rtl, capture_output=True, text=True)
            out = r.stdout + r.stderr
            if r.returncode != 0:
                errs.append("make sim falló:\n" + out[-800:])
            elif "PASS" not in out or re.search(r"\b(FAIL|ERROR)\b", out):
                errs.append("la simulación no terminó en PASS:\n" + out[-800:])
            subprocess.run(["make", "clean"], cwd=rtl, capture_output=True)
    return errs, warns


def all_cores():
    found = []
    for base in (ROOT / "cores", ROOT / "template" / "cores"):
        if base.is_dir():
            found += [d for d in sorted(base.iterdir())
                      if d.is_dir() and not d.name.startswith((".", "_"))]
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cores", nargs="*", type=Path)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--no-sim", action="store_true")
    ap.add_argument("--require-sim", action="store_true", help="falla si no hay iverilog")
    ap.add_argument("--registered", action="store_true")
    a = ap.parse_args()

    targets = all_cores() if a.all else [c.resolve() for c in a.cores]
    if not targets:
        ap.error("indique un core o use --all")
    failed = False
    for c in targets:
        errs, warns = check_core(c, sim=not a.no_sim, registered=a.registered,
                                 require_sim=a.require_sim)
        status = "FALLA" if errs else "OK"
        print(f"[{status}] {c.relative_to(ROOT) if ROOT in c.parents else c}")
        for w in warns:
            print("   aviso:", w)
        for e in errs:
            print("   error:", e)
        failed |= bool(errs)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
