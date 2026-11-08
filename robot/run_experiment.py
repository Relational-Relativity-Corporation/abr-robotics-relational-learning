"""Two stop-and-sense trials of ONE field; object relocation is experimenter-only."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from signals import (InstructionMemory, InformationRouter, geometry_packet,
                     forward_return, node_values, drive_projection)
from substrate import PythonRobot

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent


def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write_json(path,value):
    with Path(path).open('x',encoding='utf-8') as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n')


class KernelBridge:
    def __init__(self,config_path,stage1_path):
        exe=HERE/'kernel_bridge/target/debug/relational-robot-kernel-bridge.exe'
        if not exe.exists():exe=exe.with_suffix('')
        if not exe.exists():raise RuntimeError('build robot/kernel_bridge first')
        self.process=subprocess.Popen([str(exe),str(config_path),str(stage1_path)],
            stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True,encoding='utf-8')

    def execute(self,request):
        self.process.stdin.write(json.dumps(request,allow_nan=False)+'\n');self.process.stdin.flush()
        line=self.process.stdout.readline()
        if not line:raise RuntimeError('Kernel bridge exited without a response')
        response=json.loads(line)
        if response['status']!='EXECUTED':raise RuntimeError(json.dumps(response))
        return response

    def close(self):
        self.process.stdin.close();self.process.stdout.close()
        if self.process.wait(timeout=10)!=0:raise RuntimeError('Kernel bridge failed')


class RobotController:
    """Receives component packets only; has no simulator/world reference."""
    def __init__(self,config,stage1,kernel):
        self.config,self.router,self.kernel=config,InformationRouter(stage1),kernel
        self.step=0

    def observe_and_command(self,body,scan,motor,memory):
        beam=forward_return(scan,self.config)
        if beam is None:
            return {'status':'NO_VALID_FORWARD_RETURN','command':{'left_rad_s':0.,'right_rad_s':0.,'reason':'invalid_sensor_stop'},
                    'kernel':None,'values':None}
        packets={'N1':body,'N2':{'forward':beam,'scan_sample_count':len(scan)},'N3':motor,'N4':memory}
        inboxes,deliveries=self.router.route(packets)
        values=node_values(inboxes)
        self.step+=1
        request={'values':values,'process_step':self.step,'observation_id':f"{self.config['field_id']}/observation-{self.step}"}
        result=self.kernel.execute(request)
        clearance=beam['range_m']-body['lidar_to_front_m']
        command=drive_projection(result,clearance,memory['front_clearance_target_m'],self.config)
        return {'status':'EXECUTED','packets':packets,'deliveries':deliveries,'values':values,
                'kernel_request':request,'kernel':result,'front_clearance_m':clearance,'command':command}


def run(output):
    config_path=HERE/'config.json';config=json.loads(config_path.read_text())
    stage1_path=ROOT/config['stage1_file']
    if digest(stage1_path)!=config['stage1_sha256']:raise RuntimeError('Stage 1 changed')
    stage1=json.loads(stage1_path.read_text());InformationRouter(stage1)
    output=Path(output);output.mkdir(parents=True,exist_ok=False)
    write_json(output/'config.json',config)
    (output/'stage1.json').write_bytes(stage1_path.read_bytes())
    memory=InstructionMemory(output/'genetic_instruction.json',config['genetic_instruction'])
    body=geometry_packet(config)
    robot=PythonRobot(config,.9)
    bridge=KernelBridge(config_path,stage1_path)
    controller=RobotController(config,stage1,bridge)
    summaries=[]
    try:
        for trial,object_x in enumerate((.9,1.3),1):
            # This operation belongs to the experimenter, outside the controller.
            if trial==2:robot._object=(object_x,0.,.1)
            directory=output/f'trial-{trial}';directory.mkdir()
            stable=0;records=[];previous=None
            with (directory/'observations.jsonl').open('x',encoding='utf-8') as log, \
                 (directory/'raw_lidar.jsonl').open('x',encoding='utf-8') as raw, \
                 (directory/'independent_evaluation.jsonl').open('x',encoding='utf-8') as evaluation:
                for frame in range(500):
                    scan=robot.scan()
                    motor=robot.motor_packet()
                    if previous is not None:motor['previous_application']=previous
                    record=controller.observe_and_command(body,scan,motor,memory.packet())
                    record['trial_frame']=frame
                    # A missing return is fail-closed, never replaced by zero/last range.
                    previous=robot.apply(record['command']);record['motor_application']=previous
                    raw.write(json.dumps({'trial_frame':frame,'samples':scan},allow_nan=False)+'\n')
                    evaluation.write(json.dumps({'trial_frame':frame,**robot.independent_evaluation()},allow_nan=False)+'\n')
                    log.write(json.dumps(record,allow_nan=False)+'\n');records.append(record)
                    stable=stable+1 if record['command']['reason']=='measured_stop' else 0
                    if stable==5:break
            end=robot.independent_evaluation()
            measured=[r['front_clearance_m'] for r in records if 'front_clearance_m' in r]
            tolerance=config['control_projection']['clearance_tolerance_m'];target=memory.packet()['front_clearance_target_m']
            success=stable==5 and target-1e-10<=measured[-1]<=target+tolerance and all(abs(v)<1e-10 for v in end['actual_shaft_velocity_rad_s'])
            summaries.append({'trial':trial,'observation_count':len(records),'kernel_executions':sum(r['kernel'] is not None for r in records),
                'initial_measured_clearance_m':measured[0] if measured else None,
                'final_measured_clearance_m':measured[-1] if measured else None,
                'independently_evaluated_final_clearance_m':end['true_front_clearance_m'],
                'final_shaft_velocity_rad_s':end['actual_shaft_velocity_rad_s'],'five_stopped_observations':stable==5,
                'minimum_valid_forward_range_m':min(r['packets']['N2']['forward']['range_m'] for r in records if r['kernel']),
                'successful_execution':all(r['status']=='EXECUTED' for r in records),'observed_behavioral_success':success,
                'first_process_step':records[0].get('kernel_request',{}).get('process_step'),
                'last_process_step':records[-1].get('kernel_request',{}).get('process_step')})
            write_json(directory/'summary.json',summaries[-1])
    finally:bridge.close()
    kernel_root=ROOT.parent/'abr-kernel'
    kernel_commit=subprocess.check_output(['git','-C',str(kernel_root),'rev-parse','HEAD'],text=True).strip()
    kernel_status=subprocess.check_output(['git','-C',str(kernel_root),'status','--porcelain'],text=True)
    # Snapshot executable sources/configuration for reproducibility without overwrites.
    sources=output/'sources';sources.mkdir()
    for source in HERE.glob('*.py'):(sources/source.name).write_bytes(source.read_bytes())
    for name in ('Cargo.toml','Cargo.lock','src/main.rs'):
        source=HERE/'kernel_bridge'/name;dest=sources/'kernel_bridge'/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(source.read_bytes())
    exe=HERE/'kernel_bridge/target/debug/relational-robot-kernel-bridge.exe'
    if not exe.exists():exe=exe.with_suffix('')
    summary={'origin':'Python simulated component I/O; no physical or Isaac execution claimed','field_id':config['field_id'],
        'stage1_sha256':digest(stage1_path),'kernel_commit':kernel_commit,'kernel_worktree_status':kernel_status,
        'kernel_executable_sha256':digest(exe),'trials':summaries,
        'canonical_executions':controller.step,'persistence':'same bridge and actual prior retained across object relocation',
        'success':all(s['observed_behavioral_success'] for s in summaries)}
    write_json(output/'summary.json',summary)
    manifest={str(p.relative_to(output)):digest(p) for p in sorted(output.rglob('*')) if p.is_file()}
    write_json(output/'manifest.json',manifest)
    print(json.dumps(summary,indent=2))
    return summary


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True)
    args=parser.parse_args();result=run(args.output)
    raise SystemExit(0 if result['success'] else 1)
