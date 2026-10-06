# P0_REQUIREMENTS — A-BYSS / BlackMamba Aerospace

Versión: 0.1 · Fecha: 2026-10-06 · Estado: requisitos propuestos para validación conceptual.

> W-HALE lifts, M-RAY travels, T-SHARK moves fast, A-BYSS connects.

## Alcance y reglas de lectura

P0 debe determinar si una misión civil, modular y sin tripulación cierra físicamente y tiene una arquitectura verificable. Los números de este documento son **umbrales iniciales propuestos**, no datos de la conversación, límites certificados ni capacidades demostradas. Deben revisarse y congelarse antes de ejecutar la campaña. No autorizan vuelo, repostaje real ni transporte humano.

G0 fija el escenario y los rangos; G1 evalúa su cumplimiento. Un requisito con dato crítico pendiente queda **abierto**, nunca aprobado por ausencia de evidencia. Si una función se excluye de la baseline, se registra N/A con justificación e impacto: su capacidad no podrá anunciarse como validada. Todos los requisitos aplicables son obligatorios para cerrar P0.

Métodos: **I** inspección documental; **A** análisis; **S** simulación; **T** ensayo (sólo donde exista banco). Roles propuestos, pendientes de asignación: MIS misión, SYS sistemas, AER aerodinámica, ORB órbitas/propulsión, THM térmico, EPS potencia, SW software, SAF seguridad, V&V verificación. V&V revisa resultados de otro responsable.

## Tabla de requisitos

