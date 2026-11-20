# Changelog

## [Unreleased]

### Añadido

- **ReadyUp** admite la preparación en cooperativo.
- **Traducciones** incorpora frases compatibles en portugués brasileño y chino.

### Cambiado

- **SpecHUD** muestra la latencia de cada jugador y los puntos y porcentajes del bonus. El reingreso de espectadores se difiere brevemente al pasar a live.
- **Distribución** los ZIP nuevos usan el prefijo `l4d2-competitive-rework-override-` en los mismos canales. El instalador incluye las fuentes de los 14 plugins, sus APIs y recursos de producto, el README, la licencia y los avisos. Los includes compartidos se conservan como dependencias de compilación y los logs quedan fuera del ZIP.

### Corregido

- **Vote Poll Fix** se instala en `plugins/fixes/` para reemplazar el binario que carga `generalfixes.cfg`.
- **ReadyUp** resuelve la capacidad del panel con `mv_maxplayers`, luego `sv_maxplayers` y finalmente `GetMaxHumanPlayers()`.
- **Comandos** se validan los clientes de ReadyUp, Match Vote, Caster System, Tank Control y Hybrid Scoremod. `sm_mapinfo` devuelve el desglose de puntuación desde la consola.
- **Boss Percent** reconoce porcentajes de un dígito en Dark Carnival: Remix. **Tank Control** evita un error de depuración cuando no hay un controlador humano.
