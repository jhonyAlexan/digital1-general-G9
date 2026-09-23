# Diagramas generales del sistema

> Diagramas del SoC completo. Cada periférico tiene los suyos en `cores/<periferico>/diagramas/`.
> Mantenga estos diagramas coherentes con `interfaces/memory_map.yml`.

## Diagrama de bloques del SoC
```mermaid
flowchart LR
    subgraph CPU[femtoRV32]
        DP[Datapath] --- CU[Unidad de control]
    end
    CPU <--> BUS{{Bus Wishbone}}
    BUS --> ROM[ROM integrada]
    BUS --> SRAM[SRAM integrada]
    BUS --> RAM[Main RAM]
    BUS --> CSR[Bus CSR LiteX<br/>UART · Timer · Ctrl]
    BUS --> W1[Ventana periférico 1]
    BUS --> W2[Ventana periférico 2]
    BUS --> WN[... periférico N]
    W1 --> P1[(pines FPGA)]
    W2 --> P2[(pines FPGA)]
```
Imagen equivalente en `diagrama_soc_digital2.svg`.

## Flujo de una operación de firmware sobre un periférico
```mermaid
sequenceDiagram
    participant FW as Firmware (C)
    participant CPU as femtoRV32
    participant BUS as Wishbone
    participant WR as WishbonePeripheral
    participant P as perip_X (Verilog)
    FW->>CPU: *(volatile uint32_t*)(BASE+off) = valor
    CPU->>BUS: escritura (adr, dat_w, we)
    BUS->>WR: cyc/stb en la ventana
    WR->>P: cs=1, wr=1, addr=off, d_in=valor (1 ciclo)
    WR-->>BUS: ack
    BUS-->>CPU: fin de la escritura
```

## Flujo de desarrollo (repo general ⇄ equipos)
```mermaid
flowchart LR
    G[Repo general] -- PR automático: actualizaciones comunes --> T[Repo del equipo]
    T -- etiqueta validado/periferico/vN --> V{Validación<br/>estructura + simulación}
    V -- OK --> PR[PR de integración en repo general]
    PR -- revisión del profesor --> G
```