| ID / responsable | Requisito P0 | Métrica | Umbral inicial propuesto | Método de verificación | Criterio de salida / gate |
|---|---|---|---|---|---|
| P0-001 / MIS | Definir misión logística de referencia y alternativa convencional | Campos completos: carga, masas, órbita, cadencia, duración, lanzamiento, destinos, reservas, retorno/fin de vida | 10/10 campos con valor o rango; 0 campos críticos sin resolver | I: CONOPS y registro de hipótesis | Baseline versionada y revisada; G0 |
| P0-002 / SYS | Trazar funciones a vehículos, interfaces y evidencia | Cobertura de funciones/requisitos aplicables | 100%; 0 funciones críticas sin propietario | I: matriz de trazabilidad | Matriz completa, roles asignados; G0 |
| P0-003 / V&V | Hacer reproducibles los modelos | Modelos con unidades, marcos, versión, entradas, semilla si aplica y ejecución documentada | 100%; un revisor reproduce resultados dentro de tolerancia numérica declarada | I + ejecución independiente | Paquete reproducible de baseline; G0; confirmar G1 |
| P0-004 / SYS | Cerrar masa de cada vehículo, hub y etapa externa | Margen `(masa admisible − masa presupuestada)/masa admisible`; cobertura de partidas | Margen ≥20% en baseline conceptual; 100% partidas de estructura, propulsión, energía, térmico, aviónica, carga, consumibles y adaptadores contabilizadas | A: presupuestos enlazados y sensibilidad | Cierre en todos los segmentos; sin doble conteo; G1 |
| P0-005 / ORB | Cerrar maniobras y reservas por segmento | Delta-v disponible / delta-v requerido; reservas de aborto | ≥1.15 por segmento propulsivo; combustible de aborto definido además de demanda nominal, sin contarlo dos veces | A + S: masa variable, pérdidas y maniobras | Todas las ramas nominales y de aborto seleccionadas factibles; G1 |
| P0-006 / ORB | Validar modelo orbital antes de usarlo | Deriva relativa de energía y momento angular en caso de dos cuerpos; diferencia de delta-v frente a solución analítica | Deriva ≤10⁻⁵ en 100 órbitas del caso de prueba; diferencia ≤1% | S: casos de dos cuerpos, transferencia analítica y convergencia de paso | Pruebas pasan; perturbaciones documentadas aparte; G1 |
| P0-007 / AER | Cerrar vuelo convencional de W-HALE en la envolvente elegida | Capacidad de sustentación/peso y empuje requerido/disponible en puntos congelados | Capacidad de sustentación/peso ≥1.20; empuje requerido ≤80% del disponible en puntos de entrega y crucero | A + S: polar convencional, balance de fuerzas y restricciones | Todos los puntos pasan; estabilidad/control y límites estructurales identificados; G1 |
| P0-008 / AER | Evaluar separación W-HALE–etapa sin contacto | Distancia mínima entre envolventes geométricas; violaciones en dispersión | ≥1 m adicional a envolventes con incertidumbre geométrica; 0 contactos en ≥1,000 casos dentro de rangos congelados | S: dinámica relativa y dispersión de estado, aerodinámica y actuadores | Campaña reproducible; corredor y aborto definidos; no acredita separación real; G1 |
| P0-009 / EPS | Cerrar potencia y energía de A-BYSS y vehículos | Margen de potencia; energía utilizable / demanda del peor eclipse + respuesta segura | Potencia disponible ≥1.25×demanda simultánea; energía utilizable ≥1.20×demanda incluyendo pérdidas y degradación asumida | A + S: ciclo temporal de misión | Sin déficit; cargas críticas y prioridades trazadas; G1 |
| P0-010 / THM | Cerrar balance térmico en casos caliente/frío | Capacidad de rechazo/demanda; distancia al límite de temperatura seleccionado | Rechazo ≥1.20×carga térmica caliente; ≥10 K de margen a límites de componentes no criogénicos; criogenia evaluada por P0-011 | A + S: régimen transitorio, orientación y eclipse | Ninguna excursión fuera de límites declarados; G1 |
| P0-011 / THM | Presupuestar almacenamiento y transferencia del recurso elegido | Fracción perdida durante permanencia de referencia; balance de masa | Pérdidas acumuladas ≤2% de inventario inicial; residuo de balance ≤1%; energía activa incluida en P0-009 | A + S: depósito, transferencia y duración fijados en G0 | Recurso compatible y caso nominal/degradado cerrado, o función excluida explícitamente; G1 |
| P0-012 / THM | Evaluar reentrada de variante M-RAY de retorno | Demanda térmica / capacidad candidata; temperatura estructural | Capacidad de absorber/rechazar energía ≥1.20×demanda integrada; temperatura ≥10 K por debajo del límite estructural seleccionado | A + S: perfiles de calentamiento y material/TPS candidato con incertidumbre | Perfil completo y limitaciones declaradas; no equivale a calificar TPS; G1 o N/A si no hay reentrada |
| P0-013 / SAF | Contener fallos únicos críticos en baseline | Fallos únicos analizados; peligros críticos sin respuesta viable | 100% del catálogo FMEA de funciones críticas cubierto; 0 peligros críticos sin mitigación y evidencia conceptual | A + S: FMEA, causas comunes y árbol de fallos | Respuestas con detección, aislamiento, plazo y reservas definidas; revisión SAF; G1 |
| P0-014 / SW | Respetar límites de seguridad y modos | Comandos fuera de envolvente bloqueados; transiciones inválidas; tiempo de respuesta | 100% bloqueados; 0 transiciones inválidas aceptadas en catálogo; detección+respuesta ≤50% del tiempo hasta peligro de cada escenario | S: inyección de fallos, datos obsoletos, enlace perdido y conflicto de autoridad | Todos los casos pasan; sin acceso directo de IA a actuadores críticos; G1 |
| P0-015 / SYS | Definir contratos de interfaces aplicables | ICD completos y consistentes en ambos extremos | 100% IF-01…IF-10 aplicables con rangos, unidades, secuencias, interlocks y responsables; 0 incompatibilidades abiertas | I + A: revisión cruzada de ICD | Contratos baseline aprobados para simulación/bancos; G1 |
| P0-016 / ORB | Demostrar rendezvous/captura simulada dentro de envolvente | Éxito nominal; violaciones de exclusión; velocidad de contacto | ≥99% éxitos en ≥1,000 casos nominales dispersos; 0 violaciones en campaña nominal/fallos; velocidad de contacto ≤0.10 m/s y dentro del límite mecánico elegido si es menor | S: navegación, control, geometría e incertidumbres | Fallos seleccionados terminan en hold/retirada segura; precisión angular/posición fijada por IF-04; G1 |
| P0-017 / MIS | Dar significado medible a T-SHARK moves fast | Tiempo despacho+transferencia+servicio frente a referencia para misma tarea/destino/carga | ≤80% del tiempo baseline; P0-004/005/013 también pasan | A + S: comparación pareada de misión | Beneficio y coste de propelente/energía reportados; si no pasa, reformular «fast»; G1 |
| P0-018 / SYS | Demostrar modularidad del hub | Módulos de servicio reemplazables; funciones críticas preservadas durante retiro | 100% de módulos de servicio previstos con secuencia de aislamiento/reemplazo; 0 pérdida de control, comunicación de emergencia o supervivencia energética durante caso analizado | I + S: retirar cada módulo en configuración de mantenimiento | Dependencias estructurales y restricciones explícitas; núcleo tratado por plan aparte; G1 |
| P0-019 / SYS | Evaluar robustez a incertidumbre | Cierre de presupuestos bajo rangos y esquinas adversas | 100% de esquinas críticas seleccionadas pasan; sensibilidad al menos a masa seca +20%, Isp −5%, demanda eléctrica +20% y disipación +20% respecto de estimaciones sin margen | A + S: sensibilidad individual y casos combinados físicamente compatibles | Sin usar margen dos veces; cualquier fallo obliga rediseño o cambio formal de baseline; G1 |
| P0-020 / SAF | Definir separación de riesgos y fin de vida | Escenarios de fuga, pluma, corto, robótica, pérdida de enlace y disposición final con respuesta | 6/6 familias cubiertas; 0 intersecciones no mitigadas de zonas de riesgo con áreas protegidas en configuración analizada | A + S: geometría, hazard log y secuencias | Zonas/distancias y estrategia de fin de vida justificadas por misión; G1 |

