# Geometría, accesos y balance del interior — 0.4.0

2026-10-06 · Layouts hipotéticos para detectar incompatibilidades, sin dimensionamiento aeronáutico acreditado.

## Hipótesis geométricas

El [catálogo](../models/geometry_assumptions.json) añade envolventes rectangulares a las masas de 0.3.0. Son elecciones exploratorias propias, no datos de fabricantes o normas. Las dimensiones no prueban que cuatro personas quepan con asientos, postura, equipaje y salida adecuados. PAX y CARGO comparten aquí la caja exterior de su clase, pendiente de CAD específico.

| Clase | Caja de módulo X/Y/Z, m | Interior X/Y/Z, m | Apertura lateral X/Z, m | Distribución |
|---|---|---|---|---|
| WH | 2.4 / 2.0 / 2.2 | 11.6 / 5.2 / 2.5 | 2.6 / 2.4 | Cuatro filas de dos módulos, pasillo central |
| MR | 2.4 / 2.0 / 2.2 | 6.4 / 3.2 / 2.5 | 2.6 / 2.4 | Dos módulos longitudinales, pasillo lateral |
| TS | 2.2 / 1.8 / 2.0 | 4.0 / 3.0 / 2.3 | 2.4 / 2.2 | Un módulo, pasillo lateral |

Pasillo reservado de 0.8 m, sin afirmación de suficiencia humana. Holgura mínima módulo/pared: 0.05 m; entre módulos: 0.05 m. Para apertura se exige caja proyectada más 0.05 m en cada borde. Estas asignaciones no incluyen revestimientos reales, tuberías o mecanismos salvo el espacio libre dibujado; geometrías reales podrían invalidarlas.

X aumenta hacia popa desde el plano anterior del interior; Y positivo hacia estribor; Z hacia arriba desde piso. Origen y marco son del interior, no datum del avión. Los diagramas son vistas superiores rectangulares; no representan la forma exterior ni una geometría BWB.

## Accesos: qué se comprueba

Se compara módulo X/Z con una apertura lateral para traslación sin giro en Y. Es una condición necesaria, no una simulación del recorrido. La apertura aún no tiene ubicación estructural; no se diseña una puerta por módulo ni se afirma que se pueda llevar la caja a su posición a través del pasillo. Ningún caso puede declarar acceso completamente verificado.

También se revisan envolvente de cabina, colisiones entre cajas, invasión de zonas reservadas y consistencia entre volumen útil y volumen exterior. El pasillo no invade las cajas candidatas; no están modeladas puertas de módulo, orientación de asientos, rutas de evacuación o maniobras de giro.

Si no existe recorrido de entrada, las alternativas son subconjuntos desmontables o rediseñar el acceso. La siguiente etapa debe comprobar volumen barrido continuo, ubicación de puertas y efecto estructural sobre el casco.

## Centro de gravedad del payload

```text
CG_payload = suma(masa_bruta_modulo_i × CG_bruto_modulo_i) / suma(masa_bruta_modulo_i)
CG_bruto_modulo_i = centro_posicion_i + desplazamiento_CG_declarado_i
```

Se cuenta tara aun cuando se descarga la mercancía. PAX-4 conserva cuatro ocupantes; descarga de pasajeros, módulos retirados y consumo temporal no se modelan aquí. Los manifiestos declaran explícitamente fracción de carga y desplazamiento del CG bruto, sin deducir este último sólo de volumen.

| Clase | Ventana X, m | Ventana Y, m | Ventana Z, m |
|---|---|---|---|
| WH | 3.7…7.7 | −0.35…0.35 | 0.8…1.5 |
| MR | 2.5…3.9 | −0.8…−0.2 | 0.8…1.5 |
| TS | 1.5…2.5 | −0.75…−0.15 | 0.7…1.4 |

Ventanas arbitrarias de estudio para ejercitar detección, no límites de estabilidad/control. MR/TS tienen pasillo lateral y el interior está desplazado respecto al centro geométrico. No se infiere desequilibrio del vehículo completo, cuyas masas restantes no se conocen. No calcular CG total usando sólo módulos: faltan estructura, propulsión, combustible, sistemas comunes y transformaciones de marco.

La distribución de mercancía parte de la cota uniforme del calculador 0.3.0 y admite reducir carga por posición con fracciones entre 0 y 1. No optimiza redistribución: descargar una posición no aumenta automáticamente la asignación de otra. La fracción cambia contenido, no tara ni volumen físico de la caja.

## Casos reproducibles y uso

- `wh_combi`: PAX en las filas extremas, CARGO en las dos centrales; simetría lateral.
- `mr_combi`: PAX anterior, CARGO posterior.
- `ts_cargo`: una posición CARGO.
- `wh_unbalanced_unload`: descarga de mercancía de todo un lateral, manteniendo contenedores; fallo deliberado de ventana Y.

```bash
python3 software/layout_check.py models/layouts/mr_combi.json
python3 software/layout_check.py models/layouts/wh_unbalanced_unload.json
python3 software/generate_layout_report.py
python3 -m unittest discover -s tests -v
```

Salida 0: comprobaciones parciales pasan; 1: incompatibilidad detectada; 2: datos inválidos/incompletos. Siempre `UNVALIDATED` y `NOT_RELEASED`; `whole_vehicle_cg_m` sigue nulo y `access_route_status` sigue `NOT_EVALUATED`. [Resultados y diagramas](../evidence/P0-021/README.md).

## Pendientes con responsable propuesto

SYS/estructura: ubicación de puertas, geometría CAD, límites de piso/anclajes y masa fija. GNC: datum global, tensor de inercia y envolvente por fase. Factores humanos: postura, asientos, accesibilidad y evacuación. Integración: camino de instalación y herramientas. MIS: misión y secuencia de carga/descarga/consumo. Cierre conceptual previsto G1; validación física en G2 o programa correspondiente.

Esta evidencia contribuye parcialmente a P0-021/022. No cierra IF-11, G0 ni G1. El conjunto de veinte pruebas valida aritmética y reglas del software, no estos supuestos físicos.
