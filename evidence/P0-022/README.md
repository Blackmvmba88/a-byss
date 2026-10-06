# P0-022 — evidencia aritmética parcial

**Estado del requisito: ABIERTO.** Asignaciones ilustrativas sin validar.

Densidad aparente: 100 kg/m³. Las cifras de carga son cotas del interior bajo hipótesis; no son capacidades de vuelo.

| Vehículo | Plazas objetivo ocupadas | Módulos CARGO | Cota de carga, kg | Masa instalada interior, kg |
|---|---:|---:|---:|---:|
| W-HALE-T | 32 | 0 | 0 | 5840 |
| W-HALE-T | 16 | 4 | 3200 | 6720 |
| W-HALE-T | 0 | 8 | 6400 | 7600 |
| M-RAY | 8 | 0 | 0 | 1860 |
| M-RAY | 4 | 1 | 700 | 1880 |
| M-RAY | 0 | 2 | 1400 | 1900 |
| T-SHARK | 4 | 0 | 0 | 820 |
| T-SHARK | 0 | 1 | 500 | 700 |

Reproducir desde raíz: `python3 software/generate_payload_report.py`.

[Resultados y hashes](exploratory_results.json) · [Hipótesis y exclusiones](../../docs/SIZING_BASELINE.md).

Faltan masa total de vehículo, misión, geometría/puertas, CG/inercia, cargas, potencia, térmico y servicios humanos. No existe revisión independiente de ingeniería; no se declara cierre de G0 o G1.
