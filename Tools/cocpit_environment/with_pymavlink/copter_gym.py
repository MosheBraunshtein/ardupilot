import gymnasium
import numpy as np
from env import Sitl
import random
from reference_flight import trajectory


class CopterGym(gymnasium.Env):
    def __init__(self,out_of_bound_penalty=100,max_steps=100):
        super(CopterGym, self).__init__()
        
        # Define the action space (roll, pitch, yaw, throttle)
        self.action_space = gymnasium.spaces.Box(low=1000, high=2000, shape=(4,),dtype=np.float32)  # Example 4 actions for throttle, roll, pitch, and yaw

        # Define the observation space (roll, pitch, yaw)
        self.observation_space = gymnasium.spaces.Box(low=-90, high=90, shape=(3,))

        # Other environment-specific parameters
        self.max_steps = max_steps
        self.out_of_bounds_penalty = out_of_bound_penalty
        

    def step(self, action):
        '''
        apply the action to the drone and simulate a step using ArduPilot SITL

        '''
        print(f"Gym: step {self.current_step}")

                # Check if the episode is done
        done = self.current_step >= self.max_steps

        if done:
            # save copter trajectory
            self.reference_trajectory.save_real_path()
            self.close()
            return None,None,done
    
        # Send control commands to the drone using the SITL connection
        # Example: action = [1500,1500,1500,1500]
        self.sitl_env.set_rc(action)

        # Receive telemetry data from the drone
        gps , attitude = self.sitl_env.get_gps_and_attitude()

        lat, long, alt = gps

        self.reference_trajectory.real_path_step(lat=lat, long=long, alt=alt)

        # Calculate reward (simplified for demonstration)
        reward = self.reference_trajectory.distance_realLocation_toPath(realGPS=gps)

        self.total_reward += reward

        self.progress(f" REWARD = {reward}")


        self.current_step += 1

        return attitude, reward, done

    def reset(self):
        '''
        start new episode
        '''
        # Initialize the ArduPilot SITL connection
        self.sitl_env = Sitl()

        initial_lat, initial_long, initial_alt, initial_heading = self.sitl_env.run()

        self.reference_trajectory = None

        self.angle_of_attack = random.randint(30,40)
        

        self.progress(f"generate refernce trajectory for {self.angle_of_attack} deg")

        self.reference_trajectory = trajectory(lat=initial_lat, long=initial_long, alt=initial_alt, heading=initial_heading, angle_of_attack=self.angle_of_attack,real_path_Nsteps=self.max_steps)

        self.current_step = 0
        self.total_reward = 0

        # get sensor data effected by the action
        gps, attitude = self.sitl_env.get_gps_and_attitude()

        #some manipulation with gps to get reward
 
        return attitude
    


    def reward(self,min_distance,prev_point):
        reward = 0

        return reward

    def render(self, mode='human'):
        # Implement rendering of the environment (optional)
        pass

    def close(self):
        self.sitl_env.close()

    def progress(self,data):
        print(f"Gym:{data}\n")