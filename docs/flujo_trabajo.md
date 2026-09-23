# Flujo: repositorio general ⇄ repositorios de equipo

## ① Hacia los equipos (sincronización)
`sync-equipos.yml` corre al cambiar `main` del repo general. Por cada equipo de `teams.yml` ejecuta
`tools/sync_to_team.py` y abre el PR «Actualización del repositorio general» (rama `upstream/actualizacion-comun`).

| Tipo | Rutas | Comportamiento |
|---|---|---|
| Gestionado | `soc/ interfaces/ tools/ docs/ teams.yml firmware/include/ .github/ planificacion/ cores/blink/` | Se reemplaza siempre |
| Semilla | `README.md diagramas/ firmware/main.c diagrama_soc_digital2.svg` | Solo si no existe; luego es del equipo |
| Cores integrados | `cores/<x>/` | Se copian a los demás equipos, salvo el core propio (`teams.yml → cores`) |

## ② Hacia el repo general (integración)
1. El equipo valida: `python3 tools/validate_core.py cores/<core> --registered`.
2. Crea la etiqueta `validado/<core>/vN` (`git tag ... && git push origin ...`).
3. `solicitar-integracion.yml` (equipo) valida y envía `repository_dispatch` al repo general.
4. `integrar-equipo.yml` (general) ejecuta `tools/integrate_core.py`: exige que el core pertenezca al equipo
   (`teams.yml`), esté asignado a él en `memory_map.yml`, tenga estructura completa y simulación en PASS.
   Luego abre el PR `integracion/<equipo>/<core>`.
5. El profesor revisa y fusiona; la siguiente sincronización lo reparte a los demás equipos.

## Configuración inicial (profesor)
1. Subir este repo a `main`; crear un repo por equipo con el contenido de `template/` (o con `sync_to_team.py`).
2. Registrar equipos en `teams.yml`.
3. Secrets/variables:

| Dónde | Nombre | Contenido |
|---|---|---|
| Repo general (secret) | `TEAMS_TOKEN` | PAT/App con `contents`, `pull-requests`, `workflow` sobre los repos de equipo |
| Repo de equipo (secret) | `GENERAL_REPO_TOKEN` | PAT con `contents: write` sobre el repo general |
| Repo de equipo (variable) | `GENERAL_REPO` | `ORG/repo-general` |

4. Repo general: *Settings → Actions → permitir que los workflows creen Pull Requests*. Proteger `main`.

Solo el integrador modifica `interfaces/memory_map.yml` (luego `python3 tools/gen_memmap.py`; el CI lo verifica).
