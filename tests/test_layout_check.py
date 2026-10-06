import copy
import json
from pathlib import Path
import unittest
from software.layout_check import analyze

ROOT = Path(__file__).resolve().parents[1]
def read(name):
    return json.loads((ROOT / name).read_text())

class LayoutTests(unittest.TestCase):
    def setUp(self):
        self.catalog = read('models/module_assumptions.json')
        self.geometry = read('models/geometry_assumptions.json')
        self.manifest = read('models/layouts/mr_combi.json')

    def run_case(self):
        return analyze(self.catalog, self.geometry, self.manifest)

    def test_hand_calculated_moment(self):
        result = self.run_case()
        self.assertEqual(result['partial_check_status'], 'PASS_PARTIAL')
        self.assertAlmostEqual(result['payload_cg_m'][0], (930*1.6+950*4.4)/1880)
        self.assertEqual(result['payload_gross_mass_kg'], 1880)
        self.assertIsNone(result['whole_vehicle_cg_m'])
        self.assertEqual(result['release_status'], 'NOT_RELEASED')

    def test_unbalanced_unload_is_detected(self):
        self.manifest = read('models/layouts/wh_unbalanced_unload.json')
        result = self.run_case()
        self.assertIn('PAYLOAD_CG_Y_OUTSIDE_STUDY_WINDOW', result['failures'])
        self.assertAlmostEqual(result['payload_cg_m'][1], 4800/4400)

    def test_aperture_insufficient_even_when_volume_fits(self):
        self.geometry['vehicles']['MR']['lateral_aperture_xz_m'] = [2.0, 2.4]
        self.assertIn('APERTURE_TOO_SMALL', self.run_case()['failures'])

    def test_exact_aperture_clearance_is_accepted(self):
        self.geometry['vehicles']['MR']['lateral_aperture_xz_m'] = [2.5, 2.3]
        self.assertNotIn('APERTURE_TOO_SMALL', self.run_case()['failures'])

    def test_module_collision(self):
        self.geometry['vehicles']['MR']['positions'][1]['center_m'] = [1.6, -0.5, 1.15]
        self.assertTrue(any(x.startswith('MODULE_COLLISION:') for x in self.run_case()['failures']))

    def test_reserved_aisle_and_cabin(self):
        self.geometry['vehicles']['MR']['positions'][0]['center_m'] = [1.6, 1, 1.15]
        failures = self.run_case()['failures']
        self.assertTrue(any(x.startswith('RESERVED_ZONE:') for x in failures))
        self.assertTrue(any(x.startswith('OUTSIDE_CABIN:') for x in failures))

    def test_duplicate_missing_and_unknown_positions(self):
        for mode in ['duplicate', 'missing', 'unknown']:
            with self.subTest(mode=mode):
                m = copy.deepcopy(self.manifest)
                if mode == 'duplicate': m['assignments'][1]['position_id'] = 'MR-01'
                if mode == 'missing': m['assignments'].pop()
                if mode == 'unknown': m['assignments'][1]['position_id'] = 'MR-99'
                with self.assertRaises(ValueError): analyze(self.catalog, self.geometry, m)

    def test_incompatible_revision_and_class(self):
        for mode in ['revision', 'class']:
            m = copy.deepcopy(self.manifest)
            if mode == 'revision': m['interface_revision'] = 'other'
            else: m['assignments'][0]['interface_class'] = 'WH'
            with self.assertRaises(ValueError): analyze(self.catalog, self.geometry, m)

    def test_invalid_offsets_and_fill(self):
        for offset, fill in [([4,0,0],1), ([float('nan'),0,0],1), ([0,0,0],-1), ([0,0,0],1.1)]:
            m = copy.deepcopy(self.manifest)
            m['assignments'][1]['module_gross_cg_offset_m'] = offset
            m['assignments'][1]['cargo_fill_fraction'] = fill
            with self.assertRaises(ValueError): analyze(self.catalog, self.geometry, m)

    def test_required_data_is_not_defaulted(self):
        del self.manifest['assignments'][1]['module_gross_cg_offset_m']
        with self.assertRaises(KeyError): self.run_case()

    def test_remaining_empty_container_still_counts(self):
        self.manifest['assignments'][1]['cargo_fill_fraction'] = 0
        result = self.run_case()
        self.assertEqual(result['payload_gross_mass_kg'], 1180)
        self.assertAlmostEqual(result['payload_cg_m'][0], (930*1.6+250*4.4)/1180)
        self.assertEqual(result['cargo_net_kg'],0)

    def test_all_reference_examples_have_expected_status(self):
        for name, expected in [('wh_combi','PASS_PARTIAL'),('mr_combi','PASS_PARTIAL'),('ts_cargo','PASS_PARTIAL'),('wh_unbalanced_unload','FAIL')]:
            result = analyze(self.catalog,self.geometry,read(f'models/layouts/{name}.json'))
            self.assertEqual(result['partial_check_status'],expected)

if __name__ == '__main__':
    unittest.main()
