#!/usr/bin/env python3
"""Validación de los mapas a 1 A y referencias de la sección 4, solo stdlib."""
from __future__ import annotations
from csv import DictReader
from pathlib import Path
from math import sqrt, pi
from hashlib import sha256
P=Path(__file__).resolve().parent.parent/'assets'/'magnetostatica'

def read(name):
    with (P/name).open(newline='',encoding='utf8') as f:
        rows=[{k:float(v) for k,v in row.items()} for row in DictReader(f)]
    assert len(rows)==len({(x['r'],x['z']) for x in rows}),f'coordenadas repetidas en {name}'
    assert all(abs(x['B']-sqrt(x['Br']**2+x['Bz']**2))<1e-12 for x in rows),f'modulo inconsistente {name}'
    return {(x['r'],x['z']):x for x in rows}
rf=read('C-RF_1A.csv');ex=read('C-EXTRACT_1A.csv')
assert rf.keys()==ex.keys(), 'La geometría de las dos bobinas debe coincidir'
rs=sorted({r for r,z in rf});zs=sorted({z for r,z in rf})
assert (len(rs),len(zs),len(rf))==(27,42,1134)
assert all(abs((rs[i+1]-rs[i])-0.01)<1e-12 for i in range(len(rs)-1))
assert all(abs((zs[i+1]-zs[i])-0.01)<1e-12 for i in range(len(zs)-1))

def field_at(r,z,irf=41.4,iex=87.8):
    a=rf[(r,z)];b=ex[(r,z)]
    br=irf*a['Br']+iex*b['Br'];bz=irf*a['Bz']+iex*b['Bz']
    return br,bz,sqrt(br*br+bz*bz)
assert abs(field_at(0.,-.1)[1]-0.06360827210720629)<1e-10
assert abs(field_at(0.,0.)[1]-0.09864317919902911)<1e-10
bres=2*pi*2.45e9*9.1093837139e-31/1.602176634e-19
crossings=[]
for z0,z1 in zip(zs,zs[1:]):
    y0=field_at(0.,z0)[2]-bres;y1=field_at(0.,z1)[2]-bres
    if y0*y1<=0:
        crossings.append(z0+(z1-z0)*(-y0)/(y1-y0))
assert len(crossings)==2
assert abs(crossings[0]+0.0452327)<0.0001
assert abs(crossings[1]-0.0442487)<0.0001
print(f'OK: {len(rf)} nodos por bobina, 27 r × 42 z, Δ=10 mm')
print('I_RF=41.4 A, I_EX=87.8 A')
print('Bz(z=-100 mm,r=0):',round(field_at(0.,-.1)[1]*1000,3),'mT')
print('Bz(z=0,r=0):',round(field_at(0.,0.)[1]*1000,3),'mT')
print('B_ECR:',round(bres*1000,5),'mT')
print('Cruces axiales (mm):',*[round(z*1000,3) for z in crossings])
for name in ('C-RF_1A.csv','C-EXTRACT_1A.csv'):
    print('SHA256',name,sha256((P/name).read_bytes()).hexdigest())
