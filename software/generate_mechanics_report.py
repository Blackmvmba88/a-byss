"""Generate reproducible scalar comparison reports without rendering or solver dependencies."""
import hashlib
import json
from pathlib import Path
from xml.sax.saxutils import escape

from mechanical_screen import screen

ROOT = Path(__file__).resolve().parents[1]
LABELS = dict(axial='Carga axial', torsion='Torsión', separation='Separación de unión',
              fracture='Fractura', wear='Desgaste', fatigue='Fatiga')


def main():
    out = ROOT / 'evidence/mechanics'
    out.mkdir(parents=True, exist_ok=True)
    rows = ['# Comparación mecánica rápida', '',
            'Ejemplos escalares independientes. No son una evaluación estructural de CARGO-MR.', '',
            '![Comparación visual](comparison.svg)', '',
            '| Caso | Modo | Utilización | Estado |', '|---|---|---:|---|']
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="850" viewBox="0 0 1100 850">',
           '<rect width="1100" height="850" fill="white"/>',
           '<g font-family="sans-serif" fill="#111">',
           '<text x="30" y="35" font-size="24">A-BYSS · FILTRO MECÁNICO RÁPIDO</text>',
           '<text x="30" y="62" font-size="16">Demo sintética ≠ capacidad del vehículo. Barras: demanda / límite introducido.</text>']
    manifest = {'inputs': {}, 'code': {}, 'release_status': 'NOT_RELEASED'}
    y = 105
    for name, filename in [('demo', 'demo.json'), ('cargo_mr', 'cargo_mr_pending.json')]:
        source = ROOT / 'models/mechanics' / filename
        manifest['inputs'][str(source.relative_to(ROOT))] = hashlib.sha256(source.read_bytes()).hexdigest()
        result = screen(json.loads(source.read_text()))
        (out / f'{name}_results.json').write_text(json.dumps(result, indent=2, allow_nan=False) + '\n')
        svg.append(f'<text x="30" y="{y}" font-size="20">{escape(result["case_id"])}</text>')
        y += 35
        for kind, check in result['checks'].items():
            ratio = check['utilization']
            value = '—' if ratio is None else f'{ratio:.3f}'
            rows.append(f'| {name} | {LABELS[kind]} | {value} | {check["status"]} |')
            color = '#aaa' if ratio is None else '#e33248' if ratio >= 1 else '#edb700' if ratio >= .8 else '#00a9c7'
            width = 0 if ratio is None else min(ratio, 1.5) * 240
            svg += [f'<text x="30" y="{y}" font-size="17">{LABELS[kind]}</text>',
                    f'<rect x="250" y="{y-18}" width="360" height="24" fill="#eee"/>',
                    f'<rect x="250" y="{y-18}" width="{width}" height="24" fill="{color}"/>',
                    f'<path d="M490 {y-22} v32" stroke="#111" stroke-width="2"/>',
                    f'<text x="630" y="{y}" font-size="16">{value} · {check["status"]}</text>']
            y += 42
        y += 25
    svg += ['<text x="30" y="785" font-size="15">Línea negra = 1.0. Amarillo desde 0.8: atención visual, sin margen de seguridad implícito.</text>',
            '<text x="30" y="812" font-size="15">Sin datos = sin barra. Escala hasta 1.5; cifra sin recorte. NOT_RELEASED.</text>', '</g></svg>']
    (out / 'comparison.svg').write_text('\n'.join(svg) + '\n')
    rows += ['', 'CARGO-MR permanece incompleto: faltan cargas, materiales y caracterización de uniones.', '',
             'La carga axial recibe una fuerza conocida; no calcula el empuje de un motor. Los colores del modelo 3D identifican piezas, no tensiones.', '',
             '[Métodos, supuestos y ejecución](../../docs/FAST_MECHANICS.md).']
    (out / 'README.md').write_text('\n'.join(rows) + '\n')
    for filename in ['software/mechanical_screen.py', 'software/generate_mechanics_report.py']:
        manifest['code'][filename] = hashlib.sha256((ROOT / filename).read_bytes()).hexdigest()
    manifest['outputs'] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in sorted(out.iterdir()) if p.is_file() and p.name != 'manifest.json'}
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')


if __name__ == '__main__':
    main()
