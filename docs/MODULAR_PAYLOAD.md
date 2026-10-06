# Interiores modulares — pasajeros, carga y servicio

Versión 0.2.0 · Propuesta de investigación.

## Concepto

Cuatro plazas por módulo como unidad inicial. Mantener fijos estructura primaria, casco de presión, propulsión y control; sustituir interiores mediante posiciones con anclajes y servicios definidos. Primera conversión en tierra, sin ocupantes y con servicios aislados.

La puerta debe admitir la envolvente del módulo o se deben diseñar subconjuntos desmontables y validar su secuencia. No se abre estructuralmente el casco de presión en cada cambio. Sustituir asientos por carga no cambia automáticamente la presurización del volumen.

## Catálogo

| Código, por clase WH/MR/TS | Uso | Masas a contabilizar | Servicios y restricciones |
|---|---|---|---|
| PAX-4 | Cuatro plazas adaptadas al entorno | Asientos, anclajes, ocupantes, equipaje, equipo personal y servicios incrementales | Acceso, retención, comunicación, ventilación/soporte vital |
| CARGO | Mercancía compatible | Pallet/contenedor, embalaje, barreras, sujeciones y mercancía | Piso, anclajes, accesos, incendio y compatibilidad |
| SERVICE | Instrumentos/equipos | Rack, instrumentos, cableado y consumibles propios | Potencia, datos y calor |
| HAB-MR, futuro | Habitabilidad de misión prolongada | Equipamiento y consumibles | Ocupa posiciones y reduce plazas disponibles |

PAX-4-WH, PAX-4-MR y PAX-4-TS comparten concepto, no dimensiones ni certificación. Propelentes, baterías de alta energía y mercancías peligrosas requieren análisis específico, no se aceptan como carga genérica por caber en la posición.

## Configuraciones de referencia

| Vehículo | Inventario de módulos | Plazas objetivo | Posiciones de carga |
|---|---|---:|---:|
| W-HALE-T | 8 PAX-4-WH | 32 | 0 |
| W-HALE-T | 4 PAX-4-WH + 4 CARGO-WH | 16 | 4 |
| W-HALE-T | 8 CARGO-WH | 0 | 8 |
| M-RAY | 2 PAX-4-MR | 8 | 0 |
| M-RAY | PAX-4-MR + CARGO-MR | 4 | 1 |
| M-RAY | 2 CARGO-MR | 0 | 2 |
| T-SHARK | PAX-4-TS | 4 | 0 |
| T-SHARK | CARGO-TS | 0 | 1 |
| T-SHARK | SERVICE-TS | 0 | 0 |

Inventarios lógicos: no definen ubicación longitudinal ni pasillos. COMBI exige acceso/evacuación y separación entre carga/personas adecuados a cada entorno. Las capacidades humanas son objetivos futuros; no amplían el gate P0 logístico a operación humana.

## Cálculo de capacidad

```text
M_total = M_base_fija + M_prop_y_reservas + M_servicios_comunes
        + suma(M_modulo_vacio_i + M_contenido_i + M_consumibles_i)

CG = suma(m_j * r_j) / suma(m_j)   [todas las masas del vehículo]
N_pasajeros = 4 * N_modulos_PAX4 - plazas_usadas_por_tripulacion
```

Las partidas son exclusivas: no contar dos veces soporte vital, reservas o embalaje. Evaluar centro de gravedad e inercia durante consumo y descarga. La carga neta es la máxima masa de mercancía que cumple simultáneamente masa total/márgenes, rendimiento/reservas, carga por posición, piso/anclajes, CG/inercia, envolvente/puerta, potencia, térmico y requisitos de ocupantes.

**Ejemplo aritmético ficticio, sin asignación a vehículos:** una posición con límite bruto de 1,000 kg tras márgenes y un módulo CARGO vacío de 150 kg tiene un techo local por masa de 850 kg de mercancía. El valor sólo es utilizable si cumple las otras restricciones. Retirar cuatro personas no demuestra un aumento igual de carga: cambian equipamiento, distribución y misión.

No se declara capacidad de carga en toneladas hasta dimensionar cada clase y cerrar misión, módulos y servicios.

## Conversión y liberación

1. Elegir configuración/ misión y revisar clase y revisión de interfaz.
2. Descargar ocupantes/contenido, asegurar vehículo y aislar servicios.
3. Retirar módulo mediante procedimiento y herramientas definidos.
4. Inspeccionar piso, anclajes, conectores y sellos aplicables.
5. Instalar módulo, comprobar retenciones y conexiones/aislamiento.
6. Actualizar manifiesto, masas, CG, inercia, consumibles y software de configuración.
7. Verificar accesos, retención, servicios y respuestas a fallos.
8. Liberar configuración con evidencia y responsables.

Medir tiempo desde vehículo asegurado hasta liberación, incluyendo inspección y ensayos; registrar personas-hora, herramientas y anomalías. La meta temporal se fija tras un banco, sin prometer cambios instantáneos.

## Manifiesto mínimo

Identidad del vehículo, variante, misión y revisión de configuración; posición, módulo, clase y revisión de interfaz; masa vacía, contenido, consumibles, CG, inercia y envolvente; ocupantes, potencia, disipación, clasificación de carga, estado de inspección y evidencias. Unidades explícitas, CG con datum/marco, inercia con marco/punto de referencia. Datos críticos faltantes bloquean liberación.

## Trazabilidad

[IF-11](../interfaces/IF-11_MODULAR_CABIN.md), [ADR-001](../decisions/ADR-001-modular-payload.md), P0-021…025 y [fuentes](REFERENCES.md). NASA orienta el estudio de factores humanos; Airbus aporta antecedentes de modularidad/conversión, sin validar la propuesta A-BYSS.
