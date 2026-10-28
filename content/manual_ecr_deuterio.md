# Física y simulación de un inyector ECR de deuterio a 2,45 GHz

**Manual técnico evolutivo · edición 1.0 · 27 de octubre de 2026**  
**Caso de estudio:** fuente ECR tipo SILHI/LIPAc; haz nominal de **D⁺ = 140 mA** y **100 keV**; microondas **2,45 GHz**; **600–900 W de RF suministrada** y **2–5 sccm de D₂** como intervalo de estudio facilitado para este manual. **Los últimos dos rangos no se presentan como valores operativos publicados y verificados de LIPAc.**

> **Cómo utilizar este manual.** Leer los capítulos en orden constituye el hilo físico recomendado. En cada uno se indican aplicación, formulación e hipótesis, aproximaciones numéricas, órdenes de magnitud y bibliografía. La edición científica se realiza en este archivo Markdown. La versión HTML contiene calculadoras y tablas derivadas, y puede regenerarse ejecutando `python construir_manual.py`. Los resultados interactivos son **estimaciones analíticas**, no simulaciones ni mediciones del inyector.

> **Convenciones.** SI en las ecuaciones; las temperaturas electrónicas expresadas en eV significan $k_BT_e=e\,T_e[\mathrm{eV}]$. $D_2$ es gas neutro molecular; $D^+$ un deuterón; $D_2^+$ y $D_3^+$ son iones moleculares. La potencia de *microondas* no es la potencia del acelerador RFQ ni la potencia del haz. Cuando aparezcan parámetros no medidos, se marcarán como **supuesto ilustrativo**.

## 1. El sistema físico completo y sus límites

### Aplicación al inyector

Una fuente ECR introduce moléculas de deuterio en una cámara evacuada. Un magnetrón de 2,45 GHz entrega una onda electromagnética a través de una guía y un acoplamiento; un campo magnético de bobinas coloca regiones de la cámara cerca de la resonancia ciclotrónica electrónica. Los electrones ganan energía, chocan con $D_2$, disocian e ionizan; los iones se aceleran electrostáticamente, atraviesan electrodos de extracción y pasan a la LEBT. El objetivo es obtener alta corriente **de deuterones** con una distribución de especies, emitancia y estabilidad aceptables. El requisito nominal LIPAc de 140 mA a 100 keV está documentado [R1, R2].

**No confundir tres corrientes:** corriente total extraída, corriente de $D^+$ y corriente transportada a la entrada del RFQ. Tampoco mezclar potencias: $P_{\rm RF,forward}$, $P_{\rm RF,abs}$, $P_{\rm beam}=IV$, pérdidas eléctricas en fuentes HV y pérdidas térmicas de paredes.

### Formulación e hipótesis

La descripción rigurosa resulta del sistema acoplado: Maxwell para $\mathbf E,\mathbf B$; cinética de Boltzmann/Vlasov para $f_s(\mathbf x,\mathbf v,t)$; colisiones/reacciones; balances de neutrales; ecuación de Poisson y contornos electrostáticos para extracción; y modelos de superficie. Una ecuación esquemática de especie es

$$\frac{\partial f_s}{\partial t}+\mathbf v\cdot\nabla_{\mathbf x}f_s+\frac{q_s}{m_s}(\mathbf E+\mathbf v\times\mathbf B)\cdot\nabla_{\mathbf v}f_s=C_s[f]+S_s.$$

La hipótesis más importante es definir la **frontera de cada subsistema**: ¿la RF es prescrita o autoconsistente?, ¿los neutrales son un campo de fondo o partículas?, ¿el sheath se resuelve o se modela?, ¿hay gas reciclado en superficies? Sin esa definición podemos contar dos veces cargas, energía y colisiones.

### Modelos y software

Un enfoque gradual es: FEMM/superB para $\mathbf B_0$; Struphy/Meep para RF; PICLas para partículas, Poisson, colisiones y superficies; Molflow+ o SPARTA para neutrales dependiendo de Knudsen; un modelo reducido 0D para comprobar química y balance energético [R10–R15]. Ninguna herramienta, por sí sola, proporciona automáticamente el gemelo digital validado de la fuente.

### Órdenes de magnitud

Para $I_{D^+}=0.140$ A y $V=100$ kV, $P_{\rm beam,D^+}=14$ kW, y $\dot N_{D^+}=I/e\approx8.74\times10^{17}\ \mathrm{s^{-1}}$. Son magnitudes **del haz**, no potencias generadas por microondas. Si hay corriente adicional de $D_2^+$ y $D_3^+$, la potencia total del haz incluye esas contribuciones a igual potencial de aceleración.

### Lecturas clave

LIPAc [R1, R2, R3]; revisión ECR [R4]; PIC ECR reciente [R5].

## 2. Gas de alimentación: sccm, caudal de partículas y balances

### Aplicación al inyector

La inyección de 2–5 sccm establece una **entrada de moléculas**, no la presión ni la densidad de neutrales dentro del plasma. Estas dependen de la velocidad efectiva de bombeo, conductancias, gas caliente, reacciones, superficie y geometría. La unidad sccm depende de la condición estándar usada por el instrumento.

### Formulación e hipótesis

Usando **0 °C y 1 atm únicamente como referencia explícita de conversión**,

$$1\ \mathrm{sccm}=\frac{10^{-6}}{60}\ \mathrm{m^3\,s^{-1}}\quad\text{(volumen estándar)}.$$

$$\dot N_{D_2}=\frac{p_{\rm std}\dot V_{\rm std}}{k_BT_{\rm std}},\qquad \dot N_{D,\rm in}=2\dot N_{D_2}.$$

La equivalencia de throughput a la temperatura del gas real es $Q(T_g)=\dot N_{D_2}k_BT_g$ en Pa·m³/s. Solo para un volumen aproximadamente isotérmico, estacionario y con una velocidad efectiva de bombeo conocida, $p\simeq Q/S_{\rm eff}$. El gas disociado, ionizado o reemitido modifica esta aproximación.

Definimos una cota cinemática para utilización atómica de gas:

$$\eta_{D,\rm gas}=\frac{\dot N_{D^+,\rm beam}}{2\dot N_{D_2,\rm in}}=\frac{I_{D^+}}{2e\dot N_{D_2}}.$$

