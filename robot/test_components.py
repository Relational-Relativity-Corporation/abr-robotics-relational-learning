import copy
import json
import tempfile
import unittest
from pathlib import Path
from signals import InstructionMemory, InformationRouter, geometry_packet, forward_return, drive_projection
from substrate import PythonRobot

HERE = Path(__file__).resolve().parent
CONFIG = json.loads((HERE/'config.json').read_text())
STAGE1 = json.loads((HERE.parent/'field/stage1_robotics_domain.json').read_text())


class Components(unittest.TestCase):
    def test_mount_and_invalid_return(self):
        self.assertAlmostEqual(geometry_packet(CONFIG)['lidar_to_front_m']+.1,.22)
        r=PythonRobot(CONFIG,.22)  # surface range .12, inside blind zone
        self.assertIsNone(forward_return(r.scan(),CONFIG))
        r=PythonRobot(CONFIG,.32)  # .22 sensor range, .10 body clearance
        beam=forward_return(r.scan(),CONFIG)
        self.assertAlmostEqual(beam['range_m']-.12,.1)

    def test_feedback_is_not_command(self):
        r=PythonRobot(CONFIG,.9)
        response=r.apply({'left_rad_s':5.,'right_rad_s':5.})
        driven=response['during_drive']
        self.assertLess(driven['shaft_velocity_rad_s'][0],driven['command_rad_s'][0])
        self.assertGreater(driven['encoder_angle_rad'][0],0.)
        self.assertEqual(response['after_braking']['shaft_velocity_rad_s'],[0.,0.])

    def test_differential_drive_and_sensor_only_packet(self):
        r=PythonRobot(CONFIG,.9)
        r.apply({'left_rad_s':1.,'right_rad_s':3.})
        e=r.independent_evaluation()
        self.assertNotEqual(e['robot_world_y_m'],0.)
        scan=r.scan()
        self.assertTrue(all(set(s)=={'sample_index','acquisition_time_s','bearing_rad','range_m','valid','origin'} for s in scan))

    def test_persistence_readback_refuses_replacement(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'instruction.json'
            mem=InstructionMemory(p,CONFIG['genetic_instruction'])
            self.assertEqual(mem.packet()['front_clearance_target_m'],.1)
            self.assertEqual(InstructionMemory(p,CONFIG['genetic_instruction']).packet(),mem.packet())
            with self.assertRaises(ValueError):InstructionMemory(p,{'front_clearance_target_m':.2})

    def test_twelve_real_deliveries_and_no_reversed_edges(self):
        router=InformationRouter(STAGE1)
        packets={f'N{i}':{'source_marker':i} for i in range(1,5)}
        inboxes,deliveries=router.route(packets)
        self.assertEqual(len(deliveries),12)
        self.assertTrue(all(len(v)==3 for v in inboxes.values()))
        for d in deliveries:self.assertIs(d['payload'],packets[d['source']])
        bad=copy.deepcopy(STAGE1);bad['abr_topology']['edges'][0]['to_node']='N3'
        with self.assertRaises(ValueError):InformationRouter(bad)

    def test_command_requires_canonical_R_and_measured_stop(self):
        kernel={'spatial':{'R':[[1.]*12]}}
        self.assertGreater(drive_projection(kernel,.5,.1,CONFIG)['left_rad_s'],0)
        kernel['spatial']['R']=[[0.]*12]
        self.assertEqual(drive_projection(kernel,.5,.1,CONFIG)['left_rad_s'],0)
        kernel['spatial']['R']=[[1.]*12]
        self.assertEqual(drive_projection(kernel,.1,.1,CONFIG)['reason'],'measured_stop')


if __name__=='__main__':unittest.main(verbosity=2)
