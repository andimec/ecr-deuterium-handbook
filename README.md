# ECR Deuterium Handbook

**Manual científico, editable e interactivo sobre un inyector ECR de deuterio de 2,45 GHz.**

**Página publicada (si GitHub Pages está habilitado):** https://andimec.github.io/ecr-deuterium-handbook/  
**Fuente editable:** [`content/manual_ecr_deuterio.md`](content/manual_ecr_deuterio.md)

## Alcance científico

Caso de estudio: 2,45 GHz, 140 mA de D⁺, 100 keV nominales, RF 600–900 W, caudal D₂ 2–5 sccm. Los rangos RF y caudal son especificaciones del estudio, no medidas operativas públicas verificadas. La presión, la EEDF, la absorción y los diagnósticos de plasma mostrados en el panel son hipótesis/estimaciones, no medidas de LIPAc.

**Edición 1.1 — Magnetostática del capítulo 4:** integra un visor de campo 2D a partir de dos mapas de FEMM a 1 A proporcionados por el autor. Corrientes de referencia: 41,4 A RF y 87,8 A extracción. El mapa se interpola y escala de manera lineal. Esto NO demuestra linealidad para componentes ferromagnéticos saturables ni valida el modelo frente a medidas.

## Contenido del capítulo 4

El visor interactivo incluye las tres componentes |B|, Br, Bz, flechas, isocontornos y su suavizado opcional, representaciones de cámara y disco BN, perfil axial, sonda interactiva, resolución inversa de corrientes a dos puntos, búsqueda de cruces ECR, y exportación de campo combinado. Ambos mapas se embeben automáticamente en el HTML final; no hay que seleccionarlos para usar la web.

## Estructura

- `content/manual_ecr_deuterio.md`: fuente de los capítulos científicos.
- `assets/magnetostatica/C-RF_1A.csv` y `C-EXTRACT_1A.csv`: resultados FEMM a 1 A proporcionados por el autor.
- `assets/magnetostatica/magnetic_field_viewer_v5BIS.html`: visor de origen, conservado sin alteraciones.
- `scripts/integrar_magnetica.py`: construye el visor autónomo a partir del original y los CSV.
- `scripts/construir_manual.py`: genera la web autónoma con el visor en el capítulo 4.
- `scripts/verificar_campo.py`: malla, hashes de entrada y puntos de referencia magnetostáticos.
- `scripts/verificar_magnitudes.py`: órdenes de magnitud analíticos.
- `scripts/verificar_publicacion.py`: estructura HTML y enlaces.
- `site/index.html`: salida generada (no versionada).

## Generación y validación

```bash
python -m pip install -r requirements.txt
python scripts/verificar_magnitudes.py
python scripts/verificar_campo.py
python scripts/integrar_magnetica.py
python scripts/construir_manual.py
python scripts/verificar_publicacion.py
python -m http.server 8000 --directory site
```

Visita http://localhost:8000/. Para actualizar los campos, reemplaza los CSV por otros mapas **con la misma convención de columnas y una malla compartida** y regenera. El visor permite seleccionar otros CSV en el navegador sin modificar los originales del repositorio. Para editar el contenido científico, modifica el Markdown y regenera.

**Criterio de publicación:** la incorporación de mapas de simulación asociados con instalaciones reales debe contar con los derechos y permisos institucionales necesarios antes de publicarse en una rama pública. El titular del repositorio debe verificar la procedencia y autorización para publicar cualquier dato no disponible públicamente.

**Instrucciones:** [Publicación](docs/PUBLICACION.md) · [Criterios científicos](docs/CRITERIOS_CIENTIFICOS.md) · [Contribuciones](CONTRIBUTING.md).

**Licencia:** MIT según `LICENSE`, sujeta a los derechos de terceros y a las restricciones de los mapas de origen.
