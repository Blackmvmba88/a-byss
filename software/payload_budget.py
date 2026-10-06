"""Illustrative interior mass/volume budget. Never authorizes a configuration."""
import argparse
import json
import math
from pathlib import Path

DEFAULT_CATALOG = Path(__file__).resolve().parents[1] / 'models/module_assumptions.json'


def number(value, name, positive=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f'{name}: expected a finite number')
    if not math.isfinite(value) or value < 0 or (positive and value == 0):
        raise ValueError(f'{name}: invalid range')
    return value


def calculate(catalog, vehicle, pax_modules, density_kg_m3):
    if catalog['schema_version'] != 1:
        raise ValueError('Unsupported catalog schema')
    if vehicle not in catalog['vehicles']:
        raise ValueError('Unknown vehicle')
    spec = catalog['vehicles'][vehicle]
    positions = spec['positions']
    if type(positions) is not int or positions < 1:
        raise ValueError('positions must be a positive integer')
    if type(pax_modules) is not int or not 0 <= pax_modules <= positions:
        raise ValueError('pax_modules outside available positions')
    number(density_kg_m3, 'density_kg_m3', positive=True)
    person = number(catalog['person_and_baggage_kg'], 'person_and_baggage_kg', True)
    for key in ('gross_limit_per_position_kg', 'gross_payload_limit_kg',
                'cargo_usable_volume_m3'):
        number(spec[key], key, True)
    for key in ('pax_module_empty_kg', 'pax_module_incremental_supplies_kg',
                'cargo_module_empty_kg'):
        number(spec[key], key)
    margin = number(spec['mass_margin_fraction'], 'mass_margin_fraction')
    if margin >= 1:
        raise ValueError('mass_margin_fraction must be less than 1')
    local_limit = spec['gross_limit_per_position_kg'] * (1 - margin)
    total_limit = spec['gross_payload_limit_kg'] * (1 - margin)
    cargo_modules = positions - pax_modules
    pax_gross = spec['pax_module_empty_kg'] + 4 * person + spec['pax_module_incremental_supplies_kg']
    if pax_modules and pax_gross > local_limit:
        raise ValueError('PAX module exceeds local mass allocation')
    if cargo_modules and spec['cargo_module_empty_kg'] > local_limit:
        raise ValueError('Empty CARGO module exceeds local mass allocation')
    fixed_mass = pax_modules * pax_gross + cargo_modules * spec['cargo_module_empty_kg']
    if fixed_mass > total_limit:
        raise ValueError('Installed modules and occupants exceed total allocation')
    constraints = {
        'local_mass': cargo_modules * (local_limit - spec['cargo_module_empty_kg']),
        'total_mass': total_limit - fixed_mass,
        'volume_at_density': cargo_modules * spec['cargo_usable_volume_m3'] * density_kg_m3,
    }
    for key, value in constraints.items():
        number(value, key)
    # Only equal-class CARGO positions, distributed evenly; no CG calculation.
    cargo = min(constraints.values()) if cargo_modules else 0.0
    active = [key for key, val in constraints.items() if math.isclose(val, cargo)] if cargo_modules else []
    return {
        'vehicle': spec['name'], 'pax_modules': pax_modules,
        'cargo_modules': cargo_modules, 'passenger_places_target': pax_modules * 4,
        'cargo_density_kg_m3': density_kg_m3,
        'cargo_net_upper_bound_kg': cargo,
        'cargo_per_module_kg': cargo / cargo_modules if cargo_modules else 0.0,
        'installed_payload_gross_kg': fixed_mass + cargo,
        'mass_allocation_after_margin_kg': total_limit,
        'unused_mass_allocation_kg': total_limit - fixed_mass - cargo,
        'cargo_volume_used_m3': cargo / density_kg_m3,
        'cargo_bounds_kg': constraints, 'binding_constraints': active,
        'calculation_scope': 'illustrative interior mass and bulk volume only',
        'engineering_status': 'UNVALIDATED', 'release_status': 'NOT_RELEASED',
        'omitted_checks': ['whole_vehicle_mass', 'CG_and_inertia', 'loads_and_restraints',
                           'door_and_packing_geometry', 'power_and_thermal',
                           'mission_and_propellant', 'crew_and_common_services',
                           'human_survival_and_evacuation'],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalog', type=Path, default=DEFAULT_CATALOG)
    parser.add_argument('--vehicle', required=True, choices=['WH', 'MR', 'TS'])
    parser.add_argument('--pax-modules', required=True, type=int)
    parser.add_argument('--cargo-density', type=float, default=100,
                        help='Illustrative packed bulk density, kg/m3 (default 100)')
    args = parser.parse_args()
    try:
        catalog = json.loads(args.catalog.read_text())
        result = calculate(catalog, args.vehicle, args.pax_modules, args.cargo_density)
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.exit(2, f'Invalid input: {exc}\n')
    print(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False))


if __name__ == '__main__':
    main()
