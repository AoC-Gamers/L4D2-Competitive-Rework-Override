# Trabajo en L4D2-Competitive-Rework-Override

Consulta el [índice](docs/README.md) y la [guía de compilación](docs/build/README.md) antes de modificar la estructura o la distribución.

- Conserva las rutas instalables bajo `addons/sourcemod/`, los nombres de los `.smx` y los contratos de las APIs públicas. Declara los plugins y recursos de producto en `scripts/package/package-map.json`.
- Ejecuta compilación, empaquetado y validación mediante el Makefile raíz. Para cambios de distribución, ejecuta `make deps-smx`, `make build-smx`, `make package-smx`, `make release` y `make validate-artifact` en orden.
- Mantén las salidas locales en `.deps/`, `.build/` y `dist/`. Los ZIP incluyen las fuentes de los plugins, los recursos de producto y los textos legales. Conserva la autoría y los avisos de terceros.
- Distingue compilación, validación offline y prueba dentro de SRCDS. Publicar, desplegar o actualizar proveedores de ejecución requiere autorización.