Esto **no es eficiencia de ionización interna ni de extracción**. Supone corriente atribuible a deuterones monovalentes y alimentación pura de $D_2$; moléculas de gas recicladas y fuentes adicionales requieren ampliar el balance.

### Modelos y simplificaciones

0D: fijar $\dot N$, $S_{\rm eff}$ y $T_g$; 1D/3D: conductancias, geometría, temperaturas y perfiles de presión; Molflow+ cuando el transporte molecular predomina; DSMC cuando colisiones entre neutros importan. PICLas puede tratar gases de fondo o dinámicos según el módulo y el régimen [R10, R14, R15].

### Órdenes de magnitud

Con referencia **0 °C**, 1 sccm equivale aproximadamente a $4.48\times10^{17}$ moléculas/s. Así, 2–5 sccm corresponden a $(0.896–2.24)\times10^{18}$ moléculas $D_2$/s, o el doble en átomos de D. Para 140 mA exclusivamente de $D^+$ la cota $\eta_{D,\rm gas}$ vale aproximadamente **49% a 2 sccm** y **20% a 5 sccm**. Un porcentaje imposible (>100%) indicaría inconsistencia entre corriente atribuida, medida de flujo y definición estándar.

### Lecturas clave

Metrología y operación LIPAc [R1, R3]; flujo molecular [R14]; DSMC [R15].

## 3. Vacío y flujo rarificado: ¿Molflow+, DSMC o continuo?

### Aplicación al inyector

La cámara y el sistema de bombeo no están necesariamente en el mismo régimen de flujo. Una línea de entrada estrecha puede operar en régimen continuo/viscoso, la cámara en transición y una región aguas abajo a vacío elevado en régimen molecular. **Es erróneo seleccionar Molflow+ solo porque el sistema se denomina “vacío”.**

### Formulación e hipótesis

Para moléculas neutras aproximadamente como esferas duras:

$$n_g=\frac{p_g}{k_BT_g},\qquad \lambda_g=\frac{k_BT_g}{\sqrt{2}\pi d^2p_g},\qquad \mathrm{Kn}=\frac{\lambda_g}{L}.$$

$d$ es diámetro de colisión efectivo **supuesto**, no una constante universal; depende de especie y modelo. Una guía habitual es: $\mathrm{Kn}<0.01$ continuo, $0.01$–$0.1$ deslizamiento, $0.1$–$10$ transición y $\mathrm{Kn}>10$ molecular libre. Son fronteras orientativas, no cambios bruscos de física.

En flujo molecular, partículas neutras avanzan casi balísticamente entre superficies y la conductancia suele escalar aproximadamente como $1/\sqrt{M}$. En transición, el operador de Boltzmann y las colisiones intermoleculares no pueden omitirse. Para neutrales dinámicos:

$$\partial_t f_n+\mathbf v\cdot\nabla f_n=C_{nn}[f_n]+C_{n\!p}[f_n,f_p]+S_{\rm in}-S_{\rm wall}.$$

### Modelos y software

**Molflow+**: Monte Carlo de moléculas de prueba y choques con paredes, apropiado si $\mathrm{Kn}\gg1$; no resuelve colisiones entre moléculas. **SPARTA**: DSMC, resuelve colisiones gas-gas y superficies y necesita pasos temporales y celdas adecuados a escalas cinéticas [R14, R15]. **PICLas DSMC** puede reducir el número de códigos en una arquitectura integrada, previa validación de sus límites. Navier–Stokes es útil solo donde exista separación de escalas suficiente; los modelos difusos requieren coeficientes de acomodación y condiciones de pared.

### Órdenes de magnitud

**Supuesto ilustrativo, NO presión LIPAc:** $p_g=0.05$ Pa, $T_g=300$ K, $d=0.30$ nm y $L=0.10$ m producen $\lambda_g\approx0.21$ m y $\mathrm{Kn}\approx2.1$: régimen de transición. Así, Molflow+ aislado no sería automáticamente válido en toda la cámara. Cambiar diámetro efectivo, presión o longitud geométrica modifica el diagnóstico de régimen.

### Lecturas clave

Guía SPARTA [R15]; Molflow+ [R14]; PICLas DSMC/background gas [R10, R11].

## 4. Magnetostática y superficies de resonancia

### Aplicación al inyector

La corriente de las bobinas configura $B_r(r,z)$ y $B_z(r,z)$, la topología de confinamiento y las superficies donde los electrones responden resonantemente a 2,45 GHz. Las partículas D⁺ son mucho más pesadas: la ECR fundamental es **electrónica**, no deuterónica.

### Formulación e hipótesis

$$\nabla\times\mathbf H=\mathbf J_{\rm bobinas},\quad \nabla\cdot\mathbf B=0,\quad\mathbf B=\nabla\times\mathbf A.$$

$$\omega_{ce}=\frac{e|\mathbf B_0|}{m_e},\qquad B_{\rm ECR}=\frac{2\pi m_ef_{\rm RF}}{e}.$$

Si la geometría es axisimétrica puede resolverse en 2D $(r,z)$ y reconstruirse en 3D. Eso requiere $B_x=B_r x/r$, $B_y=B_r y/r$ y tratamiento especial del eje $r=0$. En geometrías con multipolos/asimetría es necesario un cálculo 3D. El plasma de beta pequeño puede permitir despreciar inicialmente su retroacción magnetostática, pero no su efecto dieléctrico RF.

### Modelos y software

FEMM: magnetostática plana y axisimétrica; PICLas `superB` o campo externo tabulado; GetDP/Elmer para magnetostática 3D si la simetría no es suficiente. La interpolación debe controlar $\nabla\cdot\mathbf B$, el error del módulo $B$ y la posición de la capa ECR [R10, R12].

### Órdenes de magnitud

$B_{\rm ECR}=87.52$ mT para 2.45 GHz. En ese campo, $f_{c,D^+}\simeq0.667$ MHz, frente a 2450 MHz para electrones. Para electrones característicos de 5 eV, $v_{\rm th}=\sqrt{2eT_e/m_e}\approx1.33\times10^6$ m/s y $\rho_e\approx86\ \mu$m.

