# ARCHITECTURE — A-BYSS / BlackMamba Aerospace

Versión: 0.1 · Fecha: 2026-10-06 · Estado: arquitectura candidata de investigación civil.

> W-HALE lifts, M-RAY travels, T-SHARK moves fast, A-BYSS connects.

## 1. Contexto y baseline

La familia conecta atmósfera, órbita terrestre y espacio cislunar mediante máquinas especializadas. P0 estudia una misión logística sin tripulación. El transporte humano y el descenso lunar se mantienen como extensiones sujetas a validación separada.

La conversación aporta el concepto, no prestaciones demostradas. Las alas adaptativas, la piel biomimética, la criogenia de larga duración, la gravedad artificial y la fabricación orbital son líneas de investigación. La mitigación de ráfagas se evaluará como reducción de cargas/aceleración; no se exige eliminar la turbulencia atmosférica.

## 2. Topología del sistema

```text
TIERRA / infraestructura de carga y mantenimiento
   ├─ W-HALE → entrega atmosférica → ETAPA DE LANZAMIENTO EXTERNA ─┐
   └─ lanzamiento terrestre convencional ────────────────────────┤
                                                                ↓
                    inserción orbital → vehículo/carga → A-BYSS
                                                         ↕   ↕
                                                      M-RAY T-SHARK
                                                         ↕
                                              destinos cislunares
                                              / módulo lunar opcional

SEGMENTO TERRENO ↔ comunicaciones, planificación y supervisión
```

W-HALE no alcanza órbita ni se acopla al hub. La etapa de lanzamiento tiene presupuesto, interfaces y riesgos propios; ningún cierre de misión puede omitirla. Repostar redistribuye la logística de masa y energía: todo recurso del depósito necesita una cadena de suministro.

| Elemento | Responsabilidad | Subsistemas candidatos | Límite funcional |
|---|---|---|---|
| W-HALE | Elevar carga/etapa hasta un estado de entrega atmosférico y regresar | Estructura BWB candidata, propulsión atmosférica, superficies convencionales, sensores, GNC, tren de aterrizaje, interfaz de carga/separación | Sin inserción orbital; mejoras adaptativas sólo tras baseline convencional |
| M-RAY | Transporte logístico orbital/cislunar; futura evolución humana | Estructura, propulsión y RCS, navegación, docking, potencia, térmico, comunicaciones; TPS para variante de retorno | Reentrada y descenso lunar no se presuponen resueltos por el mismo vehículo |
| T-SHARK | Inspección, servicio y logística de respuesta rápida | Propulsión/RCS, navegación relativa, sensores, carga útil modular, docking, potencia, control térmico | «Fast» se mide en tiempo total de servicio dentro del presupuesto; no velocidad ilimitada |
| A-BYSS | Conectar tráfico, recursos, energía, mantenimiento y carga | Núcleo, puertos, energía, radiadores, depósito aislable, carga y robótica; hábitat futuro | El núcleo coordina; cada módulo mantiene protección local y aislamiento |
| Lanzamiento externo | Pasar del estado de entrega a inserción orbital | Etapas y sistemas de separación/propulsión según alternativa | Debe cerrar masa, cargas y trayectoria con el vehículo transportado |
| Segmento terreno | Preparación, supervisión, análisis y recuperación | Control de misión, estaciones de enlace, repositorio de configuración y simulación | La pérdida de enlace no debe impedir una respuesta local segura |

## 3. A-BYSS modular

```text
                         ENERGÍA / ARRAYS
                                |
PUERTO A ── aislador ── NÚCLEO ── aislador ── PUERTO B
                         |  |  |
                       CARGA | ROBÓTICA
                             |
                    SERVICIO / interfaz aislable
                             |
                       DEPÓSITO separado

HÁBITAT futuro → zona separada y aislable, con supervivencia propia
RADIADORES → circuitos compatibles con cada dominio térmico
```

La forma radial es candidata. La separación física de depósitos se determina por análisis de fugas, plumas, cargas y calor; las distancias mencionadas en la conversación no son distancias de seguridad acreditadas. El depósito experimental puede incorporarse después del núcleo inicial.

