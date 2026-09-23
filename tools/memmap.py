"""Carga y valida interfaces/memory_map.yml (módulo compartido por las herramientas)."""
import sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
MAP_FILE = ROOT / "interfaces" / "memory_map.yml"


def load(path=MAP_FILE):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate(m):
    """Devuelve una lista de errores (vacía si el mapa es coherente)."""
    errs = []
    win = m["periph_window"]
    w0, w1 = win["origin"], win["origin"] + win["size"]
    spans = [(n, r["origin"], r["origin"] + r["size"]) for n, r in m["regions"].items()]
    names = set()
    for p in m.get("peripherals", []):
        n, base, size = p["name"], p["base"], p["size"]
        if n in names:
            errs.append(f"{n}: nombre duplicado")
        names.add(n)
        if size & (size - 1):
            errs.append(f"{n}: size 0x{size:X} no es potencia de 2")
        if base % size:
            errs.append(f"{n}: base 0x{base:X} no está alineada a size 0x{size:X}")
        if not (w0 <= base and base + size <= w1):
            errs.append(f"{n}: fuera de la ventana de periféricos "
                        f"(0x{w0:X}-0x{w1:X})")
        if (1 << p["addr_width"]) > size:
            errs.append(f"{n}: addr_width={p['addr_width']} excede el tamaño de la ventana")
        for r in p.get("registers", []):
            if r["offset"] >= (1 << p["addr_width"]):
                errs.append(f"{n}.{r['name']}: offset 0x{r['offset']:X} no cabe en addr_width")
            if r["offset"] % 4:
                errs.append(f"{n}.{r['name']}: offset no alineado a 4 bytes")
        spans.append((n, base, base + size))
    spans.sort(key=lambda s: s[1])
    for (na, _, ea), (nb, sb, _) in zip(spans, spans[1:]):
        if sb < ea:
            errs.append(f"solapamiento entre '{na}' y '{nb}'")
    return errs


def die_on_errors(m):
    errs = validate(m)
    if errs:
        print("Mapa de memoria inválido:", file=sys.stderr)
        for e in errs:
            print("  -", e, file=sys.stderr)
        sys.exit(1)