### Lecturas clave

Revisión ECR [R4]; FEMM [R12]; modelos magnetizados [R13].


### Caso real de estudio: dos bobinas con mapas FEMM a 1 A

Los siguientes campos son **resultados aportados por el usuario**, no una simulación nueva ni una medición de campo. El archivo `C-RF_1A.csv` contiene el campo de la **bobina RF** a 1 A y `C-EXTRACT_1A.csv` contiene el de la **bobina de extracción** a 1 A. Cada CSV tiene las columnas `r,z,B,Br,Bz`, con posición en metros y campo en teslas. Ambos comparten una malla rectangular axisimétrica de **42 posiciones en z** (−0,250 a +0,160 m) y **27 posiciones en r** (0 a 0,260 m), espaciadas 0,010 m. La columna `B` representa el módulo del campo de cada bobina por separado; **no deben sumarse los módulos**.

Para las corrientes de trabajo iniciales:

- **Bobina RF:** $I_{\rm RF}=41.4$ A.
- **Bobina de extracción:** $I_{\rm EX}=87.8$ A.

Si se cumple la aproximación magnetostática lineal, la superposición vectorial proporciona:

$$B_r(r,z)=I_{\rm RF}B_{r,{\rm RF},1A}(r,z)+I_{\rm EX}B_{r,{\rm EX},1A}(r,z),$$

$$B_z(r,z)=I_{\rm RF}B_{z,{\rm RF},1A}(r,z)+I_{\rm EX}B_{z,{\rm EX},1A}(r,z), \qquad |\mathbf B|=\sqrt{B_r^2+B_z^2}.$$

El escalado es exacto para un modelo magnetostático lineal con geometría y permeabilidades constantes. **No queda demostrado por disponer de mapas a 1 A que sea exacto si hay acero ferromagnético saturable, histéresis o cualquier otro elemento no lineal**. En ese caso se requiere un barrido del solver magnetostático a distintas corrientes o una validación con mediciones.

**Valores de referencia obtenidos de los CSV**, a 41,4 A y 87,8 A:

| Observable sobre el eje, $r=0$ | Resultado |
|---|---:|
| $B_z$ en $z=-100$ mm | 63,61 mT |
| $B_z$ en $z=0$ mm | 98,64 mT |
| Primer cruce de $|\mathbf B|=B_{\rm ECR}$ | $z\approx-45,2$ mm |
| Segundo cruce de $|\mathbf B|=B_{\rm ECR}$ | $z\approx+44,2$ mm |
| Máximo $|\mathbf B|$ **sobre el eje** de la malla | 98,64 mT |

Se ha utilizado $B_{\rm ECR}=87,523$ mT, correspondiente a 2,45 GHz y electrones no relativistas; los cruces resultan de interpolación lineal entre nodos separados 10 mm. **No son una determinación experimental de la región de absorción ECR.** El mapa completo incluye posiciones fuera de la cámara indicada por las superposiciones geométricas del visor; no debe interpretarse su máximo global como el campo dentro del plasma.

### Laboratorio de magnetostática interactivo

El siguiente visor reproduce y amplía el HTML proporcionado originalmente. Mantiene las vistas $|B|$, $B_r$, $B_z$, vectores, isocontornos con suavizado opcional, geometrías superpuestas, perfil axial, sondas por coordenadas o clic, resolución inversa de corrientes para dos puntos y búsqueda de cruces en el eje. Carga automáticamente ambos mapas originales a 1 A, permite sustituirlos y exportar el campo combinado. Las corrientes se sincronizan con el panel de condiciones iniciales del manual.

**Interpretación:** el isocontorno representa una superficie geométrica de módulo magnético; no calcula por sí solo deposición de potencia, EEDF ni calentamiento. El suavizado cambia solamente la representación del contorno. La interpolación y las búsquedas están limitadas por la resolución de los CSV.

[[ECR_MAGNETIC_VIEWER]]

## 5. RF: propagación, guía, cavidad, polarización y potencia real

### Aplicación al inyector

El magnetrón entrega 600–900 W **nominales para los escenarios del documento**. Parte puede reflejarse en el sistema de acoplamiento o disiparse en paredes y ventanas. Solo el remanente efectivamente transferido a partículas y procesos del plasma determina su calentamiento. La frecuencia de 2,45 GHz corresponde a una longitud de onda de vacío comparable a dimensiones de fuentes ECR compactas: no puede suponerse un campo eléctrico espacialmente uniforme.

### Formulación e hipótesis

$$\nabla\times\mathbf E=-\partial_t\mathbf B,\qquad\nabla\times\mathbf H=\mathbf J+\partial_t\mathbf D.$$

En régimen armónico $e^{-i\omega t}$, una formulación de ondas es:

$$\nabla\times\mu_r^{-1}\nabla\times\widetilde{\mathbf E}-k_0^2\boldsymbol\varepsilon_r(\omega,\mathbf x)\widetilde{\mathbf E}=i\omega\mu_0\widetilde{\mathbf J}_{\rm ext}.$$

La potencia incidente y reflejada puede estimarse con $|S_{11}|^2=P_{\rm refl}/P_{\rm inc}$ si la definición de puerto y calibración es apropiada. Un balance completo es $P_{\rm inc}=P_{\rm refl}+P_{\rm otros\ puertos}+P_{\rm paredes}+P_{\rm plasma}+dU_{\rm EM}/dt$. **No identificar** $P_{\rm plasma}$ con $P_{\rm inc}$ ni con $P_{\rm inc}-P_{\rm refl}$ cuando hay pérdidas adicionales.

### Modelos y software

Meep: FDTD temporal, opción girotrópica experimental; Struphy: Maxwell FEEC y `ColdPlasma`; solver RF FEM en frecuencia: materiales anisótropos, puertos y campos complejos. En todos ellos deben verificarse paredes PEC finitas, impedancia de puerto, acoplamiento real, pérdidas, reflexión y convergencia de malla [R5, R13]. El tensor frío puede ser adecuado para propagación, no constituye por sí solo un modelo de calentamiento cinético.

### Órdenes de magnitud

