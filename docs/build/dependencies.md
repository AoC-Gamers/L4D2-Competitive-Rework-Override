# Dependencias

| Dependencia | Revisión o procedencia | Uso |
| --- | --- | --- |
| SourceMod | Rama `1.12` por defecto. La descarga oficial de la rama puede cambiar de revisión. | SDK y `spcomp` al compilar. SourceMod, SDKTools y SDKHooks en el servidor. |
| Left4DHooks, BuiltinVotes, Confogl y L4D2Lib | Includes versionados en este repositorio. La revisión Git de Fix identifica las copias exactas. | Compilación. Los proveedores de natives necesarios se instalan con el servidor competitivo. |
| Pause, LerpMonitor, Witch and Tankifier y utilidades L4D2 | Includes versionados en este repositorio. | Compilación e integraciones opcionales según el plugin. |
| SteamIDTools | Copia de la serie 4.0.0 incorporada en el commit `2dd5974` de Fix. | Conversiones y adaptadores compilados en Caster System. |
| Colored Chat Functions | Cabecera `1.3.2` en `colors.inc`. | Stocks de compilación. Consulta los [avisos](../../NOTICES.md) para su procedencia. |
| L4D2-Competitive-Rework | Proyecto base del que provienen los plugins y recursos de ejecución. | Provee la configuración competitiva y frases base como `readyup.phrases.txt`, `autopause.phrases.txt` y `l4d_tank_control_eq.phrases.txt`. |

El mapa de paquetes declara las APIs de los plugins de Fix que acompañan al binario.
Los includes de compilación compartidos se mantienen en el repositorio para que
los consumidores tomen las mismas revisiones. Las cabeceras y versiones de plugins
de terceros se conservan en sus fuentes. [Avisos y licencia](../../NOTICES.md)
