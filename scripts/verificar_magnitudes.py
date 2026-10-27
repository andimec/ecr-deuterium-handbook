"""Pruebas independientes de los ejemplos dimensionales del manual ECR.
Solo verifica identidades analíticas: NO valida física de una fuente real.
"""
from math import pi, sqrt

e = 1.602176634e-19
me = 9.1093837139e-31
mD = 3.3435837724e-27
kb = 1.380649e-23
eps0 = 8.8541878128e-12
mu0 = 1.25663706127e-6
c = 299792458

f = 2.45e9
omega = 2*pi*f
B = me*omega/e
ncrit = eps0*me*omega**2/e**2
molecules_per_sccm = 101325*(1e-6/60)/(kb*273.15)
ions_s = 0.140/e
beam_power = 0.140*100000
Te = 5
ne = 1e17
lambdaD = sqrt(eps0*Te/(ne*e))
rL = sqrt(2*Te*e/me)/omega
neutral_mfp = kb*300/(sqrt(2)*pi*(.30e-9)**2*.05)
cs = sqrt(Te*e/mD)

assert abs(B - .08752347556)/B < .00001
assert abs(ncrit - 7.44575675e16)/ncrit < .00001
assert abs(molecules_per_sccm - 4.47796685e17)/molecules_per_sccm < .00001
assert abs(beam_power - 14000) < .01
assert abs(lambdaD - .0525659e-3)/lambdaD < .0001
assert abs(rL - 86.1519e-6)/rL < .0001
assert abs(neutral_mfp - .2071701)/neutral_mfp < .0001
assert abs(cs - 15478.7)/cs < .0001

for name, v, unit in [
    ('Campo ECR', B*1000, 'mT'),
    ('Densidad crítica no magnetizada', ncrit, 'm^-3'),
    ('Moléculas/s por 1 sccm a 0 °C', molecules_per_sccm, 's^-1'),
    ('Flujo de deuterones a 140 mA', ions_s, 's^-1'),
    ('Potencia del haz a 100 kV', beam_power/1000, 'kW'),
    ('Longitud de Debye (ne=1e17, Te=5 eV)', lambdaD*1e3, 'mm'),
    ('Radio de Larmor electrónico', rL*1e6, 'micrómetros'),
    ('Recorrido libre neutro ilustrativo', neutral_mfp*100, 'cm'),
    ('Velocidad de Bohm ilustrativa', cs/1000, 'km/s'),
]: print(f'{name}: {v:.6g} {unit}')
print('PASS: comprobaciones de magnitud analítica.')
