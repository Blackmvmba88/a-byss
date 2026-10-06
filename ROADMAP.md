# ROADMAP — A-BYSS / BlackMamba Aerospace

Versión: 0.2.0 · Fecha: 2026-10-06 · Estado: propuesta de investigación.

> W-HALE lifts, M-RAY travels, T-SHARK moves fast, A-BYSS connects.

## Propósito y alcance

Desarrollar una arquitectura civil y modular de logística Tierra–órbita–Luna, mediante modelos reproducibles, ensayos de subsistemas y demostradores progresivos. Este roadmap convierte la conversación conceptual en una propuesta de trabajo; no acredita viabilidad, certificación ni capacidad operacional.

P0 valida física y arquitectura; P1 caracteriza subsistemas; P2 integra demostradores. Las operaciones orbitales, lunares y con personas requieren programas posteriores con sus propios requisitos, recursos y revisiones. El calendario se fija después de estimar equipo, presupuesto e instalaciones; las fases se gobiernan por evidencia, no por fechas prometidas.

Documentos asociados: [arquitectura](ARCHITECTURE.md) y [requisitos P0](P0_REQUIREMENTS.md).

## Fases, entregables y gates

| Fase | Trabajo y entregables versionados | Gate y criterio de salida | Dependencias |
|---|---|---|---|
| F0 — Baseline de misión | CONOPS; diccionario de unidades y marcos; registro de hipótesis; escenario de referencia; responsables; matriz de requisitos | G0: escenario completo, alcance civil aprobado y cero variables críticas sin valor o rango; P0-001/002/003 | Ninguna |
| F1 — Cierre P0 | Presupuestos de masa, delta-v, potencia, energía y calor; modelos atmosféricos/orbitales; estudio de reentrada; análisis de riesgos; ICD v0.1; informe de alternativas | G1: todos los requisitos P0 aplicables pasan con evidencia; cero fallos críticos abiertos; revisión independiente documentada | G0; prestaciones de la etapa de lanzamiento y datos de tecnologías candidatas |
| F2 — Bancos P1 | Sección de ala convencional e instrumentada; banco de docking; distribución eléctrica; circuito térmico; gemelo digital; control supervisor con inyección de fallos | G2: correlación modelo–ensayo dentro de tolerancias congeladas antes del ensayo; repetibilidad demostrada; todos los peligros del banco mitigados | G1 para hardware representativo; preparación de bancos de bajo riesgo puede comenzar antes |
| F3 — Integración en tierra / HIL | A-BYSS-G; emuladores M-RAY/T-SHARK; navegación y tráfico; carga/servicio; campañas nominales y degradadas; informes de configuración | G3: misión de extremo a extremo en hardware-in-the-loop; fallos y abortos ejecutados; interfaces compatibles; sin acciones críticas de cierre pendientes | G2; ICD revisados; instrumentos calibrados |
| F4 — Demostradores P2 | W-HALE-X atmosférico sin tripulación; M-RAY-X de cuerpo sustentador cuando proceda; T-SHARK-X como banco orbital emulado; informe de escalado | G4: cada demostrador cumple su propia envolvente y plan de ensayos; recuperación y contingencias verificadas; revisión específica previa a cualquier vuelo | G3 para subsistemas integrados; instalaciones, autorizaciones aplicables y recursos del ensayo |
| F5 — Demostración orbital civil sin tripulación | Programa separado: lanzamiento, A-BYSS núcleo/energía/comunicaciones y dos puertos candidatos; rendezvous; inspección; depósito experimental opcional | G5: cierre de requisitos orbitales nuevos, revisión de preparación y evidencia de operaciones/fin de vida; P0 no basta para autorizar esta fase | G4 pertinente; lanzador; segmento terreno; financiación; diseño detallado; gestión de residuos orbitales |
| F6 — Expansión de servicios | Carga, robótica y repostaje validados; más puertos según demanda; M-RAY logístico cislunar; T-SHARK logístico rápido | G6: beneficio logístico medido frente a baseline, compatibilidad y riesgos de cada incremento cerrados | G5; reposición de consumibles; transferencia de fluidos validada; mantenimiento |
| F7 — Investigación avanzada | Hábitat y transporte humano; gravedad artificial; fabricación y ensamblaje orbital; descenso lunar como paquetes separados | Gate propio por paquete: seguridad humana, dinámica, soporte vital o manufactura acreditados según misión | G6 pertinente; programas específicos. Ninguno es requisito para cerrar P0 |

## Orden de trabajo y camino crítico

