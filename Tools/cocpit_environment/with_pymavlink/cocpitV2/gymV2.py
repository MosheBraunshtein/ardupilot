#!/usr/bin/python3

import gymnasium as gym
import numpy as np
from physical_env import Sitl
from collections import namedtuple, deque
from gymnasium import Wrapper
from utils.gps_distansce_calc import compute_next_ref_gps
import sys

# sys.path.append("/ardupilot/Tools/cocpit_environment/with_pymavlink")

Pose = namedtuple('Initial_pose',['lat','long','alt','heading'])
Quadcopter_state = namedtuple('Quadcopter_state',['roll','pitch','yaw','roll_speed','pitch_speed','yaw_speed'])

#TODO: check max_steps truncate implementation
class CopterGym(gym.Env):

    def __init__(self,max_steps=100) -> None:
        super(CopterGym, self).__init__()
        
        self.observation_space = gym.spaces.Dict(
            {
                "roll" : gym.spaces.Box(low = -90,high = 90,shape=(1,),dtype=np.float32),
                "pitch" : gym.spaces.Box(low = -90,high = 90,shape=(1,),dtype=np.float32),
                "yaw" : gym.spaces.Box(low = -90,high = 90,shape=(1,),dtype=np.float32),
                "roll_speed" : gym.spaces.Box(low = -100,high = 100,shape=(1,),dtype=np.float32),
                "pitch_speed" : gym.spaces.Box(low = -100,high = 100,shape=(1,),dtype=np.float32),
                "yaw_speed" : gym.spaces.Box(low = -100,high = 100,shape=(1,),dtype=np.float32),
            }
        )

        self.action_space = gym.spaces.Dict(
            {
                "roll_pwm" : gym.spaces.Box(low=1000,high=2000,shape=(1,),dtype=np.float32),
                "pitch_pwm" : gym.spaces.Box(low=1000,high=2000,shape=(1,),dtype=np.float32),
                "throttle_pwm" : gym.spaces.Box(low=1000,high=2000,shape=(1,),dtype=np.float32),
                "yaw_pwm" : gym.spaces.Box(low=1000,high=2000,shape=(1,),dtype=np.float32),
            }
        )

        self.max_steps = max_steps
        

    def step(self, action):
        '''
        apply the action to the drone and simulate a step using ArduPilot SITL

        '''

        # Example: action = [1500,1500,1500,1500]
        assert not any(1000 > x or x > 2000 for x in action) , 'Env: pwm is too high or low '
        self.sitl_env.set_rc(action)
        
        # Receive telemetry data from the drone
        gps , attitude = self.sitl_env.get_gps_and_attitude()
        real_pose = Pose(lat=gps[0],long=gps[1],alt=gps[2],heading=gps[3])
        observation = Quadcopter_state(roll=attitude[0],pitch=attitude[1],yaw=attitude[2],roll_speed=attitude[3],pitch_speed=attitude[4],yaw_speed=attitude[5])

        # generate new ref_point, update paths 
        ref_gps = compute_next_ref_gps(last_ref_pose=self.ref_path[-1])
        ref_pose = Pose(lat=ref_gps[0],long=ref_gps[1],alt=ref_gps[2],heading=None)
        self.real_path.append(real_pose)
        self.ref_path.append(ref_pose)

        # condition for done
        self.isCrushed = real_pose.alt < 2 
        self.beyond_wall = real_pose.alt > 101

        # Check if the episode is done
        terminated = self.isCrushed or self.beyond_wall

        reward = -10 if terminated else 0

        info = {
            "ref_point" : ref_pose,
            "real_pose" : real_pose
        }

        self.render()

        return observation, reward, terminated, False, info

    def reset(self) -> (Pose, Quadcopter_state):
        '''
        start new episode
        '''

        # Initialize the ArduPilot SITL connection
        self.sitl_env = Sitl()

        self.sitl_env.run()

        # initialize paths for computes reward
        self.real_path = deque(maxlen=self.max_steps)
        self.ref_path = deque(maxlen=self.max_steps)

        # get sensor data effected by the action
        gps , attitude = self.sitl_env.get_gps_and_attitude()
        pose = Pose(lat=gps[0],long=gps[1],alt=gps[2],heading=gps[3])
        initial_observation = Quadcopter_state(roll=attitude[0],pitch=attitude[1],yaw=attitude[2],roll_speed=attitude[3],pitch_speed=attitude[4],yaw_speed=attitude[5])

        self.real_path.append(pose)
        self.ref_path.append(pose)

        info = None
        return initial_observation, info
    

    def render(self,action,observation,reward):
        print(f"""obs : 
                    roll = {observation.roll} 
                    pitch = {observation.pitch}
                    yaw = {observation.yaw}
                    roll_speed = {observation.roll_speed}
                    pitch_speed = {observation.pitch_speed}
                    yaw_speed = {observation.yaw_speed}
            """)
        print(f"""action : 
                    roll = {action[0]} 
                    pitch = {action[1]}
                    yaw = {action[2]}
            """)
        print(f"Total Reward : {reward}")
        print("="*60)
    

    def save_paths(self):
        pass

    def close(self):
        '''
        close sitl process
        '''
        self.save_paths()
        self.sitl_env.close()








base_env = CopterGym()
action = base_env.observation_space.sample()
p = action['pitch']
print(p)
# print(state)
# itter = 0
# while True:
#     copter_state,reward,done,pose = base_env.step([1500,1500,1000,1500])
#     if done:
#         print("episode end")
#         break





# env_stepLimit = Wrapper(env=base_env).step

# pose,state = env_stepLimit.reset()
# print(state)
# itter = 0
# while True:
#     copter_state,reward,done,pose = env_stepLimit.env.step([1500,1500,1000,1500])
#     print(copter_state._asdict())
#     if done:
#         print("episode end")
#         break