#!/usr/bin/env python3
"""Construcción base del SoC del curso (LiteX + femtoRV32 + periféricos del curso).

Ejemplos:
  python3 soc/build.py --board colorlight_i5 --build
  python3 soc/build.py --board <placa> --build --load
  python3 soc/build.py --board <placa> --only blink --build      # solo estos periféricos

Usa el `BaseSoC` del target de `litex_boards` de la placa elegida y le agrega las
ventanas de periféricos declaradas en interfaces/memory_map.yml.
"""
import argparse
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "soc"))

import memmap                                    # noqa: E402
from migen import Signal                             # noqa: E402
from litex.build.parser import LiteXArgumentParser   # noqa: E402
from litex.soc.integration.builder import Builder    # noqa: E402
from litex.soc.integration.soc import SoCRegion      # noqa: E402
from wb_peripheral import WishbonePeripheral         # noqa: E402

CORE_DIRS = [ROOT / "cores", ROOT / "template" / "cores"]   # orden de búsqueda


def find_core(name):
    for d in CORE_DIRS:
        if (d / name / "rtl").is_dir():
            return d / name
    sys.exit(f"ERROR: no se encontró el core '{name}' en cores/ ni template/cores/")


def add_course_peripherals(soc, mm, only=None):
    for p in mm.get("peripherals", []):
        if only and p["name"] not in only:
            continue
        rtl = find_core(p["core"]) / "rtl"
        srcs = [f for f in sorted(rtl.glob("*.v")) if not f.stem.endswith("_TB")]
        for f in srcs:
            soc.platform.add_source(str(f))

        pins = {}
        for q in p.get("ports", []):
            res, idx = q["connect"].split(":")
            try:
                pad = soc.platform.request(res, int(idx))
            except Exception as e:                # recurso ausente en esta placa
                print(f"AVISO: {p['name']}.{q['name']}: la placa no tiene '{q['connect']}' ({e})")
                pad = Signal(q["width"])          # sin conectar
            pins[q["name"]] = (q["dir"], pad)

        wb = WishbonePeripheral(p["module"], p["addr_width"], pins)
        setattr(soc, f"periph_{p['name']}", wb)      # LiteXModule lo registra como submódulo
        soc.bus.add_slave(
            name=f"periph_{p['name']}", slave=wb.bus,
            region=SoCRegion(origin=p["base"], size=p["size"], cached=False))


def main():
    pre = argparse.ArgumentParser(add_help=False)
    pre.add_argument("--board", required=True, help="nombre del target en litex_boards.targets")
    pre.add_argument("--only", nargs="*", help="limitar a estos periféricos")
    pre_args, _ = pre.parse_known_args()

    target = importlib.import_module(f"litex_boards.targets.{pre_args.board}")
    platform_mod = importlib.import_module(f"litex_boards.platforms.{pre_args.board}")

    mm = memmap.load()
    memmap.die_on_errors(mm)

    parser = LiteXArgumentParser(platform=platform_mod.Platform,
                                 description="SoC Diseño Digital 2 (femtoRV32 + periféricos)")
    parser.add_argument("--board", help="placa (litex_boards)")
    parser.add_argument("--only", nargs="*")
    parser.add_argument("--sys-clk-freq", default=50e6, type=float, help="frecuencia del sistema (Hz)")
    parser.set_defaults(cpu_type="femtorv",                      # CPU del curso
                        integrated_rom_size=mm["regions"]["rom"]["size"],
                        integrated_sram_size=mm["regions"]["sram"]["size"])
    args = parser.parse_args()

    soc = target.BaseSoC(sys_clk_freq=args.sys_clk_freq, **parser.soc_argdict)
    add_course_peripherals(soc, mm, pre_args.only)

    builder = Builder(soc, **parser.builder_argdict)
    if args.build:
        builder.build(**parser.toolchain_argdict)
    if args.load:
        prog = soc.platform.create_programmer()
        prog.load_bitstream(builder.get_bitstream_filename(mode="sram"))


if __name__ == "__main__":
    main()