```text
CONOPS → escenario y etapa de lanzamiento → masa + delta-v → misión factible
                                                     ↓
                                  potencia + térmico + consumibles
                                                     ↓
                            interfaces + fallos + integración → G1
                                                     ↓
                                      bancos → HIL → demostradores
```

El depósito depende de la elección de propelente y del balance térmico. El viaje lunar depende de masa, delta-v, reservas y reposición del depósito. El docking depende de navegación relativa, captura mecánica y autoridad de control. El hábitat depende de una arquitectura de supervivencia y evacuación independiente de los objetivos de carga.

Después de G0, aerodinámica, órbitas y arquitectura del hub pueden estudiarse en paralelo usando la misma baseline. Cada cambio de masa o misión obliga a recalcular los presupuestos afectados. W-HALE no es una dependencia obligatoria del primer demostrador orbital: se comparará su contribución con lanzamiento terrestre convencional.

## Decisiones prioritarias

| Decisión | Evidencia requerida | Cierre previsto |
|---|---|---|
| Órbita inicial, carga, cadencia y tiempo máximo de misión | CONOPS y demanda hipotética explícita | G0 |
| Etapa externa de inserción y contribución real de W-HALE | Comparación masa/coste/energía con lanzamiento convencional | G1 |
| M-RAY integrado o módulos separados de transferencia, reentrada y descenso | Presupuestos y complejidad por alternativa | G1 |
| Significado medible de «fast» para T-SHARK | Tiempo de preparación + transferencia + servicio, con delta-v y reservas | G1 |
| Propelente, almacenamiento y política de repostaje | Compatibilidad, pérdidas, potencia de refrigeración y logística | G1 |
| Geometría del hub y separación depósito/hábitat | Plumas, fuga, cargas, térmico, accesibilidad y aislamiento | G1 conceptual; actualización en P1 |
| Superficies adaptativas, control de flujo y piel biomimética | Beneficio neto frente a ala convencional, incluyendo masa y energía | G2; no condicionan P0 |

## Gestión de gates y cambios

Cada gate genera acta con versión de modelos, matriz de cumplimiento, riesgos residuales, acciones, responsable y decisión: pasar, repetir o reformular. Un resultado negativo es un resultado válido de investigación, pero no equivale a aprobar el gate. No se compensan incumplimientos de seguridad con buenos resultados de rendimiento.

Para modificar un umbral: registrar motivo, evidencia, impacto en interfaces y presupuestos, responsable de revisión y nueva versión; repetir verificaciones afectadas. No cambiar límites después de observar resultados sólo para declarar éxito.

## Primera iteración ejecutable

1. Nombrar responsables de misión, modelos, interfaces y revisión.
2. Congelar un escenario logístico sin tripulación y una alternativa convencional.
3. Crear presupuestos enlazados de masa y delta-v antes de refinar geometrías.
4. Ejecutar pruebas analíticas de modelos y registrar incertidumbres.
5. Evaluar todos los P0 y emitir una decisión G1 con evidencia reproducible.

Estructura sugerida: `docs/`, `models/`, `interfaces/`, `simulation/`, `research/`, `tests/`, `evidence/` y `decisions/`. Cada informe debe indicar entradas, unidades, versión, método, límites de validez y ubicación de resultados.

## Incremento 0.2.0 — pasajeros y carga modulares

| Fase | Entregable adicional | Dependencia / salida |
|---|---|---|
| F0 | Comparativa de variantes WH-T/WH-L, MR y TS; posiciones y ocupación candidatas | PAX-4 es objetivo de estudio; congelar rangos antes de G0 |
| F1 | IF-11, manifiestos y modelo de capacidad por configuración | Cerrar P0-021…025 para configuración logística seleccionada; capacidad humana sólo conceptual |
| F2 | Banco de interior y sustitución PAX/CARGO sin ocupantes | Protocolo congelado antes de ensayar; ≥10 ciclos completos, 0 retenciones fallidas no detectadas, informe de tiempo/personas-hora y desgaste |
| F3 | Integración de detección de módulo y configuración inválida | Ningún módulo incompatible o manifiesto incompleto consigue liberación en catálogo de pruebas |
| F4–F7 | Demostración según entorno; conversión orbital y variantes humanas posteriores | Gates propios de vuelo, manipulación orbital y supervivencia; no inferirlos del banco de interiores |

Las clases WH/MR/TS se dimensionan de forma separada. Si los objetivos de 32/8/4 plazas no cierran, se revisan junto con posiciones, duración y arquitectura. La licencia de reutilización se elegirá como decisión del titular, sin bloquear el trabajo documental.
