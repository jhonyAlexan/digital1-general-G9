# Planificación con GitHub Projects

Cada equipo planifica su trabajo con **un proyecto de GitHub (Projects)** del repositorio del equipo y
crea las tareas con el formulario `Nueva tarea` (`.github/ISSUE_TEMPLATE/tarea.yml`).

## 1. Crear el proyecto (una sola vez)
1. En la organización/usuario: **Projects → New project → Board**. Nombre: `Equipo XX – Consola D2`.
2. Enlace el repositorio: **Settings del proyecto → Manage access / Add repository**.
3. Configure los campos (**+ New field**):

| Campo | Tipo | Valores |
|---|---|---|
| `Estado` | Single select | Backlog · En progreso · En revisión · Hecho |
| `Sprint` | Iteration | Iteraciones de 1 semana (o la duración del curso) |
| `Periférico` | Single select | uno por periférico del equipo + `General` |
| `Tipo` | Single select | RTL · Testbench · Firmware · Diagrama · Integración · Documentación |
| `Prioridad` | Single select | Alta · Media · Baja |
| `Estimación (h)` | Number | horas |
| `Responsable` | Assignees (nativo) | — |

4. Vistas recomendadas:
   - **Tablero** (Board) agrupado por `Estado`.
   - **Tabla por sprint** agrupada por `Sprint`, con `Responsable` y `Estimación (h)`.
   - **Roadmap** (Roadmap) por `Sprint`.
5. Automatizaciones (**Workflows** del proyecto): *Item added → Estado = Backlog*;
   *Item closed → Estado = Hecho*; *Pull request merged → Estado = Hecho*; auto-agregar issues del repo.

## 2. Ciclo de una tarea
1. **Crear** el issue con el formulario (los criterios de aceptación son obligatorios y verificables).
2. **Planificar**: asignar `Sprint`, `Responsable`, `Estimación (h)`.
3. **Ejecutar**: rama `feat/<periferico>-<tema>`; el PR referencia la tarea con `Closes #N`.
4. **Revisar**: otro integrante revisa; el CI (`make sim`) debe pasar.
5. **Cerrar**: al fusionar el PR la tarea pasa a `Hecho`.

## 3. Convenciones
- Una tarea = un resultado verificable, de a lo sumo unas 8 h. Si es mayor, divídala.
- Toda tarea de RTL incluye su testbench; toda tarea de firmware dice cómo se prueba.
- Tareas de integración (tipo `Integración`) enlazan la etiqueta `validado/...` correspondiente.
