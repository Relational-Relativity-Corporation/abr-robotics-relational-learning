"""Isaac/ROS component ports; SDK imports are lazy. No pose API is used.

The articulation and scan source are injected. A ROS LaserScan is normalized
without exporting point clouds, world positions, object IDs or localization.
SDK integration is unverified until run under the installed Isaac version.
"""
import math


def laser_scan_packet(message, config):
    base = message.header.stamp.sec + message.header.stamp.nanosec*1e-9
    lo, hi = config['lidar']['min_range_m'], config['lidar']['max_range_m']
    out=[]
    for i,raw in enumerate(message.ranges):
        valid=math.isfinite(raw) and max(lo,message.range_min)<=raw<=min(hi,message.range_max)
        bearing=message.angle_min+i*message.angle_increment
        out.append({'sample_index':i,'acquisition_time_s':base+i*message.time_increment,
                    'bearing_rad':(bearing+math.pi)%(2*math.pi)-math.pi,
                    'range_m':float(raw) if valid else None,'valid':valid,
                    'origin':'Isaac simulated LaserScan' })
    return out


class IsaacWheelPort:
    def __init__(self, wheeled_robot, config, step_seconds, clock_seconds, action_factory=None):
        self.robot,self.config=wheeled_robot,config
        self.step_seconds,self.clock_seconds=step_seconds,clock_seconds
        self.command=[0.,0.]
        if action_factory is None:
            from isaacsim.core.utils.types import ArticulationAction
            import numpy as np
            action_factory=lambda v: ArticulationAction(joint_velocities=np.array(v))
        self.action_factory=action_factory

    def motor_packet(self):
        angles=list(map(float,self.robot.get_wheel_positions()))
        velocities=list(map(float,self.robot.get_wheel_velocities()))
        if len(angles)!=2 or len(velocities)!=2 or not all(map(math.isfinite,angles+velocities)):
            raise ValueError('two finite actual wheel positions and velocities required')
        return {'command_rad_s':list(self.command),'applied_drive_state':'velocity_action_submitted',
                'encoder_angle_rad':angles,'shaft_velocity_rad_s':velocities,
                'encoder_mean_arc_m':sum(angles)/2*self.config['geometry']['wheel_radius_m'],
                'acquisition_time_s':self.clock_seconds(),
                'origin':'Isaac articulation joint feedback; not XM430 register telemetry',
                'electrical_drive_feedback':None}

    def apply(self, command):
        limit=self.config['motor']['max_wheel_rad_s']
        self.command=[max(-limit,min(limit,command[k])) for k in ('left_rad_s','right_rad_s')]
        self.robot.apply_wheel_actions(self.action_factory(self.command))
        self.step_seconds(self.config['motor']['pulse_s'])
        driven=self.motor_packet()
        self.command=[0.,0.]
        self.robot.apply_wheel_actions(self.action_factory(self.command))
        self.step_seconds(self.config['motor']['brake_s'])
        return {'during_drive':driven,'after_braking':self.motor_packet()}


def author_mount_and_bumper(stage, chassis_path, config):
    """Attach explicit physical design to an existing Jetbot chassis, in metres.

    Caller must verify asset units and existing collision bounds do not extend
    ahead of the declared bumper; this function does not assert that inspection.
    The sensor itself is attached by the version-specific RTX/ROS setup.
    """
    from pxr import UsdGeom, UsdPhysics, Gf
    g=config['geometry']
    mount=UsdGeom.Xform.Define(stage,chassis_path+'/lidar_mount')
    mount.AddTranslateOp().Set(Gf.Vec3d(*g['lidar_mount_m']))
    bumper=UsdGeom.Cube.Define(stage,chassis_path+'/front_bumper')
    bumper.CreateSizeAttr(1.)
    bumper.AddTranslateOp().Set(Gf.Vec3d(g['front_surface_x_m']-.005,0.,.04))
    bumper.AddScaleOp().Set(Gf.Vec3f(.01,g['chassis_width_m'],.04))
    UsdPhysics.CollisionAPI.Apply(bumper.GetPrim())
    return str(mount.GetPath())
