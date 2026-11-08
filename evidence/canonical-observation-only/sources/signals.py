"""Hardware-neutral component packets. No world coordinates enter this module."""
import hashlib
import json
import math
from pathlib import Path


class InstructionMemory:
    def __init__(self, path, instruction):
        self.path = Path(path)
        if not self.path.exists():
            with self.path.open('x', encoding='utf-8') as f:
                json.dump(instruction, f, sort_keys=True)
        if self.read() != instruction:
            raise ValueError('existing instruction differs; refusing overwrite')

    def read(self):
        return json.loads(self.path.read_text(encoding='utf-8'))

    def packet(self):
        raw = self.path.read_bytes()
        return {'front_clearance_target_m': self.read()['front_clearance_target_m'],
                'instruction_sha256': hashlib.sha256(raw).hexdigest(), 'role': 'instruction_readback'}


def geometry_packet(config):
    g = config['geometry']
    offset = g['front_surface_x_m'] - g['lidar_mount_m'][0]
    if offset <= 0 or offset + config['genetic_instruction']['front_clearance_target_m'] < config['lidar']['min_range_m']:
        raise ValueError('mount does not resolve sensor minimum range')
    return {'lidar_to_front_m': offset, 'geometry': g, 'role': 'declared_geometry_readback'}


def forward_return(scan, config):
    """Forward beam only; no object pose, identity, map, or held-last return."""
    lo, hi = config['lidar']['min_range_m'], config['lidar']['max_range_m']
    candidates = [s for s in scan if s['valid'] and s['range_m'] is not None
                  and math.isfinite(s['range_m']) and lo <= s['range_m'] <= hi
                  and abs(s['bearing_rad']) < 1e-8]
    if not candidates:
        return None
    return dict(max(candidates, key=lambda s: s['acquisition_time_s']))


class InformationRouter:
    """Twelve independently identified directed deliveries to software inboxes."""
    def __init__(self, stage1):
        t = stage1['abr_topology']
        self.nodes = t['nodes']
        self.edges = t['edges']
        if [n['id'] for n in self.nodes] != ['N1', 'N2', 'N3', 'N4']:
            raise ValueError('unexpected nodes')
        expected = [(1,2),(2,1),(1,3),(3,1),(1,4),(4,1),(2,3),(3,2),(2,4),(4,2),(3,4),(4,3)]
        if [(e['id'],e['from_node'],e['to_node']) for e in self.edges] != [
                (f'E{i}', f'N{a}', f'N{b}') for i,(a,b) in enumerate(expected,1)]:
            raise ValueError('unexpected topology')

    def route(self, packets):
        inboxes = {n['id']: [] for n in self.nodes}
        deliveries = []
        for e in self.edges:
            delivery = {'edge_id': e['id'], 'source': e['from_node'], 'target': e['to_node'],
                        'payload': packets[e['from_node']],
                        'receiver': f"{e['to_node']}.information_inbox",
                        'meaning': 'component information delivery; not a new sensor observation'}
            inboxes[e['to_node']].append(delivery)
            deliveries.append(delivery)
        return inboxes, deliveries


def node_values(inboxes):
    # Read exactly one actual source packet per component, through routed I/O.
    packets = {d['source']: d['payload'] for msgs in inboxes.values() for d in msgs}
    return [packets['N1']['lidar_to_front_m'], packets['N2']['forward']['range_m'],
            packets['N3']['encoder_mean_arc_m'], packets['N4']['front_clearance_target_m']]


