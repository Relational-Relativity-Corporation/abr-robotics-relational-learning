"""Conventional Python physics ONLY. Private world state never sent to controller.

Ray/circle first-return calculation adapted from abr-robotics-demo/abr_v06_loop.py
lidar_range; same 8000 Hz, 5.5 Hz clockwise rotation and 0.15..12 m limits.
New mobile mounting and finite-acceleration differential drive are engineering
substrate code, not ABR. Sensors/feedback are simulated, not hardware evidence.
"""
import math


class PythonRobot:
    def __init__(self, config, object_x_m, object_y_m=0.0):
        self.config = config
        self._x = self._y = self._yaw = self._t = 0.0
        self._object = (object_x_m, object_y_m, 0.1)
        self._angles = [0.0, 0.0]
        self._velocity = [0.0, 0.0]
        self._command = [0.0, 0.0]

    def _advance(self, duration, command):
        m, g = self.config['motor'], self.config['geometry']
        self._command = [max(-m['max_wheel_rad_s'], min(m['max_wheel_rad_s'], v)) for v in command]
        steps = max(1, math.ceil(duration / 0.001))
        dt = duration / steps
        for _ in range(steps):
            for i in range(2):
                change = max(-m['acceleration_rad_s2']*dt, min(m['acceleration_rad_s2']*dt, self._command[i]-self._velocity[i]))
                self._velocity[i] += change
                self._angles[i] += self._velocity[i] * dt
            vl, vr = [w*g['wheel_radius_m'] for w in self._velocity]
            self._yaw += (vr-vl)/g['wheel_base_m'] * dt
            self._x += (vl+vr)/2 * math.cos(self._yaw) * dt
            self._y += (vl+vr)/2 * math.sin(self._yaw) * dt
            self._t += dt

    def motor_packet(self):
        return {'command_rad_s': list(self._command), 'applied_drive_state': 'IDLE' if not any(self._command) else 'DRIVEN',
                'encoder_angle_rad': list(self._angles), 'shaft_velocity_rad_s': list(self._velocity),
                'encoder_mean_arc_m': sum(self._angles)/2*self.config['geometry']['wheel_radius_m'],
                'acquisition_time_s': self._t, 'origin': 'simulated shaft feedback; not XM430 registers'}

    def apply(self, command):
        self._advance(self.config['motor']['pulse_s'], [command['left_rad_s'], command['right_rad_s']])
        driven = self.motor_packet()
        self._advance(self.config['motor']['brake_s'], [0.0, 0.0])
        return {'during_drive': driven, 'after_braking': self.motor_packet()}

    def scan(self):
        if any(abs(v)>1e-10 for v in self._velocity):
            raise RuntimeError('stop-and-sense acquisition requires stopped shafts')
        l, g = self.config['lidar'], self.config['geometry']
        mx, my, _ = g['lidar_mount_m']
        sx = self._x + mx*math.cos(self._yaw)-my*math.sin(self._yaw)
        sy = self._y + mx*math.sin(self._yaw)+my*math.cos(self._yaw)
        ox, oy, radius = self._object
        dx, dy = ox-sx, oy-sy
        scan = []
        n = math.ceil(l['sample_rate_hz']/l['rotation_hz'])
        for k in range(n):
            elapsed = k/l['sample_rate_hz']
            bearing = (-2*math.pi*l['rotation_hz']*elapsed+math.pi)%(2*math.pi)-math.pi
            beam = self._yaw+bearing
            along = dx*math.cos(beam)+dy*math.sin(beam)
            across = -dx*math.sin(beam)+dy*math.cos(beam)
            value = None
            if along>0 and abs(across)<=radius:
                r = along-math.sqrt(max(0.0,radius*radius-across*across))
                if l['min_range_m']<=r<=l['max_range_m']:
                    value = r
            scan.append({'sample_index': k, 'acquisition_time_s': self._t+elapsed,
                         'bearing_rad': bearing, 'range_m': value, 'valid': value is not None,
                         'origin': 'simulated RPLIDAR-like ray return; noiseless'})
        self._advance(n/l['sample_rate_hz'], [0.0,0.0])
        return scan

    def independent_evaluation(self):
        ox, oy, radius = self._object
        return {'robot_world_x_m': self._x, 'robot_world_y_m': self._y,
                'object_center_world_m': [ox,oy], 'object_radius_m': radius,
                'true_front_clearance_m': ox-radius-self._x-self.config['geometry']['front_surface_x_m'],
                'actual_shaft_velocity_rad_s': list(self._velocity), 'time_s': self._t}
