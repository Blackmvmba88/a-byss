# IF-11 B — carga descentrada por posición

Versión 0.9.0 · Estudio civil · NOT_RELEASED.

El resultado centrado de 0.8.0 se amplía con una fuerza normal aplicada fuera del centro del anclaje. Se conserva B y la precarga de referencia de 5000 N/perno; no se modifica retrospectivamente el estudio anterior.

## Modelo rápido y verificable

Cuatro posiciones `(±p/2, ±p/2)` en XY, con p=0.07 m. Fuerza F en +Z aplicada en `(ex,ey)`. Momentos: Mx=F·ey y My=−F·ex. Se supone una placa rígida y cuatro caminos locales de carga lineales e idénticos, antes de apertura. La rigidez de la placa real de 4 mm no está demostrada.

La demanda normal externa por posición es:

`Ni = F/4 + F·ex·xi/Σx² + F·ey·yi/Σy²`.

Conserva fuerza normal y los dos momentos. Ni es demanda externa local, no tensión total del perno. El índice precursor de apertura es `(1−C)Ni/Pmin`; mientras todo el grupo queda por debajo de uno, la tensión de perno se estima como `Pmin+C·Ni`. Una demanda negativa deja el caso fuera de este modelo, sin recortarla artificialmente.

Un par puro T alrededor de Z produce componentes de cortante `Qxi=−T·yi/Σr²`, `Qyi=T·xi/Σr²`. Se verifica equilibrio del par y suma nula de fuerzas laterales. El modelo no predice reparto por fricción, deslizamiento ni resistencia combinada.

Cuando alguna posición alcanza el índice uno, se anula la predicción de tensión de **todos** los pernos: hace falta resolver redistribución y contacto. Los índices guardados siguen siendo extrapolaciones del precursor lineal para detectar el límite, no una solución física tras separación. Tampoco se calculan flexión de placa, efecto de palanca, apoyo local o rigidez del soporte.

Referencia de contexto: [NASA Fastener Design Manual, RP-1228](https://ntrs.nasa.gov/api/citations/19900009424/downloads/19900009424.pdf), sección Design Criteria, cargas en grupos de fijaciones. Las ecuaciones anteriores declaran un modelo simétrico propio; no sustituyen el análisis de eje de giro/contacto de un soporte real descrito por el manual.

## Barrido y hallazgo

Cuatro posiciones hipotéticas de la carga: (0,0), (10,0), (25,0), (10,10) mm. Se cruzan con F=4/8/12 kN, T=0/80 N·m, retención de precarga 70%/100% y C=0.1/0.2/0.3: **144 casos**. No son probabilidades ni cargas derivadas de misión.

| Desplazamiento | Peor índice local | Casos que alcanzan apertura |
|---|---:|---:|
| Centrado | 0.771 | 0/36 |
| X=10 mm | 0.992 | 0/36 |
| X=25 mm | 1.322 | 6/36 |
| X=10, Y=10 mm | 1.212 | 4/36 |

El resultado centrado anterior se reproduce exactamente. Un desplazamiento pequeño puede concentrar carga en determinadas posiciones. Estar bajo el umbral a 10 mm no demuestra robustez: la holgura numérica es escasa y el modelo no incluye la flexibilidad real.

## Decisión para la siguiente iteración

La precarga de 5000 N se conserva como hipótesis, no como solución aprobada. Antes de aumentarla, definir el punto real de aplicación de carga, la contraplaca y el soporte; revisar si puede centrarse el camino de carga. Luego evaluar deformación local y contacto. Materiales, precarga medida, resistencia combinada y fatiga siguen abiertos. No hay cambio de capacidad de CARGO-MR ni cierre de G0/G1.

## Ejecución

```sh
python3 software/if11_eccentric.py
python3 -m unittest discover -s tests
```

[Reporte y resultados por perno](../evidence/IF-11/eccentric/README.md). Entradas en `models/mechanics/if11_eccentric.json`, geometría y rangos heredados de `if11_variants.json`. Manifiesto de hashes incluido. Las pruebas comprueban equilibrio, simetría, recuperación del caso centrado, parada al abrir y rechazo de datos inválidos; no validan hardware.