El reemplazo modular requiere interfaces desacoplables, rutas alternativas de servicios críticos y una configuración estable durante mantenimiento. Retirar el núcleo estructural no es una operación ordinaria; su reemplazo requeriría un modo específico validado. La modularidad no elimina dependencias estructurales.

## 4. Interfaces y contratos

Cada ICD (Interface Control Document) registra propietario en ambos extremos, versión, unidades SI, marcos de referencia, rangos nominales/degradados, tolerancias, secuencia de conexión, interlocks, fallos, desconexión segura y método de verificación. Compatibilidad lógica no implica compatibilidad mecánica o de fluidos.

| ID | Extremos | Contenido obligatorio | Condición de habilitación |
|---|---|---|---|
| IF-01 | Tierra ↔ W-HALE / lanzador | Masa, centro de gravedad, geometría, carga, abastecimiento y configuración | Configuración liberada y restricciones satisfechas |
| IF-02 | W-HALE ↔ carga/etapa | Cargas, fijación, energía/datos, estado de entrega y corredor de separación | Envolvente válida y confirmaciones independientes; separación inhibida fuera de límites |
| IF-03 | Lanzador ↔ vehículo/carga | Volumen, cargas, inserción, separación, telemetría | Trayectoria y presupuesto acordados |
| IF-04 | M-RAY/T-SHARK/carga ↔ puertos | Captura, cargas, navegación relativa, tolerancias, acoplamiento y liberación | Puerto reservado, estimación válida y corredor libre |
| IF-05 | Módulo/vehículo ↔ bus eléctrico | Tensión, corriente, polaridad, aislamiento, prioridad, preconexión y fallo | Compatibilidad y aislamiento comprobados antes de energizar |
| IF-06 | Redes vehículo/hub/terreno | Identidad, comandos, tiempo, marcos, calidad/edad de datos, prioridad y confirmación | Autenticación, autorización y datos vigentes |
| IF-07 | Depósito ↔ vehículo compatible | Especie química, limpieza, presión, temperatura, caudal, sellado, masa y venteo | Captura estable, ensayo de estanqueidad e interlocks; incompatible = transferencia bloqueada |
| IF-08 | Módulos ↔ servicios térmicos | Calor, temperatura, presión, fluido, conectores y aislamiento | Compatibilidad química y térmica; sin unir circuitos incompatibles |
| IF-09 | Robótica ↔ módulo/carga | Grapple, cargas, volumen barrido, herramientas y parada | Zona excluida, objetivo autorizado y actitud estable |
| IF-10 | Hábitat futuro ↔ vehículo/hub | Presión, atmósfera, escotillas, contaminación y evacuación | Integridad y compatibilidad acreditadas; no se infiere de docking de carga |

No todos los puertos transportan fluidos, calor o personas. Usar perfiles de servicio declarados: carga, inspección, repostaje y, posteriormente, tripulación. IF-07 debe ser específico por recurso.

## 5. Subsistemas transversales

- **GNC:** estimación de posición, velocidad, actitud y tasas con covarianza, calidad y edad de datos; marcos y tiempo explícitos. Rendezvous y captura se autorizan por etapas.
- **Potencia:** generación solar candidata, almacenamiento, distribución redundante y desconexión selectiva. Reservar energía para eclipse, aborto y estado seguro.
- **Térmico:** balance integrado de radiación, conducción, disipación interna y orientación; refrigeración criogénica se presupuesta por separado. Radiadores y plumas tienen restricciones geométricas.
- **Propulsión y fluidos:** presupuestos por segmento, inventario verificable, aislamiento local y control de presión. Elección de propelente abierta en P0.
- **Estructura y salud:** cargas estáticas/dinámicas, fatiga, impactos y medición de deformación. El gemelo digital informa incertidumbre; porcentajes genéricos de «salud» no sustituyen criterios de aceptación.
- **Software y comunicaciones:** separar comandos críticos, telemetría y carga útil; registrar configuración y eventos; admitir operación autónoma limitada durante pérdida de enlace.
- **Robótica:** inspección y manipulación con zonas de exclusión, límites de fuerza/movimiento y parada verificable.
- **Soporte vital futuro:** presión, atmósfera, agua, control de CO₂, incendio, radiación y refugio/evacuación; fuera del demostrador P0 sin tripulación.

