"""Partial rectangular geometry and PAYLOAD-only CG checks; never releases a vehicle."""
import argparse
import json
import math
from pathlib import Path
try:
    from .payload_budget import calculate, number
except ImportError:
    from payload_budget import calculate, number

ROOT = Path(__file__).resolve().parents[1]


def vector(value, name, positive=False):
    if not isinstance(value, list) or len(value) != 3:
        raise ValueError(f'{name}: expected three coordinates')
    for item in value:
        if isinstance(item, bool) or not isinstance(item, (int, float)) or not math.isfinite(item):
            raise ValueError(f'{name}: non-finite coordinate')
        if positive and item <= 0:
            raise ValueError(f'{name}: dimensions must be positive')
    return value


def overlaps(a, b, gap=0):
    return all(abs(a['center_m'][i] - b['center_m'][i]) <
               (a['size_m'][i] + b['size_m'][i]) / 2 + gap - 1e-9 for i in range(3))


def analyze(catalog, geometry, manifest):
    if geometry['schema_version'] != 1 or manifest['schema_version'] != 1:
        raise ValueError('Unsupported schema')
    vehicle = manifest['vehicle']
    spec = geometry['vehicles'][vehicle]
    if spec['interface_class'] != vehicle or manifest['interface_revision'] != spec['interface_revision']:
        raise ValueError('Incompatible interface class or revision')
    size = vector(spec['module_size_m'], 'module_size_m', True)
    cabin = vector(spec['cabin_size_m'], 'cabin_size_m', True)
    aperture = spec['lateral_aperture_xz_m']
    if not isinstance(aperture, list) or len(aperture) != 2:
        raise ValueError('Aperture requires width along X and height along Z')
    for value in aperture:
        number(value, 'aperture', True)
    gap = number(spec['clearance_m'], 'clearance_m')
    limits = spec['payload_cg_window_m']
    if len(limits) != 3:
        raise ValueError('CG window requires three axes')
    for interval in limits:
        if len(interval) != 2:
            raise ValueError('CG interval requires two bounds')
        vector([*interval, 0], 'CG bounds')
        if interval[0] > interval[1]:
            raise ValueError('Reversed CG interval')
    positions = spec['positions']
    ids = [p['id'] for p in positions]
    if len(ids) != len(set(ids)) or len(ids) != catalog['vehicles'][vehicle]['positions']:
        raise ValueError('Duplicate or inconsistent catalog positions')
    assignments = manifest['assignments']
    assigned = [a['position_id'] for a in assignments]
    if len(assigned) != len(set(assigned)) or set(assigned) != set(ids):
        raise ValueError('Every position must be assigned exactly once')
    for assignment in assignments:
        if assignment['kind'] not in ('PAX4', 'CARGO'):
            raise ValueError('Unsupported module kind')
        if assignment['interface_class'] != vehicle:
            raise ValueError('Module class mismatch')
        fraction = number(assignment['cargo_fill_fraction'], 'cargo_fill_fraction')
        if fraction > 1 or (assignment['kind'] == 'PAX4' and fraction != 0):
            raise ValueError('Invalid cargo fill fraction')
    pax = sum(a['kind'] == 'PAX4' for a in assignments)
    budget = calculate(catalog, vehicle, pax, manifest['cargo_density_kg_m3'])
    module_spec = catalog['vehicles'][vehicle]
    if math.prod(size) < module_spec['cargo_usable_volume_m3']:
        raise ValueError('Usable volume exceeds external box volume')
    failures = []
    if size[0] + 2 * gap > aperture[0] + 1e-9 or size[2] + 2 * gap > aperture[1] + 1e-9:
        failures.append('APERTURE_TOO_SMALL')
    reserved = spec['reserved_boxes']
    for zone in reserved:
        vector(zone['center_m'], 'reserved center')
        vector(zone['size_m'], 'reserved size', True)
    installed = []
    total_mass, total_cargo = 0.0, 0.0
    moments = [0.0, 0.0, 0.0]
    lookup = {a['position_id']: a for a in assignments}
    for position in positions:
        center = vector(position['center_m'], 'position center')
        assignment = lookup[position['id']]
        offset = vector(assignment['module_gross_cg_offset_m'], 'module CG offset')
        if any(abs(offset[i]) > size[i] / 2 for i in range(3)):
            raise ValueError('Module gross CG lies outside its envelope')
        box = {'id': position['id'], 'center_m': center, 'size_m': size}
        low = [0, -cabin[1] / 2, 0]
        high = [cabin[0], cabin[1] / 2, cabin[2]]
        if any(center[i] - size[i] / 2 < low[i] + gap - 1e-9 or
               center[i] + size[i] / 2 > high[i] - gap + 1e-9 for i in range(3)):
            failures.append(f'OUTSIDE_CABIN:{position["id"]}')
        for zone in reserved:
            if overlaps(box, zone):
                failures.append(f'RESERVED_ZONE:{position["id"]}:{zone["id"]}')
        for other in installed:
            if overlaps(box, other, gap):
                failures.append(f'MODULE_COLLISION:{position["id"]}:{other["id"]}')
        if assignment['kind'] == 'PAX4':
            cargo = 0.0
            mass = module_spec['pax_module_empty_kg'] + 4 * catalog['person_and_baggage_kg'] + module_spec['pax_module_incremental_supplies_kg']
        else:
            cargo = budget['cargo_per_module_kg'] * assignment['cargo_fill_fraction']
            mass = module_spec['cargo_module_empty_kg'] + cargo
        cg = [center[i] + offset[i] for i in range(3)]
        for i in range(3):
            moments[i] += mass * cg[i]
        total_mass += mass
        total_cargo += cargo
        installed.append({**box, 'kind': assignment['kind'], 'gross_mass_kg': mass, 'gross_cg_m': cg})
    if total_mass <= 0 or not math.isfinite(total_mass) or not all(math.isfinite(m) for m in moments):
        raise ValueError('Invalid mass or moment sum')
    cg = [moment / total_mass for moment in moments]
    for i, axis in enumerate('XYZ'):
        if not limits[i][0] - 1e-9 <= cg[i] <= limits[i][1] + 1e-9:
            failures.append(f'PAYLOAD_CG_{axis}_OUTSIDE_STUDY_WINDOW')
    return {'case_id': manifest['case_id'], 'vehicle': vehicle,
            'partial_check_status': 'FAIL' if failures else 'PASS_PARTIAL',
            'failures': failures, 'payload_gross_mass_kg': total_mass,
            'cargo_net_kg': total_cargo, 'payload_cg_m': cg,
            'payload_cg_window_m': limits, 'installed_modules': installed,
            'whole_vehicle_cg_m': None, 'access_route_status': 'NOT_EVALUATED',
            'engineering_status': 'UNVALIDATED', 'release_status': 'NOT_RELEASED',
            'omitted_checks': ['continuous_installation_path', 'whole_vehicle_CG_and_inertia',
                               'loads_and_restraints', 'human_layout_and_evacuation',
                               'power_thermal_and_mission']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('--catalog', type=Path, default=ROOT / 'models/module_assumptions.json')
    parser.add_argument('--geometry', type=Path, default=ROOT / 'models/geometry_assumptions.json')
    args = parser.parse_args()
    try:
        result = analyze(json.loads(args.catalog.read_text()), json.loads(args.geometry.read_text()),
                         json.loads(args.manifest.read_text()))
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.exit(2, f'Invalid input: {exc}\n')
    print(json.dumps(result, indent=2, allow_nan=False))
    raise SystemExit(1 if result['failures'] else 0)


if __name__ == '__main__':
    main()
