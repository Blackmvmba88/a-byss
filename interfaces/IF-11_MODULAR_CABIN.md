# IF-11 — Posición de misión ↔ módulo interior

Versión 0.1 · Contrato conceptual abierto · Dueños propuestos: SYS, diseñador de vehículo y diseñador de módulo.

Perfiles WH (atmosférico), MR (orbital/cislunar), TS (orbital compacto). Manifiesto común; dimensiones y cargas propias. Los adaptadores tienen masa, altura, cargas y evidencia propias.

| Dominio | Campos obligatorios para baseline G1 | Verificación prevista |
|---|---|---|
| Mecánico | Datum, acceso, dimensiones, masa bruta, CG, inercia, anclajes, cargas por eje y rigidez | CAD, balance, análisis de cargas; banco posterior |
| Eléctrico | Tensión, corriente, aislamiento, secuencia, protección y puesta a tierra | Análisis y prueba de compatibilidad |
| Datos | Identidad, clase, revisión, integridad, autoridad y retenciones | Emulador de combinaciones válidas/ inválidas |
| Térmico | Disipación, límites y conexiones cuando apliquen | Casos caliente/frío |
| Personas | Plazas, retención, accesos, salidas, atmósfera y duración | Layout y necesidades humanas; programa humano posterior |
| Carga | Masa, embalaje, sujeción, envolvente y clasificación | Manifiesto, acceso y análisis de cargas |
| Mantenimiento | Herramientas, inspección, ciclos/vida y rechazo | Procedimiento y campaña de cambios |

Estados: `UNINSTALLED → INSTALLED_UNVERIFIED → LOCKED → SERVICES_CHECKED → RELEASED`. Discrepancias llevan a `REJECTED` o `MAINTENANCE`. Identificar electrónicamente el módulo no sustituye comprobar sus retenciones mecánicas. Desconectar sólo tras aislar y asegurar.

IF-05/06/08 y, cuando proceda, IF-10 siguen vigentes. No circular propelente por esta interfaz genérica ni retirar casco/estructura primaria durante cambio ordinario.

| Abierto | Responsable propuesto | Gate |
|---|---|---|
| Geometría, puertas y posición WH/MR/TS | SYS + estructura | G0 rangos; G1 baseline |
| Masa bruta, CG, inercia y cargas | Estructura + GNC | G1 |
| Potencia, térmico, ocupación y duración | EPS + THM + factores humanos | G1 conceptual |
| Tiempo y repetibilidad de conversión | Integración/mantenimiento | G2 |

Estado actual: valores no congelados, compatibilidad física no aprobada.

## Exploración 0.4.0

El [modelo geométrico](../docs/GEOMETRY_AND_BALANCE.md) propone cajas y posiciones con revisión `0.1-study`. Esa revisión identifica hipótesis de simulación, no compatibilidad aprobada. La [evidencia parcial](../evidence/P0-021/README.md) no verifica instalación continua, anclajes ni CG global.
