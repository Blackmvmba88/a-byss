"""Regenerate illustrative evidence from the versioned catalog."""
import hashlib
import json
from pathlib import Path
from payload_budget import calculate

ROOT = Path(__file__).resolve().parents[1]

def main():
    raw = (ROOT / 'models/module_assumptions.json').read_bytes()
    catalog = json.loads(raw)
    cases = [('WH', 8), ('WH', 4), ('WH', 0), ('MR', 2), ('MR', 1), ('MR', 0), ('TS', 1), ('TS', 0)]
    results = [calculate(catalog, vehicle, pax, 100) for vehicle, pax in cases]
    folder = ROOT / 'evidence/P0-022'
    folder.mkdir(parents=True, exist_ok=True)
    hashes = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in
              ['models/module_assumptions.json', 'software/payload_budget.py', 'software/generate_payload_report.py']}
    (folder / 'exploratory_results.json').write_text(json.dumps(
        {'evidence_type': 'partial_arithmetic_only', 'requirement_status': 'OPEN',
         'input_and_code_sha256': hashes, 'results': results}, indent=2, ensure_ascii=False, allow_nan=False) + '\n')
    lines = ['# P0-022 — evidencia aritmética parcial', '',
             '**Estado del requisito: ABIERTO.** Asignaciones ilustrativas sin validar.', '',
             'Densidad aparente: 100 kg/m³. Las cifras de carga son cotas del interior bajo hipótesis; no son capacidades de vuelo.', '',
             '| Vehículo | Plazas objetivo ocupadas | Módulos CARGO | Cota de carga, kg | Masa instalada interior, kg |',
             '|---|---:|---:|---:|---:|']
    for r in results:
        lines.append(f"| {r['vehicle']} | {r['passenger_places_target']} | {r['cargo_modules']} | {r['cargo_net_upper_bound_kg']:.0f} | {r['installed_payload_gross_kg']:.0f} |")
    lines += ['', 'Reproducir desde raíz: `python3 software/generate_payload_report.py`.', '',
              '[Resultados y hashes](exploratory_results.json) · [Hipótesis y exclusiones](../../docs/SIZING_BASELINE.md).', '',
              'Faltan masa total de vehículo, misión, geometría/puertas, CG/inercia, cargas, potencia, térmico y servicios humanos. No existe revisión independiente de ingeniería; no se declara cierre de G0 o G1.']
    (folder / 'README.md').write_text('\n'.join(lines) + '\n')
    print('Generated evidence/P0-022/README.md and exploratory_results.json')

if __name__ == '__main__':
    main()
