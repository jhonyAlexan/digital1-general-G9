# Consola de videojuegos sobre FPGA — Repositorio general (Diseño Digital 1)

Contiene lo **compartido por el curso**: arquitectura, construcción base del SoC LiteX (femtoRV32),
interfaces, mapa de memoria e integración. Cada equipo trabaja en **su propio repositorio**: recibe de aquí
las actualizaciones comunes y devuelve aquí sus resultados validados.

## Estructura
```
soc/                    build.py (SoC LiteX) y wb_peripheral.py (periférico <-> Wishbone)
interfaces/
  memory_map.yml        MAPA DE MEMORIA Y PERIFÉRICOS (fuente única de verdad)
firmware/include/       memory_map.h (generado desde el YAML)
docs/                   mapa_memoria.md (generado) y flujo_trabajo.md
tools/                  memmap.py  gen_memmap.py  validate_core.py  sync_to_team.py  integrate_core.py
cores/                  periféricos ya integrados (validados por los equipos)
teams.yml               equipos, sus repos y los cores que posee cada uno
.github/workflows/      ci.yml  sync-equipos.yml  integrar-equipo.yml
template/               lo que reciben los repos de equipo:
  .github/ISSUE_TEMPLATE/tarea.yml    formulario de tareas
  .github/workflows/                  ci.yml, solicitar-integracion.yml
  planificacion/                      GitHub Projects
  diagramas/  diagrama_soc_digital2.svg
  cores/blink/                        periférico de referencia
    diagramas/  rtl/{Makefile, perip_blink.v, perip_blink_TB.v, perip_blink_TB.gtkw}  firmware/
  firmware/main.c                     programas C de integración/prueba y juego
  README.md
```

## Contrato de un periférico

## Comandos
```bash
pip install pyyaml && sudo apt install iverilog gtkwave
python3 tools/gen_memmap.py                    # regenera memory_map.h y docs/mapa_memoria.md (--check en CI)
python3 tools/validate_core.py --all           # estructura + interfaz + simulación de los cores
python3 soc/build.py --board <placa> --build   # requiere LiteX
```
Flujo repo general ⇄ equipos y configuración de GitHub: [`docs/flujo_trabajo.md`](docs/flujo_trabajo.md).
