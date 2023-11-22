import gymnasium
import numpy as np
from physical_env import Sitl
import random
from flight_path import FlightPath


class CopterGym(gymnasium.Env):
    def __init__(self,max_steps=100):
        super(CopterGym, self).__init__()
        
        # Define the action space (roll, pitch, yaw, throttle)
        self.action_space = gymnasium.spaces.Box(low=1000, high=2000, shape=(4,),dtype=np.float32)  # Example 4 actions for throttle, roll, pitch, and yaw

        # Define the observation space (roll, pitch, yaw)
        self.observation_space = gymnasium.spaces.Box(low=-90, high=90, shape=(3,))

        # Other environment-specific parameters
        self.max_steps = max_steps
        self.isCrushed = False
        

    def step(self, action):
        '''
        apply the action to the drone and simulate a step using ArduPilot SITL

        '''
        print(f"Gym: step {self.current_step}")

        # # Check if the episode is done
        # done = self.current_step >= self.max_steps or self.isCrushed

        # if done:
        #     self.flight_path.save_real_path()
        #     self.sitl_env.close()
        #     return None,0,done
    
        # Example: action = [1500,1500,1500,1500]
        self.sitl_env.set_rc(action)

        # Receive telemetry data from the drone
        (lat,long,alt) , attitude = self.sitl_env.get_gps_and_attitude()

        distance_form_refPath,bad_step = self.flight_path.distance_realLocation_toPath(lat=lat,long=long,alt=alt)

        penalty = self.compute_penalty(min_distance=distance_form_refPath,bad_step=bad_step)

        self.progress(f"PENALTY = {penalty}")

        self.current_step += 1
        self.isCrushed = alt < 0

        # Check if the episode is done
        done = self.current_step >= self.max_steps or self.isCrushed

        if done:
            self.flight_path.save_real_path()
            self.sitl_env.close()

        return attitude, penalty, done

    def reset(self):
        '''
        start new episode
        '''
        # Initialize the ArduPilot SITL connection
        self.sitl_env = Sitl()

        initial_lat, initial_long, initial_alt, initial_heading = self.sitl_env.run()

        self.flight_path = None

        self.angle_of_attack = random.randint(30,40)
        

        self.progress(f"generate refernce trajectory for {self.angle_of_attack} deg")

        self.flight_path = FlightPath(lat=initial_lat, long=initial_long, alt=initial_alt, heading=initial_heading, angle_of_attack=self.angle_of_attack,real_path_Nsteps=self.max_steps)

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

    def progress(self,data):
        print(f"Gym:{data}\n")