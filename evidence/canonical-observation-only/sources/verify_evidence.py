"""Read-only artifact verification; optional replay of recorded inputs in V9.

Replay runs no simulator, changes no observations, and writes no execution evidence.
"""
import argparse
import hashlib
import io
import json
import zipfile
import tempfile
from pathlib import Path
from run_experiment import KernelBridge, HERE, ROOT
from signals import forward_return


def verify(path,replay=False):
    archive=zipfile.ZipFile(path) if Path(path).is_file() else None
    def read(name):return archive.read(name.replace(chr(92), '/')) if archive else (Path(path)/name).read_bytes()
    def lines(name):return [json.loads(s) for s in io.BytesIO(read(name))]
    manifest=json.loads(read('manifest.json'))
    for name,expected in manifest.items():
        assert hashlib.sha256(read(name)).hexdigest()==expected, f'hash mismatch: {name}'
    cfg=json.loads(read('config.json'));stage=json.loads(read('stage1.json'));summary=json.loads(read('summary.json'))
    assert hashlib.sha256(read('stage1.json')).hexdigest()==cfg['stage1_sha256']
    assert read('stage1.json')==(ROOT/cfg['stage1_file']).read_bytes()
    expected=[(e['id'],e['from_node'],e['to_node']) for e in stage['abr_topology']['edges']]
    # Replay the saved declaration, including historical configurations, not
    # today's active runner configuration. Historical evidence is immutable.
    replay_directory=tempfile.TemporaryDirectory() if replay else None
    if replay:
        replay_config=Path(replay_directory.name)/'config.json'
        replay_config.write_bytes(read('config.json'))
    bridge=KernelBridge(replay_config,ROOT/cfg['stage1_file']) if replay else None
    observation_only=summary.get('execution_mode')=='canonical_observation_only'
    previous_id=None;step=0;last_time=-1.;counts=[]
    def no_world(value):
        if isinstance(value,dict):
            assert not any(k in value for k in ('robot_world_x_m','robot_world_y_m','object_center_world_m','true_front_clearance_m','x_W','x_A','x_P','gt_separation_m'))
            for v in value.values():no_world(v)
        elif isinstance(value,list):
            for v in value:no_world(v)
    try:
        for trial in (1,2):
            records=lines(f'trial-{trial}/observations.jsonl');scans=lines(f'trial-{trial}/raw_lidar.jsonl')
            evaluation=lines(f'trial-{trial}/independent_evaluation.jsonl')
            assert len(records)==len(scans)==len(evaluation)
            for record,scan in zip(records,scans):
                assert record['status']=='EXECUTED'
                packets=record['packets'];no_world(packets)
                beam=forward_return(scan['samples'],cfg)
                assert beam==packets['N2']['forward']
                assert beam['acquisition_time_s']>last_time;last_time=beam['acquisition_time_s']
                assert [(d['edge_id'],d['source'],d['target']) for d in record['deliveries']]==expected
                for d in record['deliveries']:assert d['payload']==packets[d['source']]
                angles=packets['N3']['encoder_angle_rad']
                assert record['values']==[packets['N1']['lidar_to_front_m'],beam['range_m'],sum(angles)/2*cfg['geometry']['wheel_radius_m'],packets['N4']['front_clearance_target_m']]
                assert record['front_clearance_m']==beam['range_m']-packets['N1']['lidar_to_front_m']
                assert record['kernel_request']['values']==record['values']
                step+=1;assert record['kernel_request']['process_step']==step
                kernel=record['kernel'];assert kernel['spatial']['field_id']==cfg['field_id']
                assert kernel['spatial']['edge_ids']==[e[0] for e in expected]
                assert kernel['spatial']['edge_endpoints']==[[e[1],e[2]] for e in expected]
                assert all(len(kernel['spatial'][key][0])==12 for key in ('A','B','R'))
                if previous_id is None:assert kernel['persistence'] is None
                else:assert kernel['persistence']['prior_observation_id']==previous_id
                previous_id=record['kernel_request']['observation_id']
                if replay:assert bridge.execute(record['kernel_request'])==kernel, f'canonical replay mismatch {step}'
            if observation_only:
                for record in records:
                    assert record['command'] is None
                    assert record['actuation']['status']=='NOT_ISSUED'
                    assert record['actuation']['reason']=='NO_ORIGIN_AUTHORIZED_OPERATOR_TO_ACTUATOR_MAPPING'
                    assert record['actuator_state']['command_rad_s']==[0.,0.]
                    assert record['actuator_state']['shaft_velocity_rad_s']==[0.,0.]
                    assert record['actuator_state']['encoder_angle_rad']==[0.,0.]
                    assert 'motor_application' not in record
            else:
                # Historical evidence audit only. Never a live control rule.
                for record in records[-5:]:
                    assert record['command']['reason']=='measured_stop'
                    assert record['motor_application']['after_braking']['shaft_velocity_rad_s']==[0.,0.]
            assert abs(records[-1]['front_clearance_m']-evaluation[-1]['true_front_clearance_m'])<1e-12
            if not observation_only:assert .1<=records[-1]['front_clearance_m']<=.101
            counts.append(len(records))
        assert summary['success'] and step==summary['canonical_executions']
    finally:
        if bridge:bridge.close()
        if replay_directory:replay_directory.cleanup()
        if archive:archive.close()
    result={'manifest_files_verified':len(manifest),'trial_samples':counts,'canonical_states':step,
            'persistence_pairs':step-1,'bit_exact_canonical_replay':replay,'behavioral_checks':'PASS'}
    print(json.dumps(result,indent=2));return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('evidence');p.add_argument('--replay-kernel',action='store_true');a=p.parse_args()
    verify(a.evidence,a.replay_kernel)
