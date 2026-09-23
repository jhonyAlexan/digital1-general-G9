# Repositorio del equipo — Consola de videojuegos sobre FPGA (Diseño Digital 2)

Creado desde la plantilla del curso. Recibe actualizaciones del repositorio general (Pull Request
automático) y devuelve sus periféricos validados mediante etiquetas de integración.

| Ruta | Dueño | ¿Editable? |
|---|---|---|
| `cores/<su periférico>/`, `firmware/main.c`, `diagramas/` | Equipo | Sí |
| `soc/`, `interfaces/`, `tools/`, `docs/`, `firmware/include/`, `.github/`, `planificacion/` | Repo general | **No** (se sobrescriben) |
| `cores/blink/` | Repo general | Solo lectura (referencia) |
| `cores/<otros equipos>/` | Otros equipos | Solo lectura |

## Flujo
1. Cree tareas con el formulario **Nueva tarea** y organícelas según `planificacion/README.md`.
2. Nuevo periférico: copie `cores/blink/` a `cores/<nombre>/` y renombre `perip_blink*` → `perip_<nombre>*`.
   Pida su ventana de direcciones con un issue en el repo general.
3. Simule: `cd cores/<nombre>/rtl && make sim`. Valide: `python3 tools/validate_core.py cores/<nombre> --registered`.
4. Integre: `git tag validado/<nombre>/v1 && git push origin validado/<nombre>/v1`.
5. Revise y fusione los PR «Actualización del repositorio general».