$\lambda_0=c/f\approx12.24$ cm; periodo RF $T=1/f\approx408$ ps. Un cálculo de demostración con $P_{\rm inc}=750$ W, 10% de reflexión y 20% de pérdidas del remanente entrega $P_{\rm plasma}\approx540$ W: **ejemplo ficticio de balance, no medición**. La densidad de campo y los máximos locales dependen de la geometría, puertos, densidad y polarización; no se pueden inferir solamente a partir de los vatios.

### Lecturas clave

PIC RF ECR de 2,45 GHz [R6, R7]; Struphy [R13]; Meep [R16].

## 6. Dispersión de plasma frío y cuándo deja de ser válida

### Aplicación al inyector

A medida que aumenta $n_e$, el plasma modifica la onda incidente: aparecen cutoffs, modos R/L, regiones resonantes y fenómenos de conversión. El corte de plasma **no magnetizado** es útil como referencia, pero no representa la transmisión completa en un plasma magnetizado anisótropo.

### Formulación e hipótesis

La frecuencia de plasma es $\omega_{pe}=\sqrt{n_e e^2/(\varepsilon_0m_e)}$. El plasma frío desprecia presión térmica y dispersión de velocidades en la respuesta RF. Para un campo uniforme $\mathbf B_0$ en $z$, el tensor dieléctrico tiene la forma:

$$\boldsymbol\varepsilon_r=\begin{pmatrix} S&-iD&0\\ iD&S&0\\0&0&P\end{pmatrix},\quad S=\frac{R+L}{2},\quad D=\frac{R-L}{2}.$$

$$R=1-\sum_s\frac{\omega_{ps}^2}{\omega(\omega+\Omega_s)},\qquad L=1-\sum_s\frac{\omega_{ps}^2}{\omega(\omega-\Omega_s)},\quad P=1-\sum_s\frac{\omega_{ps}^2}{\omega^2}.$$

Aquí $\Omega_s=q_sB_0/m_s$ **con signo**; el nombre R/L depende de convención de propagación y polarización, por lo que debe comprobarse en el solver. La versión sin colisiones es ideal y local. Si un solver introduce $\nu$ efectivo en el tensor, su significado y el balance de energía deben justificarse.

### Modelos y simplificaciones

Struphy `ColdPlasma` contiene una ecuación de corriente acoplada a Maxwell; Meep ofrece susceptibilidades Drude girotrópicas experimentales; un tensor caliente requiere integrar una distribución electrónica, no únicamente sustituir $T_e$ en la matriz fría. Es posible representar absorción efectiva mediante amortiguamiento calibrado, pero no equivale a resolver Vlasov-PIC [R13, R16, R7].

### Órdenes de magnitud

Para 2,45 GHz, $n_{\rm crit}=\varepsilon_0m_e\omega^2/e^2\approx7.45\times10^{16}$ m⁻³. Si $n_e=10^{17}$ m⁻³, $f_{pe}\approx2.84$ GHz, mayor que $f_{\rm RF}$. **No concluye que la onda no entre**: modos magnetizados y gradientes requieren analizar el tensor completo. La estimación térmica de corrección lejos de resonancia utiliza $\eta=|k_\parallel|v_{\rm th}/|\omega-\omega_{ce}|$; cuando $\eta\gtrsim1$, la aproximación fría deja de estar controlada.

### Lecturas clave

Revisión ECR [R4]; Neri [R7]; Struphy [R13].

## 7. ECRH: cómo los electrones absorben realmente energía

### Aplicación al inyector

El calentamiento ECR impulsa electrones hasta energías que permiten disociar e ionizar $D_2$. Sin embargo, la transferencia RF-electrón depende de la órbita, fase relativa con la RF, tiempo de residencia en la zona ECR y distribución de velocidades. No basta con dibujar la superficie $B=B_{\rm ECR}$.

### Formulación e hipótesis

$$\frac{d\mathbf p}{dt}=q(\mathbf E+\mathbf v\times\mathbf B),\qquad \frac{dK}{dt}=q\mathbf v\cdot\mathbf E.$$

La resonancia relativista/ Doppler puede escribirse:

$$\omega-k_\parallel v_\parallel=\frac{n\omega_{ce}}{\gamma},\quad \gamma=(1-v^2/c^2)^{-1/2},\quad n=1,2,\ldots$$

La componente RF con polarización correcta es fundamental. El campo magnético por sí solo no realiza trabajo ($\mathbf v\cdot(\mathbf v\times\mathbf B)=0$). La dinámica puede describirse mediante Vlasov-Boltzmann/PIC-MCC; un modelo cuasilineal promedia fases y representa difusión en velocidad bajo hipótesis de aleatorización de fase y amplitudes suficientemente débiles.

La potencia realmente transferida a electrones PIC es $P_{e\leftarrow\rm RF}=\int\mathbf J_e\cdot\mathbf E_{\rm RF}\,dV$ (con signos y convenciones de corriente consistentes), o suma $\sum_p q_p\mathbf v_p\cdot\mathbf E_{\rm RF}(\mathbf x_p)$ en partículas ponderadas. Una disipación añadida en Maxwell **no puede añadirse otra vez** a las partículas sin reconciliar el balance.

### Modelos y simplificaciones

**Cold plasma ideal:** ondas y corriente colectiva, pero sin temperatura ni deposición irreversible en la distribución electrónica. **Modelo colisionado:** respuesta compleja efectiva $\nu_{\rm eff}$, cuya interpretación física debe calibrarse. **Test-particles:** RF y B prescritos, sin realimentación. **PIC electromagnético autoconsistente:** partículas y Maxwell; **PIC-MCC:** añade ionización/pérdidas. `ColdPlasmaVlasov` de Struphy ofrece fluido frío más población electrónica cinética, pero no química colisional nativa equivalente a PICLas [R5, R13].

### Órdenes de magnitud

Para $T_e=5$ eV, $v_{\rm th}\approx1.33\times10^6$ m/s y $\rho_e\approx86$ µm en 87.5 mT. El período RF es 408 ps; un paso conservador $\Delta t=0.02/\omega_{ce}\approx1.30$ ps implicaría $\sim7.7\times10^7$ pasos por 100 µs. **No significa que todos los algoritmos PIC estén obligados a ese paso**: es una referencia de resolución orbital; esquemas implícitos/reducidos deben validarse por separado. La frecuencia electrónica de colisiones varía según EEDF y secciones eficaces; no fijarla únicamente con sccm.

