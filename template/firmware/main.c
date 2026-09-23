/* Programa de integración / prueba del equipo (y, más adelante, el juego).
 *
 * Ejemplo mínimo: usa el driver del periférico de referencia `blink`.
 * Reemplácelo por pruebas de sus propios periféricos y luego por el juego.
 */
#include <stdint.h>
#include "memory_map.h"
#include "blink.h"

int main(void)
{
    blink_start(5000000u);   /* ~10 Hz con reloj de 50 MHz: cambia el LED cada 5e6 ciclos */
    while (1) {
        /* bucle principal del juego / prueba */
    }
    return 0;
}
