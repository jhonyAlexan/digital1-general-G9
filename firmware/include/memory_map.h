/* GENERADO por tools/gen_memmap.py desde interfaces/memory_map.yml. NO EDITAR. */
#ifndef MEMORY_MAP_H
#define MEMORY_MAP_H

#define ROM_BASE  0x00000000u
#define ROM_SIZE  0x00010000u
#define SRAM_BASE  0x10000000u
#define SRAM_SIZE  0x00002000u
#define MAIN_RAM_BASE  0x40000000u
#define MAIN_RAM_SIZE  0x00800000u
#define CSR_BASE  0xF0000000u
#define CSR_SIZE  0x00010000u

/* blink (equipo: referencia) */
#define BLINK_BASE  0x00500000u
#define BLINK_SIZE  0x00001000u
#define BLINK_CONTROL_OFFSET  0x00u
#define BLINK_PERIOD_OFFSET  0x04u

#endif /* MEMORY_MAP_H */
