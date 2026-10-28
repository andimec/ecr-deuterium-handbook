"""Comprobaciones de integridad de la página generada (no validación científica)."""
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parent.parent
html_path = ROOT / 'site' / 'index.html'
source_path = ROOT / 'content' / 'manual_ecr_deuterio.md'
assert html_path.is_file(), 'Falta site/index.html. Ejecuta construir_manual.py.'
text = html_path.read_text(encoding='utf-8')
source = source_path.read_text(encoding='utf-8')

class Inspector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = set()
        self.elements = []
    def handle_starttag(self, tag, attrs):
        at = dict(attrs)
        self.elements.append(tag)
        if 'id' in at:
            assert at['id'] not in self.ids, f'ID HTML duplicado: {at["id"]}'
            self.ids.add(at['id'])
        if tag == 'a' and at.get('href', '').startswith('#'):
            self.links.add(at['href'][1:])

p = Inspector()
p.feed(text)
assert 'lang="es"' in text, 'Falta idioma español.'
assert '<script type="application/json" id="markdownSource">' in text, 'Falta fuente editable incrustada.'
assert 'mathjax' in text.lower(), 'Falta renderizador de ecuaciones.'
assert '<svg' in text, 'Faltan visualizaciones.'
assert all(i in p.ids for i in ['calc','editor','gasChart','resonanceChart','markdownSource']), 'Falta un componente interactivo.'
assert len([i for i in p.ids if i.startswith('sec-')]) >= 14, 'Se perdieron capítulos.'
assert all(i in p.ids for i in p.links), f'Anclas rotas: {p.links - p.ids}'
assert 'Edición 1.1 · 28/10/2026' in text, 'La versión visible de la cabecera no se actualizó.'
assert 'Ver visor magnético · §04' in text, 'Falta acceso directo al capítulo 4.'
assert 'id="magneticFrame"' in text and 'srcdoc=' in text, 'Falta visor magnético integrado.'
assert '41.4' in text and '87.8' in text, 'Faltan corrientes de referencia de las bobinas.'
assert '# Física y simulación' in source, 'No parece ser el manual maestro.'
print(f'PASS: página {html_path.stat().st_size:,} bytes, {len(p.links)} enlaces internos comprobados.')
