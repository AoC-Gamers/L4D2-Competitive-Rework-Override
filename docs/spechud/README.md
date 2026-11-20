# spechud

## Fuente principal

- `addons/sourcemod/scripting/spechud.sp`

## Módulos

- `addons/sourcemod/scripting/spechud/types.sp`
- `addons/sourcemod/scripting/spechud/helpers.sp`
- `addons/sourcemod/scripting/spechud/runtime.sp`
- `addons/sourcemod/scripting/spechud/render.sp`

## Motivo del cambio

`spechud` dependía de consultar varios estados opcionales en runtime, incluyendo boss percents y datos de `readyup`.
Eso generaba acoplamiento innecesario con bibliotecas, mezclaba orquestación con render, y obligaba al panel a asumir que ciertas APIs siempre estaban listas.

## Cambios aplicados

### Consumo por forward

`spechud` ahora recibe los boss percents por:

- `L4D2_OnBossPercentsUpdated(int tankPercent, int witchPercent)`

Ese callback alimenta el estado interno del HUD y evita el polling directo de `GetStoredTankPercent()` y `GetStoredWitchPercent()` en el flujo principal del round.

### Estado tipado

Se agregaron estructuras para concentrar estado relacionado:

- `RuntimeState`
  - `lateload`
  - `readyUp`
  - `pause`
  - `l4dBossPercent`
  - `hybridScoremod`
  - `tankControlEq`
  - `lerpMonitor`
  - `witchAndTankifier`
  - `tankSelection`
- `BossFlowState`
  - `tankPercent`
  - `witchPercent`
  - `synced`
- `BossRoundState`
  - `tankCount`
  - `witchCount`
  - `roundHasFlowTank`
  - `roundHasFlowWitch`
  - `flowTankActive`
  - `customBossSys`
- `TankHudSnapshot`
- `WeaponSnapshot`
- `SurvivorSnapshot`
- `InfectedSnapshot`

### Runtime simplificado

`RuntimeState` es la fuente de verdad para la disponibilidad de bibliotecas opcionales.
`spechud` usa esos flags para omitir o agregar secciones del panel sin asumir que una API exista.

### Readyup simplificado

`RefreshServerNameCache()` y `RefreshReadyCfgName()` usan `g_Runtime.readyUp` como guardia primaria.
Si `readyup` no está cargado, el plugin cae a `hostname` y no intenta resolver convars que no existen.

### Panel más declarativo

La construcción del HUD quedó más segmentada:

- `HudDrawTimer()` orquesta
- las funciones de contenido deciden internamente si pintan algo
- el estado de bosses, round y runtime se consume desde structs en lugar de globals sueltos

### Actualización del panel y paso a live

- El HUD se actualiza cada segundo. Las filas de supervivientes e infectados especiales muestran la latencia en milisegundos o `BOT`. Los nombres largos se recortan sin partir caracteres UTF-8.
- En Versus, el panel muestra los puntos y el porcentaje del máximo en cada componente del bonus que informa el modo de `l4d2_hybrid_scoremod`. En `legacy` se muestra el componente de salud.
- La reserva de munición de cada arma, incluida la MP5, se consulta a Left4DHooks mediante `L4D_GetReserveAmmo()`.
- Al pasar a live, el plugin espera 0,2 segundos antes de ejecutar `sm_spectate` para los espectadores humanos, para dar tiempo a que suene la campana. Si la ronda termina, se reinicia o cambia el mapa durante la espera, el timer se cancela.

### Localización

El panel sigue construyéndose por cliente, así que cada receptor obtiene el HUD en su idioma.
Los nombres propios y clases del juego se conservan en inglés donde corresponde. El archivo en portugués brasileño cubre los avisos de activación y uso del HUD. Las frases restantes recurren al archivo base.

### Estructura interna

El plugin fue dividido por responsabilidad:

- `types.sp` para estado y snapshots
- `helpers.sp` para helpers genéricos
- `runtime.sp` para setup, hooks y flujo de bibliotecas
- `render.sp` para construcción del panel

## Compatibilidad

- si `l4d_boss_percent` está presente, `spechud` consume el forward
- si la biblioteca no está disponible, `spechud` mantiene fallback seguro para la sincronización inicial

## Resultado

`spechud` quedó menos acoplado a natives opcionales y más guiado por estado reactivo.
Eso reduce consultas repetidas, separa mejor las responsabilidades y deja más clara la relación entre runtime, render y dependencias opcionales.
