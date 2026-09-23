# Mapa de memoria

> GENERADO por tools/gen_memmap.py desde interfaces/memory_map.yml. NO EDITAR.

## Regiones del SoC

| Región | Origen | Tamaño | Descripción |
|---|---|---|---|
| `rom` | `0x00000000` | `0x10000` | ROM integrada (BIOS/firmware) |
| `sram` | `0x10000000` | `0x2000` | SRAM integrada |
| `main_ram` | `0x40000000` | `0x800000` | RAM principal (depende de la placa) |
| `csr` | `0xF0000000` | `0x10000` | Bus CSR de LiteX (UART, timer, ctrl...) |

## Ventana de periféricos del curso

Origen `0x00500000`, tamaño `0x100000`. Cada periférico usa una ventana alineada a su tamaño.

| Periférico | Base | Tamaño | Equipo | Puertos extra |
|---|---|---|---|---|
| `blink` | `0x00500000` | `0x1000` | referencia | `led` (out, 1b → `user_led:0`) |

### `blink`

| Offset | Registro | Acceso | Descripción |
|---|---|---|---|
| `0x00` | `CONTROL` | RW | Bit 0: habilita el parpadeo |
| `0x04` | `PERIOD` | RW | Ciclos de reloj por cada cambio del LED |