### Lecturas clave

Eremin y col. PIC-MCC [R5]; Neri [R7]; revisión ECR [R4].

## 8. Estado del plasma: temperatura, densidad, presión y escalas

### Aplicación al inyector

La fuente es un plasma de baja temperatura iónica y neutrales relativamente fríos, pero con electrones más energéticos y fuera de equilibrio térmico. Hablar de *temperatura del plasma* como una sola variable suele ser insuficiente. La EEDF puede no ser Maxwelliana y pueden existir poblaciones caliente/fría y anisotropía $T_\perp\ne T_\parallel$.

### Formulación e hipótesis

Para Maxwelliana isótropa, $\langle K_e\rangle=\tfrac32 k_BT_e$, $p_e=n_ek_BT_e$. La longitud de Debye y la frecuencia plasma son

$$\lambda_D=\sqrt{\frac{\varepsilon_0 k_BT_e}{n_e e^2}},\qquad\omega_{pe}=\sqrt{\frac{n_e e^2}{\varepsilon_0m_e}}.$$

El plasma beta electrónico es $\beta_e=2\mu_0p_e/B^2$. Para una distribución no isotrópica, reemplazar la presión escalar por momentos $\mathbf P_e=m_e\int(\mathbf v-\mathbf u_e)(\mathbf v-\mathbf u_e)f_e\,d^3v$. La cuasineutralidad en el volumen se aproxima por $n_e\simeq n_{D^+}+n_{D_2^+}+n_{D_3^+}+\cdots$, pero **no aplica dentro de sheaths y capas de carga**.

### Modelos y simplificaciones

0D global: densidades y energía promediadas; drift-diffusion: cierre fluido con movilidad/difusión; Vlasov: sin colisiones; PIC-MCC: distribuciones y efectos no locales. En FEM/fluidos se debe justificar un cierre para energía y transporte; usar una única $T_e$ puede fallar en tasas de reacción de alto umbral [R5, R8].

### Órdenes de magnitud

**Ejemplo, no medición:** $n_e=10^{17}$ m⁻³, $T_e=5$ eV, $B=0.08752$ T → $\lambda_D\approx0.0526$ mm; $p_e\approx0.080$ Pa; $p_B\approx3.05$ kPa; $\beta_e\approx2.63\times10^{-5}$. Esto sugiere pequeña modificación magnetostática por presión, pero no efecto dieléctrico RF pequeño.

### Lecturas clave

Revisión ECR [R4]; Eremin [R5]; modelo de química 0D/3D [R8].

## 9. Química de deuterio: cómo aparecen D⁺, D₂⁺ y D₃⁺

### Aplicación al inyector

El criterio de éxito no es producir cualquier ion, sino una gran fracción de $D^+$ y cumplir requisitos de corriente/emitancia. Iones moleculares transportan carga y pueden contribuir a la corriente eléctrica total, pero tienen masa/carga diferente y responden de forma distinta en extracción y transporte.

### Formulación e hipótesis

Reacciones representativas — **no mecanismo completo ni listado de tasas validadas**:

1. $e+D_2\rightarrow D_2^++2e$ (ionización molecular).
2. $e+D_2\rightarrow D+D+e$ (disociación).
3. $e+D_2\rightarrow D^++D+2e$ (ionización disociativa).
4. $e+D\rightarrow D^++2e$ (ionización atómica).
5. $D_2^++D_2\rightarrow D_3^++D$ (conversión ion-molécula).
6. $D_2^++e\rightarrow D+D$ (recombinación disociativa).
7. Excitación vibracional/rotacional/electrónica de $D_2$ y procesos de pared.

Para una reacción electrón-neutral, $k_j=\langle\sigma_j(E)v(E)\rangle_{\rm EEDF}$, $R_j=k_j n_e n_{D_2}$ para binaria con neutral molecular. Para una población térmica Maxwelliana, usar un promedio de Maxwell. Para EEDF no Maxwelliana, usar histogramas cinéticos y secciones eficaces originales.

En un mecanismo 0D $dn_i/dt=\sum_r\nu_{ir}R_r-\Gamma_i A/V$, con términos de entrada, pérdidas y superficie especificados. Cada reacción debe conservar número de núcleos de deuterio y carga eléctrica.

### Modelos y simplificaciones

PICLas MCC/XSec, DSMC y química: reacción por probabilidad $P=1-\exp(-n_g\sigma(E)v\Delta t)$ para un blanco de fondo fijo y un canal definido; enfoque de colisiones nulas cuando sea adecuado [R11]. 0D global o PLASIMO/COMSOL para barridos de parámetros; **no aplicar automáticamente secciones $H_2$ a $D_2$**: diferencias vibratorias, disociativas y de transferencia de carga pueden importar. Struphy Vlasov no incluye por sí mismo el mecanismo completo de reacciones [R9, R13].

### Órdenes de magnitud

Umbrales energéticos de referencia: disociación $D_2\to2D$ del orden de **4.6 eV** e ionización molecular $D_2\to D_2^+$ del orden de **15.5 eV**. Son energías umbral, **no energías medias requeridas por cada deuterón extraído**. La química depende fuertemente de la cola energética; dos EEDF con la misma energía media pueden tener tasas de ionización diferentes. Las tasas numéricas deberán tomarse de datos de $D_2$ específicos [R9].

### Lecturas clave

Revisión de secciones eficaces de deuterio [R9]; modelo 28 reacciones (para hidrógeno, como comparación) [R8]; PICLas MCC [R11].

## 10. Paredes, BN, emisión secundaria, sheaths y reciclaje

### Aplicación al inyector

Las paredes absorben partículas y energía, recombinan D atómico y reciben impactos iónicos/electrónicos. Los discos y superficies de nitruro de boro pueden cargarse y emitir electrones secundarios. Esto modifica potencial, pérdidas electrónicas, EEDF y estabilidad. La duración del disco necesita física de erosión independiente de la dinámica de plasma.

### Formulación e hipótesis

