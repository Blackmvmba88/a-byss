import copy
import json
from pathlib import Path
import unittest
from software.payload_budget import calculate

CATALOG = json.loads((Path(__file__).resolve().parents[1] / 'models/module_assumptions.json').read_text())


class PayloadBudgetTests(unittest.TestCase):
    def test_volume_limited_wh(self):
        result = calculate(CATALOG, 'WH', 0, 100)
        self.assertEqual(result['cargo_net_upper_bound_kg'], 6400)
        self.assertEqual(result['installed_payload_gross_kg'], 7600)
        self.assertEqual(result['binding_constraints'], ['volume_at_density'])

    def test_mass_limited_wh_margin_applied_once(self):
        result = calculate(CATALOG, 'WH', 0, 200)
        self.assertEqual(result['cargo_net_upper_bound_kg'], 6800)
        self.assertEqual(result['installed_payload_gross_kg'], 8000)

    def test_mixed_mray(self):
        result = calculate(CATALOG, 'MR', 1, 100)
        self.assertEqual(result['passenger_places_target'], 4)
        self.assertEqual(result['cargo_net_upper_bound_kg'], 700)
        self.assertEqual(result['installed_payload_gross_kg'], 1880)

    def test_aggregate_limit_overrides_local_limits(self):
        catalog = copy.deepcopy(CATALOG)
        catalog['vehicles']['WH']['gross_payload_limit_kg'] = 8000
        result = calculate(catalog, 'WH', 0, 200)
        self.assertEqual(result['cargo_net_upper_bound_kg'], 5200)
        self.assertEqual(result['binding_constraints'], ['total_mass'])

    def test_all_pax_has_no_cargo(self):
        result = calculate(CATALOG, 'TS', 1, 100)
        self.assertEqual(result['cargo_net_upper_bound_kg'], 0)
        self.assertEqual(result['cargo_modules'], 0)

    def test_invalid_inputs(self):
        for vehicle, pax, density in [('WH', -1, 100), ('MR', 3, 100),
                                      ('TS', True, 100), ('TS', 0, 0),
                                      ('TS', 0, -1), ('TS', 0, float('nan')),
                                      ('TS', 0, float('inf')), ('TS', 0, 1e308), ('OTHER', 0, 100)]:
            with self.subTest(vehicle=vehicle, pax=pax, density=density):
                with self.assertRaises(ValueError):
                    calculate(CATALOG, vehicle, pax, density)

    def test_missing_data_and_overweight_are_not_silently_accepted(self):
        catalog = copy.deepcopy(CATALOG)
        del catalog['vehicles']['MR']['pax_module_empty_kg']
        with self.assertRaises(KeyError):
            calculate(catalog, 'MR', 1, 100)
        catalog = copy.deepcopy(CATALOG)
        catalog['vehicles']['TS']['pax_module_empty_kg'] = 2000
        with self.assertRaises(ValueError):
            calculate(catalog, 'TS', 1, 100)
        catalog = copy.deepcopy(CATALOG)
        catalog['vehicles']['WH']['gross_payload_limit_kg'] = 100
        with self.assertRaises(ValueError):
            calculate(catalog, 'WH', 0, 100)

    def test_never_releases_configuration(self):
        for vehicle, positions in [('WH', 8), ('MR', 2), ('TS', 1)]:
            for pax in range(positions + 1):
                result = calculate(CATALOG, vehicle, pax, 100)
                self.assertEqual(result['release_status'], 'NOT_RELEASED')
                self.assertEqual(result['engineering_status'], 'UNVALIDATED')


if __name__ == '__main__':
    unittest.main()
