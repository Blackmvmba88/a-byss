"""Small, deterministic IF-11 plate/fastener trade study; no structural release."""
import hashlib
import itertools
import json
import math
from pathlib import Path
try:
    from .mechanical_screen import evaluate, number
except ImportError:
    from mechanical_screen import evaluate, number

ROOT = Path(__file__).resolve().parents[1]


def compare(data):
    if data['schema_version'] != 1:
        raise ValueError('Unsupported schema')
    density = number(data['density_kg_m3'], True)
    for key in ['tension_N', 'torque_Nm', 'retained_preload_fraction', 'stiffness_fraction']:
        if not data[key]:
            raise ValueError('Empty sweep')
        for value in data[key]:
            number(value)
            if key == 'retained_preload_fraction' and not 0 < value <= 1:
                raise ValueError('Invalid retained preload')
            if key == 'stiffness_fraction' and not 0 <= value <= 1:
                raise ValueError('Invalid stiffness fraction')
    results = []
    for v in data['variants']:
        for key in ['side_m', 'thickness_m', 'pitch_m', 'hole_diameter_m',
                    'fastener_assembly_mass_kg', 'preload_per_bolt_N']:
            number(v[key], True)
        if v['pitch_m'] + v['hole_diameter_m'] >= v['side_m'] or v['hole_diameter_m'] >= v['pitch_m']:
            raise ValueError('Overlapping holes or holes outside plate')
        volume = (v['side_m']**2 - math.pi*v['hole_diameter_m']**2)*v['thickness_m']
        mass = density*volume + 4*v['fastener_assembly_mass_kg']
        radius = v['pitch_m']/math.sqrt(2)
        cases = []
        for force, torque, retained, stiffness in itertools.product(
                data['tension_N'], data['torque_Nm'], data['retained_preload_fraction'], data['stiffness_fraction']):
            sep = evaluate('separation', dict(tensile_force_N=force, bolt_count=4,
                minimum_preload_per_bolt_N=retained*v['preload_per_bolt_N'],
                stiffness_fraction=stiffness, applicable=True, basis=data['basis']))
            cases.append(dict(tension_N=force, torque_Nm=torque, retained_preload_fraction=retained,
                stiffness_fraction=stiffness, separation=sep,
                torque_only_shear_per_bolt_N=torque/(4*radius),
                shear_capacity_status='INCOMPLETE'))
        results.append(dict(id=v['id'], partial_mass_kg=mass, cases=cases,
            separation_limit_cases=sum(c['separation']['utilization'] >= 1 for c in cases),
            worst_separation_utilization=max(c['separation']['utilization'] for c in cases)))
    return dict(variants=results, release_status='NOT_RELEASED',
                scope='Independent axial separation and pure torque demand. No combined-load acceptance.')


def main():
    source = ROOT/'models/mechanics/if11_variants.json'
    data = json.loads(source.read_text())
    result = compare(data)
    out = ROOT/'evidence/IF-11'
    out.mkdir(parents=True, exist_ok=True)
    (out/'results.json').write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')
    lines = ['# IF-11 — tres variantes de estudio', '',
             'Datos hipotéticos, masas parciales. NOT_RELEASED. Ninguna variante queda aprobada.', '',
             '![Placas y patrones](variants.svg)', '',
             '| Variante | Masa parcial (kg) | Peor índice separación | Casos ≥1 / total |',
             '|---|---:|---:|---:|']
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="960" height="370" viewBox="0 0 960 370">',
           '<rect width="960" height="370" fill="white"/>',
           '<g font-family="sans-serif" fill="#111"><text x="20" y="28" font-size="20">IF-11 · PLACAS HIPOTÉTICAS · MISMA ESCALA</text>']
    for i, (v, r) in enumerate(zip(data['variants'], result['variants'])):
        lines.append(f'| {r["id"]} | {r["partial_mass_kg"]:.4f} | {r["worst_separation_utilization"]:.3f} | {r["separation_limit_cases"]} / {len(r["cases"])} |')
        cx, cy, scale = 160+i*320, 165, 1800
        side, pitch, hole = [v[k]*scale for k in ['side_m','pitch_m','hole_diameter_m']]
        svg.append(f'<rect x="{cx-side/2}" y="{cy-side/2}" width="{side}" height="{side}" fill="{["#00d5ee","#ffe100","#ff7040"][i]}" stroke="black" stroke-width="2"/>')
        for x, y in itertools.product([-1,1], repeat=2):
            svg.append(f'<circle cx="{cx+x*pitch/2}" cy="{cy+y*pitch/2}" r="{hole/2}" fill="white" stroke="black"/>')
        svg.append(f'<text x="{cx-120}" y="285" font-size="16">{v["id"]}: lado {v["side_m"]*1000:.0f} / paso {v["pitch_m"]*1000:.0f} mm</text>')
        svg.append(f'<text x="{cx-120}" y="309" font-size="16">Espesor {v["thickness_m"]*1000:.0f} mm · {r["partial_mass_kg"]:.4f} kg</text>')
    svg += ['<text x="20" y="350" font-size="15">Vista superior. Colores = identidad, no resistencia. No es plano de fabricación.</text></g></svg>']
    (out/'variants.svg').write_text('\n'.join(svg)+'\n')
    lines += ['', 'B y C tienen igual resultado de separación porque comparten precarga y rango de rigidez supuesto. El espesor extra de C sólo cambia la masa en este modelo; su efecto estructural está pendiente.', '',
              'El conteo representa puntos de una cuadrícula, no probabilidad de fallo. Los valores de torsión no alteran el filtro axial independiente.', '',
              '[Hipótesis, límites y siguiente ensayo](../../docs/IF11_ANCHOR_STUDY.md).']
    (out/'README.md').write_text('\n'.join(lines)+'\n')
    paths = [source, ROOT/'software/if11_trade.py', ROOT/'software/mechanical_screen.py',
             out/'results.json', out/'README.md', out/'variants.svg']
    manifest = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    (out/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')


if __name__ == '__main__':
    main()