Poisson: $\nabla\cdot(\varepsilon\nabla\phi)=-\rho$, $\mathbf E_{\rm ES}=-\nabla\phi$. En una interfaz dieléctrica, $\hat n\cdot(\mathbf D_2-\mathbf D_1)=\sigma_s$. La carga superficial evoluciona por corrientes incidentes, emisión secundaria y fugas superficiales/volumétricas:

$$\partial_t\sigma_s=J_{\rm incident,n}-J_{\rm emitted,n}-J_{\rm leakage,n}.$$

La convención algebraica de signos debe mantenerse en el código. Para un sheath no colisional simple, criterio de Bohm $u_i\gtrsim c_s=\sqrt{k_BT_e/m_i}$ (iones fríos, electrones Maxwellianos, ionización débil dentro del sheath). Si hay especies moleculares, temperaturas distintas o colisiones, se necesita una generalización.

### Modelos y simplificaciones

PICLas documenta emisión secundaria y carga de dieléctricos resueltos, con restricciones por método de deposición; Struphy dispone de fronteras cinéticas básicas pero no de un conjunto equivalente de procesos plasma-BN [R10]. Una frontera absorbente ideal sin SEE puede servir para una primera prueba, pero no para predecir envejecimiento o estabilidad. El coeficiente $\delta(E,\theta)$ de SEE, rendimiento de sputtering y coeficientes de reciclaje deben medirse o extraerse de datos para BN y D, con incertidumbre explícita.

### Órdenes de magnitud

Si $T_e=5$ eV, $c_{s,D^+}\approx15.5$ km/s. No confundir esa velocidad de entrada al sheath con la velocidad final a 100 keV ($\sim3.10\times10^6$ m/s), que procede de la aceleración externa. La longitud de Debye ilustrativa de 0.053 mm exige cuidado numérico en regiones de carga, aunque las simulaciones de plasma cuasineutro pueden modelar el sheath mediante condiciones efectivas.

### Lecturas clave

PICLas fronteras [R10]; revisión no equilibrio y sheaths [R17]; Neri [R7].

## 11. Extracción, espacio de carga y LEBT

### Aplicación al inyector

Los iones que alcanzan el menisco se extraen mediante electrodos HV y aceleran hacia 100 keV por carga elemental. La corriente **de deuterones** no equivale necesariamente a la corriente total si hay $D_2^+$ o $D_3^+$. La LEBT incorpora solenoides y compensación de carga espacial por electrones secundarios/residuales; la corriente transportada puede diferir de la extraída.

### Formulación e hipótesis

En modelo 1D estacionario limitado por espacio de carga, ley de Child–Langmuir:

$$J_{\rm CL}=\frac49\varepsilon_0\sqrt{\frac{2q}{m_i}}\frac{V^{3/2}}{d^2}.$$

Para partículas de carga $+e$, $K=eV$ y $v=\sqrt{2eV/m_i}$ en aproximación no relativista. La potencia del haz es $P_{\rm beam}=\sum_j I_jV$ si todas las especies monovalentes experimentan el mismo potencial. La envolvente del haz y la perveancia generalizada introducen las fuerzas de espacio de carga y focalización; la compensación espacial modifica el potencial pero no debe confundirse con ausencia de carga.

### Modelos y simplificaciones

Poisson/PIC para menisco, óptica y space charge; trazado de partículas en campos prescritos para primeras aproximaciones; IBSimu, PICLas o códigos ópticos de haces especializados según objetivo y modelo de menisco. Child–Langmuir es una **estimación 1D ideal**, no un cálculo del extractor real con varios electrodos. El RFQ/LEBT necesita su propio modelo de transporte [R1–R3].

### Órdenes de magnitud

D⁺ a 100 keV: $v\approx3.10\times10^6$ m/s. 140 mA: $8.74\times10^{17}$ iones/s y 14 kW; si el modo fuese CW, esa es potencia continua de deuterones. Para 600–900 W de RF suministrada, **no** deducir eficiencia energética $14\,\mathrm{kW}/P_{\rm RF}>1$ como violación: la energía cinética la entrega la fuente de alta tensión.

### Lecturas clave

Documentación técnica LIPAc [R1–R3]; aceptación de inyector [R2].

## 12. Estrategias numéricas: de 0D hasta modelos acoplados HPC

### Aplicación al inyector

Para investigar física y desarrollar un código útil, conviene aumentar complejidad según el observable: $n_{D^+}$ y fracciones iónicas globales, distribución RF, calentamiento electrónico o emitancia requieren niveles diferentes. El coste de simular ciclos de 2,45 GHz durante decenas de microsegundos es enorme; evitar mezclar todos los tiempos y escalas sin necesidad.

### Formulación e hipótesis

**0D:** balances temporales promediados espacialmente. **Fluido:** densidad, velocidad, energía con cierres constitutivos. **PIC electrostático-MCC:** resuelve órbitas bajo RF prescrita, campo electrostático propio y colisiones. **PIC electromagnético:** Maxwell autoconsistente, corrientes PIC y colisiones. **Acoplamiento híbrido:** solver RF calcula campos con propiedades promedio $n_e, f_e$; el PIC actualiza cinética y química, iterando hasta convergencia.

Las restricciones numéricas de PIC explícito suelen exigir resolver escalas de plasma, Debye, giro y CFL según esquema:

$$\omega_{pe}\Delta t\ll1,\quad \Delta x/\lambda_D\ \text{controlado},\quad\omega_{ce}\Delta t\ll1\quad(\text{según algoritmo y precisión}).$$

Las técnicas implícitas o subciclado cambian restricciones de estabilidad, **no eliminan la necesidad de verificar precisión física**. En el acoplamiento RF-PIC hay que evitar doble conteo de corrientes y potencia: Struphy fluido y PICLas no deben responder simultáneamente a la misma población de electrones sin corrección.

### Formulaciones y herramientas

