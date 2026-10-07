"""One-command A-BYSS -> 3defect -> Blender -> measured contract pipeline."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from bridges.mamba3d_bridge import make_contract, accept_measurements


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--provider',type=Path,required=True,help='Trusted local 3defect checkout')
    parser.add_argument('--blender',default='blender')
    parser.add_argument('--style',choices=['saturated','photocopy'],default='saturated')
    args=parser.parse_args()
    provider=args.provider.expanduser().resolve()
    validator=provider/'defect3d/asset_contract.py'
    if not validator.is_file(): parser.error('3defect asset_contract.py not found')
    executable=shutil.which(args.blender)
    if not executable: parser.error('Blender executable not found')
    work=ROOT/'work';work.mkdir(exist_ok=True)
    # Failed builds retain diagnostic logs in work, without replacing the last delivery.
    stage=Path(tempfile.mkdtemp(prefix='cargo-mr-',dir=work))
    spec=importlib.util.spec_from_file_location('provider_asset_contract',validator)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    try:
        contract=make_contract(json.loads((ROOT/'models/geometry_assumptions.json').read_text()))
        module.assert_valid_asset_contract(contract)
        (stage/'contract.json').write_text(json.dumps(contract,indent=2)+'\n')
        commands=[
          [executable,'--background','--factory-startup','--python-exit-code','2','--python',str(ROOT/'blender/build_cargo_mr.py'),'--','--provider',str(provider),'--contract',str(stage/'contract.json'),'--output',str(stage),'--style',args.style],
          [executable,'--background',str(stage/'cargo-mr.blend'),'--python-exit-code','2','--python',str(ROOT/'blender/measure_cargo_mr.py'),'--','--output',str(stage/'measurements.json')]]
        for label,command in zip(('build','measure'),commands):
            print(f'{label}: Blender',flush=True)
            with (stage/f'{label}.log').open('w') as log:
                subprocess.run(command,cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True)
        measurements=json.loads((stage/'measurements.json').read_text())
        verified=accept_measurements(contract,measurements)
        verified['exports']=['blend','glb','png','json']
        module.assert_valid_asset_contract(verified)
        (stage/'verified_contract.json').write_text(json.dumps(verified,indent=2)+'\n')
        artifacts=['contract.json','cargo-mr.blend','cargo-mr.glb','cargo-mr-preview.png','provider_execution.json','provider_geometry.json','pipeline_plan.json']
        evidence=['measurements.json','verified_contract.json']
        for name in artifacts+evidence:
            if not (stage/name).is_file() or (stage/name).stat().st_size==0: raise ValueError('Missing output: '+name)
        assetdir=ROOT/'assets/cargo-mr'; evdir=ROOT/'evidence/bridge-cargo-mr'
        assetdir.mkdir(parents=True,exist_ok=True);evdir.mkdir(parents=True,exist_ok=True)
        for name in artifacts: shutil.copy2(stage/name,assetdir/name)
        for name in evidence: shutil.copy2(stage/name,evdir/name)
        paths=['models/geometry_assumptions.json','bridges/mamba3d_bridge.py','bridges/run_cargo_mr.py','blender/build_cargo_mr.py','blender/measure_cargo_mr.py']
        paths += ['assets/cargo-mr/'+name for name in artifacts]+['evidence/bridge-cargo-mr/'+name for name in evidence]
        record={'status':'PASS_DIGITAL_ROUND_TRIP','measurement_scope':'reopened .blend; GLB exported but not independently reimported',
                'manufacturing_ready':False,'release_status':'NOT_RELEASED',
                'files_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}}
        (evdir/'run_manifest.json').write_text(json.dumps(record,indent=2)+'\n')
        print('PASS_DIGITAL_ROUND_TRIP: assets/cargo-mr and evidence/bridge-cargo-mr')
    except (ValueError,KeyError,OSError,subprocess.CalledProcessError) as exc:
        parser.exit(2,f'Bridge failed: {exc}\nDiagnostics: {stage}\n')

if __name__=='__main__': main()
