"""Reproduce partial geometry evidence and top-down vector diagrams."""
import hashlib
import json
from pathlib import Path
from html import escape
from layout_check import analyze

ROOT = Path(__file__).resolve().parents[1]


def svg(result, spec):
    scale=62
    width=850
    height=round(spec['cabin_size_m'][1]*scale+160)
    def rect(center,size,color,label=''):
        x=60+(center[0]-size[0]/2)*scale
        y=80+(spec['cabin_size_m'][1]/2-center[1]-size[1]/2)*scale
        w,h=size[0]*scale,size[1]*scale
        text=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}" stroke="#334155"/>'
        if label: text+=f'<text x="{x+w/2}" y="{y+h/2}" text-anchor="middle" font-size="13">{escape(label)}</text>'
        return text
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
         '<style>text{font-family:Arial,sans-serif;fill:#0f172a}</style>',
         '<rect width="100%" height="100%" fill="#f8fafc"/>',
         f'<text x="30" y="28" font-size="19">{escape(result["case_id"])} — vista superior conceptual</text>',
         '<text x="30" y="51" font-size="12">X hacia popa → · Y positivo arriba · dimensiones en metros · no es plano de fabricación</text>']
    cabin=spec['cabin_size_m']
    out.append(rect([cabin[0]/2,0,cabin[2]/2],cabin,'#ffffff'))
    for zone in spec['reserved_boxes']: out.append(rect(zone['center_m'],zone['size_m'],'#cbd5e1'))
    for mod in result['installed_modules']:
        out.append(rect(mod['center_m'],mod['size_m'],'#a5f3fc' if mod['kind']=='PAX4' else '#fde68a',mod['id']+' '+mod['kind']))
    cg=result['payload_cg_m']
    cx,cy=60+cg[0]*scale,80+(cabin[1]/2-cg[1])*scale
    out += [f'<circle cx="{cx}" cy="{cy}" r="6" fill="#dc2626"/>',
            f'<text x="30" y="{height-42}" font-size="13">Cian: PAX-4 · amarillo: CARGO · gris: pasillo reservado · rojo: CG del interior</text>',
            f'<text x="30" y="{height-20}" font-size="12">Cabina {cabin[0]} × {cabin[1]} m · CG ({cg[0]:.3f}, {cg[1]:.3f}, {cg[2]:.3f}) · {result["partial_check_status"]} · NOT_RELEASED</text>', '</svg>']
    return '\n'.join(out)+'\n'


def main():
    names=['wh_combi','mr_combi','ts_cargo','wh_unbalanced_unload']
    catalog=json.loads((ROOT/'models/module_assumptions.json').read_text())
    geometry=json.loads((ROOT/'models/geometry_assumptions.json').read_text())
    folder=ROOT/'evidence/P0-021'
    folder.mkdir(parents=True,exist_ok=True)
    results=[]
    paths=['models/module_assumptions.json','models/geometry_assumptions.json','software/payload_budget.py','software/layout_check.py','software/generate_layout_report.py']
    for name in names:
        path=f'models/layouts/{name}.json'; paths.append(path)
        result=analyze(catalog,geometry,json.loads((ROOT/path).read_text()))
        results.append(result)
        (folder/f'{name}.svg').write_text(svg(result,geometry['vehicles'][result['vehicle']]))
    hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}
    (folder/'layout_results.json').write_text(json.dumps({'requirement_status':'OPEN','scope':'partial geometry and payload CG only','input_and_code_sha256':hashes,'results':results},indent=2)+'\n')
    lines=['# P0-021 / P0-022 — evidencia parcial de layout','','Requisitos abiertos. Geometría rectangular hipotética y CG del interior; no se evalúa el CG del vehículo completo ni el recorrido de instalación.','','| Caso | Masa interior kg | CG X/Y/Z m | Resultado parcial |','|---|---:|---|---|']
    for r in results:
        cg='/'.join(f'{v:.3f}' for v in r['payload_cg_m'])
        lines.append(f'| {r["case_id"]} | {r["payload_gross_mass_kg"]:.0f} | {cg} | {r["partial_check_status"]} |')
    lines += ['','El caso de descarga unilateral falla el rango Y hipotético: conservar masa admisible no garantiza equilibrio. Ningún caso libera operación.','','[Hipótesis y alcance](../../docs/GEOMETRY_AND_BALANCE.md) · [Resultados y hashes](layout_results.json).','','Reproducir: `python3 software/generate_layout_report.py`.']
    for name in names: lines += ['',f'## {name}','',f'![Layout {name}]({name}.svg)']
    (folder/'README.md').write_text('\n'.join(lines)+'\n')
    print('Generated 4 layouts, evidence table and JSON hashes')

if __name__ == '__main__':
    main()
