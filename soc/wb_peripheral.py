"""Adaptador: periférico Verilog del curso  <->  bus Wishbone de LiteX.

Interfaz estándar que debe cumplir el RTL de cada periférico (ver docs/arquitectura.md):

    input  clk, rst
    input  [31:0]         d_in     dato de escritura
    input                 cs       chip-select, pulso de UN ciclo por acceso
    input  [ADDR_W-1:0]   addr     offset local en bytes (dirección base ya restada)
    input                 rd, wr
    output [31:0]         d_out    dato de lectura (combinacional mientras cs & rd)

Este adaptador:
  * genera `cs` como pulso de 1 ciclo por transacción Wishbone,
  * resta la base de la ventana (la ventana está alineada a su tamaño, así que
    basta truncar la dirección),
  * captura `d_out` y lo devuelve con `ack` un ciclo después.
Accesos de 32 bits (se ignoran los byte-selects `sel`).
"""
from migen import *
from litex.gen import LiteXModule
from litex.soc.interconnect import wishbone


class WishbonePeripheral(LiteXModule):
    def __init__(self, module, addr_width, ports=None):
        """
        module     : nombre del módulo Verilog (p. ej. "perip_blink")
        addr_width : ancho del puerto `addr` del RTL
        ports      : dict {nombre_puerto_verilog: (dir, señal_migen)} para los pines extra
        """
        self.bus = bus = wishbone.Interface(data_width=32, address_width=32,
                                            addressing="word")
        cs    = Signal()
        rd    = Signal()
        wr    = Signal()
        addr  = Signal(addr_width)
        d_out = Signal(32)
        ack   = Signal()
        dat_r = Signal(32)

        # offset local en bytes = {adr_palabra[addr_width-3:0], 2'b00}
        self.comb += [
            cs.eq(bus.cyc & bus.stb & ~ack),   # pulso de un ciclo por acceso
            wr.eq(bus.we),
            rd.eq(~bus.we),
            addr.eq(Cat(Constant(0, 2), bus.adr[:addr_width - 2])),
            bus.ack.eq(ack),
            bus.dat_r.eq(dat_r),
        ]
        self.sync += [
            ack.eq(bus.cyc & bus.stb & ~ack),
            If(cs, dat_r.eq(d_out)),
        ]

        kw = dict(i_clk=ClockSignal("sys"), i_rst=ResetSignal("sys"),
                  i_d_in=bus.dat_w, i_cs=cs, i_addr=addr, i_rd=rd, i_wr=wr,
                  o_d_out=d_out)
        for name, (direction, sig) in (ports or {}).items():
            kw[("o_" if direction == "out" else "i_") + name] = sig
        self.specials += Instance(module, **kw)
