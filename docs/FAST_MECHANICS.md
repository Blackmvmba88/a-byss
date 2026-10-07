# Mecánica rápida — seis filtros escalares

Versión 0.6.0 · Investigación aeroespacial civil · NOT_RELEASED.

Objetivo: detectar pronto qué hipótesis necesita atención con fórmulas pequeñas, JSON y un reporte de tabla/barras. Python estándar; no requiere Blender para calcular. Se conserva el contexto de cada modelo mediante `basis`, unidades SI y una declaración explícita de aplicabilidad. Esa declaración debe justificarse: no demuestra por sí misma que el modelo represente la pieza.

## Ejecutar

Desde la raíz del repositorio:

```sh
python3 software/mechanical_screen.py models/mechanics/demo.json
python3 software/mechanical_screen.py models/mechanics/cargo_mr_pending.json
python3 software/generate_mechanics_report.py
python3 -m unittest discover -s tests
```

El reporte reproducible se guarda en [evidence/mechanics](../evidence/mechanics/README.md), con hashes de entradas, código y salidas. El tiempo que imprime el calculador mide sólo `screen()`, excluyendo arranque de Python y escritura. No representa tiempo de simulación del vehículo. La CLI entrega estados por modo; un código de salida cero no equivale a aceptación mecánica.

## Modelos y alcance

| Modo | Cálculo | Condiciones y límites |
|---|---|---|
| Carga axial | σ=F/A; δ=FL/(AE) | Barra uniforme, carga axial de tracción, pequeña deformación elástica. F es una entrada conocida: no se predice empuje del motor. Sin pandeo, flexión ni concentradores. |
| Torsión | τ=Tr/J; θ=TL/(GJ) | Eje circular uniforme elástico; J es el momento polar. No aplicar esta fórmula directamente a la caja rectangular CARGO-MR ni a secciones con alabeo. |
| Separación de unión | Reserva lineal=n·Pmin−(1−C)·F | Unión precargada simétrica, tracción concéntrica, reparto uniforme; C es la fracción de carga externa que aumenta la carga del perno. Sin momentos, palanca, deslizamiento ni cálculo de rotura de pernos. Reserva negativa indica superar el umbral del modelo, no compresión física negativa. |
| Fractura | KI=Y·σ·√(πa) | Mecánica de fractura lineal elástica, modo I, pequeña zona plástica. Y y la definición de a deben corresponder a la misma geometría. El límite introducido requiere fundamento material y ambiental. No calcula propagación de grietas. |
| Desgaste | V=k·W·s/H | Archard, k adimensional caracterizado para el contacto, régimen y ambiente; dureza H en Pa. No predice cambios de régimen, lubricación ni fatiga superficial. |
| Fatiga | D=Σ(ni/Ni) | Miner: Ni debe provenir de datos de vida compatibles con tensión, esfuerzo medio, temperatura y acabado de cada bloque. No calcula Ni a partir de una carga, ni efectos de secuencia. D=1 es un umbral del modelo, no una garantía de vida. |

La utilización compara demanda con límite introducido; en separación compara pérdida lineal de precarga con precarga disponible. No se mezclan ni suman los seis índices: representan mecanismos distintos. Las comprobaciones son independientes y no resuelven interacción entre mecanismos. Un análisis posterior del conjunto necesita rutas de carga, condiciones de apoyo e interfaces coherentes.

## Dos clases de evidencia

- `demo.json`: seis probetas hipotéticas independientes para verificar aritmética. No son materiales elegidos para el vehículo ni resultados de ensayo. Se incluyen límites excedidos intencionalmente.
- `cargo_mr_pending.json`: plantilla del caso real, sin propiedades inventadas; los seis modos permanecen `INCOMPLETE`. El espesor visual del bridge no se adopta automáticamente como espesor estructural.

Estados: `INCOMPLETE` cuando faltan datos o aplicabilidad; `INVALID` para entradas no admisibles; `BELOW_INPUT_LIMIT` si el cociente es menor que uno; `AT_OR_ABOVE_LIMIT` cuando alcanza o supera uno. Ninguno libera fabricación ni vuelo.

Cian: cociente <0.8; amarillo: [0.8,1); rojo: ≥1; sin barra: sin resultado. El corte 0.8 es una ayuda visual, no un factor de seguridad. Los números y las etiquetas permiten interpretar el reporte sin depender del color. Las barras se recortan en 1.5; el número conserva el valor completo. Los colores saturados del 3D identifican piezas; no representan un campo de tensiones.

## Flujo de trabajo corto

1. Registrar carga, material, unión, ambiente y fuente en el caso; comprobar si aplica cada modelo.
2. Comparar alternativas editando casos pequeños. Conservar los resultados individuales, incluidos los incompletos.
3. Revisar primero límites alcanzados, hipótesis débiles y datos faltantes. Pasar a un solver local o ensayo cuando el fenómeno no esté representado, haya interacción relevante o el resultado se acerque al límite.

La siguiente iteración útil es caracterizar una unión IF-11: fuerza de separación, precarga mínima, rigideces y distribución de carga. No hace falta mallar toda la nave para empezar.

## Referencias de los métodos

- [NASA — Fastener Design Manual](https://ntrs.nasa.gov/api/citations/19900009424/downloads/19900009424.pdf): precarga y comportamiento de uniones atornilladas.
- [MIT — Torsion](https://web.mit.edu/course/3/3.11/www/modules/torsion.pdf): torsión elástica de ejes circulares.
- [NASA — factores de intensidad de tensiones](https://ntrs.nasa.gov/api/citations/20140008837/downloads/20140008837.pdf): dependencia de la geometría en mecánica de fractura.
- [COMSOL — daño acumulativo](https://doc.comsol.com/6.3/doc/com.comsol.help.fatigue/fatigue_ug_sme.4.25.html): regla de Miner.
- [COMSOL — desgaste](https://doc.comsol.com/6.4/doc/com.comsol.help.sme/sme_ug_theory.06.093.html): formulación de Archard.

Referencias metodológicas; no constituyen certificación ni validación de estos casos.
