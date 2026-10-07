import json
import math
from pathlib import Path
import unittest
from software.if11_trade import compare

class TradeTests(unittest.TestCase):
    def setUp(self):
        self.data=json.loads((Path(__file__).resolve().parents[1]/'models/mechanics/if11_variants.json').read_text())

    def test_mass_subtracts_four_holes(self):
        v=compare(self.data)['variants'][0]
        expected=(.08**2-4*math.pi*(.007/2)**2)*.004*2700+4*.012
        self.assertAlmostEqual(v['partial_mass_kg'],expected)
        self.assertEqual(len(v['cases']),54)

    def test_torque_equilibrium(self):
        c=compare(self.data)['variants'][0]['cases'][-1]
        self.assertAlmostEqual(4*(.05/math.sqrt(2))*c['torque_only_shear_per_bolt_N'],80)
        self.assertEqual(c['shear_capacity_status'],'INCOMPLETE')

    def test_thickness_does_not_invent_strength(self):
        a,b,c=compare(self.data)['variants']
        self.assertLess(b['partial_mass_kg'],c['partial_mass_kg'])
        self.assertEqual(b['cases'],c['cases'])
        self.assertGreater(a['worst_separation_utilization'],b['worst_separation_utilization'])
        self.assertAlmostEqual(a['worst_separation_utilization'],12000*.9/(4*1500*.7))

    def test_invalid_geometry_and_ranges(self):
        self.data['variants'][0]['pitch_m']=.079
        with self.assertRaises(ValueError): compare(self.data)
        self.setUp(); self.data['retained_preload_fraction']=[0]
        with self.assertRaises(ValueError): compare(self.data)
        self.setUp(); self.data['torque_Nm']=[float('nan')]
        with self.assertRaises(ValueError): compare(self.data)

if __name__=='__main__': unittest.main()
