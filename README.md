# ECR Deuterium Handbook

**Manual científico, editable e interactivo sobre un inyector ECR de deuterio de 2,45 GHz.**

**Página publicada (una vez habilitado GitHub Pages):** https://andimec.github.io/ecr-deuterium-handbook/  
**Fuente editable:** [`content/manual_ecr_deuterio.md`](content/manual_ecr_deuterio.md)

## Alcance y advertencias científicas

Caso de estudio: 2,45 GHz, 140 mA de D⁺, 100 keV nominales, rango de potencia RF de estudio 600–900 W, y caudal D₂ de estudio 2–5 sccm. Los rangos de RF y caudal proceden de la especificación del proyecto, **no constituyen una medida operativa pública verificada**. Presiones, temperaturas, densidades y factores de acoplamiento mostrados en los controles son escenarios **ilustrativos**.

Los cálculos de la página son fórmulas analíticas y estimaciones, **no simulaciones de plasma**; su validez está limitada por las hipótesis indicadas en cada capítulo. No se publican datos experimentales internos de LIPAc.

## Contenido

El texto sigue el hilo: alimentación y vacío → electromagnetismo/RF → absorción ECR → distribución energética electrónica → colisiones y química deuterio → superficies BN → extracción y transporte → modelos numéricos, validación y bibliografía. Cada capítulo incluye aplicación, hipótesis, ecuaciones, órdenes de magnitud y referencias.

## Estructura

```text
ecr-deuterium-handbook/
├── .github/workflows/pages.yml          # comprobación y despliegue automático
├── .github/ISSUE_TEMPLATE/              # propuestas de mejora y correcciones
├── content/manual_ecr_deuterio.md       # fuente científica principal
├── scripts/construir_manual.py          # compilador Markdown → HTML autónomo
├── scripts/verificar_magnitudes.py      # regresiones de magnitudes analíticas
├── scripts/verificar_publicacion.py     # integridad del HTML
├── site/                                # HTML generado (ignorado por Git)
├── docs/PUBLICACION.md                  # instalación y despliegue paso a paso
├── docs/CRITERIOS_CIENTIFICOS.md        # política de calidad y referencias
├── requirements.txt
└── README.md
```

## Generar la página en tu ordenador

Requiere Python 3.10+ (la acción de GitHub utiliza Python 3.12):

```bash
python -m pip install -r requirements.txt
python scripts/verificar_magnitudes.py
python scripts/construir_manual.py
python scripts/verificar_publicacion.py
```

Abre `site/index.html` con un navegador o usa `python -m http.server 8000 --directory site` y visita http://localhost:8000/.

## Publicación y edición

1. Configura el repositorio `andimec/ecr-deuterium-handbook` como público en GitHub → Settings → General → Danger Zone → Change repository visibility.
2. Sube los archivos a la rama `main` y selecciona **Settings → Pages → Source: GitHub Actions**.
3. El workflow genera `site/index.html`, ejecuta las pruebas y despliega la página tras cada `push` a `main`.
4. Para editar contenido, modifica `content/manual_ecr_deuterio.md` desde GitHub y confirma el cambio. Para los scripts, trabaja preferentemente con una rama y pull request.

**Instrucciones detalladas:** [Publicación](docs/PUBLICACION.md).  
**Criterios científicos:** [Calidad](docs/CRITERIOS_CIENTIFICOS.md).  
**Colaboración:** [CONTRIBUTING.md](CONTRIBUTING.md).

## Licencia y derechos de autor

El repositorio contiene una licencia MIT creada por su titular. El manual y los scripts quedan cubiertos por la licencia incluida en `LICENSE`, salvo que se indique expresamente otra licencia para materiales de terceros. Las referencias y atribuciones científicas siguen siendo obligatorias.


## Referencias principales

Las fuentes y enlaces científicos se identifican en la bibliografía del [manual](content/manual_ecr_deuterio.md). El uso de nombres de instituciones o códigos científicos no implica respaldo institucional a este sitio.
