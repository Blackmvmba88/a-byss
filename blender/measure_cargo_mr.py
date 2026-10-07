"""Measure evaluated mesh vertices after reopening a saved .blend."""
import argparse
import json
from pathlib import Path
import sys
import bpy


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    scene=bpy.context.scene
    if scene.unit_settings.system!='METRIC' or abs(scene.unit_settings.scale_length-1)>1e-12: raise ValueError('Scene units changed')
    collection=bpy.data.collections['CARGO-MR_PARTS']; deps=bpy.context.evaluated_depsgraph_get()
    parts=[]; all_vertices=[]
    for obj in collection.objects:
        if obj.type!='MESH': raise ValueError('Unexpected non-mesh part')
        evaluated=obj.evaluated_get(deps); mesh=evaluated.to_mesh()
        vertices=[evaluated.matrix_world @ v.co for v in mesh.vertices]
        if not vertices: raise ValueError('Empty part')
        low=[min(v[i] for v in vertices) for i in range(3)]; high=[max(v[i] for v in vertices) for i in range(3)]
        parts.append({'part_id':obj['part_id'],'dimensions_m':[high[i]-low[i] for i in range(3)],'center_m':[(high[i]+low[i])/2 for i in range(3)],'rotation_rad':list(evaluated.matrix_world.to_euler())})
        all_vertices.extend([list(v) for v in vertices]); evaluated.to_mesh_clear()
    if not parts: raise ValueError('Missing geometry')
    sockets=[{'id':o.name,'position_m':list(o.matrix_world.translation),'rotation_rad':list(o.matrix_world.to_euler())} for o in bpy.data.collections['IF-11_REFERENCE_SOCKETS'].objects]
    report={'asset_id':scene['abyss_asset_id'],'contract_sha256':scene['abyss_contract_sha256'],'units':'m',
            'measurement_method':'evaluated world-space mesh vertices from reopened blend','blender_version':bpy.app.version_string,
            'parts':sorted(parts,key=lambda p:p['part_id']),'sockets':sorted(sockets,key=lambda s:s['id']),
            'envelope_m':[max(v[i] for v in all_vertices)-min(v[i] for v in all_vertices) for i in range(3)]}
    args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    print('MEASURED',len(parts),'parts',len(sockets),'sockets')

if __name__=='__main__': main()
