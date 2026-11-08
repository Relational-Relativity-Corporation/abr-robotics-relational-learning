import json
import unittest
from pathlib import Path
from types import SimpleNamespace as NS
from run_experiment import KernelBridge, RobotObserver, ROOT, HERE
from signals import geometry_packet
from substrate import PythonRobot
from isaac_adapter import laser_scan_packet, IsaacWheelPort

CFG=json.loads((HERE/'config.json').read_text())
STAGE=json.loads((ROOT/CFG['stage1_file']).read_text())


class Integration(unittest.TestCase):
    def test_two_observations_canonical_loop_and_no_fabricated_missing(self):
        bridge=KernelBridge(HERE/'config.json',ROOT/CFG['stage1_file'])
        try:
            c=RobotObserver(CFG,STAGE,bridge)
            r=PythonRobot(CFG,.9)
            memory={'front_clearance_target_m':.1,'role':'test instruction'}
            body=geometry_packet(CFG)
            a=c.observe(body,r.scan(),r.motor_packet(),memory)
            self.assertEqual(a['kernel']['spatial']['edge_ids'],[f'E{i}' for i in range(1,13)])
            self.assertEqual(a['values'],[.12,.8,0.,.1])
            self.assertEqual(len(a['deliveries']),12)
            self.assertIsNone(a['command'])
            b=c.observe(body,r.scan(),r.motor_packet(),memory)
            self.assertEqual(b['values'],a['values'])
            self.assertEqual(r.motor_packet()['shaft_velocity_rad_s'],[0.,0.])
            self.assertEqual(b['actuation']['status'],'NOT_ISSUED')
            self.assertEqual(b['kernel']['persistence']['prior_observation_id'],a['kernel_request']['observation_id'])
            no=c.observe(body,[],r.motor_packet(),memory)
            self.assertIsNone(no['kernel']);self.assertEqual(c.step,2)
            self.assertIsNone(no['command'])
        finally:bridge.close()

    def test_operator_outputs_never_generate_motion_or_target_decisions(self):
        class Kernel:
            def execute(self,request):
                return {'status':'EXECUTED','spatial':{'R':[[1e20]*12]}}
        observer=RobotObserver(CFG,STAGE,Kernel())
        # Different observations, references and operator magnitudes cannot
        # activate an absent mapping. The front clearance is reported only.
        for placement,target in ((.9,.1),(.32,.1),(.32,.5)):
            robot=PythonRobot(CFG,placement)
            result=observer.observe(geometry_packet(CFG),robot.scan(),robot.motor_packet(),
                                    {'front_clearance_target_m':target})
            self.assertIsNone(result['command'])
            self.assertEqual(result['actuation']['reason'],'NO_ORIGIN_AUTHORIZED_OPERATOR_TO_ACTUATOR_MAPPING')

    def test_experiment_never_calls_actuator_apply(self):
        import contextlib,io,tempfile
        from unittest.mock import patch
        from run_experiment import run
        with tempfile.TemporaryDirectory() as directory, \
             patch.object(PythonRobot,'apply',side_effect=AssertionError('motion API called')), \
             contextlib.redirect_stdout(io.StringIO()):
            summary=run(Path(directory)/'new-evidence',samples_per_placement=2)
        self.assertTrue(summary['success'])
        self.assertEqual(summary['canonical_executions'],4)
        self.assertEqual(summary['actuator_motion_commands_issued'],0)

    def test_isaac_scan_rejects_blind_zone_and_nonfinite_without_pose(self):
        msg=NS(header=NS(stamp=NS(sec=1,nanosec=500)),ranges=[.1,.22,float('inf')],
               range_min=.15,range_max=12.,angle_min=0.,angle_increment=.1,time_increment=.001)
        scan=laser_scan_packet(msg,CFG)
        self.assertEqual([s['valid'] for s in scan],[False,True,False])
        self.assertIsNone(scan[0]['range_m']);self.assertAlmostEqual(scan[1]['range_m'],.22)

    def test_isaac_feedback_not_replaced_by_command(self):
        class Wheels:
            def get_wheel_positions(self):return [.1,.2]
            def get_wheel_velocities(self):return [.3,.4]
            def apply_wheel_actions(self,action):self.action=action
        wheels=Wheels();port=IsaacWheelPort(wheels,CFG,lambda seconds:None,lambda:1.,lambda v:list(v))
        result=port.apply({'left_rad_s':2.,'right_rad_s':3.})
        self.assertEqual(result['during_drive']['command_rad_s'],[2.,3.])
        self.assertEqual(result['during_drive']['shaft_velocity_rad_s'],[.3,.4])
        self.assertIsNone(result['during_drive']['electrical_drive_feedback'])
        self.assertAlmostEqual(result['during_drive']['encoder_mean_arc_m'],.0045)
        self.assertEqual(wheels.action,[0.,0.])


if __name__=='__main__':unittest.main(verbosity=2)
