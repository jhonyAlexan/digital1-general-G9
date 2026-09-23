#!/usr/bin/env python3
"""Trae un periférico validado de un repo de equipo hacia cores/ del repo general.

  python3 tools/integrate_core.py --team-dir /ruta/repo-equipo --core uart --team equipo-01

Pasos: (1) verifica que el equipo sea dueño del core según teams.yml y memory_map.yml,
(2) valida estructura + simulación, (3) copia cores/<core> al repo general.
El resultado se propone luego como Pull Request (lo hace el workflow integrar-equipo).
"""
import argparse
import shutil
import sys
from pathlib import Path
import yaml

import memmap
from validate_core import check_core

ROOT = memmap.ROOT


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--team-dir", required=True, type=Path)
    ap.add_argument("--core", required=True)
    ap.add_argument("--team", required=True)
    ap.add_argument("--no-sim", action="store_true")
    a = ap.parse_args()

    teams = yaml.safe_load((ROOT / "teams.yml").read_text())["equipos"] or []
    team = next((t for t in teams if t["name"] == a.team), None)
    if not team or a.core not in team.get("cores", []):
        sys.exit(f"ERROR: '{a.core}' no pertenece a '{a.team}' en teams.yml")

    mm = memmap.load()
    entry = next((p for p in mm["peripherals"] if p["core"] == a.core), None)
    if not entry or entry["owner"] != a.team:
        sys.exit(f"ERROR: '{a.core}' no está asignado a '{a.team}' en interfaces/memory_map.yml")

    src = a.team_dir / "cores" / a.core
    errs, warns = check_core(src, sim=not a.no_sim, registered=False, require_sim=True)
    for w in warns:
        print("aviso:", w)
    if errs:
        print("El core NO cumple los requisitos de integración:")
        for e in errs:
            print(" -", e)
        sys.exit(1)

    dst = ROOT / "cores" / a.core
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("*.vcd", "*.out", "__pycache__"))
    print(f"Integrado: {src} -> {dst.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
