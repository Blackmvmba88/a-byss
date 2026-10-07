# IF-11 B — material y fijación candidatos

Versión 0.8.0 · Estudio para banco terrestre civil · NOT_RELEASED.

Se conserva B: placa 100 × 100 × 4 mm, cuatro agujeros de 9 mm en patrón de 70 mm. Se propone 6061-T6 y fijaciones M8 de paso grueso clase 8.8 como candidatos para desarrollar el modelo. No son selección de vuelo ni lista de compra: faltan longitud de agarre, tuerca, arandelas, acabado, contraplaca y certificados. Ningún cambio se aplica a CARGO-MR.

## Datos y procedencia

| Dato | Valor usado | Evidencia y límite |
|---|---|---|
| Densidad de placa | 2700 kg/m³ | Kaiser, ficha 6061 rev. 05/06, página 2: 2.70 Mg/m³ a 20 °C. Propiedad nominal, no certificado de lote. |
| Carga de prueba de referencia del perno | 21200 N | Fila M8, columna 8.8 del índice público de Bossard. El PDF original no pudo recuperarse (404); revisión indicada en índice F-en-2023.05. Provisional hasta revisar documento, notas y producto concreto. |
| Masa por conjunto de fijación | 20 g | Hipótesis anterior, no masa de producto seleccionado. |
| Precarga de referencia | 2500 y 5000 N/perno | Opciones de estudio propias; no recomendación de apriete. |
| Retención mínima / extremo superior | 0.70 / 1.20 de referencia | Hipótesis de sensibilidad, no dispersión medida del montaje. |
| Fracción de rigidez | 0.1–0.3 | Hipótesis anterior; no derivada del espesor ni del material candidato. |

Fuentes consultadas el 2026-10-07:

- [Kaiser — 6061 Sheet, Coil & Plate](https://online.kaiseraluminum.com/depot/PublicProductInformation/Document/1015/Kaiser_Aluminum_6061_Sheet_Coil_and_Plate.pdf).
- [Bossard — Materials screws & nuts](https://www.bossard.com/global-en/-/media/bossard-group/website/documents/technical-resources/en/f-004-en.pdf), datos recuperados del índice; enlace directo devolvió 404. No se conserva una copia completa ni se afirma haber revisado sus notas.

No se importan valores típicos de resistencia de la placa como límites admisibles. No se adopta una vida de fatiga desde un único valor de catálogo.

## Comprobación axial

Se mantienen las cargas anteriores: 4/8/12 kN por anclaje y par puro 0/40/80 N·m, con seis combinaciones de retención y rigidez: 54 puntos por opción. El par no interviene en la aceptación axial. Sigue registrada su demanda por perno, sin evaluar resistencia combinada.

Para evitar apertura en el peor extremo axial:

`P_ref > (1−C_min) F_max / (4 × retención_min)`.

Con los supuestos actuales resulta `P_ref > 3857.1 N/perno`. La igualdad marca inicio de apertura en este modelo, sin margen adicional.

La envolvente superior de carga axial en un perno, mientras se mantiene contacto, es:

`F_bolt,max = 1.20 P_ref + C_max F_max / 4`.

Su comparación con 21200 N es provisional y sólo axial. No incluye par de montaje, flexión de perno ni fricción. Si la condición de contacto no se satisface en ese extremo, el calculador no extrapola y devuelve dato nulo. El límite algebraico superior es 16916.7 N/perno; **no es un rango autorizado de instalación**.

Con referencia 5000 N, la precarga mínima supuesta es 3500 N, el índice máximo de separación es 0.771 y la envolvente superior por perno es 6900 N. El cociente frente a la prueba provisional es 0.325. Bajar de uno en estos dos filtros no cierra el diseño de la unión.

## Próximo cierre concreto

1. Recuperar ficha completa y certificado del perno seleccionado, con geometría, clase y condiciones aplicables.
2. Definir contraplaca, tuerca, arandelas y camino de carga; evaluar apoyo local, flexión, arrancamiento y carga combinada.
3. Caracterizar precarga y rigidez con instrumentación. No convertir todavía 5000 N a un par de apriete.
4. Registrar material, montaje y datos de ciclos para fatiga/desgaste. El efecto térmico y la compatibilidad de materiales siguen abiertos.

Los 5000 N sólo se adoptan como hipótesis candidata para la siguiente iteración. No se cambian límites retrospectivamente ni se cierra G0/G1.

## Reproducir

```sh
python3 software/if11_candidate.py
python3 -m unittest discover -s tests
```

[Resultados completos](../evidence/IF-11/candidate/README.md). JSON de fuentes y entradas: `models/mechanics/if11_candidate.json`. Los hashes cubren entradas, código y reportes generados, no certifican la autenticidad del catálogo externo.

## Continuación 0.9.0

[La carga descentrada](IF11_ECCENTRIC.md) alcanza apertura local en algunos casos manteniendo la precarga de referencia. El resultado centrado no se generaliza a otras posiciones de carga.
