#ifndef BLINK_H
#define BLINK_H

#include <stdint.h>
#include "memory_map.h"   /* generado desde interfaces/memory_map.yml */

/* BLINK_BASE viene del mapa de memoria compartido. No fijar direcciones aquí. */
#define BLINK_BASE_ADDR   BLINK_BASE
#define BLINK_CONTROL_REG (*(volatile uint32_t *)(BLINK_BASE_ADDR + 0x00u))
#define BLINK_PERIOD_REG  (*(volatile uint32_t *)(BLINK_BASE_ADDR + 0x04u))

void blink_start(uint32_t period_cycles);
void blink_stop(void);

#endif