| Herramienta | Fortalezas relevantes | Limitaciones a validar para D₂ ECR |
|---|---|---|
| PICLas | PIC/Poisson/Maxwell, MCC y superficies, MPI | Inyección RF prescrita y química D₂ completa, coste 3D |
| Struphy | Maxwell-FEEC, ColdPlasma, VlasovMaxwell, ColdPlasmaVlasov | MCC D₂ y superficies no equivalentes; puertos y geometría |
| Meep | FDTD, medios dispersivos/girotrópicos experimentales | Absorción cinética y estabilidad RF magnetizada heterogénea |
| FEMM | Solenoides y magnetostática axisimétrica | No magnetostática 3D arbitraria |
| Molflow+ | Monte Carlo de neutros en régimen molecular | No colisiones gas-gas en transición |
| SPARTA | DSMC en gas rarificado con colisiones | No plasma PIC/electromagnetismo por sí solo |
| 0D químico | Muy rápido, valida balances/reacciones | No resuelve campos, sheath y geometría 3D |

Las funcionalidades se fundamentan en manuales y repositorios [R10–R16]. La **exactitud relativa y el rendimiento** entre herramientas todavía requieren pruebas propias; no se infieren de que el software anuncie un método de alto orden.

### Órdenes de magnitud

A $n_e=10^{17}$ m⁻³ y $T_e=5$ eV, $\lambda_D\approx0.053$ mm. Un volumen hipotético 100 × 100 × 200 mm refinado de forma uniforme a esa escala requeriría del orden de $10^{10}$ celdas: **demostración de inviabilidad de discretización homogénea, no propuesta de malla**. La fase inicial debe usar casos reducidos y benchmarks antes de HPC.

### Lecturas clave

PICLas [R10, R11]; Struphy [R13]; Eremin [R5]; Neri [R7].

## 13. Validación y incertidumbre: qué datos hacen falta

### Aplicación al inyector

Un software que produce curvas plausibles todavía no es predictivo. Debemos demostrar resultados reproducibles para la configuración concreta de deuterio. La primera campaña debe separar datos usados para calibrar del conjunto independiente reservado para validar.

### Formulación e hipótesis

Usar conservación de carga $dQ/dt+\oint\mathbf J\cdot d\mathbf A=\text{fuentes}$, balance de partículas D por núcleos, energía electromagnética (teorema de Poynting) y balance de potencia de partículas/reacciones. La medida de una tasa $R$ depende de $n$, $f_e$ y $\sigma(E)$; la incertidumbre de cada entrada debe propagarse, por ejemplo mediante barridos de sensibilidad o Monte Carlo de parámetros.

**No confundir validación** (coincidencia con observaciones independientes) **con verificación** (resolver correctamente las ecuaciones implementadas).

### Métodos y software

Benchmarks: órbita ciclotrónica; dispersión R/L y rotación de Faraday; ionización de una celda cerrada con $\sigma(E)$ conocida; equilibrio $p=Q/S$ en un volumen; plasma sin RF con energía conservada; perfil de colisiones DSMC. CI numérico y controles de versión: toda figura debe registrar parámetros, incertidumbres y hash de simulación.

### Órdenes de magnitud y observables

Prioridades de medición: potencia incidente y reflejada RF (con calibración); corrientes y tensiones de bobinas; flujo de $D_2$ con estándar definido; presiones y tipo de gauge; corriente total y fracción $D^+$, $D_2^+$, $D_3^+$; voltajes del extractor, emitancia y perfiles; datos de operación CW/pulsada; geometría y materiales BN; si existen, diagnósticos de $n_e$, EEDF/$T_e$, espectros ópticos o grados de disociación. **No inferir un perfil 3D de densidad a partir de un único valor de corriente.**

### Lecturas clave

LIPAc [R1–R3]; simulaciones experimentales [R5, R8]; manuales [R10–R16].

## 14. Itinerario de estudio y actividades comprobables

### Aplicación al inyector

El aprendizaje sigue el flujo físico: alimentación → neutrales y vacío → $\mathbf B$ y RF → ECRH → EEDF → reacciones → sheath/BN → extracción → LEBT. Cada modelo nuevo debe explicar un observable que el anterior no representaba o cuya precisión era insuficiente.

### Formulación e hipótesis

**Etapa A, unidades y balances:** derivar $B_{\rm ECR}$, $n_{\rm crit}$, $\dot N_{D_2}$, utilización de gas, $P_{\rm beam}$, $\lambda$, Kn y Debye. **Etapa B, pruebas aisladas:** resolver órbitas y polarización RF; comparar Struphy ColdPlasma/Meep frente a dispersión analítica; PICLas con colisiones D₂. **Etapa C, acoplamiento:** actualizar densidad y coeficientes RF mediante iteraciones con balance de potencia; **Etapa D, fuente**: superficies, química extensa y extracción con datos contrastados.

### Modelos y simplificaciones

Primer paper potencial: mapa de validez de modelos RF fríos, amortiguados y cinéticos en un plasma magnetizado de 2,45 GHz. Segundo: influencia de EEDF sobre la composición $D^+/D_2^+/D_3^+$ en una fuente de deuterio. La combinación Struphy-PICLas es **hipótesis de I+D**, no herramienta integrada demostrada.

### Órdenes de magnitud y criterios de salida

Antes de una campaña extensa deben existir curvas de convergencia (malla, $\Delta t$, macropartículas), mediciones de horas de núcleo por µs simulado y un caso analítico reproducible. Se recomienda empezar con 1–10 mil partículas de prueba y dominios simples, incrementando tras medir el coste. Este intervalo es **un tamaño de prototipo**, no una especificación del inyector.

### Lecturas clave

Toda la bibliografía del manual; especialmente [R5], [R7], [R10] y [R13].

## Anexo A. Constantes, definiciones y advertencias

| Símbolo | Significado | Unidad SI |
|---|---|---|
| $e$ | Carga elemental (valor absoluto) | C |
| $m_e,m_D$ | Masas del electrón y deuterón | kg |
| $k_B$ | Constante de Boltzmann | J/K |
| $\varepsilon_0,\mu_0$ | Constantes del vacío | F/m, H/m |
| $n_e,n_g$ | Densidad electrónica y neutra | m⁻³ |
| $T_e$ | Temperatura electrónica, definida por momentos si EEDF no Maxwelliana | eV o K |
| $p_g$ | Presión parcial de gas neutro | Pa |
| $P_{\rm RF,inc}$ | RF incidente en plano de referencia | W |
| $P_{\rm RF,abs}$ | RF realmente absorbida por plasma | W |
| $P_{\rm beam}$ | Potencia cinética transportada por haz | W |
| $\eta_{D,\rm gas}$ | Flujo de deuterones extraído / átomos D alimentados | adimensional |

