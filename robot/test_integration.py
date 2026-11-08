import json
import unittest
from pathlib import Path
from types import SimpleNamespace as NS
from run_experiment import KernelBridge, RobotController, ROOT, HERE
from signals import geometry_packet
from substrate import PythonRobot
from isaac_adapter import laser_scan_packet, IsaacWheelPort

CFG=json.loads((HERE/'config.json').read_text())
STAGE=json.loads((ROOT/CFG['stage1_file']).read_text())


class Integration(unittest.TestCase):
    def test_two_observations_canonical_loop_and_no_fabricated_missing(self):
        bridge=KernelBridge(HERE/'config.json',ROOT/CFG['stage1_file'])
        try:
            c=RobotController(CFG,STAGE,bridge)
            r=PythonRobot(CFG,.9)
            memory={'front_clearance_target_m':.1,'role':'test instruction'}
            body=geometry_packet(CFG)
            a=c.observe_and_command(body,r.scan(),r.motor_packet(),memory)
            self.assertEqual(a['kernel']['spatial']['edge_ids'],[f'E{i}' for i in range(1,13)])
            self.assertEqual(a['values'],[.12,.8,0.,.1])
            self.assertEqual(len(a['deliveries']),12)
            r.apply(a['command'])
            b=c.observe_and_command(body,r.scan(),r.motor_packet(),memory)
            self.assertGreater(b['values'][2],0.)
            self.assertLess(b['values'][1],a['values'][1])
            self.assertEqual(b['kernel']['persistence']['prior_observation_id'],a['kernel_request']['observation_id'])
            no=c.observe_and_command(body,[],r.motor_packet(),memory)
            self.assertIsNone(no['kernel']);self.assertEqual(c.step,2)
            self.assertEqual(no['command']['left_rad_s'],0.)
        finally:bridge.close()

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
