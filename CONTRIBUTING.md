# Cómo contribuir al manual

Agradecemos revisiones científicas y propuestas de contenido. Para correcciones o nuevas secciones, crea un issue; para cambios directos, presenta una pull request contra `main`.

## Edición de la física

- Modifica `content/manual_ecr_deuterio.md`, no `site/index.html` (generado automáticamente).
- Conserva la secuencia didáctica aplicación → formulación → hipótesis → modelos/software → órdenes de magnitud → bibliografía.
- Incluye bibliografía identificable (DOI, manual oficial o enlace permanente) y deja claro qué es estimación y qué es medida.
- Añade incertidumbres, unidades y límites de validez.
- No publiques datos no autorizados de laboratorios o instituciones.

## Comprobación local

```bash
python -m pip install -r requirements.txt
python scripts/verificar_magnitudes.py
python scripts/construir_manual.py
python scripts/verificar_publicacion.py
```

El workflow revisa automáticamente estos pasos. Ninguna modificación se publica en Pages hasta incorporarse a `main`.

## Licencia

Todavía no se ha elegido una licencia de reutilización. No envíes contenido de terceros o contribuciones sujetas a licencias incompatibles.