## Definiciones para evitar falsos cierres

- La masa presupuestada incluye propelente, consumibles, interfaces y crecimiento estimado; la masa admisible procede de capacidad documentada del elemento que soporta/transporta esa configuración. El margen del 20% no constituye una partida que pueda gastarse dos veces.
- Delta-v disponible usa masa inicial/final y rendimiento candidato del segmento; el requerido incluye pérdidas aplicables y maniobras de servicio. Trayectorias de aborto deben evaluarse desde estados concretos.
- «Tiempo hasta peligro» proviene del modelo del escenario, no de un plazo universal elegido por comodidad. Si no puede estimarse, P0-014 permanece abierto.
- Los porcentajes de éxito de simulación describen la campaña y sus distribuciones; no demuestran probabilidad de fallo operacional ni seguridad humana. Guardar semillas y todos los fallos, no sólo resultados exitosos.
- Capacidad térmica, propulsiva y eléctrica exige datos de una tecnología candidata y su incertidumbre. Si no hay datos adecuados, el resultado es una hipótesis pendiente.
- El escenario criogénico debe fijar duración, llenado, especie, orientación, presión y pérdidas de transferencia. No se extrapola una tasa constante sin justificarla.
- P0-019 aplica perturbaciones a estimaciones previas a márgenes. Registrar combinaciones correlacionadas y razones para excluir escenarios imposibles.

## Evidencia y criterio global de salida

Para cada ID guardar: responsable, estado (`abierto`, `pasa`, `falla`, `N/A`), versión de requisito, entradas, modelo, resultados, incertidumbre, informe de verificación y firma/fecha de revisión. Ruta sugerida: `evidence/<ID>/<revision>/`. Toda exclusión N/A debe aparecer también en CONOPS y arquitectura.

**G1 / salida de P0:** 100% de requisitos aplicables pasan; cero datos críticos sin resolver; cero peligros críticos sin mitigación conceptual; reproducción independiente completada; interfaces coherentes; lista explícita de capacidades todavía no verificadas. El acta decide avanzar a P1, repetir análisis o reformular la arquitectura. La aprobación de P0 acredita únicamente el cierre conceptual de la baseline estudiada.

Siguientes documentos: [ROADMAP.md](ROADMAP.md) y [ARCHITECTURE.md](ARCHITECTURE.md).

## Procedencia

Base conceptual: conversación «Eliminar turbulencias en aviones», ID `6aa01422-ce98-83e8-807c-b0a46462cc1b`, y solicitud de los tres documentos. Umbrales, gates y contratos detallados añadidos como propuestas para iterar; no se presentan como requisitos de una autoridad aeroespacial ni como resultados de ensayos.
