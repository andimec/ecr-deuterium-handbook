# Criterios de edición y verificación científica

## Tipos de afirmación

Separa explícitamente:

1. **Dato publicado o medido:** fuente, fecha, condiciones, incertidumbre, unidad y contexto del diagnóstico.
2. **Requisito de diseño:** documento de especificación; no confundir con rendimiento alcanzado.
3. **Estimación analítica:** fórmula, hipótesis, parámetros, unidad y rango de validez.
4. **Resultado numérico:** solver, versión, geometría, malla, convergencia, condiciones iniciales/de contorno, y comparación experimental.
5. **Hipótesis de trabajo:** indicar que aún no está validada.

## Convenciones y controles

- Emplear SI; electronvoltios como energía `k_B T` cuando proceda.
- No confundir potencia RF incidente, reflejada, absorbida y potencia electrostática del haz.
- Separar H₂ de D₂: bases de datos, masas, química isotópica, caudales y especies iónicas.
- No inferir `p` directamente de `sccm` sin velocidad efectiva de bombeo, temperatura y régimen de flujo.
- Distinguir el flujo total extraído de la corriente de D⁺ y de la corriente transportada al RFQ.
- Evitar atribuir propiedades específicas a LIPAc sin referencia publicada o autorización de datos internos.
- Añadir una cita bibliográfica para modelos materiales, tasas, parámetros experimentales y resultados controvertidos.
- Mantener pruebas de regresión para los calculadores y los resultados de referencia.

## Modificar una ecuación

1. Documentar su derivación y sus hipótesis.
2. Verificar unidades mediante análisis dimensional.
3. Probar límites conocidos (vacío, sin campo, simetría, campos homogéneos, etc.).
4. Añadir/comprobar cálculos automáticos para evitar regresiones.
5. Revisar concordancia con referencias citadas.

## Material no público

No incluir geometrías CAD institucionales, logs del inyector, consignas operativas internas ni resultados sujetos a restricciones sin permiso de publicación. El manual es educativo y de investigación, no un procedimiento operativo autorizado de la instalación.
