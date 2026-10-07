"""Source-tracked candidate and preload envelopes; neither torque prescription nor release."""
import copy
import hashlib
import json
from pathlib import Path
try:
    from .if11_trade import compare
    from .mechanical_screen import number
except ImportError:
    from if11_trade import compare
    from mechanical_screen import number
ROOT=Path(__file__).resolve().parents[1]


def assess(trade, candidate):
    if candidate['schema_version'] != 1:
        raise ValueError('Unsupported schema')
    proof=number(candidate['fastener']['proof_load_reference_N'],True)
    upper=number(candidate['upper_preload_multiplier'],True)
    if upper < 1:
        raise ValueError('Upper multiplier must be at least one')
    if not candidate['reference_preload_options_N']:
        raise ValueError('No preload options')
    baseline=next(v for v in trade['variants'] if v['id']=='B')
    study=copy.deepcopy(trade)
    study['density_kg_m3']=candidate['plate']['density_kg_m3']
    study['variants']=[]
    for preload in candidate['reference_preload_options_N']:
        number(preload,True)
        v=copy.deepcopy(baseline)
        v.update(id=f'B-P{preload:g}',preload_per_bolt_N=preload)
        study['variants'].append(v)
    result=compare(study)
    fmax=max(study['tension_N'])
    cmin=min(study['stiffness_fraction'])
    cmax=max(study['stiffness_fraction'])
    retention=min(study['retained_preload_fraction'])
    # Equality is onset of opening; reference preload must exceed this value.
    lower=(1-cmin)*fmax/(4*retention)
    upper_bound=(proof-cmax*fmax/4)/upper
    result['reference_preload_bounds_N']={
        'strict_lower_for_no_axial_opening':lower,
        'strict_upper_for_bolt_tension_below_provisional_proof':upper_bound,
        'nonempty':upper_bound>lower,
        'status':'MODEL_ENVELOPE_NOT_INSTALLATION_SPEC'}
    for v,preload in zip(result['variants'],candidate['reference_preload_options_N']):
        pmax=preload*upper
        closed=(1-cmax)*fmax < 4*pmax
        demand=pmax+cmax*fmax/4 if closed else None
        v['upper_preload_per_bolt_N']=pmax
        v['upper_envelope_bolt_tension_N']=demand
        v['bolt_tension_to_provisional_proof_ratio']=None if demand is None else demand/proof
        v['bolt_tension_status']='PROVISIONAL_REFERENCE_ONLY' if closed else 'OUTSIDE_CLOSED_JOINT_MODEL'
    result['candidate']=candidate['candidate']
    result['source_status']=candidate['fastener']['evidence_status']
    result['combined_load_status']='INCOMPLETE'
    result['scope']='Axial preload envelope only; pure torque demands retained without combined acceptance.'
    return result


def main():
    inputs=[ROOT/'models/mechanics/if11_variants.json',ROOT/'models/mechanics/if11_candidate.json']
    result=assess(*(json.loads(p.read_text()) for p in inputs))
    out=ROOT/'evidence/IF-11/candidate'
    out.mkdir(parents=True,exist_ok=True)
    (out/'results.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    rows=['# B — material y precarga candidatos','',
          '**NOT_RELEASED.** Referencia de perno provisional; documento completo y lote pendientes. Cargas y dispersión hipotéticas.','',
          '| Precarga referencia/perno | Peor índice separación | Casos ≥1 | Carga axial superior/perno | Cociente frente a prueba provisional |',
          '|---|---:|---:|---:|---:|']
    for v in result['variants']:
        demand=v['upper_envelope_bolt_tension_N']; ratio=v['bolt_tension_to_provisional_proof_ratio']
        rows.append(f'| {v["id"]} N | {v["worst_separation_utilization"]:.3f} | {v["separation_limit_cases"]}/{len(v["cases"])} | {demand} N | {ratio} |')
    bounds=result['reference_preload_bounds_N']
    rows+=['',f'Intervalo algebraico abierto: {bounds["strict_lower_for_no_axial_opening"]:.1f} < P_ref < {bounds["strict_upper_for_bolt_tension_below_provisional_proof"]:.1f} N por perno. Sólo dos restricciones axiales del modelo; no es rango autorizado de montaje.', '',
           'La masa parcial sigue siendo 0.1853 kg; los 20 g por conjunto de fijación siguen siendo una hipótesis.', '',
           '[Fuentes, supuestos y pendientes](../../../docs/IF11_CANDIDATE.md).']
    (out/'README.md').write_text('\n'.join(rows)+'\n')
    paths=inputs+[ROOT/f'software/{name}.py' for name in ['if11_candidate','if11_trade','mechanical_screen']]+[out/'results.json',out/'README.md']
    (out/'manifest.json').write_text(json.dumps({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},indent=2)+'\n')


if __name__=='__main__': main()