## 6. Modos y transiciones

| Elemento | Secuencia nominal | Modos degradados y límites |
|---|---|---|
| W-HALE | Preparación → ascenso → entrega → regreso → inspección | Cancelar entrega ante navegación/cargas inválidas; continuar con carga sólo si la configuración es recuperable y validada |
| M-RAY | Preparación → inserción externa → crucero → rendezvous → docking → servicio → salida/transferencia | Hold, retirada o retorno según reservas y trayectoria; reentrada/descenso son secuencias de variantes específicas |
| T-SHARK | Espera → despacho → transferencia → inspección/servicio → regreso | Suspender servicio y retirarse ante pérdida de navegación o reserva mínima; objetivo rápido subordinado a seguridad |
| A-BYSS | Despliegue → comisionado → operación → recepción → servicio → liberación → mantenimiento | Aislamiento de módulo, gestión de emergencia, reducción de cargas y estado seguro definido por amenaza |

Cada transición requiere guardas, plazo, autoridad, confirmación y alternativa. No existe un único estado seguro universal: una fuga exige aislamiento; una aproximación fallida puede exigir retirada; un fallo eléctrico exige preservar cargas críticas. Estas respuestas se definen por escenario en P0-013/014.

Secuencia de docking: reserva → aproximación lejana → punto de espera → autorización local → aproximación final → captura → verificación estructural → habilitación de servicios. Una pérdida de navegación válida bloquea el avance. Fluido/energía y apertura de escotillas tienen habilitaciones independientes.

## 7. Safety boundaries

| Frontera | Regla de arquitectura | Evidencia requerida |
|---|---|---|
| IA / control crítico | IA propone planes; supervisor determinista valida límites y controladores ejecutan. IA sin acceso directo a actuadores críticos ni modificación de límites durante operación | Inyección de comandos fuera de envolvente; todos rechazados y registrados |
| Vehículo / hub | Hub reserva tráfico y servicios; vehículo conserva capacidad local de hold/aborto. Autoridad de puerto y vehículo explícita | Pruebas de comandos contradictorios, enlace perdido y puerto ocupado |
| Depósito / resto | Aislamiento de fluidos, energía y riesgos térmicos; ningún repostaje con captura o compatibilidad no válidas | Análisis de fuga/plumas y prueba de interlocks |
| Potencia / datos | Fallos de un módulo no se propagan sin contención; redes críticas separadas de cargas experimentales | Inyección de corto, nodo defectuoso y pérdida de bus |
| Hábitat / zonas de servicio | Supervivencia, aislamiento y evacuación definidos sin depender de una sola zona de riesgo | Programa de seguridad humana posterior; no se acredita en P0 |
| Experimento / baseline | Piel inteligente, IA y superficies adaptativas no son la única vía de control seguro | Comparación con configuración convencional y degradación verificable |
| Operación / ambiente | Corredores de aproximación, exclusión de plumas y robótica; disposición de fin de vida | Geometría y análisis por misión, actualizados tras cada cambio |

La redundancia se analiza incluyendo causas comunes: alimentación, sensores, software, entorno y conexiones. Tres computadoras idénticas no demuestran independencia. P0 identifica fallos únicos peligrosos y propone contención; la seguridad de hardware requiere evidencia posterior.

## 8. Decisiones abiertas y trazabilidad

Órbita, masas, número de vehículos, propelente, potencia, distancias de separación, dimensiones de puerto y capacidades lunares permanecen por decidir en G0/G1. Las opciones se comparan con supuestos comunes. Mantener un registro ADR por decisión, vinculado a requisito, interfaz y evidencia.

La evidencia se organiza como `evidence/<ID>/<revision>/`: entradas, modelo, versión, resultados, incertidumbres y revisión. Las propuestas de umbrales están en [P0_REQUIREMENTS.md](P0_REQUIREMENTS.md); la secuencia de maduración está en [ROADMAP.md](ROADMAP.md).
