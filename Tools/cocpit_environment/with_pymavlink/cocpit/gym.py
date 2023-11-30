import gymnasium
import numpy as np
from physical_env import Sitl
import random
from flight_path import FlightPath
from utils.prints import print_episode, report_to_file 


class CopterGym(gymnasium.Env):
    def __init__(self,max_steps=100):
        super(CopterGym, self).__init__()
        
        # Define the action space (roll, pitch, yaw, throttle)
        self.action_space = gymnasium.spaces.Box(low=1000, high=2000, shape=(4,),dtype=np.float32)  # Example 4 actions for throttle, roll, pitch, and yaw

        # Define the observation space (roll, pitch, yaw, )
        self.observation_space = gymnasium.spaces.Box(low=-90, high=90, shape=(6,))

        # Other environment-specific parameters
        self.max_steps = max_steps

        self.sitl_env = None
        

    def step(self, action):
        '''
        apply the action to the drone and simulate a step using ArduPilot SITL

        '''
    
        # Example: action = [1500,1500,1500,1500]
        self.sitl_env.set_rc(action)

        # Receive telemetry data from the drone
        (lat,long,alt) , attitude = self.sitl_env.get_gps_and_attitude()

        distance_from_refPath,bad_step = self.flight_path.distance_realLocation_toPath(lat=lat,long=long,alt=alt)

        penalty = self.compute_penalty(min_distance=distance_from_refPath,bad_step=bad_step)

        self.current_step += 1

        # condition for done
        self.isCrushed = alt < 2 
        self.beyond_wall = alt > 101
        self.end_episode = self.current_step >= self.max_steps

        # Check if the episode is done
        done = self.end_episode or self.isCrushed or self.beyond_wall

        if done:
            penalty += self.beyond_wall*10
            # give penalty if real_path.endpoint far from ref_path.endpoint
            penalty += 10*self.flight_path.endpoint_penalty(real_path_endpoint=(lat,long,alt))

        self.progress(f"PENALTY = -{penalty}\n")

        return attitude, penalty, done

    def reset(self):
        '''
        start new episode
        '''
        # insure sitl is not running
        self.sitl_env.close() if self.sitl_env is not None else None

        self.flight_path = None
        self.isCrushed = False
        self.beyond_wall = False
        self.end_episode = False

        # Initialize the ArduPilot SITL connection
        self.sitl_env = Sitl()

        initial_lat, initial_long, initial_alt, initial_heading = self.sitl_env.run()

        # self.angle_of_attack = random.randint(30,40)

        self.angle_of_attack = 40

        self.progress(f"generate refernce trajectory for {self.angle_of_attack} deg")

        self.flight_path = FlightPath(lat=initial_lat, long=initial_long, alt=initial_alt, heading=initial_heading, angle_of_attack=self.angle_of_attack)

        self.current_step = 0

        # get sensor data effected by the action
        gps, attitude = self.sitl_env.get_gps_and_attitude()
 
        return attitude
    

    def compute_penalty(self,min_distance,bad_step):
        '''
        motivation : overall penalty = 70% for min_distance , 30% for bad_step

        my assumption

        min_distance can be large value (0-50) when the copter goes wrong path, in this situation the value of bad_step is not importent 

        but if the copter in goos sense, min_distance value will be small (0-0.4 m) so the value of bad_step will be critic.

        for conclusion : bad_step begin to affect in small distances from ref

        '''
        penalty = min_distance + 10*bad_step

        return penalty


    def save_episode_path(self,episode,total_penalty):
        self.flight_path.save_real_path(episode=episode)
        print_episode(episode_count=episode)
        report_to_file(episode_N=episode,total_penalty=total_penalty,steps=self.current_step)

    def print_current_step(self):
        print(f"step - {self.current_step}")
    def progress(self,data):
        print(f"Gym:{data}")