**Advertencias:** (1) 100 keV presupone aceleración de 100 kV de una especie monovalente. (2) 140 mA se interpreta como corriente $D^+$ ideal para calculadoras; si es corriente total multiespecie, recalcular. (3) Presión, geometría, temperatura gas, densidad y EEDF no se deducen de los rangos de potencia/flujo. (4) El radio de Debye no es la escala espacial universal de un solver RF. (5) RF ECR a 2.45 GHz es distinta de la RFQ que acelera el haz a MeV.

## Anexo B. Datos reales todavía necesarios para el caso LIPAc

1. ¿Los **600–900 W** corresponden a potencia directa medida del magnetrón, entregada a la guía, neta en el puerto o potencia absorbida estimada? ¿Existe $P_{\rm refl}$?
2. ¿Los **2–5 sccm** se especifican a 0 °C, 20 °C u otra temperatura estándar? ¿Dónde está calibrado el MFC?
3. ¿La corriente **140 mA** es estrictamente de $D^+$, total extraída, o transportada? ¿Se dispone de espectro de especies para cada condición?
4. Presión operativa real, instrumentos, factores de sensibilidad para D₂, temperaturas de gas/paredes y configuración de bombeo.
5. Geometría de cámara, guía, ventana dieléctrica, discos BN, electrodos y bobinas; materiales y curvas magnéticas.
6. Corrientes de bobinas, campos medidos/simulados y calibración de fuentes HV; geometría de extracción.
7. Formato y permisos para datos experimentales; observables de EEDF, densidad o diagnósticos espectroscópicos disponibles.

Estas incógnitas **no impiden estudiar las ecuaciones**. Sí limitan la precisión de una predicción de la instalación real.

## Bibliografía comentada y documentación de referencia

- **[R1]** IFMIF/EVEDA, *Injector + LEBT*. Descripción institucional del haz nominal y línea de transporte. https://www.ifmif.org/injectorlebt/
- **[R2]** Fusion for Energy, *LIPAc injector passes acceptance tests* (2012). Fuente ECR 2,45 GHz; deuterones 140 mA a 100 keV y especies moleculares adicionales. https://fusionforenergy.europa.eu/news/ifmif-eveda-accelerator-lipac-injector-passes-acceptance-tests/
- **[R3]** Akagi y colaboradores, *CW operation of high-current deuteron injector for LIPAc*, ICIS 2025. Actualización de operación y corriente CW. https://indico.stfc.ac.uk/event/1192/contributions/8884/
- **[R4]** P. Svarnas (2025), *Electron cyclotron resonance (ECR) plasmas: A topical review through representative results obtained over the last 60 years*. Journal of Applied Physics 137, 070701. DOI https://doi.org/10.1063/5.0249342
- **[R5]** D. Eremin et al. (2025), *Electromagnetic particle-in-cell modeling of an electron cyclotron resonance plasma discharge in hydrogen*, Plasma Sources Science and Technology 34, 065001. **Es H₂, no D₂**; referencia metodológica PIC-MCC. https://doi.org/10.1088/1361-6595/add9c7
- **[R6]** L. Neri y col. (2024), *PIC simulation of a 2.45 GHz ECR ion source using COMSOL tensorial permittivity RF capability*. Modelo tensorial RF magnetizado y PIC. https://www.comsol.fr/paper/pic-simulation-of-a-245-ghz-ecr-ion-source-using-comsol-tensorial-permittivity-rf-capability-134492
- **[R7]** L. Neri et al., *Advances in PIC simulation of 2.45 GHz ECR ion sources*, ECRIS 2024, TUB3. **Presentación de congreso, no tratar como artículo completo revisado por pares.** https://accelconf.web.cern.ch/ecris2024/html/clas007.htm
- **[R8]** M. Asadi Aghbolaghi et al. (2024), *Characterization of hydrogen plasma bulk in 2.45 GHz ECR ion source*. International Journal of Hydrogen Energy 66, 406–414. **Caso H₂; comparar 0D vs fluido 3D**, no copiar tasas al deuterio. https://doi.org/10.1016/j.ijhydene.2024.04.035
- **[R9]** J.-S. Yoon et al. (2010), *Electron-impact cross sections for deuterated hydrogen and deuterium molecules*, Reports on Progress in Physics 73, 116401. **Secciones eficaces D₂/HD específicas**. https://doi.org/10.1088/0034-4885/73/11/116401
- **[R10]** PICLas, *User Guide; Maxwell, Poisson, PIC, DSMC y superficies*. https://piclas.readthedocs.io/en/latest/
- **[R11]** PICLas, *Background Gas, MCC y secciones eficaces*. https://piclas.readthedocs.io/en/stable/userguide/features-and-models/BGG.html
- **[R12]** FEMM, documentación oficial de magnetostática plana y axisimétrica. https://femm.info/doku/doku.php?id=documentation
- **[R13]** Struphy, manual v3.5 y modelos `ColdPlasma`, `ColdPlasmaVlasov`, `VlasovMaxwellOneSpecies`; FEEC. https://struphy.readthedocs.io/en/latest/
- **[R14]** CERN, Molflow+ para flujo molecular en vacío. https://cern.ch/molflow
- **[R15]** Sandia, SPARTA DSMC, guía y modelos de gas rarificado. https://sparta.github.io/doc/Manual.html
- **[R16]** Meep, documentación sobre medios girotrópicos Drude/Lorentz (experimental). https://meep.readthedocs.io/en/stable/Materials/
- **[R17]** *Low-pressure non-equilibrium plasma technologies: scientific background and technological challenges* (2025). Sheaths y procesos de superficie. https://link.springer.com/article/10.1007/s41614-025-00201-x

**Criterio bibliográfico:** los enlaces identifican la documentación o publicación; no implican que todas las formulaciones de este manual provengan de una única fuente. Las ecuaciones fundamentales se presentan en notación estándar y los cálculos derivados se realizan con constantes SI. Para una publicación científica, la bibliografía deberá ampliarse con páginas y ecuaciones primarias seleccionadas para cada modelo implementado.
