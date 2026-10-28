#!/usr/bin/env python3
"""Construye un HTML autónomo (excepto la tipografía matemática opcional de MathJax) desde Markdown.

Uso:
    python construir_manual.py
La fuente editable es manual_ecr_deuterio.md.
"""
from __future__ import annotations
import html
import json
import re
from pathlib import Path
from markdown_it import MarkdownIt

BASE = Path(__file__).resolve().parent.parent
SOURCE = BASE / 'content' / 'manual_ecr_deuterio.md'
OUTPUT = BASE / 'site' / 'index.html'
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
source = SOURCE.read_text(encoding='utf-8')

# Protect math from Markdown punctuation handling, then restore MathJax delimiters.
maths = []
def protect_math(m, block=False):
    token = f'MATHHOLDER{len(maths):05d}X'
    raw = m.group(1).strip()
    rendered = f'<div class="equation">\\[{html.escape(raw)}\\]</div>' if block else f'<span class="inline-math">\\({html.escape(raw)}\\)</span>'
    maths.append((token, rendered))
    return '\n\n'+token+'\n\n' if block else token

text = re.sub(r'\$\$(.+?)\$\$', lambda m: protect_math(m, True), source, flags=re.S)
text = re.sub(r'(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)', lambda m: protect_math(m), text, flags=re.S)
md = MarkdownIt('commonmark', {'html': False, 'linkify': True, 'typographer': True}).enable('table')
rendered = md.render(text)
for token, replacement in maths:
    rendered=rendered.replace(f'<p>{token}</p>',replacement).replace(token,replacement)
# Embeber el visor íntegro, con sus CSV, solo en el HTML final.
# El marcador permanece en el Markdown editable; no mezclar JS con la fuente física.
viewer_path=BASE/'assets'/'magnetostatica'/'visor_magnetico_integrado.html'
viewer_html=viewer_path.read_text(encoding='utf-8')
widget = ("""<div class="magnetic-panel"><div class="magnetic-toolbar">
    <div><strong>Simulación magnética interactiva — mapas a 1 A</strong><small>RF: 41,4 A · Extracción: 87,8 A · datos originales integrados</small></div>
    <button class="btn" type="button" id="openMagneticFull">Abrir visor en pestaña independiente</button>
    </div>
    <iframe id="magneticFrame" title="Visor interactivo del campo magnético de dos bobinas"
            width="100%" height="1790" loading="eager" srcdoc='""" + html.escape(viewer_html,quote=True) + """'></iframe>
    <div class="magnetic-foot">El iframe contiene una copia autónoma de los CSV. También funciona sin abrir el archivo del visor por separado.</div>
    </div>""")
assert rendered.count('<p>[[ECR_MAGNETIC_VIEWER]]</p>')==1, 'marcador de visor ausente'
rendered=rendered.replace('<p>[[ECR_MAGNETIC_VIEWER]]</p>',widget)
# Anchor original references inside bibliography, when possible.
for i in range(1,18):
    rendered=rendered.replace(f'<strong>[R{i}]</strong>', f'<strong id="R{i}">[R{i}]</strong>')
# Add IDs and wrapping sections automatically; bibliography annex uses h2 as well.
sections=[]
seq=0
for line in rendered.splitlines():
    if line.startswith('<h2>'):
        seq+=1
        title=re.sub('<[^>]*>','',line).replace('&amp;','&').strip()
        label = f'sec-{seq:02d}'
        sections.append((label,title))
        rendered=rendered.replace(line,f'<h2 id="{label}">{html.escape(title)}</h2>',1)

nav='\n'.join(f'<a class="nav-link" href="#{id_}" data-target="{id_}"><span>{i:02d}</span> {html.escape(title)}</a>' for i,(id_,title) in enumerate(sections,1))

