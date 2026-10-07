"""Two simply supported strip surrogate; elastic demand only, no release."""
import hashlib
import json
import math
from pathlib import Path
try:
    from .mechanical_screen import number
except ImportError:
    from mechanical_screen import number
ROOT=Path(__file__).resolve().parents[1]


def strip_response(force,span,width,thickness,modulus):
    number(force)
    for value in [span,width,thickness,modulus]:number(value,True)
    load=force/2
    inertia=width*thickness**3/12
    moment=load*span/4
    stress=moment*(thickness/2)/inertia
    deflection=load*span**3/(48*modulus*inertia)
    return dict(load_per_strip_N=load,reaction_per_support_N=load/2,
                bending_stress_Pa=stress,midspan_deflection_m=deflection,
                status='ELASTIC_SURROGATE_ONLY',release_status='NOT_RELEASED')


def backing_mass(config,thickness):
    for key in ['strip_length_m','strip_width_m','support_span_m','hole_diameter_m','density_kg_m3']:
        number(config[key],True)
    number(thickness,True)
    length,width,span,diameter=[config[k] for k in ['strip_length_m','strip_width_m','support_span_m','hole_diameter_m']]
    if span+diameter>=length or diameter>=width or diameter>=span:
        raise ValueError('Holes outside strip or overlapping')
    # Two strips, two through holes each. Holes are counted only in mass.
    return 2*(length*width-2*math.pi*(diameter/2)**2)*thickness*config['density_kg_m3']


def main():
    source=ROOT/'models/mechanics/if11_support.json'
    c=json.loads(source.read_text())
    if c['schema_version']!=1:raise ValueError('Unsupported schema')
    rows=[]
    for thickness in c['thickness_options_m']:
        rows.append(dict(thickness_m=thickness,backing_strips_mass_kg=backing_mass(c,thickness),
            cases=[dict(force_N=f,**strip_response(f,c['support_span_m'],c['strip_width_m'],thickness,c['E_Pa'])) for f in c['source_force_N']]))
    out=ROOT/'evidence/IF-11/support';out.mkdir(parents=True,exist_ok=True)
    (out/'results.json').write_text(json.dumps(dict(variants=rows,basis=c['basis'],release_status='NOT_RELEASED'),indent=2,allow_nan=False)+'\n')
    text=['# Contraplaca dividida — respuesta elástica de estudio','',
          'Dos tiras de 100 × 25 mm; luz ideal 70 mm. Carga total 12 kN, 6 kN por tira. **No valida la pieza real.**','',
          '| Espesor | Masa de ambas tiras | Tensión nominal elástica | Flecha central |',
          '|---|---:|---:|---:|']
    for row in rows:
        r=row['cases'][-1]
        text.append(f'| {row["thickness_m"]*1000:g} mm | {row["backing_strips_mass_kg"]*1000:.1f} g | {r["bending_stress_Pa"]/1e6:.1f} MPa | {r["midspan_deflection_m"]*1000:.3f} mm |')
    text+=['','Los números son extrapolaciones elásticas; si el material plastifica, no predicen la respuesta real. Sin límite admisible ni selección aprobada. Masa del travesaño, soporte y herrajes excluida.','',
           '[Camino de carga y alcance](../../../docs/IF11_LOAD_PATH.md).']
    (out/'README.md').write_text('\n'.join(text)+'\n')
    files=[source,ROOT/'software/if11_support.py',ROOT/'software/mechanical_screen.py',out/'README.md',out/'results.json']
    (out/'manifest.json').write_text(json.dumps({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},indent=2)+'\n')


if __name__=='__main__':main()
