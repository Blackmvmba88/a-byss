import unittest
from software.if11_support import strip_response,backing_mass
class SupportTests(unittest.TestCase):
    def test_reference_and_equilibrium(self):
        r=strip_response(12000,.07,.025,.006,68.3e9)
        self.assertAlmostEqual(r['bending_stress_Pa'],700e6)
        self.assertAlmostEqual(4*r['reaction_per_support_N'],12000)
    def test_scaling(self):
        a=strip_response(12000,.07,.025,.006,68.3e9)
        b=strip_response(12000,.07,.025,.012,68.3e9)
        self.assertAlmostEqual(a['bending_stress_Pa']/b['bending_stress_Pa'],4)
        self.assertAlmostEqual(a['midspan_deflection_m']/b['midspan_deflection_m'],8)
    def test_zero_load_and_bad_geometry(self):
        self.assertEqual(strip_response(0,.07,.025,.006,68.3e9)['midspan_deflection_m'],0)
        with self.assertRaises(ValueError):strip_response(12000,0,.025,.006,68.3e9)
        with self.assertRaises(ValueError):backing_mass(dict(strip_length_m=.1,strip_width_m=.025,support_span_m=.099,hole_diameter_m=.009,density_kg_m3=2700),.006)