CSS=r''' 
:root{--bg:#f6f8fb;--surface:#fff;--ink:#192d42;--muted:#62758a;--line:#dce5ec;--accent:#126c89;--accent2:#12654f;--pale:#e9f5f8;--warn:#98521c;--warn-bg:#fff6eb;--code:#f2f6fb}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.7 system-ui,-apple-system,'Segoe UI',sans-serif}
.top{position:sticky;top:0;z-index:20;background:var(--ink);color:white;min-height:62px;display:flex;align-items:center;gap:16px;padding:9px 24px;box-shadow:0 3px 12px #11203030}
.brand{font-weight:750;letter-spacing:-.02em;font-size:16px}.brand small{display:block;font-weight:400;font-size:11px;color:#b8d7e5}.spacer{flex:1}
.btn{font:inherit;cursor:pointer;border-radius:7px;padding:7px 11px;border:1px solid #bdd2dc;background:white;color:#134d64;font-size:12px;font-weight:650}.btn:hover{filter:brightness(.96)}.top .btn{background:#22465b;border-color:#54758a;color:white}
.layout{display:grid;grid-template-columns:265px minmax(0,1fr);max-width:1600px;margin:0 auto}
.sidebar{position:sticky;top:62px;height:calc(100vh - 62px);overflow-y:auto;padding:22px 13px 22px 23px;border-right:1px solid var(--line);background:#f2f6f9}
.sidebar strong{font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:#577388}.side-search{width:100%;padding:9px;margin:12px 0;border:1px solid var(--line);border-radius:7px;background:white;color:var(--ink)}
.nav-link{display:flex;gap:8px;align-items:baseline;text-decoration:none;color:#40566b;font-size:12px;line-height:1.35;padding:9px 8px;border-radius:6px}.nav-link span{color:#7a94a3;font-variant-numeric:tabular-nums}.nav-link:hover,.nav-link.active{color:var(--accent);background:#dfeef3}.sidebar-foot{font-size:11px;color:#73889c;margin-top:22px}
.main{max-width:1150px;padding:30px clamp(18px,3.8vw,64px) 130px;width:100%;margin:auto}
.hero{background:linear-gradient(145deg,#17354d,#126c89);border-radius:17px;padding:30px 32px;color:white;margin-bottom:22px}.hero h1{font-size:clamp(25px,3.5vw,42px);line-height:1.18;margin:8px 0 14px}.hero p{color:#e4f4fb;max-width:800px;margin:0}.tag{font-size:11px;letter-spacing:.08em;font-weight:750;color:#83e0d6;text-transform:uppercase}
.metrics{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin:16px 0}.metric{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:14px}.metric strong{display:block;font-size:20px;line-height:1.5;font-variant-numeric:tabular-nums}.metric small{color:var(--muted);font-size:11px}
.panel{background:var(--surface);padding:22px;border:1px solid var(--line);border-radius:14px;margin:16px 0 26px}.panel h2{font-size:19px;margin:0 0 8px}.panel p{margin:6px 0;color:var(--muted);font-size:13px}
.inputs{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin:20px 0}.field label{display:block;color:#4d6377;font-size:12px;margin-bottom:5px;font-weight:600}.field input,.field select{width:100%;padding:8px 9px;border:1px solid #cbdde6;border-radius:7px;font:inherit;color:var(--ink);background:white}.field small{display:block;color:var(--muted);font-size:10px;margin-top:3px}.outputs{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}.output{padding:12px;background:#f3f9fa;border:1px solid #d6ecea;border-radius:9px}.output small{display:block;color:#587480;font-size:11px}.output strong{font-size:17px;color:#124e60;white-space:nowrap}
.note{border-left:4px solid var(--accent);background:#e9f5f8;padding:13px 16px;border-radius:0 7px 7px 0;font-size:13px;margin-top:14px}
.visual{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:18px}.visual>div{padding:12px;border:1px solid var(--line);border-radius:9px;background:white}.visual svg{display:block;width:100%;height:auto}.visual h3{font-size:13px;margin:0}.legend{font-size:11px;color:var(--muted)}
.doc{background:white;padding:clamp(20px,4vw,48px);border:1px solid var(--line);border-radius:13px;box-shadow:0 7px 20px #2f476608}.doc>h1{display:none}.doc h2{font-size:25px;letter-spacing:-.028em;border-top:2px solid #e9eff4;padding-top:34px;margin-top:45px;scroll-margin-top:90px;color:#173e5a}.doc h2:first-of-type{margin-top:0}.doc h3{font-size:16px;color:#155572;margin-top:24px;margin-bottom:9px}.doc p,.doc li{line-height:1.77}.doc ul,.doc ol{padding-left:24px}.doc blockquote{border-left:4px solid #e3a954;padding:12px 16px;background:var(--warn-bg);margin:18px 0;color:#684624}.doc blockquote p{margin:0}.doc strong{font-weight:730}.doc a{color:#006c8f;word-break:break-word}.doc table{width:100%;border-collapse:collapse;margin:20px 0;font-size:12px;line-height:1.5;display:block;overflow-x:auto}.doc thead{background:#eef5f9}.doc th,.doc td{padding:9px 11px;border:1px solid var(--line);vertical-align:top;text-align:left;min-width:80px}.doc code{padding:2px 5px;border-radius:5px;background:var(--code)}.equation{text-align:center;padding:14px 6px;margin:12px 0;background:#fafcfe;overflow-x:auto;border-radius:8px}
.magnetic-panel{border:1px solid #dce5ec;border-radius:12px;overflow:hidden;background:#101529;margin:24px -22px 28px}
.magnetic-toolbar{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;padding:12px 15px;color:#e8f1ff;background:#16364a}
.magnetic-toolbar strong{font-size:13px}.magnetic-toolbar small{display:block;font-size:11px;color:#a5c0d5}.magnetic-toolbar a{background:#edf8fc;color:#174761;text-decoration:none}
#magneticFrame{width:100%;height:1790px;display:block;border:0;background:#0d0d1a}
.magnetic-foot{color:#99b4c8;font-size:11px;padding:9px 14px;background:#152337}
@media(max-width:600px){.magnetic-panel{margin-left:-12px;margin-right:-12px}#magneticFrame{height:1950px}}
.editor{display:none;position:fixed;inset:62px 0 0 0;z-index:25;background:#fff}.editor.visible{display:grid;grid-template-rows:auto 1fr}.editorbar{display:flex;align-items:center;gap:12px;padding:12px 22px;border-bottom:1px solid var(--line);flex-wrap:wrap}.editorbar p{color:var(--muted);font-size:11px;flex:1;min-width:200px}.editor textarea{padding:20px 24px;border:0;resize:none;outline:0;font:13px/1.7 ui-monospace,Consolas,monospace;color:#123;background:#fafcff;width:100%;height:100%}
@media(max-width:950px){.layout{grid-template-columns:1fr}.sidebar{display:none}.inputs,.outputs{grid-template-columns:repeat(2,1fr)}.main{padding:18px 16px}.metrics{grid-template-columns:repeat(2,1fr)}}
@media(max-width:600px){.inputs,.outputs,.visual{grid-template-columns:1fr}.hero{padding:22px}.doc{padding:19px}.top{padding:8px 12px;gap:8px}.brand{font-size:13px}}
@media print{.top,.sidebar,.panel,.metrics,.editor{display:none!important}.layout{display:block}.main{max-width:none;padding:0}.doc{border:0;padding:0;box-shadow:none}.doc h2{break-after:avoid}.doc table{display:table}body{font-size:11pt}}
'''

