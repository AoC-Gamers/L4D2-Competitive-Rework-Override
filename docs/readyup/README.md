# readyup

## Plugin

- `addons/sourcemod/scripting/readyup.sp`
- `addons/sourcemod/scripting/readyup/`
- `addons/sourcemod/scripting/include/readyup.inc`

## Motivo del Override

`readyup` fue movido a `L4D2-Competitive-Rework-Fix` porque recibió correcciones locales para evitar crashes en flujos de voto y errores por índices inválidos en el footer.

## Cambios Aplicados

### Cooperativo

ReadyUp consulta a Left4DHooks al iniciar la preparación para saber si el modo tiene infectados controlados por jugadores. En cooperativo, los modos de `l4d_ready_enabled` funcionan así.

| Valor | Condición |
| --- | --- |
| `1` | Todos los supervivientes humanos deben estar listos y debe haber al menos uno. |
| `2` | El inicio automático calcula el umbral de `l4d_ready_autostart_min` a partir de `survivor_limit`. |
| `3` | Basta con que un superviviente humano esté listo. |

Con `l4d_ready_autoready` activo, el panel omite los avisos de ready manual. ReadyUp guarda el valor de `director_no_specials` al entrar en preparación y lo restaura al pasar a live, al cambiar de mapa durante la preparación o al descargar el plugin.

### Capacidad que muestra el panel

En cada actualización, el panel usa esta prioridad para mostrar el total en `Slots`.

1. Usa `mv_maxplayers` si existe y su valor es distinto de `-1`.
2. Si `mv_maxplayers` falta o vale `-1`, usa `sv_maxplayers` si existe y su valor es distinto de `-1`.
3. Si `sv_maxplayers` también falta o vale `-1`, consulta a SourceMod por el cupo humano efectivo con `GetMaxHumanPlayers()`. [Referencia de SourceMod](https://sm.alliedmods.net/new-api/clients/GetMaxHumanPlayers)

`l4d_ready_autostart_min` usa los límites de los equipos para calcular el umbral de inicio automático.

### Validación de clientes

En `readyup/player.inc`:

- `IsPlayer()` ahora valida:
  - `client > 0`
  - rango válido
  - `IsClientInGame(client)`

Esto evita llamadas inválidas a `GetClientTeam()`. Los comandos `sm_unready`, `sm_toggleready`, `sm_hide`, `sm_show` y `sm_return` también comprueban que el cliente esté en juego.

### Flujo de voto

En `readyup.sp`:

- `Vote_Callback()` ahora sale temprano si el cliente no está en juego

Esto corrige el flujo reportado desde:

- `Vote_Callback -> Ready_Cmd -> IsPlayer`

### Footer

En `readyup/footer.inc`:

- `Footer.Edit()` ahora exige `index >= 0` antes de `SetString`
- `FooterGet()` ahora exige `index >= 0` antes de `GetString`

Esto evita errores tipo:

- `Invalid index -1`

cuando otro plugin intenta editar un footer aún no agregado.

### Recolección de basura

En `readyup.sp`:

- `OnPluginEnd()` ahora hace cleanup explícito del módulo principal
- desengancha `HookEvent(...)`
- remueve `AddChangeHook(...)`
- desactiva command listeners de voto rápido
- libera timers visibles del plugin principal
- libera `Footer` y `GlobalForward`

### Estructura del override

- `readyup` debe tratarse como un plugin multiarchivo
- el comportamiento del override no vive solo en `readyup.sp`, sino también en:
  - `readyup/action.inc`
  - `readyup/command.inc`
  - `readyup/game.inc`
  - `readyup/native.inc`
  - `readyup/panel.inc`
  - `readyup/player.inc`
  - `readyup/setup.inc`
  - `readyup/sound.inc`
  - `readyup/util.inc`

## Compatibilidad

- En modos con infectados controlados por jugadores, las condiciones de ready siguen considerando ambos equipos.
- El soporte para cooperativo usa `L4D_HasPlayerControlledZombies()` de Left4DHooks.

## Archivos Asociados

- fuente principal
- carpeta `readyup/`
- include `readyup.inc`
- Requiere `translations/readyup.phrases.txt` del proyecto competitivo base. El ZIP de Fix incluye `translations/pt/readyup.phrases.txt`.
