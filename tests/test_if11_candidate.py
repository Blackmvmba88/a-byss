import copy,json,unittest
from pathlib import Path
from software.if11_candidate import assess
ROOT=Path(__file__).resolve().parents[1]
class CandidateTests(unittest.TestCase):
    def setUp(self):
        self.trade=json.loads((ROOT/'models/mechanics/if11_variants.json').read_text())
        self.candidate=json.loads((ROOT/'models/mechanics/if11_candidate.json').read_text())
    def test_preload_improves_separation_without_release(self):
        r=assess(self.trade,self.candidate);a,b=r['variants']
        self.assertEqual(a['separation_limit_cases'],15)
        self.assertEqual(b['separation_limit_cases'],0)
        self.assertAlmostEqual(b['worst_separation_utilization'],10800/14000)
        self.assertEqual(r['release_status'],'NOT_RELEASED')
        self.assertEqual(r['combined_load_status'],'INCOMPLETE')
    def test_upper_envelope_includes_preload_scatter_and_external_load(self):
        b=assess(self.trade,self.candidate)['variants'][1]
        self.assertEqual(b['upper_envelope_bolt_tension_N'],6900)
        self.assertAlmostEqual(b['bolt_tension_to_provisional_proof_ratio'],6900/21200)
    def test_bounds_and_no_input_mutation(self):
        before=copy.deepcopy(self.trade)
        b=assess(self.trade,self.candidate)['reference_preload_bounds_N']
        self.assertAlmostEqual(b['strict_lower_for_no_axial_opening'],10800/2.8)
        self.assertAlmostEqual(b['strict_upper_for_bolt_tension_below_provisional_proof'],20300/1.2)
        self.assertEqual(before,self.trade)
    def test_no_closed_joint_extrapolation(self):
        self.candidate['reference_preload_options_N']=[1]
        v=assess(self.trade,self.candidate)['variants'][0]
        self.assertIsNone(v['upper_envelope_bolt_tension_N'])
    def test_bad_upper_bound(self):
        self.candidate['upper_preload_multiplier']=.9
        with self.assertRaises(ValueError):assess(self.trade,self.candidate)
