"""Run only in a fresh background Blender process; uses installed 3defect checkout."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import bpy
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from bridges.mamba3d_bridge import digest


def material(name,color,metal=0):
    mat=bpy.data.materials.new(name); mat.diffuse_color=(*color,1); mat.use_nodes=True
    node=mat.node_tree.nodes['Principled BSDF']; node.inputs['Base Color'].default_value=(*color,1); node.inputs['Metallic'].default_value=metal; node.inputs['Roughness'].default_value=.34
    return mat


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--provider',type=Path,required=True)
    parser.add_argument('--contract',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--style',choices=['saturated','photocopy'],default='saturated')
    args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
    if not bpy.app.background: raise RuntimeError('This builder requires a fresh background process')
    sys.path.insert(0,str(args.provider.resolve()))
    from defect3d import Cube, CompositePart
    from defect3d.asset_contract import assert_valid_asset_contract
    from defect3d.core.serializer import serialize_composite
    from defect3d.pipeline import plan_asset_pipeline
    contract=json.loads(args.contract.read_text()); assert_valid_asset_contract(contract)
    if contract['units']!='m': raise ValueError('Bridge supports meters only')
    out=args.output.resolve(); out.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene=bpy.context.scene; scene.unit_settings.system='METRIC'; scene.unit_settings.scale_length=1.0
    scene['abyss_contract_sha256']=digest(contract); scene['abyss_asset_id']=contract['asset_id']; scene['release_status']='NOT_RELEASED'
    payload=bpy.data.collections.new('CARGO-MR_PARTS'); scene.collection.children.link(payload)
    sockets=bpy.data.collections.new('IF-11_REFERENCE_SOCKETS'); scene.collection.children.link(sockets)
    palette={'BASE':(0.0,.85,1.0),'TOP':(.55,.08,1.0),'PORT':(1.0,.03,.35),'STARBOARD':(1.0,.75,0.0),'FORE':(.1,1.0,.15),'AFT':(1.0,.18,0.0)}
    gray={'BASE':.95,'TOP':.65,'PORT':.30,'STARBOARD':.85,'FORE':.50,'AFT':.12}
    mats={key:material(key, color if args.style=='saturated' else (gray[key],)*3) for key,color in palette.items()}
    assembly=CompositePart(contract['asset_id']); objects=[]
    for part in contract['parts']:
        dims=[part['dimensions'][a]['target'] for a in 'xyz']
        primitive=Cube(size=1,position=tuple(part['center_m']),scale=tuple(dims))
        primitive.name=part['part_id']; assembly.add_part(primitive)
        lower,upper=primitive.get_bounds()
        # 3defect provides actual primitive bounds; Blender builds this provider geometry.
        vertices=[(float(x),float(y),float(z)) for x in [lower[0],upper[0]] for y in [lower[1],upper[1]] for z in [lower[2],upper[2]]]
        faces=[(0,1,3,2),(4,6,7,5),(0,4,5,1),(2,3,7,6),(0,2,6,4),(1,5,7,3)]
        mesh=bpy.data.meshes.new(part['part_id']); mesh.from_pydata(vertices,[],faces); mesh.update()
        obj=bpy.data.objects.new(part['part_id'],mesh); payload.objects.link(obj)
        obj['part_id']=part['part_id']; obj['asset_id']=contract['asset_id']; obj['source']='3defect.Cube'; obj['engineering_status']='UNVALIDATED'
        key=part['part_id'].rsplit('-',1)[-1]
        obj.data.materials.append(mats[key]); obj.color=mats[key].diffuse_color; objects.append(obj)
    for spec in contract['bridge']['sockets']:
        obj=bpy.data.objects.new(spec['id'],None); sockets.objects.link(obj); obj.location=spec['position_m']; obj.empty_display_type='ARROWS'; obj.empty_display_size=.14; obj['reference_only']=True
    lower,upper=assembly.get_bounds()
    provider={'repository':'https://github.com/Blackmvmba88/3defect','commit':subprocess.check_output(['git','-C',str(args.provider),'rev-parse','HEAD'],text=True).strip(),
              'files_sha256':{str(p.relative_to(args.provider)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((args.provider/'defect3d').rglob('*.py'))},
              'contract_sha256':digest(contract),'blender_version':bpy.app.version_string,'provider_bounds_m':[lower.tolist(),upper.tolist()],
              'executed':['asset_contract_validation','Cube','CompositePart','serialization','pipeline_planning'],
              'external_pipeline_steps_executed':False}
    (out/'provider_execution.json').write_text(json.dumps(provider,indent=2)+'\n')
    (out/'provider_geometry.json').write_text(json.dumps(serialize_composite(assembly),indent=2)+'\n')
    (out/'pipeline_plan.json').write_text(json.dumps(plan_asset_pipeline(contract),indent=2)+'\n')
    # Export only asset geometry and reference sockets, without camera or floor.
    bpy.ops.object.select_all(action='DESELECT')
    for obj in [*objects,*sockets.objects]: obj.select_set(True)
    bpy.ops.export_scene.gltf(filepath=str(out/'cargo-mr.glb'),export_format='GLB',use_selection=True,export_extras=True)
    # Preview cutaway: roof and port panel hidden for render only. Geometry remains intact.
    for obj in objects:
        if obj.name.endswith(('TOP','PORT')): obj.hide_render=True
    center=Vector(contract['bridge']['position_m'])
    bpy.ops.mesh.primitive_plane_add(size=200,location=(center.x,center.y,0))
    floor=bpy.context.object; floor.name='PREVIEW_FLOOR'; floor.data.materials.append(material('Floor',(.025,.04,.065)))
    bpy.ops.object.camera_add(location=center+Vector((4,-6,4)))
    camera=bpy.context.object; camera.name='PREVIEW_CAMERA'; camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler(); camera.data.type='ORTHO'; camera.data.ortho_scale=5.2; scene.camera=camera
    # Fast technical preview: no ray tracing, lights, denoising or simulation.
    floor.hide_render=True
    scene.render.engine='BLENDER_WORKBENCH'
    shading=scene.display.shading
    shading.light='FLAT'; shading.color_type='OBJECT'
    shading.background_type='WORLD'; shading.show_shadows=False
    shading.show_cavity=True; shading.cavity_type='BOTH'
    shading.curvature_ridge_factor=2.5; shading.curvature_valley_factor=2.5
    shading.show_object_outline=True; shading.object_outline_color=(0,0,0)
    scene.view_settings.view_transform='Standard'
    scene.view_settings.look='None'
    scene.view_settings.exposure=0; scene.view_settings.gamma=1
    # Camera-aligned annotation, excluded from delivery geometry by export order.
    for name,body,location,font_size in [
        ('TITLE','CARGO-MR / VISTA RAPIDA',(-2.4,1.7,-5),.14),
        ('LEGEND','BASE: CIAN   LATERAL: AMARILLO   FRENTE: VERDE   FONDO: NARANJA' if args.style=='saturated' else 'BASE: BLANCO   LATERAL: GRIS CLARO   FRENTE: GRIS   FONDO: NEGRO',(-2.4,-1.7,-5),.065),
        ('NOTE','CORTE VISUAL / 6 PIEZAS / GEOMETRIA CONCEPTUAL',(-2.4,-1.82,-5),.075)]:
        curve=bpy.data.curves.new(name,'FONT'); curve.body=body; curve.size=font_size
        label=bpy.data.objects.new('PREVIEW_'+name,curve); scene.collection.objects.link(label)
        label.parent=camera; label.location=location; label.color=(0,0,0,1)
    scene['preview_style']=args.style
    scene.render.resolution_x=1200; scene.render.resolution_y=900; scene.render.resolution_percentage=100
    scene.world=bpy.data.worlds.new('Preview world'); scene.world.color=(1,1,1); scene.render.filepath=str(out/'cargo-mr-preview.png')
    scene['preview_note']='Cutaway render hides TOP and PORT; six-panel model and GLB remain complete.'
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'cargo-mr.blend'))
    bpy.ops.render.render(write_still=True)

if __name__=='__main__': main()
