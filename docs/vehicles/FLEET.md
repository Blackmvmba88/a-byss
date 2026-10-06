# Familia aeroespacial — definición inicial

Versión 0.2.0 · 2026-10-06 · Propuesta para comparar alternativas.

El usuario delegó la elección inicial de escala. Se propone PAX-4, cuatro plazas por módulo, con clases físicas separadas por vehículo. Las posiciones son hipótesis de dimensionamiento. La tripulación de operación se presupuesta aparte; si ocupa plazas del módulo, reduce pasajeros uno a uno.

| Plataforma | Posiciones candidatas | Plazas objetivo | Carga neta actual | Entorno |
|---|---:|---:|---|---|
| W-HALE-T | 8 WH | 32 | Por dimensionar | Atmósfera |
| M-RAY | 2 MR | 8 | Por dimensionar | Órbita/cislunar |
| T-SHARK | 1 TS | 4 | Por dimensionar | Órbita |

PAX-4 se adapta a cada clase. No implica que M-RAY pueda transportar ocho personas a la Luna ni que T-SHARK mantenga su rapidez con cuatro ocupantes; cada misión exige cierre propio.

## W-HALE — lifts

Aeronave reutilizable de transporte atmosférico pesado. Geometría blended-wing-body candidata y control convencional como referencia previa a superficies adaptativas.

**Variantes:** WH-T transporte modular; WH-L portador de etapa/vehículo de lanzamiento; WH-X demostrador atmosférico sin tripulación. WH-T admite estudio de PAX, CARGO y COMBI. WH-L tiene integración estructural y separación propias: no es una sustitución ordinaria de asientos. No se propone lanzar una etapa con pasajeros a bordo en la baseline.

**Permanentes:** estructura, alas, propulsión, controles, tren, alimentación principal, casco de presión cuando aplique y vías de evacuación. **Intercambiables:** módulos de interior y sujeciones compatibles.

**Layouts objetivo:** 32 pasajeros; 16 pasajeros + cuatro posiciones de carga; ocho posiciones de carga. Autonomía, dimensiones y carga total permanecen abiertas. El presupuesto del lanzador en WH-L es independiente del interior WH-T.

## M-RAY — travels

Transporte orbital/cislunar con núcleo de propulsión, aviónica, potencia, térmico y docking. El interior modular ocupa un volumen de misión. La variante humana requiere supervivencia dimensionada por ocupación y duración.

**Variantes:** MR-C carga, MR-P transporte humano futuro, MR-R retorno atmosférico opcional y MR-L sistema lunar opcional. MR-R necesita TPS y reentrada; MR-L requiere descenso propulsivo en módulo separado o cierre de una variante integrada. Instalar PAX no habilita esas capacidades.

**Layouts objetivo:** dos módulos PAX-4 (8 plazas), PAX-4 + carga (4 plazas), o dos módulos de carga. Una misión larga puede dedicar una posición a habitabilidad y reservas, reduciendo plazas. Un asiento de lanzamiento no sustituye un volumen habitable.

**Abiertos:** misión, delta-v, duración, consumibles, protección, contingencias, retorno y lanzador.

## T-SHARK — moves fast

Vehículo orbital compacto para inspección, servicio y pequeños envíos urgentes. Rapidez se mide como preparación + transferencia + servicio dentro de reservas. No se presupone vuelo atmosférico o salida desde pista.

**Variantes:** TS-C carga, TS-S servicio/sensores, TS-P transporte humano futuro.

**Layouts objetivo:** una posición con PAX-4, CARGO o SERVICE. Un inserto mixto PAX-2/CARGO queda como alternativa futura con interfaz propia, fuera del catálogo baseline.

Si cuatro plazas no cierran en masa, geometría o respuesta rápida, reducir plazas o mantener plataforma no tripulada. La misión tiene prioridad sobre conservar la cifra de asientos.

## A-BYSS — connects

Recibe vehículos, carga y equipos; registra clase, revisión, masa, CG, compatibilidad y vida de módulos. Cada escotilla, manipulador y puerto necesita compatibilidad física propia.

La conversión de interiores en órbita queda para una fase posterior: requiere manipulación, almacenamiento de módulos retirados, acceso, aislamiento y liberación. W-HALE permanece en la Tierra; el hub no recibe módulos WH sin cadena de lanzamiento e integración validada.

## Cierre de capacidad

Registrar por variante: misión, configuración, masa vacía, propelente, reservas, límites de lanzamiento/aterrizaje o inserción, interfaces, volumen, accesos, tripulación, pasajeros y consumibles. Ver [modularidad](../MODULAR_PAYLOAD.md) y [requisitos](../../P0_REQUIREMENTS.md).
