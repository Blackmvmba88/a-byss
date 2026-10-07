import copy,json,math
from pathlib import Path
import unittest
from software.mechanical_screen import screen
ROOT=Path(__file__).resolve().parents[1]

class MechanicalTests(unittest.TestCase):
 def setUp(self): self.case=json.loads((ROOT/'models/mechanics/demo.json').read_text())
 def test_axial_and_torsion_reference_values(self):
  c=screen(self.case)['checks'];self.assertEqual(c['axial']['values']['stress_Pa'],1e7)
  self.assertAlmostEqual(c['torsion']['values']['shear_Pa'],100*.02/(math.pi*.02**4/2))
 def test_preload_and_failure_boundary(self):
  c=screen(self.case)['checks'];self.assertEqual(c['separation']['values']['linear_clamp_reserve_N'],-1600)
  self.assertEqual(c['separation']['status'],'AT_OR_ABOVE_LIMIT')
 def test_fracture_wear_fatigue(self):
  c=screen(self.case)['checks'];self.assertAlmostEqual(c['fracture']['values']['K_I_Pa_sqrt_m'],1.12*1e8*math.sqrt(math.pi*.01))
  self.assertAlmostEqual(c['wear']['values']['wear_volume_m3'],1e-7)
  self.assertAlmostEqual(c['fatigue']['values']['miner_damage'],1.2)
 def test_missing_material_does_not_pass(self):
  self.case['checks']['axial']['E_Pa']=None
  self.assertEqual(screen(self.case)['checks']['axial']['status'],'INCOMPLETE')
 def test_nan_and_invalid_joint_are_rejected(self):
  self.case['checks']['torsion']['G_Pa']=float('nan');self.case['checks']['separation']['stiffness_fraction']=1.1
  c=screen(self.case)['checks'];self.assertEqual(c['torsion']['status'],'INVALID');self.assertEqual(c['separation']['status'],'INVALID')
 def test_geometry_cannot_grant_applicability(self):
  self.case['checks']['torsion']['applicable']=False
  self.assertEqual(screen(self.case)['checks']['torsion']['status'],'INCOMPLETE')
 def test_cargo_mr_is_incomplete(self):
  r=screen(json.loads((ROOT/'models/mechanics/cargo_mr_pending.json').read_text()))
  self.assertTrue(all(c['status']=='INCOMPLETE' for c in r['checks'].values()))
  self.assertEqual(r['release_status'],'NOT_RELEASED')
 def test_malformed_inputs(self):
  self.case['checks']['axial']=[]
  self.case['checks']['fatigue']['blocks']=[None]
  c=screen(self.case)['checks']
  self.assertEqual(c['axial']['status'],'INVALID')
  self.assertEqual(c['fatigue']['status'],'INVALID')
  with self.assertRaises(ValueError): screen([])
  self.case['checks']=[]
  with self.assertRaises(ValueError): screen(self.case)
 def test_zero_life_and_empty_spectrum_rejected(self):
  for blocks in ([],[{'cycles':1,'cycles_to_failure':0,'life_basis':'test'}]):
   self.case['checks']['fatigue']['blocks']=blocks
   self.assertEqual(screen(self.case)['checks']['fatigue']['status'],'INVALID')

if __name__=='__main__':unittest.main()
