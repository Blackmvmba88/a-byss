# IF-11 — estudio rápido de un anclaje

Versión 0.7.0 · Investigación civil · NOT_RELEASED.

Se compara una placa cuadrada con cuatro taladros pasantes y cuatro conjuntos de fijación hipotéticos. Es una subinterfaz de estudio: no sustituye los sockets del bridge ni modifica CARGO-MR. No es un mecanismo de enganche completo ni un plano de fabricación.

## Geometría y materiales

| Variante | Lado / espesor / paso cuadrado (mm) | Diámetro del taladro (mm) | Masa asumida por conjunto de fijación (g) | Precarga de referencia por perno (N) |
|---|---|---|---|---|
| A | 80 / 4 / 50 | 7 | 12 | 1500 |
| B | 100 / 4 / 70 | 9 | 20 | 2500 |
| C | 100 / 6 / 70 | 9 | 20 | 2500 |

Todas las cifras son hipótesis editables, no especificaciones comerciales. Densidad de placa asumida: 2700 kg/m³. Aleación, temple, propiedades resistentes, diámetro nominal y grado de tornillo pendientes. El diámetro de taladro no identifica una rosca. No se prescribe par de apriete: convertir par a precarga exige caracterizar fricción y montaje.

Masa parcial = densidad × (lado² − 4π·diámetro²/4) × espesor + cuatro masas de fijación. Excluye contraplaca, soporte, insertos, actuador, sensores y estructura del vehículo. No se añade al presupuesto de CARGO-MR hasta definir esas piezas y evitar doble conteo.

## Cargas comunes y barrido

Fuerza normal de tracción sobre **un anclaje completo**, no por perno: 4, 8 y 12 kN. Par puro alrededor del eje normal de la placa: 0, 40 y 80 N·m. No se derivan de una misión ni se reparten automáticamente entre los cuatro sockets de CARGO-MR.

Se cruzan con retención de precarga 70%/100% y fracción de rigidez C=0.1/0.2/0.3: 54 puntos por variante, 162 en total. El barrido es una exploración determinista, no una distribución de probabilidad. La rigidez real depende del montaje y debe sustituir estos valores.

- Separación axial: se reutiliza el filtro de precarga de [mecánica rápida](FAST_MECHANICS.md), con tracción concéntrica y reparto uniforme. El índice es `(1−C)F/(4Pmin)`; índice ≥1 alcanza el umbral lineal de separación.
- Demanda de cortante por par puro: cuatro fijaciones iguales a radio r=paso/√2; demanda por perno `T/(4r)`, en direcciones tangenciales. Es un reparto idealizado por contacto de pernos, sin crédito por fricción y sin calcular cuándo se produce deslizamiento. No es la fórmula de torsión de un eje circular.
- Ambos resultados se guardan juntos, pero se calculan de forma independiente. No hay aceptación de carga combinada, resistencia del perno, aplastamiento, arrancamiento de borde, flexión de placa ni efecto de palanca. La pérdida de contacto puede invalidar el reparto ideal.

B y C comparten precarga y rango supuesto de C: obtienen el mismo índice axial. La mayor rigidez real de C no se ha calculado; no puede afirmarse que no tenga beneficio físico. La variante A es la más ligera, pero alcanza antes el umbral axial bajo estos supuestos. Ninguna variante supera toda la cuadrícula.

## Ciclos, fractura y desgaste

Fatiga, propagación de grietas y desgaste permanecen sin resultado: faltan espectro de cargas, datos de vida, superficies, propiedades y contacto. No se inventa una vida útil a partir del conteo de casos.

Siguiente evidencia: definir el camino de carga y la unión completa; seleccionar material/fijación con datos trazables; caracterizar precarga mínima y rigidez. Después preparar un banco instrumentado con carga axial, medición de apertura y pérdida de precarga. Los diez ciclos de conversión previstos en el roadmap comprueban repetibilidad del montaje; no demuestran vida a fatiga. Cargas y límites de un ensayo físico requieren un protocolo propio.

## Reproducir

```sh
python3 software/if11_trade.py
python3 -m unittest discover -s tests
```

[Resultados, tabla y geometría](../evidence/IF-11/README.md). Entradas: `models/mechanics/if11_variants.json`. Resultados completos en JSON y hashes de entradas, código y salidas en `manifest.json`.

Referencia metodológica: [NASA Fastener Design Manual, RP-1228](https://ntrs.nasa.gov/api/citations/19900009424/downloads/19900009424.pdf), para precarga y reparto de cargas en grupos de fijaciones. Los números de esta comparación son propios e hipotéticos; no son datos extraídos del manual.

G0/G1 y P0-021/022 siguen abiertos. El estudio aporta geometría paramétrica y demanda exploratoria, no compatibilidad aprobada.

## Continuación 0.8.0

[Material y precarga candidatos](IF11_CANDIDATE.md) conserva B y compara dos precargas sin reescribir los resultados históricos. La referencia de resistencia del perno es provisional.