JS=r'''
'use strict';
const e=1.602176634e-19, me=9.1093837139e-31, mD=3.3435837724e-27;
const eps=8.8541878128e-12, mu=1.25663706127e-6, k=1.380649e-23, c=299792458;
const fmt=(n,d=3)=>Number.isFinite(n)?n.toLocaleString('es-ES',{maximumFractionDigits:d}):'—';
const val=(id)=>parseFloat(document.getElementById(id).value);
const show=(id,s)=>{document.getElementById(id).textContent=s};
function calc(){
 const freq=val('f'), Ir=val('beam'), V=val('hv'), power=val('rf'), flow=val('flow'),
       ne=val('ne'),Te=val('te'), p=val('pg'), Tg=val('tg'), diameter=val('diameter'), L=val('L'),
       pstd=101325,Tstd=val('standard'), pumping=val('pumping'), refl=val('refl')/100,wall=val('wall')/100;
 if([freq,Ir,V,power,flow,ne,Te,p,Tg,diameter,L,Tstd,pumping,refl,wall].some(v=>!Number.isFinite(v))||[freq,flow,ne,Te,p,Tg,diameter,L,Tstd,pumping].some(v=>v<=0))return;
 const omega=2*Math.PI*freq*1e9, B=omega*me/e, nCrit=eps*me*omega*omega/(e*e);
 const Nstd=pstd*(1e-6/60)/(k*Tstd), molFlow=flow*Nstd, ionFlux=(Ir/1000)/e, gasUse=ionFlux/(2*molFlow);
 const beamPower=Ir/1000*V*1e3, nGas=p/(k*Tg), lambda=k*Tg/(Math.sqrt(2)*Math.PI*(diameter*1e-9)**2*p);
 const lambdaD=Math.sqrt(eps*Te/(ne*e)), vth=Math.sqrt(2*e*Te/me), rL=vth/omega,
       cS=Math.sqrt(e*Te/mD), pmag=B*B/(2*mu), pe=ne*e*Te, beta=pe/pmag;
 const Qin=molFlow*k*Tg, pressureEst=Qin/(pumping/1000), pref=power*refl, pwall=(power-pref)*wall,
       pabs=Math.max(0,power-pref-pwall);
 const out={
  oB:fmt(B*1000,3)+' mT',oCritical:(nCrit/1e16).toFixed(3)+' ×10¹⁶ m⁻³',
  oWavelength:fmt(c/(freq*1e9)*1000,2)+' mm',oMolecules:fmt(molFlow/1e18,3)+' ×10¹⁸ s⁻¹',
  oGasUse:fmt(gasUse*100,1)+' %',oIonFlux:fmt(ionFlux/1e17,3)+' ×10¹⁷ s⁻¹',
  oBeamPower:fmt(beamPower/1000,2)+' kW',oRFabs:fmt(pabs,1)+' W',
  oRFcost:fmt(pabs/(Ir/1000)/1000,2)+' keV/D⁺',oNneutral:fmt(nGas/1e19,3)+' ×10¹⁹ m⁻³',
  oMFP:fmt(lambda*100,2)+' cm',oKn:fmt(lambda/L,3),oDebye:fmt(lambdaD*1000,3)+' mm',
  oRho:fmt(rL*1e6,1)+' µm',oBohm:fmt(cS/1000,2)+' km/s',oBeta:beta.toExponential(2),
  oPredictP:fmt(pressureEst,4)+' Pa'
 };
 for(let id in out)show(id,out[id]);
 let reg=lambda/L <.01?'Continuo':lambda/L<.1?'Deslizamiento':lambda/L<10?'Transición':'Molecular libre';
 show('knRegime',reg);show('modelWarning',gasUse>1?'Atención: la corriente D⁺ exige más núcleos de D que los introducidos como D₂; revisa flujo y definición de corriente.':'La utilización es una cota de balance de átomos, no eficiencia química ni de extracción.');
 const cvs=document.getElementById('gasChart'),rcvs=document.getElementById('resonanceChart');
 const circle=(x,y,r,col)=>`<circle cx="${x}" cy="${y}" r="${r}" fill="${col}"/>`;
 const toX=f=>43+(f-1)*275/6, toY=u=>184-Math.min(1,u)*155;
 let pts=[];for(let f=1;f<=7.001;f+=.05)pts.push(`${toX(f).toFixed(1)},${toY((Ir/1000/e)/(2*f*Nstd)).toFixed(1)}`);
 cvs.innerHTML=`<line x1="43" y1="29" x2="43" y2="184" stroke="#8496a3"/><line x1="43" y1="184" x2="318" y2="184" stroke="#8496a3"/><line x1="43" y1="29" x2="318" y2="29" stroke="#dcaa8f" stroke-dasharray="4 4"/><polyline points="${pts.join(' ')}" fill="none" stroke="#167b98" stroke-width="2.3"/>${circle(toX(flow),toY(gasUse),5,'#bf5c2a')}<text x="48" y="24" font-size="11" fill="#97592f">100 %</text><text x="120" y="202" font-size="11" fill="#567">Caudal D₂ (sccm)</text><text x="29" y="190" font-size="11" fill="#567">0</text><text x="18" y="35" font-size="11" fill="#567">1</text><text x="43" y="202" font-size="9" fill="#567">1</text><text x="312" y="202" font-size="9" fill="#567">7</text>`;
 const gamma=val('gamma')/100,rx=x=>43+(x+2)*275/4,ry=y=>184-155*y;
 let cpts=[];for(let x=-2;x<=2.001;x+=.0125){let y=gamma*gamma/(x*x+gamma*gamma);cpts.push(`${rx(x).toFixed(1)},${ry(y).toFixed(1)}`)}
 rcvs.innerHTML=`<line x1="43" y1="29" x2="43" y2="184" stroke="#8496a3"/><line x1="43" y1="184" x2="318" y2="184" stroke="#8496a3"/><line x1="180.5" y1="29" x2="180.5" y2="184" stroke="#cfa883" stroke-dasharray="4 4"/><polyline points="${cpts.join(' ')}" fill="none" stroke="#166c74" stroke-width="2.3"/><text x="145" y="202" font-size="11" fill="#567">Desajuste (%)</text><text x="39" y="202" font-size="9" fill="#567">−2</text><text x="306" y="202" font-size="9" fill="#567">+2</text><text x="179" y="202" font-size="9" fill="#567">0</text><text x="14" y="35" font-size="10" fill="#567">1</text>`;
 show('gammaLabel',`${fmt(val('gamma'),3)} %`);
}
for(let el of document.querySelectorAll('.field input,.field select'))el.addEventListener('input',calc);calc();
const search=document.getElementById('search');search.addEventListener('input',()=>{let q=search.value.toLocaleLowerCase('es');document.querySelectorAll('.nav-link').forEach(a=>{a.style.display=a.textContent.toLocaleLowerCase('es').includes(q)?'flex':'none'})});
const tocLinks=[...document.querySelectorAll('.nav-link')];const observer=new IntersectionObserver(entries=>{entries.forEach(en=>{if(en.isIntersecting){tocLinks.forEach(a=>a.classList.toggle('active',a.dataset.target===en.target.id))}})},{rootMargin:'-80px 0px -70% 0px'});document.querySelectorAll('.doc h2').forEach(el=>observer.observe(el));
const editor=document.getElementById('editor');const edta=document.getElementById('sourceEditor');const storage='ecr-deuterio-v2-source-edit';const original=JSON.parse(document.getElementById('markdownSource').textContent);
const safeStorage={get:()=>{try{return localStorage.getItem(storage)}catch(e){return null}},set:v=>{try{localStorage.setItem(storage,v);return true}catch(e){return false}},remove:()=>{try{localStorage.removeItem(storage)}catch(e){}}};
edta.value=safeStorage.get()??original;
document.getElementById('btnEdit').addEventListener('click',()=>{editor.classList.add('visible');edta.focus()});document.getElementById('closeEdit').addEventListener('click',()=>editor.classList.remove('visible'));
document.getElementById('saveEdit').addEventListener('click',()=>{show('editorStatus',safeStorage.set(edta.value)?'Guardado localmente en este navegador.':'Almacenamiento del navegador no disponible: utiliza Exportar .md.');});
document.getElementById('restoreEdit').addEventListener('click',()=>{if(confirm('¿Restaurar el Markdown original en el editor?')){edta.value=original;safeStorage.remove();show('editorStatus','Fuente restaurada (sin modificar archivos).')}});
function download(content, name, mime='text/plain'){const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([content],{type:mime}));a.download=name;document.body.appendChild(a);a.click();setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove()},800)}
document.getElementById('exportEdit').addEventListener('click',()=>download(edta.value,'manual_ecr_deuterio_editado.md','text/markdown'));
document.getElementById('printDoc').addEventListener('click',()=>window.print());
// Sincronización ligera de las condiciones iniciales y el visor incrustado.
const magneticFrame=document.getElementById('magneticFrame');
document.getElementById('openMagneticFull').addEventListener('click',()=>{
  const htmlText=magneticFrame.getAttribute('srcdoc');
  const url=URL.createObjectURL(new Blob([htmlText],{type:'text/html;charset=utf-8'}));
  const popup=window.open(url,'_blank');
  if(!popup)alert('El navegador ha bloqueado la ventana emergente: permite abrir la pestaña del visor.');
  setTimeout(()=>URL.revokeObjectURL(url),30000);
});
function sendMagneticCurrents(){
  if(!magneticFrame?.contentWindow)return;
  const iRF=parseFloat(document.getElementById('coilRF').value);
  const iEX=parseFloat(document.getElementById('coilEX').value);
  if(!Number.isFinite(iRF)||!Number.isFinite(iEX))return;
  magneticFrame.contentWindow.postMessage({type:'ECR_COILS_SET',iRF,iEX},'*');
}
['coilRF','coilEX'].forEach(id=>document.getElementById(id).addEventListener('change',sendMagneticCurrents));
magneticFrame?.addEventListener('load',sendMagneticCurrents);
window.addEventListener('message',event=>{
 if(event.source!==magneticFrame?.contentWindow||event.data?.type!=='ECR_COILS_CHANGED')return;
 if(Number.isFinite(event.data.iRF))document.getElementById('coilRF').value=event.data.iRF.toFixed(1);
 if(Number.isFinite(event.data.iEX))document.getElementById('coilEX').value=event.data.iEX.toFixed(1);
});
'''

