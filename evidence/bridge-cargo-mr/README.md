# Evidencia del bridge CARGO-MR

Fecha: 2026-10-07. Estado: **PASS_DIGITAL_ROUND_TRIP**.

- Blender 5.2.0 LTS; proveedor 3defect commit `ece85722d3bcb98b718900b79e8544c5cd7decde`.
- Seis piezas y cuatro referencias medidas al reabrir el `.blend` en un proceso independiente.
- Envolvente medida: [2.3999998569488525, 2.0, 2.199999999254942] m.
- Máxima diferencia dimensional por pieza: 1.43051147e-07 m; tolerancia digital 0.00001 m.
- Treinta pruebas de software aprobadas, diez específicas del bridge.
- Inyección real de escala X +1% en BASE, sólo en memoria: rechazada con salida 2.

## Archivos

- [Mediciones de Blender](measurements.json)
- [Contrato con mediciones aceptadas](verified_contract.json)
- [Manifest de ejecución y hashes](run_manifest.json)
- [Resultado de rechazo del modelo alterado](negative_probe.json)
- [Modelo editable y preview](../../assets/cargo-mr/README.md)
- [Cómo reproducir](../../docs/MAMBA3D_BRIDGE.md)

La aceptación acredita intercambio digital dimensional. Interfaces físicas y ensamblaje de ingeniería permanecen sin validar. El GLB fue exportado pero no reimportado para una comprobación independiente. No constituye validación estructural, masa real o capacidad de vuelo.
