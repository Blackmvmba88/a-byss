import unittest
from software.if11_eccentric import solve
class EccentricTests(unittest.TestCase):
    def test_force_and_moment_equilibrium(self):
        r=solve(.07,12000,.01,.01,80,5000,.2)['positions']
        self.assertAlmostEqual(sum(p['external_normal_share_N'] for p in r),12000)
        self.assertAlmostEqual(sum(p['y_m']*p['external_normal_share_N'] for p in r),120)
        self.assertAlmostEqual(sum(-p['x_m']*p['external_normal_share_N'] for p in r),-120)
        self.assertAlmostEqual(sum(p['x_m']*p['shear_y_N']-p['y_m']*p['shear_x_N'] for p in r),80)
        self.assertAlmostEqual(sum(p['shear_x_N'] for p in r),0)
        self.assertAlmostEqual(sum(p['shear_y_N'] for p in r),0)
    def test_centered_reproduces_previous_result(self):
        r=solve(.07,12000,0,0,0,3500,.1)
        self.assertEqual(r['status'],'BELOW_LOCAL_OPENING_LIMIT')
        for p in r['positions']:self.assertAlmostEqual(p['separation_index'],10800/14000)
    def test_offset_opens_group_and_stops_tension_prediction(self):
        r=solve(.07,12000,.025,0,80,3500,.1)
        self.assertEqual(r['status'],'LOCAL_OPENING_LIMIT')
        self.assertTrue(all(p['bolt_tension_N'] is None for p in r['positions']))
    def test_mirrored_offset_preserves_extrema(self):
        a=solve(.07,12000,.025,0,80,3500,.1)
        b=solve(.07,12000,-.025,0,-80,3500,.1)
        self.assertEqual(sorted(p['separation_index'] for p in a['positions']),sorted(p['separation_index'] for p in b['positions']))
    def test_negative_share_outside_model_and_invalid_inputs(self):
        self.assertEqual(solve(.07,12000,.1,0,0,3500,.1)['status'],'OUTSIDE_MODEL')
        with self.assertRaises(ValueError):solve(0,12000,0,0,0,3500,.1)
        with self.assertRaises(ValueError):solve(.07,12000,float('nan'),0,0,3500,.1)
