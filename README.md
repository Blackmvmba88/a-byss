# A-BYSS / BlackMamba Aerospace

> W-HALE lifts, M-RAY travels, T-SHARK moves fast, A-BYSS connects.

Infraestructura aeroespacial civil, modular y de investigación para conectar Tierra, atmósfera, órbita y espacio cislunar.

**Estado:** arquitectura conceptual, versión 0.1. Los umbrales iniciales son propuestas pendientes de validación.

## Familia

| Plataforma | Función |
|---|---|
| W-HALE | Transporte atmosférico pesado y entrega de carga o etapa de lanzamiento. |
| M-RAY | Transporte orbital y cislunar. |
| T-SHARK | Inspección, servicio y logística de respuesta rápida. |
| A-BYSS | Hub orbital modular de conexión, recursos y mantenimiento. |

Una etapa de lanzamiento externa realiza la inserción orbital. El transporte humano, el descenso lunar, la gravedad artificial y la fabricación orbital son extensiones sujetas a programas de validación propios.

## Documentación

- [ROADMAP.md](ROADMAP.md): fases, entregables, gates y dependencias.
- [ARCHITECTURE.md](ARCHITECTURE.md): subsistemas, interfaces, modos y límites de seguridad.
- [P0_REQUIREMENTS.md](P0_REQUIREMENTS.md): veinte requisitos iniciales medibles y criterios de salida.

## Primera iteración

1. Asignar responsables de misión, sistemas, modelos y verificación.
2. Fijar una misión logística sin tripulación y una alternativa convencional.
3. Cerrar presupuestos enlazados de masa, delta-v, potencia y calor.
4. Registrar las decisiones y la evidencia de cada requisito P0.
5. Revisar el gate G1 antes de avanzar a prototipos representativos.

Los cambios de requisitos deben conservar su justificación, impacto, versión y evidencia. Cada resultado debe documentar entradas, unidades, método, incertidumbre y límites de validez.

## Organización futura

Crear `models/`, `simulation/`, `interfaces/`, `tests/`, `evidence/` y `decisions/` conforme existan contenidos. Actualmente el repositorio contiene la base documental; no incluye simuladores ni hardware validado.
