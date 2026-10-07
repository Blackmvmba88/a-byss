"""Six independent closed-form screening models. No structural release or FEA."""
import argparse
import json
import math
from pathlib import Path
from time import perf_counter

FIELDS={
 'axial':['force_N','area_m2','allowable_Pa','length_m','E_Pa'],
 'torsion':['torque_Nm','outer_radius_m','polar_J_m4','length_m','G_Pa','allowable_shear_Pa'],
 'separation':['tensile_force_N','bolt_count','minimum_preload_per_bolt_N','stiffness_fraction'],
 'fracture':['tensile_stress_Pa','crack_a_m','geometry_Y','allowable_K_Pa_sqrt_m'],
 'wear':['dimensionless_k','normal_force_N','sliding_distance_m','hardness_Pa','allowable_volume_m3'],
 'fatigue':['blocks']}
POSITIVE={'area_m2','allowable_Pa','length_m','E_Pa','outer_radius_m','polar_J_m4','G_Pa','allowable_shear_Pa','bolt_count','minimum_preload_per_bolt_N','geometry_Y','allowable_K_Pa_sqrt_m','hardness_Pa','allowable_volume_m3'}


def number(value,positive=False):
 if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value) or value<0 or (positive and value==0):
  raise ValueError('Expected finite nonnegative value (strictly positive for denominator)')
 return value


def evaluate(kind,inputs):
 if not isinstance(inputs,dict): raise ValueError('Mode inputs must be an object')
 missing=[f for f in FIELDS[kind] if inputs.get(f) is None]
 if missing: return {'status':'INCOMPLETE','missing':missing,'utilization':None}
 # Model applicability must be explicitly declared per mode. Shape alone cannot prove it.
 if inputs.get('applicable') is not True:
  return {'status':'INCOMPLETE','missing':['applicable=true with justification'],'utilization':None}
 if not isinstance(inputs.get('basis'),str) or not inputs['basis'].strip():
  return {'status':'INCOMPLETE','missing':['basis'],'utilization':None}
 for key in FIELDS[kind]:
  if key!='blocks': number(inputs[key],key in POSITIVE)
 p=inputs
 if kind=='axial':
  stress=p['force_N']/p['area_m2']; result={'stress_Pa':stress,'extension_m':stress*p['length_m']/p['E_Pa']}; ratio=stress/p['allowable_Pa']
 elif kind=='torsion':
  stress=p['torque_Nm']*p['outer_radius_m']/p['polar_J_m4'];result={'shear_Pa':stress,'twist_rad':p['torque_Nm']*p['length_m']/(p['G_Pa']*p['polar_J_m4'])};ratio=stress/p['allowable_shear_Pa']
 elif kind=='separation':
  if type(p['bolt_count']) is not int or not 0<=p['stiffness_fraction']<=1: raise ValueError('Invalid joint parameters')
  preload=p['bolt_count']*p['minimum_preload_per_bolt_N']; relieved=(1-p['stiffness_fraction'])*p['tensile_force_N']
  result={'linear_clamp_reserve_N':preload-relieved};ratio=relieved/preload
 elif kind=='fracture':
  intensity=p['geometry_Y']*p['tensile_stress_Pa']*math.sqrt(math.pi*p['crack_a_m']);result={'K_I_Pa_sqrt_m':intensity};ratio=intensity/p['allowable_K_Pa_sqrt_m']
 elif kind=='wear':
  volume=p['dimensionless_k']*p['normal_force_N']*p['sliding_distance_m']/p['hardness_Pa'];result={'wear_volume_m3':volume};ratio=volume/p['allowable_volume_m3']
 else:
  blocks=p['blocks']
  if not isinstance(blocks,list) or not blocks: raise ValueError('Nonempty fatigue blocks required')
  damage=0
  for block in blocks:
   if not isinstance(block,dict): raise ValueError('Fatigue block must be an object')
   n=number(block['cycles']); life=number(block['cycles_to_failure'],True)
   if not isinstance(block.get('life_basis'),str) or not block['life_basis'].strip(): raise ValueError('Each fatigue block requires life_basis')
   damage+=n/life
  result={'miner_damage':damage};ratio=damage
 if not math.isfinite(ratio) or not all(math.isfinite(v) for v in result.values()): raise ValueError('Numerical overflow')
 return {'status':'AT_OR_ABOVE_LIMIT' if ratio>=1 else 'BELOW_INPUT_LIMIT','utilization':ratio,'values':result,'basis':p['basis']}


def screen(case):
 if not isinstance(case,dict): raise ValueError('Case must be an object')
 if not isinstance(case.get('checks',{}),dict): raise ValueError('Checks must be an object')
 if case['schema_version']!=1: raise ValueError('Unsupported schema')
 checks={}
 for kind in FIELDS:
  try: checks[kind]=evaluate(kind,case.get('checks',{}).get(kind,{}))
  except (ValueError,KeyError,TypeError,ZeroDivisionError,OverflowError) as exc:
   checks[kind]={'status':'INVALID','error':str(exc),'utilization':None}
 return {'case_id':case['case_id'],'evidence_level':case.get('evidence_level','unknown'),'checks':checks,
         'release_status':'NOT_RELEASED','scope':'independent scalar screening; no FEA or coupled failure prediction'}


def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('case',type=Path);parser.add_argument('--output',type=Path)
 args=parser.parse_args()
 try:
  data=json.loads(args.case.read_text());start=perf_counter();result=screen(data)
  elapsed=(perf_counter()-start)*1000
  text=json.dumps(result,indent=2,allow_nan=False)+'\n'
  if args.output: args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(text)
  else: print(text,end='')
  print(f'Screen time: {elapsed:.3f} ms',file=__import__('sys').stderr)
 except (ValueError,KeyError,TypeError,OSError) as exc: parser.exit(2,f'Invalid case: {exc}\n')

if __name__=='__main__': main()
