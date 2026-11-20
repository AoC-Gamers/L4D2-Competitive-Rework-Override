# L4D2-Competitive-Rework-Override

Conjunto de 14 plugins SourceMod que incorpora correcciones y extensiones para
servidores de Left 4 Dead 2 basados en
[L4D2-Competitive-Rework](https://github.com/SirPlease/L4D2-Competitive-Rework).

## Instalación

Instala el ZIP sobre un servidor con SourceMod y L4D2-Competitive-Rework. Copia
el árbol `addons/sourcemod/` respetando las rutas. El paquete instala
`match_vote.smx` directamente en `plugins/`, `l4d2_fix_team_shuffle.smx` en
`plugins/fixes/` y los demás plugins en `plugins/optional/`.

Hybrid Scoremod reúne `legacy`, `hybrid` y `zone` en
`l4d2_hybrid_scoremod.smx`. Las configuraciones que cargaban la variante
`l4d2_hybrid_scoremod_zone.smx` usan el plugin unificado con `smplus_mode 2`.

Las variantes de traducción en `es/`, `pt/` y `chi/` tienen cobertura según el
plugin. Conserva las frases base de la instalación competitiva junto con las
variantes que incluye el ZIP.

## Compilación local

```bash
make deps-smx
make build-smx
make package-smx
make release
make validate-artifact
```

La [guía de compilación](docs/build/README.md) detalla las dependencias, los
overrides y el flujo de CI. El [índice de documentación](docs/README.md) enlaza
la guía de cada plugin y las referencias históricas.

## Licencia

Consulta el [texto de la GPL v3](LICENSE) y los [avisos y créditos](NOTICES.md).