HTML=f'''<!doctype html>
<html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Física ECR 2,45 GHz · Inyector de deuterio</title><meta name="description" content="Manual técnico editable e interactivo sobre una fuente ECR de D₂ y haz D⁺ 140 mA.">
<style>{CSS}</style>
<script>window.MathJax={{tex:{{inlineMath:[['\\\\(','\\\\)']],displayMath:[['\\\\[','\\\\]']]}},options:{{skipHtmlTags:['script','noscript','style','textarea','pre','code']}}}};</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script></head><body>
<header class="top"><div class="brand">ECR · Física del inyector<small>Deuterio · 2,45 GHz · Edición 1.1 · 28/10/2026</small></div><div class="spacer"></div><a class="btn" href="#sec-04" style="text-decoration:none">Ver visor magnético · §04</a><button class="btn" id="btnEdit">✎ Editar Markdown</button><button class="btn" id="printDoc">Imprimir</button></header>
<div class="layout"><aside class="sidebar"><strong>Contenido</strong><input id="search" class="side-search" placeholder="Buscar capítulo..." aria-label="Buscar capítulo"><nav>{nav}</nav><div class="sidebar-foot">Archivo HTML autónomo para lectura y cálculos (las ecuaciones usan MathJax por CDN). Los cambios editoriales se conservan localmente hasta exportarlos.</div></aside>
<main class="main"><section class="hero"><div class="tag">Manual de fundamentos y simulación</div><h1>Física de una fuente ECR de deuterio</h1><p>Desde el caudal de D₂ y los neutrales hasta las microondas, absorción ECR, producción de D⁺, superficies BN y extracción. Derivaciones, hipótesis, códigos y bibliografía contrastable.</p></section>
<div class="metrics"><div class="metric"><small>RF de referencia</small><strong>2,45 GHz</strong></div><div class="metric"><small>Corriente D⁺ nominal</small><strong>140 mA</strong></div><div class="metric"><small>Potencia RF de estudio</small><strong>600–900 W</strong></div><div class="metric"><small>Inyección D₂ de estudio</small><strong>2–5 sccm</strong></div></div>
<section class="panel" id="calc"><h2>Laboratorio interactivo · órdenes de magnitud</h2><p>Cambia un dato y se actualizan magnitudes derivadas mediante fórmulas analíticas. Ninguna salida implica una simulación autoconsistente; la presión, las pérdidas RF y la EEDF no se infieren automáticamente del punto de operación.</p>
<div class="inputs">
 <div class="field"><label for="f">Frecuencia RF (GHz)</label><input type="number" id="f" value="2.45" min="0.1" step="0.01"></div>
 <div class="field"><label for="beam">Corriente de D⁺ (mA)</label><input type="number" id="beam" value="140" min="0" step="5"><small>No corriente total multiespecie</small></div>
 <div class="field"><label for="hv">Voltaje de extracción (kV)</label><input type="number" id="hv" value="100" min="0" step="5"></div>
 <div class="field"><label for="coilRF">I bobina RF (A)</label><input type="number" id="coilRF" value="41.4" min="0" max="120" step="0.1"><small>Sincronizada con el visor del capítulo 4</small></div>
 <div class="field"><label for="coilEX">I bobina de extracción (A)</label><input type="number" id="coilEX" value="87.8" min="0" max="120" step="0.1"><small>Sincronizada con el visor del capítulo 4</small></div>
 <div class="field"><label for="rf">Potencia RF incidente (W)</label><input type="number" id="rf" value="750" min="0" step="25"></div>
 <div class="field"><label for="flow">Caudal D₂ (sccm)</label><input type="number" id="flow" value="3.5" min="0.01" max="50" step="0.1"></div>
 <div class="field"><label for="standard">Temperatura estándar del sccm</label><select id="standard"><option value="273.15">0 °C, 1 atm</option><option value="293.15">20 °C, 1 atm</option></select></div>
 <div class="field"><label for="ne">Densidad e⁻ (m⁻³)</label><select id="ne"><option value="1e16">10¹⁶</option><option value="1e17" selected>10¹⁷</option><option value="1e18">10¹⁸</option></select><small>Hipótesis de plasma</small></div>
 <div class="field"><label for="te">Temperatura electrónica Tₑ (eV)</label><input type="number" id="te" value="5" min="0.1" step="0.5"><small>Hipótesis de Maxwelliana</small></div>
 <div class="field"><label for="pg">Presión D₂ en cámara (Pa)</label><input type="number" id="pg" value="0.05" min="0.000001" step="0.01"><small>Supuesto ilustrativo, no medida</small></div>
 <div class="field"><label for="tg">Temperatura de neutrales (K)</label><input type="number" id="tg" value="300" min="50" step="10"></div>
 <div class="field"><label for="diameter">Diámetro eficaz molecular d (nm)</label><input type="number" id="diameter" value="0.30" min="0.1" step="0.01"><small>Modelo de esferas duras</small></div>
 <div class="field"><label for="L">Longitud característica L (m)</label><input type="number" id="L" value="0.10" min="0.001" step="0.01"></div>
 <div class="field"><label for="pumping">Bombeo efectivo S (L/s)</label><input type="number" id="pumping" value="100" min="0.1" step="10"><small>Solo estimación ideal p ≈ Q/S</small></div>
 <div class="field"><label for="refl">Fracción RF reflejada (%)</label><input type="number" id="refl" value="10" min="0" max="100" step="1"><small>Hipótesis, no medida</small></div>
 <div class="field"><label for="wall">Pérdidas adicionales tras reflexión (%)</label><input type="number" id="wall" value="20" min="0" max="100" step="1"><small>Fracción del remanente</small></div>
</div>
<div class="outputs">
 <div class="output"><small>B resonante</small><strong id="oB"></strong></div>
 <div class="output"><small>Densidad crítica no magnetizada</small><strong id="oCritical"></strong></div>
 <div class="output"><small>Longitud de onda en vacío</small><strong id="oWavelength"></strong></div>
 <div class="output"><small>Entrada de D₂</small><strong id="oMolecules"></strong></div>
 <div class="output"><small>Utilización atómica ideal</small><strong id="oGasUse"></strong></div>
 <div class="output"><small>Flujo de D⁺ en haz</small><strong id="oIonFlux"></strong></div>
 <div class="output"><small>Potencia del haz D⁺</small><strong id="oBeamPower"></strong></div>
 <div class="output"><small>RF absorbida (balance supuesto)</small><strong id="oRFabs"></strong></div>
 <div class="output"><small>RF absorbida por D⁺ extraído</small><strong id="oRFcost"></strong></div>
 <div class="output"><small>Densidad molecular neutra</small><strong id="oNneutral"></strong></div>
 <div class="output"><small>Recorrido libre medio neutro</small><strong id="oMFP"></strong></div>
 <div class="output"><small>Knudsen</small><strong id="oKn"></strong></div>
 <div class="output"><small>Longitud de Debye</small><strong id="oDebye"></strong></div>
 <div class="output"><small>Radio térmico de Larmor e⁻</small><strong id="oRho"></strong></div>
 <div class="output"><small>Velocidad de Bohm D⁺</small><strong id="oBohm"></strong></div>
 <div class="output"><small>Beta electrónico</small><strong id="oBeta"></strong></div>
 <div class="output"><small>p ideal de Q/S a Tgas</small><strong id="oPredictP"></strong></div>
 <div class="output"><small>Régimen del gas estimado</small><strong id="knRegime"></strong></div>
</div>
<div class="note" id="modelWarning">Las salidas dependen de las hipótesis introducidas.</div>
<div class="visual"><div><h3>Utilización atómica de gas frente al caudal</h3><svg id="gasChart" viewBox="0 0 350 218" role="img" aria-label="Gráfica interactiva de utilización de gas según caudal"></svg><div class="legend">Curva analítica, para corriente D⁺ fija. Punto naranja = valor seleccionado.</div></div>
<div><h3>Perfil resonante lorentziano ilustrativo</h3><div class="field"><label for="gamma">Anchura efectiva ν/ω (%) · <span id="gammaLabel"></span></label><input id="gamma" type="range" min="0.02" max="1.0" step="0.02" value="0.30"></div><svg id="resonanceChart" viewBox="0 0 350 218" role="img" aria-label="Perfil lorentziano de resonancia dependiente de amortiguamiento"></svg><div class="legend">Perfil normalizado a su máximo, no una potencia ECR calculada ni una EEDF.</div></div></div>
</section>
<article class="doc" id="contenido">{rendered}</article>
</main></div>
<div class="editor" id="editor"><div class="editorbar"><button class="btn" id="closeEdit">← Volver a lectura</button><strong>Editar la fuente Markdown</strong><p>La vista publicada no cambia al editar: exporta el .md y ejecuta construir_manual.py para regenerarla. Guardar local conserva cambios solo en este navegador.</p><button class="btn" id="saveEdit">Guardar local</button><button class="btn" id="exportEdit">Exportar .md</button><button class="btn" id="restoreEdit">Restaurar original</button><small id="editorStatus"></small></div><textarea id="sourceEditor" spellcheck="false" aria-label="Editor Markdown completo"></textarea></div>
<script type="application/json" id="markdownSource">{json.dumps(source,ensure_ascii=False).replace('</','<\\/')}</script>
<script>{JS}</script></body></html>'''
OUTPUT.write_text(HTML,encoding='utf-8')
print('Generado',OUTPUT, 'bytes=',OUTPUT.stat().st_size, 'secciones=',len(sections))
