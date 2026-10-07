# Puente A-BYSS → Mamba3D / 3defect — 0.5.0

2026-10-07 · Primer caso ejecutado: CARGO-MR en posición MR-02.

## Flujo real

```text
models/geometry_assumptions.json
    ↓ bridge: unidades, piezas, dimensiones, origen y referencias
assets/cargo-mr/contract.json          (Mamba3D 1.0, metros, concept)
    ↓ validador real de 3defect
3defect.Cube + CompositePart          (seis paneles separados)
    ↓ adaptador Blender de A-BYSS
cargo-mr.blend + cargo-mr.glb + preview PNG
    ↓ segundo proceso Blender: reabrir .blend y medir vértices evaluados
measurements.json
    ↓ comparar contra contrato original, sin cambiar sus objetivos
verified_contract.json               (prototype, dimensions=pass)
```

Se usa código real del checkout de `3defect`: primitivas, composición, serialización, validador de contrato y planificador. El archivo `pipeline_plan.json` contiene pasos propuestos por su planificador; no significa que se ejecutaron Rod Forge, el ensamblador externo u otros proveedores.

El adaptador Blender vive en A-BYSS y consume los bounds calculados por `3defect`. No usa el exportador genérico de escenas de ese repositorio: este adaptador conserva IDs estables y controla la escena propia para la medición de retorno. No se modificó el checkout de `3defect`.

## Uso

Requiere Python 3.9+ para el coordinador, Git, un checkout local de confianza de 3defect y Blender con NumPy disponible. Probado en Blender 5.2.0 LTS. La procedencia exacta se registra en [provider_execution.json](../assets/cargo-mr/provider_execution.json).

```bash
python3 bridges/run_cargo_mr.py --provider /ruta/al/checkout/3defect
```

`--blender /ruta/al/ejecutable` selecciona otra instalación. El coordinador ejecuta Blender en procesos independientes y temporales; no opera sobre una sesión abierta del usuario. Los resultados se copian a entregables después de verificar la medición. Diagnósticos y ejecuciones temporales quedan en `work/`, excluido de Git. El script usa un proveedor local explícito; no descarga ni actualiza repositorios automáticamente.

Para generar sólo contrato o verificar un reporte ya existente:

```bash
python3 bridges/mamba3d_bridge.py contract --output assets/cargo-mr/contract.json
python3 bridges/mamba3d_bridge.py verify assets/cargo-mr/contract.json evidence/bridge-cargo-mr/measurements.json --output evidence/bridge-cargo-mr/verified_contract.json
python3 -m unittest discover -s tests -v
```

La verificación aislada conserva la lista de exportaciones del contrato original; el coordinador completo la rellena después de generar archivos. El hash identifica entradas, no firma autenticidad de un reporte de terceros.

## Contrato y límites

- Fuente de dimensiones: clase MR, 2.4 × 2.0 × 2.2 m, posición MR-02 en el datum del interior.
- Seis paneles: BASE, TOP, PORT, STARBOARD, FORE y AFT; IDs estables, piezas editables separadas.
- Espesor gráfico de 0.04 m para construir el primer volumen hueco. Es una decisión de visualización, no cálculo de material o resistencia; la masa del catálogo no se deriva de esta geometría.
- Cuatro empties IF-11 como referencias geométricas. No representan herrajes, conectores físicos, mecanismos de bloqueo o cargas admisibles.
- Tolerancia de intercambio digital: 0.00001 m; no es tolerancia de fabricación. Se miden dimensiones, centros, orientación y referencias.
- Unidades: metros, mismos ejes XYZ entre A-BYSS y Blender. El GLB usa la conversión de ejes del exportador glTF; no se ha verificado por reimportación independiente.
- Preview en corte: TOP y PORT están ocultos sólo al renderizar. El `.blend` contiene las seis piezas y el GLB se exporta completo antes de ocultarlas.

`stage=prototype` describe existencia de un modelo digital. Sólo dimensiones reciben `pass`; interfaces físicas, ensamblaje de ingeniería y geometría de fabricación siguen `unknown`. `manufacturing.ready=false` y `NOT_RELEASED` permanecen explícitos. No se acredita G1, masa física, acceso continuo o diseño apto para vuelo.

## Trazabilidad

El contrato incluye hash canónico de la geometría fuente. El reporte de Blender conserva el hash del contrato utilizado; el verificador rechaza contratos distintos, unidades incorrectas, piezas faltantes/extra/duplicadas, posiciones o dimensiones fuera de tolerancia, NaN e interfaces geométricas desplazadas.

[run_manifest.json](../evidence/bridge-cargo-mr/run_manifest.json) registra hashes de fuentes y entregables. Los archivos binarios y renders pueden variar entre versiones de Blender; se comprueba resultado geométrico, no identidad binaria universal.

## Entregables

[Blender editable](../assets/cargo-mr/cargo-mr.blend) · [GLB](../assets/cargo-mr/cargo-mr.glb) · [Vista previa](../assets/cargo-mr/cargo-mr-preview.png) · [Evidencia](../evidence/bridge-cargo-mr/README.md).

Siguiente extensión: convertir PAX-4 al mismo contrato y comprobar el recorrido completo de instalación con la posición y la apertura. La conexión con Rod Forge y la reutilización del ensamblador de sockets siguen siendo posteriores; este primer puente ya ejecuta 3defect y Blender.
