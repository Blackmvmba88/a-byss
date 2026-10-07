"""Per-position eccentric load precursor, with explicit stop at local opening."""
import hashlib
import itertools
import json
import math
from pathlib import Path
try:
    from .mechanical_screen import number
except ImportError:
    from mechanical_screen import number
ROOT=Path(__file__).resolve().parents[1]


def finite_signed(value):
    if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value):
        raise ValueError('Expected finite signed number')
    return value


def solve(pitch, force, ex, ey, torque, preload, stiffness):
    for value in [pitch,preload]: number(value,True)
    number(force);number(stiffness)
    if stiffness > 1: raise ValueError('Invalid stiffness fraction')
    for value in [ex,ey,torque]: finite_signed(value)
    coords=list(itertools.product([-pitch/2,pitch/2],repeat=2))
    sx=sum(x*x for x,y in coords);sy=sum(y*y for x,y in coords)
    polar=sx+sy
    rows=[]
    for i,(x,y) in enumerate(coords):
        # Force normal to XY at (ex,ey): Mx=F*ey, My=-F*ex.
        local=force/4 + force*ex*x/sx + force*ey*y/sy
        ratio=(1-stiffness)*local/preload
        rows.append(dict(id=i+1,x_m=x,y_m=y,external_normal_share_N=local,
            shear_x_N=-torque*y/polar,shear_y_N=torque*x/polar,
            separation_index=ratio,
            bolt_tension_N=preload+stiffness*local if local>=0 and ratio<1 else None))
    applicable=all(r['external_normal_share_N']>=0 for r in rows)
    status=('OUTSIDE_MODEL' if not applicable else 'LOCAL_OPENING_LIMIT' if
            any(r['separation_index']>=1 for r in rows) else 'BELOW_LOCAL_OPENING_LIMIT')
    if status!='BELOW_LOCAL_OPENING_LIMIT':
        # The complete group needs redistribution once any local joint opens.
        for row in rows: row['bolt_tension_N']=None
    return dict(status=status,positions=rows,combined_strength_status='INCOMPLETE',release_status='NOT_RELEASED')


def main():
    paths=[ROOT/'models/mechanics/if11_variants.json',ROOT/'models/mechanics/if11_eccentric.json']
    trade,config=[json.loads(p.read_text()) for p in paths]
    if config['schema_version']!=1: raise ValueError('Unsupported schema')
    b=next(v for v in trade['variants'] if v['id']=='B')
    cases=[]
    for offset,force,torque,retention,stiffness in itertools.product(config['offsets_m'],trade['tension_N'],config['torque_Nm'],trade['retained_preload_fraction'],trade['stiffness_fraction']):
        r=solve(b['pitch_m'],force,*offset,torque,config['reference_preload_N']*retention,stiffness)
        cases.append(dict(offset_m=offset,force_N=force,torque_Nm=torque,retention=retention,stiffness_fraction=stiffness,**r))
    out=ROOT/'evidence/IF-11/eccentric';out.mkdir(parents=True,exist_ok=True)
    (out/'results.json').write_text(json.dumps(dict(cases=cases,basis=config['basis'],release_status='NOT_RELEASED'),indent=2,allow_nan=False)+'\n')
    lines=['# B — carga descentrada','',
           'Hipótesis de placa rígida y uniones iguales; no valida la placa de 4 mm. NOT_RELEASED.','',
           '| Desplazamiento X / Y (mm) | Peor índice local | Casos con apertura / total |',
           '|---|---:|---:|']
    for offset in config['offsets_m']:
        subset=[c for c in cases if c['offset_m']==offset]
        peak=max(p['separation_index'] for c in subset for p in c['positions'])
        count=sum(c['status']=='LOCAL_OPENING_LIMIT' for c in subset)
        lines.append(f'| {offset[0]*1000:g} / {offset[1]*1000:g} | {peak:.3f} | {count}/{len(subset)} |')
    lines+=['','Al alcanzar apertura en una posición, se anula la predicción de tensión de todo el grupo. El reparto lineal queda como indicador previo, no como solución posterior a separación.','',
            '[Método y consecuencias](../../../docs/IF11_ECCENTRIC.md).']
    (out/'README.md').write_text('\n'.join(lines)+'\n')
    paths += [ROOT/'software/if11_eccentric.py',ROOT/'software/mechanical_screen.py',out/'results.json',out/'README.md']
    (out/'manifest.json').write_text(json.dumps({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},indent=2)+'\n')


if __name__=='__main__': main()
