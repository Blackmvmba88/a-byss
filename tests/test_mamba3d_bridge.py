import copy
import json
from pathlib import Path
import unittest
from bridges.mamba3d_bridge import make_contract, accept_measurements, digest

ROOT=Path(__file__).resolve().parents[1]

class BridgeTests(unittest.TestCase):
    def setUp(self):
        self.geometry=json.loads((ROOT/'models/geometry_assumptions.json').read_text())
        self.contract=make_contract(self.geometry)
        # Synthetic fixtures test rejection rules; actual Blender evidence is separate.
        self.report={'asset_id':self.contract['asset_id'],'contract_sha256':digest(self.contract),'units':'m',
          'parts':[{'part_id':p['part_id'],'dimensions_m':[p['dimensions'][a]['target'] for a in 'xyz'],
                    'center_m':p['center_m'][:],'rotation_rad':[0,0,0]} for p in self.contract['parts']],
          'envelope_m':self.contract['bridge']['envelope_m'][:],
          'sockets':[{'id':s['id'],'position_m':s['position_m'][:],'rotation_rad':[0,0,0]} for s in self.contract['bridge']['sockets']]}

    def test_canonical_contract_and_six_panels(self):
        self.assertEqual(self.contract['units'],'m')
        self.assertEqual(len(self.contract['parts']),6)
        self.assertEqual(len(self.contract['bridge']['sockets']),4)
        self.assertEqual(self.contract['bridge']['envelope_m'],[2.4,2,2.2])
        self.assertEqual(self.contract['bridge']['position_m'],[4.4,-.5,1.15])

    def test_source_is_preserved_and_no_manufacturing_claim(self):
        before=copy.deepcopy(self.contract)
        result=accept_measurements(self.contract,self.report)
        self.assertEqual(self.contract,before)
        self.assertEqual(result['stage'],'prototype')
        self.assertEqual(result['validation']['dimensions'],'pass')
        self.assertEqual(result['validation']['interfaces'],'unknown')
        self.assertFalse(result['manufacturing']['ready'])
        self.assertEqual(result['bridge']['release_status'],'NOT_RELEASED')

    def test_out_of_tolerance_geometry(self):
        self.report['parts'][0]['dimensions_m'][0]+=.01
        with self.assertRaises(ValueError): accept_measurements(self.contract,self.report)

    def test_wrong_units_stale_source_and_asset_id(self):
        for key,value in [('units','mm'),('contract_sha256','bad'),('asset_id','other')]:
            r=copy.deepcopy(self.report);r[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError): accept_measurements(self.contract,r)

    def test_missing_extra_and_duplicate_parts(self):
        for mode in ('missing','extra','duplicate'):
            r=copy.deepcopy(self.report)
            if mode=='missing': r['parts'].pop()
            if mode=='duplicate': r['parts'].append(copy.deepcopy(r['parts'][0]))
            if mode=='extra':
                p=copy.deepcopy(r['parts'][0]);p['part_id']='OTHER';r['parts'].append(p)
            with self.subTest(mode=mode),self.assertRaises(ValueError): accept_measurements(self.contract,r)

    def test_nonfinite_position_and_wrong_rotation(self):
        for field,value in [('center_m',float('nan')),('rotation_rad',.1),('dimensions_m',float('inf'))]:
            r=copy.deepcopy(self.report);r['parts'][0][field][0]=value
            with self.subTest(field=field),self.assertRaises(ValueError): accept_measurements(self.contract,r)

    def test_socket_position_rotation_inventory(self):
        for mode in ('position','rotation','missing','duplicate'):
            r=copy.deepcopy(self.report)
            if mode=='position': r['sockets'][0]['position_m'][0]+=.02
            if mode=='rotation': r['sockets'][0]['rotation_rad'][2]=.1
            if mode=='missing': r['sockets'].pop()
            if mode=='duplicate': r['sockets'].append(copy.deepcopy(r['sockets'][0]))
            with self.subTest(mode=mode),self.assertRaises(ValueError): accept_measurements(self.contract,r)

    def test_envelope_mismatch(self):
        self.report['envelope_m'][0]+=.01
        with self.assertRaises(ValueError): accept_measurements(self.contract,self.report)

    def test_invalid_source_or_thickness(self):
        for t in (-.1,0,2,float('nan'),True):
            with self.subTest(t=t),self.assertRaises(ValueError): make_contract(self.geometry,t)
        self.geometry['vehicles']['MR']['module_size_m'][0]=0
        with self.assertRaises(ValueError): make_contract(self.geometry)

    def test_changed_source_changes_digest(self):
        self.geometry['vehicles']['MR']['module_size_m'][0]=2.5
        self.assertNotEqual(digest(make_contract(self.geometry)),digest(self.contract))

if __name__=='__main__': unittest.main()
