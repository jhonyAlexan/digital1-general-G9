#!/usr/bin/env python3
"""Distribuye las actualizaciones comunes del repo general hacia un repo de equipo.

  python3 tools/sync_to_team.py --team equipo-01 --dest /ruta/al/repo-equipo
  python3 tools/sync_to_team.py --team equipo-01 --dest ... --dry-run

Reglas (ver docs/flujo_trabajo.md):
  MANAGED  -> se reemplazan siempre (compartido, los equipos no lo editan)
  SEED     -> se copian solo si no existen (punto de partida, luego es del equipo)
  CORES    -> cores integrados en el repo general: se copian a cores/<x>/ salvo los
              que el equipo posee (teams.yml -> cores)
"""
import argparse
import shutil
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent

# (origen en repo general, destino en repo de equipo)
MANAGED = [
    ("soc", "soc"),
    ("interfaces", "interfaces"),
    ("tools", "tools"),
    ("docs", "docs"),
    ("teams.yml", "teams.yml"),
    ("firmware/include", "firmware/include"),
    ("template/.github", ".github"),
    ("template/planificacion", "planificacion"),
    ("template/cores/blink", "cores/blink"),           # ejemplo de referencia
]
SEED = [
    ("template/README.md", "README.md"),
    ("template/diagramas", "diagramas"),
    ("template/firmware/main.c", "firmware/main.c"),
    ("template/diagrama_soc_digital2.svg", "diagrama_soc_digital2.svg"),
]
SKIP_NAMES = {"__pycache__", ".git"}


def cp(src: Path, dst: Path, dry):
    print(("[dry] " if dry else "") + f"{src.relative_to(ROOT)}  ->  {dst}")
    if dry:
        return
    if dst.is_dir() and src.is_dir():
        shutil.rmtree(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.is_dir():
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns(*SKIP_NAMES, "*.vcd", "*.out"))
    else:
        shutil.copy2(src, dst)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--team", required=True)
    ap.add_argument("--dest", required=True, type=Path)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    teams = yaml.safe_load((ROOT / "teams.yml").read_text())["equipos"] or []
    team = next((t for t in teams if t["name"] == a.team), None)
    if team is None:
        raise SystemExit(f"equipo '{a.team}' no está en teams.yml")
    own = set(team.get("cores", []))
    dest = a.dest.resolve()

    for s, d in MANAGED:
        # no pisar un core propio del equipo con el ejemplo/plantilla homónimos
        if d.startswith("cores/") and d.split("/")[1] in own:
            print(f"omitido {d} (core propio del equipo)")
            continue
        cp(ROOT / s, dest / d, a.dry_run)
    for s, d in SEED:
        if (dest / d).exists():
            continue
        cp(ROOT / s, dest / d, a.dry_run)
    cores_dir = ROOT / "cores"
    if cores_dir.is_dir():
        for c in sorted(cores_dir.iterdir()):
            if c.is_dir() and not c.name.startswith((".", "_")) and c.name not in own:
                cp(c, dest / "cores" / c.name, a.dry_run)


if __name__ == "__main__":
    main()
