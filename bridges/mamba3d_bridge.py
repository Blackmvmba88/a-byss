"""A-BYSS source geometry -> Mamba3D contract -> strict measured feedback."""
import argparse
import copy
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(data):
    return hashlib.sha256(json.dumps(data,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()


def finite_vec(value, label, positive=False):
    if not isinstance(value,list) or len(value)!=3:
        raise ValueError(f'{label}: expected three values')
    for x in value:
        if isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x) or (positive and x<=0):
            raise ValueError(f'{label}: invalid number')
    return value


def make_contract(geometry, thickness=0.04):
    if geometry['schema_version'] != 1:
        raise ValueError('Unsupported geometry schema')
    spec=geometry['vehicles']['MR']
    if spec['interface_class']!='MR': raise ValueError('Expected MR class')
    size=finite_vec(spec['module_size_m'],'module dimensions',True)
    position=next((p for p in spec['positions'] if p['id']=='MR-02'),None)
    if position is None: raise ValueError('MR-02 missing')
    center=finite_vec(position['center_m'],'slot center')
    if isinstance(thickness,bool) or not isinstance(thickness,(int,float)) or not math.isfinite(thickness) or not 0<thickness<min(size)/2:
        raise ValueError('Invalid visual panel thickness')
    x,y,z=size; t=thickness
    parts=[]
    # Six touching boxes, no volumetric overlap. Thickness is visualization-only.
    layouts=[('BASE',[x,y,t],[0,0,-z/2+t/2]),('TOP',[x,y,t],[0,0,z/2-t/2]),
             ('PORT',[x,t,z-2*t],[0,-y/2+t/2,0]),('STARBOARD',[x,t,z-2*t],[0,y/2-t/2,0]),
             ('FORE',[t,y-2*t,z-2*t],[-x/2+t/2,0,0]),('AFT',[t,y-2*t,z-2*t],[x/2-t/2,0,0])]
    for name,dims,local in layouts:
        parts.append({'part_id':f'CARGO-MR-{name}','name':f'CARGO-MR-{name}',
                      'revision':'A-study','status':'pending','source':'generated','material':None,
                      'dimensions':{axis:{'target':v,'tolerance':1e-5,'measured':None,'status':'unknown'} for axis,v in zip('xyz',dims)},
                      'interfaces':[], 'center_m':[center[i]+local[i] for i in range(3)],
                      'geometry_family':'box','rotation_rad':[0,0,0]})
    sockets=[]
    for i,(sx,sy) in enumerate([(-1,-1),(-1,1),(1,-1),(1,1)],1):
        sockets.append({'id':f'IF-11-MR-{i:02d}','position_m':[center[0]+sx*(x/2-t),center[1]+sy*(y/2-t),center[2]-z/2],
                        'rotation_rad':[0,0,0],'status':'unknown'})
    parts[0]['interfaces']=[{'id':s['id'],'mate':None,'position_tolerance':1e-5,'angle_tolerance_deg':0.001,'status':'unknown'} for s in sockets]
    return {'schema_version':'1.0','asset_id':'ABYSS-CARGO-MR-001','revision':'A-study','stage':'concept','units':'m',
            'blueprint':{'id':'ABYSS-GEOMETRY-MR','revision':spec['interface_revision'],'source':'models/geometry_assumptions.json'},
            'parts':parts,'validation':{'dimensions':'unknown','interfaces':'unknown','assembly':'unknown','closed_geometry':'unknown'},
            'exports':[],'manufacturing':{'ready':False,'process':None,'material_spec':None,'evidence':[]},
            'bridge':{'version':1,'source_geometry_sha256':digest(geometry),'envelope_m':size,'position_m':center,
                      'sockets':sockets,'visual_panel_thickness_m':t,'digital_tolerance_m':1e-5,
                      'frame':'A-BYSS interior X aft, Y starboard, Z up; Blender XYZ unchanged',
                      'release_status':'NOT_RELEASED','note':'Concept mesh; thickness and sockets are not structural specifications'}}


def accept_measurements(contract, report):
    """Compare external measurements against original targets; never overwrite sources."""
    if contract['units']!='m' or report['units']!='m': raise ValueError('Units must be meters')
    if report['contract_sha256']!=digest(contract): raise ValueError('Stale or different source contract')
    if report['asset_id']!=contract['asset_id']: raise ValueError('Asset ID mismatch')
    measured=report['parts']
    ids=[p['part_id'] for p in measured]
    expected={p['part_id']:p for p in contract['parts']}
    if len(ids)!=len(set(ids)) or set(ids)!=set(expected): raise ValueError('Missing, extra or duplicate parts')
    for item in measured:
        dims=finite_vec(item['dimensions_m'],'measured dimensions',True)
        center=finite_vec(item['center_m'],'measured center')
        rotation=finite_vec(item['rotation_rad'],'measured rotation')
        source=expected[item['part_id']]
        for axis,value in zip('xyz',dims):
            bound=source['dimensions'][axis]
            if abs(value-bound['target'])>bound['tolerance']: raise ValueError('Dimension out of tolerance: '+item['part_id'])
        if any(abs(center[i]-source['center_m'][i])>1e-5 for i in range(3)): raise ValueError('Part position mismatch')
        if any(abs(v)>1e-5 for v in rotation): raise ValueError('Unexpected part rotation')
    envelope=finite_vec(report['envelope_m'],'measured envelope',True)
    if any(abs(envelope[i]-contract['bridge']['envelope_m'][i])>1e-5 for i in range(3)): raise ValueError('Envelope mismatch')
    sockets=report['sockets']; source_sockets={s['id']:s for s in contract['bridge']['sockets']}
    socket_ids=[s['id'] for s in sockets]
    if len(socket_ids)!=len(set(socket_ids)) or set(socket_ids)!=set(source_sockets): raise ValueError('Socket inventory mismatch')
    for socket in sockets:
        pos=finite_vec(socket['position_m'],'socket position'); rot=finite_vec(socket['rotation_rad'],'socket rotation')
        if any(abs(pos[i]-source_sockets[socket['id']]['position_m'][i])>1e-5 for i in range(3)): raise ValueError('Socket position mismatch')
        if any(abs(v)>1e-5 for v in rot): raise ValueError('Socket rotation mismatch')
    result=copy.deepcopy(contract)
    result['stage']='prototype'
    result['validation']['dimensions']='pass'
    # Assembly and physical interfaces are NOT certified by coordinate checks.
    result['bridge']['digital_placement_check']='pass'
    for part in result['parts']:
        part['status']='in_progress'
        item=next(p for p in measured if p['part_id']==part['part_id'])
        for axis,val in zip('xyz',item['dimensions_m']):
            part['dimensions'][axis].update(measured=val,status='pass')
    result['bridge']['measurement_sha256']=digest(report)
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    build=sub.add_parser('contract'); build.add_argument('--geometry',type=Path,default=ROOT/'models/geometry_assumptions.json'); build.add_argument('--output',type=Path,required=True)
    verify=sub.add_parser('verify'); verify.add_argument('contract',type=Path); verify.add_argument('measurements',type=Path); verify.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    try:
        if args.command=='contract': result=make_contract(json.loads(args.geometry.read_text()))
        else: result=accept_measurements(json.loads(args.contract.read_text()),json.loads(args.measurements.read_text()))
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    except (ValueError,KeyError,TypeError,OSError) as exc: parser.exit(2,f'Bridge rejected: {exc}\n')
    print(args.output)

if __name__=='__main__': main()
