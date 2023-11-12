import gymnasium
import numpy as np
from sitl_env import SitlConnection


class DroneGym(gymnasium.Env):
    def __init__(self,max_angle=45,out_of_bound_penalty=100,bounds=10,max_steps=100):
        super(DroneGym, self).__init__()

        # Define the action space (roll, pitch, yaw, throttle)
        self.action_space = gymnasium.spaces.Box(low=-np.inf, high=np.inf, shape=(4,),dtype=np.float32)  # Example 4 actions for throttle, roll, pitch, and yaw

        # Define the state space (e.g., drone accelerations)
        #TODO: correct space observation based on the elevent sensor data
        self.observation_space = gymnasium.spaces.Box(low=-np.inf, high=np.inf, shape=(3,))  # Example: imu_x, imu_y, imu_z

        # Initialize the ArduPilot SITL connection
        self.sitl_env = SitlConnection()

        # Other environment-specific parameters
        self.max_steps = max_steps
        self.drone_state = np.zeros(4)  # Initial state
        self.max_angle = max_angle
        self.out_of_bounds_penalty = out_of_bound_penalty
        self.bounds = bounds

    async def step(self, action):
        '''
        apply the action to the drone and simulate a step using ArduPilot SITL

        '''
        print(f"step {self.current_step}")
        

        # Send control commands to the drone using the SITL connection
        roll, pitch, yaw, throttle = action
        await self.sitl_env.send_attitude_command(
            roll,
            pitch,
            yaw,
            throttle
        )

        # Receive telemetry data from the drone
        sensor_data = await self.sitl_env.get_sensor_data()

        # self.drone_state = np.array([new_x, new_y, new_vx, new_vy])

        # Calculate reward (simplified for demonstration)
        reward = -np.sqrt(1 ** 2 + 1 ** 2)  # Penalize distance from the origin

        # Check if the episode is done
        done = self.current_step >= self.max_steps

        self.current_step += 1

        return sensor_data, reward, done

    async def reset(self):
        '''
        start new episode
        '''

        # terminate simulator
        self.sitl_env.terminate_simulator()

        # start new session
        await self.sitl_env.run()

        # Reset the environment to the initial state
        self.current_step = 0

        # get sensor data effected by the action
        sensor_data = await self.sitl_env.get_sensor_data()
 
        return sensor_data
    

    def render(self, mode='human'):
        # Implement rendering of the environment (optional)
        pass
