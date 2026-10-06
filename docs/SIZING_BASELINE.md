# Presupuesto exploratorio de interiores — 0.3.0

2026-10-06 · Hipótesis aritméticas, no especificaciones de aeronave.

## Objetivo

Convertir el catálogo modular en un modelo reproducible para comparar ocupación y carga. El escenario E0 es una comparación estática de interiores: no define órbita, alcance, duración ni propelente. No constituye la misión de referencia exigida por G0. Toda configuración permanece `NOT_RELEASED`; P0-022 sigue abierto.

## Hipótesis editables

Datos en [module_assumptions.json](../models/module_assumptions.json). Todos los números siguientes fueron seleccionados para explorar el modelo, sin derivación de CAD, ensayo, fabricante o vehículo existente. Responsable propuesto: SYS; revisión en G0/G1. El margen de 20% es una reserva de esta asignación de payload, no prueba del margen del vehículo completo requerido por P0-004.

| Parámetro | WH | MR | TS | Significado |
|---|---:|---:|---:|---|
| Posiciones | 8 | 2 | 1 | Objetivos anteriores de diseño |
| Límite bruto nominal por posición, kg | 1,250 | 1,500 | 1,250 | Asignación hipotética antes de margen |
| Límite bruto nominal total, kg | 10,000 | 3,000 | 1,250 | Sólo interior de misión |
| Reserva de masa | 20% | 20% | 20% | Aplicada una vez a cada límite |
| Asignación por posición tras margen, kg | 1,000 | 1,200 | 1,000 | Módulo + contenido + suministros |
| PAX-4 vacío, kg | 250 | 350 | 300 | Incluye asientos y sus retenciones; excluye personas |
| Suministros incrementales PAX-4, kg | 0 | 100 | 40 | Partida ficticia para explorar; no dimensiona supervivencia |
| CARGO vacío, kg | 150 | 250 | 200 | Incluye contenedor y sujeciones del módulo |
| Volumen útil CARGO, m³ | 8 | 7 | 5 | Asignación escalar; no dimensiones de un módulo |

Persona + equipaje: **120 kg por plaza**, sólo una hipótesis de masa total. No es una norma antropométrica ni una masa de diseño de asiento. PAX-4 supone cuatro plazas ocupadas. La tripulación operativa adicional y servicios comunes del vehículo no están incluidos. Para WH, cero suministros incrementales no significa cero necesidad de ventilación, agua o servicios: esas funciones siguen fuera de este modelo.

Densidad aparente de carga por defecto: **100 kg/m³**, modificable. Debe incluir en la masa de contenido mercancía y embalaje adicional no incluido en la tara del módulo. No se usa la densidad del material macizo como sustituto del volumen embalado.

## Cálculo

```text
L_local = limite_nominal_posicion × (1 − margen)
L_total = limite_nominal_interior × (1 − margen)
M_PAX = tara_PAX + 4 × masa_persona_equipaje + suministros_PAX
M_instalada_sin_carga = n_PAX × M_PAX + n_CARGO × tara_CARGO

cota_local = n_CARGO × (L_local − tara_CARGO)
cota_total = L_total − M_instalada_sin_carga
cota_volumen = n_CARGO × volumen_util × densidad_aparente
carga_neta_exploratoria = min(cota_local, cota_total, cota_volumen)
```

Se ocupa cada posición con PAX-4 o CARGO; SERVICE, HAB y posiciones vacías no están modelados todavía. La mercancía se distribuye por igual entre posiciones CARGO de la misma clase. No se resta el 20% de nuevo a la carga resultante. Limitar tanto cada posición como la suma no duplica margen: son restricciones diferentes.

Se rechazan clases desconocidas, número de módulos inválido, masas negativas, valores no finitos, campos críticos faltantes y excesos de asignación. Resultado calculable significa coherencia aritmética con los datos de entrada, no admisibilidad de ingeniería.

## Ejecutar sin dependencias externas

Desde la raíz del repositorio, con Python 3.9 o posterior:

```bash
python3 software/payload_budget.py --vehicle MR --pax-modules 1 --cargo-density 100
python3 software/payload_budget.py --vehicle WH --pax-modules 0 --cargo-density 200
python3 -m unittest discover -s tests -v
python3 software/generate_payload_report.py
```

`--catalog` permite utilizar otro archivo de hipótesis. Códigos de salida: 0 si se calcula; 2 si la entrada es inválida. El JSON incluye siempre estado de ingeniería, falta de liberación y comprobaciones omitidas. El reporte reproducible está en [evidence/P0-022](../evidence/P0-022/README.md).

## Qué falta para pasar de asignaciones a capacidades

| Dato o comprobación | Responsable propuesto | Entregable / gate |
|---|---|---|
| Duración, entorno, ruta, carga de referencia y contingencias | MIS | CONOPS / G0 |
| Dimensiones, escotilla, pasillos y empaquetado | SYS + factores humanos | CAD/layout por clase / G1 conceptual |
| Masa seca y posición de todos los componentes | SYS + estructura | Balance de vehículo / G1 |
| Cargas, piso, anclajes, CG e inercia por fase | Estructura + GNC | Envolvente y casos de carga / G1 |
| Potencia, calor y consumibles dependientes de duración | EPS + THM + factores humanos | Presupuestos y contingencias / G1 |
| Delta-v/propelente o desempeño atmosférico | ORB / AER | Cierre de misión / G1 |
| Conversión y detección de fallos mecánicos | Integración | Banco / G2 |

No se cumple IF-11 ni P0-021…025 con este calculador parcial. La comparación ayuda a identificar sensibilidad y preparar las entradas para esos análisis.
