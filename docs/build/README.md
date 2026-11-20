# Compilación y empaquetado

Se requiere GNU Make y Python 3.10 o posterior. Ejecuta las fases desde la raíz del repositorio.

```bash
make deps-smx
make build-smx
make package-smx
make release
make validate-artifact
```

| Fase | Resultado |
| --- | --- |
| `deps-smx` | Descarga el SDK y el compilador de SourceMod en `.deps/smx/`. |
| `build-smx` | Compila los 14 plugins y prepara sus fuentes y recursos en `.build/smx/`. El log queda en `.build/build-smx-compile.log`. |
| `package-smx` | Valida y prepara el árbol instalable en `.build/package-smx/`. |
| `release` | Prepara `dist/sourcemod/artifact/` y genera el ZIP local validado en `dist/release/`. |
| `validate-artifact` | Comprueba rutas, contenido, avisos y cabeceras SMX del árbol final. |

`scripts/package/package-map.json` declara los entrypoints, destinos y recursos.
El compilador usa los includes del repositorio y del SDK. El ZIP contiene las
fuentes de los plugins, los módulos propios, las APIs declaradas, las frases de
traducción y los tres documentos raíz `README.md`, `LICENSE` y `NOTICES.md`.
Las fuentes y los documentos se comparan con la revisión del repositorio durante
el staging. Antes de reemplazar el ZIP, el empaquetador verifica su inventario e
integridad.

## Variables locales

- `PYTHON` permite seleccionar Python. Por defecto se usa `python3` en Linux y `python` en Windows.
- `SOURCEMOD_VERSION` selecciona la rama del SDK. El valor local por defecto es `1.12`.
- `SMX_PLATFORM` selecciona `linux` o `windows` para la descarga local. `SPCOMP` permite indicar un compilador instalado.
- `SMX_BUILD_DIR`, `SMX_PACKAGE_DIR`, `SMX_COMPILE_LOG` y `SOURCEMOD_ARTIFACT_DIR` permiten cambiar las salidas intermedias.
- `RELEASE_BASENAME` define el nombre del ZIP sin la extensión. El valor local es `l4d2-competitive-rework-override-local`.

`make clean` limpia `.build/` y `dist/`. `make clean-all` limpia además `.deps/`.
Los proyectos ubicados bajo `/mnt/` en WSL compilan desde un directorio temporal
para evitar la penalización de E/S del disco montado.

## CI y canales

El workflow encadena `deps-smx`, `build-smx`, `package` y `publish-release`.
Usa la variable de organización `SOURCEMOD_VERSION` para seleccionar y separar
la caché del SDK. El empaquetado usa Make y entrega el ZIP al job de publicación.
Las pull requests terminan con el ZIP como artefacto de Actions.

| Rama | Tag de canal | ZIP |
| --- | --- | --- |
| `main` | `channel/latest` | `l4d2-competitive-rework-override-latest.zip` |
| `develop` | `channel/develop` | `l4d2-competitive-rework-override-develop.zip` |

## Pruebas del producto

La integración de upstream del 20 de noviembre de 2026 compiló los 14 plugins con SourceMod 1.12 sin warnings. También pasó el validador y se verificó la integridad del ZIP y el formato de las frases modificadas. La prueba en SRCDS sigue pendiente para ReadyUp en Coop, Versus y Scavenge, las respuestas de consola y RCON, los porcentajes de Dark Carnival: Remix y la transición a live con espectadores.
