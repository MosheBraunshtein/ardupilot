import gymnasium as gym
import numpy as np
from cocpit.physical_env import Sitl
from collections import namedtuple, deque
from gymnasium import Wrapper
from rewards import compute_next_ref_point, compute_reward

Pose = namedtuple('Initial_pose',['lat','long','alt','heading'])
Quadcopter_state = namedtuple('Quadcopter_state',['roll','pitch','yaw','roll_speed','pitch_speed','yaw_speed'])

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


    def _get_obs(self):
        pass
        

    def step(self, action) -> (Quadcopter_state,int,bool,Pose):
        '''
        apply the action to the drone and simulate a step using ArduPilot SITL

        '''

        # Example: action = [1500,1500,1500,1500]
        assert not any(1000 > x or x > 2000 for x in action) , 'Env: pwm is too high or low '
        self.sitl_env.set_rc(action)
        
        # Receive telemetry data from the drone
        gps , attitude = self.sitl_env.get_gps_and_attitude()
        self.real_pose = Pose(lat=gps[0],long=gps[1],alt=gps[2],heading=gps[3])
        self.observation = Quadcopter_state(roll=attitude[0],pitch=attitude[1],yaw=attitude[2],roll_speed=attitude[3],pitch_speed=attitude[4],yaw_speed=attitude[5])

        # condition for done
        self.isCrushed = self.real_pose.alt < 2 
        self.beyond_wall = self.real_pose.alt > 101

        # Check if the episode is done
        done = self.isCrushed or self.beyond_wall

        if done:
            self.reward = -self.beyond_wall*10

        return self.observation, self.reward, done, self.real_pose

    def reset(self) -> (Pose, Quadcopter_state):
        '''
        start new episode
        '''

        # Initialize the ArduPilot SITL connection
        self.sitl_env = Sitl()

        gps = self.sitl_env.run()
        self.real_pose = Pose(lat=gps[0],long=gps[1],alt=gps[2],heading=gps[3])

        # get sensor data effected by the action
        _ , attitude = self.sitl_env.get_gps_and_attitude()
        self.observation = Quadcopter_state(roll=attitude[0],pitch=attitude[1],yaw=attitude[2],roll_speed=attitude[3],pitch_speed=attitude[4],yaw_speed=attitude[5])


        initial_pose = self.real_pose
        initial_observation = self.observation
        self.reward = 0

        return initial_pose,initial_observation
    

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
    

    def close(self):
        '''
        close sitl process
        '''
        self.sitl_env.close()



class RewardCopterGym(CopterGym):
    """
    compute reward.
    - needs to generate predicted_path
    - contain real_path 
    - distance(real_path-predicted_path)
    """
    def __init__(self, max_steps=100, additional_param=None) -> None:
        super(RewardCopterGym, self).__init__(max_steps)
        self.real_path = deque(maxlen=max_steps)
        self.ref_path = deque(maxlen=max_steps)

    def step(self, action):
        # Call the base class's step method to perform the default behavior
        observation, reward, done, real_pose = super().step(action)
        
        next_ref_point = Pose()

        last_ref_point = self.ref_path[-1]
        next_ref_point.lat, next_ref_point.long, next_ref_point.alt = compute_next_ref_point(last_ref_point)

        self.ref_path.append((next_ref_point.lat.lat,next_ref_point.long,next_ref_point.alt))
        self.real_path.append((real_pose.lat,real_pose.long,real_pose.alt))

        reward = compute_reward(real_pose,last_ref_point)

        # isCrushed = None
        # isOverCeil = None

        # done = done or isCrushed or isOverCeil


        super().render(action=action,observation=observation,reward=reward)

        return observation, reward, done, real_pose

    def reset(self):
        initial_pose,initial_obs = super().reset()
        self.ref_path.append((initial_pose.lat,initial_pose.long,initial_pose.alt))
        self.real_path.append((initial_pose.lat,initial_pose.long,initial_pose.alt))
        return initial_pose,initial_obs




 
base_env = RewardCopterGym()

pose,state = base_env.reset()
print(state)
itter = 0
while True:
    copter_state,reward,done,pose = base_env.step([1500,1500,1000,1500])
    if done:
        print("episode end")
        break





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