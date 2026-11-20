# L4D2-Competitive-Rework-Fix

Repositorio de fixes y overrides para plugins provenientes de `L4D2-Competitive-Rework`.

## Objetivo

Este repo existe para ofrecer una capa mantenida de correcciones, ajustes y documentación sobre plugins usados en servidores competitivos basados en `L4D2-Competitive-Rework`.

La idea es mantener aquí:

- overrides sobre plugins del proyecto competitivo
- fixes de estabilidad
- mejoras de tipado, API o mantenimiento
- traducciones y assets asociados cuando forman parte del override

## Estructura

Se replica la misma estructura esperada por SourceMod:

- `addons/sourcemod/scripting/`
- `addons/sourcemod/scripting/include/`
- `addons/sourcemod/translations/`
- `docs/`

Para los binarios compilados, el CI empaqueta los plugins en:

- `addons/sourcemod/plugins/anticheat/`
- `addons/sourcemod/plugins/fixes/`
- `addons/sourcemod/plugins/optional/`

`disabled/` no se gestiona desde este repo porque corresponde a una convención de despliegue de SourceMod y no a una categoría funcional del proyecto.

## Mapeo de Binarios

El archivo `plugin-package-map.json` define qué plugins deben salir fuera de `optional/`.

- `anticheat`: plugins que deben empaquetarse en `plugins/anticheat/`
- `fixes`: plugins que deben empaquetarse en `plugins/fixes/`
- `root`: plugins que deben empaquetarse directamente en `plugins/`
- cualquier plugin no listado cae por defecto en `plugins/optional/`

Actualmente:

- `match_vote` se empaqueta en `plugins/`
- `l4d2_fix_team_shuffle` se empaqueta en `plugins/fixes/`

## Build Local

Las copias de `steamidtools.inc` y `steamidtools/` corresponden a SteamIDTools
4.0.0. Caster importa conversiones puras y adaptadores de clientes, sin plugin
proveedor; no se distribuye el antiguo include stock.

Targets disponibles:

- `make deps-smx`
- `make build-smx`
- `make package-smx`
- `make release`
- `make clean`
- `make clean-all`

Comportamiento:

- `make deps-smx` descarga el compilador de SourceMod para la plataforma actual
- `make build-smx` genera salida en `.build/smx/`
- `make package-smx` prepara `.build/package-smx/`
- `make release` genera `dist/sourcemod/artifact/` y `dist/release/*.zip`

`build-smx` no descarga dependencias automáticamente.
Primero hay que ejecutar `make deps-smx`.

En Windows los targets usan `python`.
En Linux/WSL los targets usan `python3`.
En Linux/WSL, `build-smx` compila desde un workspace temporal en `/tmp/l4d2crf-build` cuando el repo está bajo `/mnt/`, para evitar la lentitud de I/O sobre discos montados.

Los builds locales incluyen solo el contenido desplegable bajo:

- `addons/sourcemod/plugins/`
- `addons/sourcemod/scripting/`
- `addons/sourcemod/translations/`

Documentación del sistema de build:

- [docs/build-system.md](docs/build-system.md)

## Documentación

Los cambios que justifican que un plugin viva en esta capa se documentan en `docs/` usando un archivo por plugin.

Documentos actuales:

- [`autopause`](docs/autopause.md)
- [`caster_assister`](docs/caster_assister.md)
- [`caster_system`](docs/caster_system.md)
- [`l4d2_character_fix`](docs/l4d2_character_fix.md)
- [`l4d2_fix_team_shuffle`](docs/l4d2_fix_team_shuffle.md)
- [`l4d2_hybrid_scoremod`](docs/l4d2_hybrid_scoremod.md)
- [`l4d_boss_percent`](docs/l4d_boss_percent.md)
- [`l4d_tank_control_eq`](docs/l4d_tank_control_eq.md)
- [`l4d_tank_damage_announce`](docs/l4d_tank_damage_announce.md)
- [`l4d_votepoll_fix`](docs/l4d_votepoll_fix.md)
- [`match_vote`](docs/match_vote.md)
- [`readyup`](docs/readyup.md)
- [`spechud`](docs/spechud.md)
- [`specrates`](docs/specrates.md)

`l4d2_hybrid_scoremod` concentra los modos `legacy`, `hybrid` y `zone`. Las guías de [Scoremod clásico](docs/l4d2_scoremod.md) y [Scoremod Zone](docs/l4d2_hybrid_scoremod_zone.md) conservan la referencia histórica.

## Traducciones incluidas

El ZIP conserva los archivos base y las variantes disponibles en `es/`, `pt/` y `chi/`. La cobertura depende del plugin. Algunas variantes complementan un archivo base del proyecto competitivo, como `readyup.phrases.txt`. Instala el ZIP sobre el árbol del servidor competitivo para conservar esos archivos base.

## Alcance

Este repo está orientado a plugins y recursos que funcionen como fixes u overrides del ecosistema competitivo base.

No busca ser:

- un paquete completo de servidor
- una colección de plugins específicos de un proyecto privado
- un reemplazo total del repo upstream
