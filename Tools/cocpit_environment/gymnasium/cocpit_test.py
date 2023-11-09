#!/usr/bin/env python3

import torch 
import gymnasium as gym
import numpy as np
import asyncio
from gym import DroneGym


env = DroneGym(max_angle=45, out_of_bound_penalty=100, bounds=10, max_steps=100)
obs_dim = env.observation_space.shape[0]
action_dim = env.action_space.shape[0]
lower_bound = env.action_space.low
upper_bound = env.action_space.high


print("############################################")
print(" Drone Gym")
print("Observation Dimension:", obs_dim)
print("Action Dimension:", action_dim)
print("Lower Bound for Actions:", lower_bound)
print("Upper Bound for Actions:", upper_bound)
print("############################################")





async def test():
    with torch.no_grad():
        while True:
            
            # obs_torch = torch.unsqueeze(torch.tensor(obs, dtype=torch.float32), 0)

            # action = pi_network(obs_torch)

            # action_numpy = action[0].detach().numpy()
            
            # clipped_action = np.clip(action_numpy, lower_bound, upper_bound)

            # action = roll, pitch, yaw, throttle
            action = (0.0,30.0,0.0,0.0)

            next_obs, reward, done = await env.step(action)

            if done:
                break

            obs = next_obs


            
async def main():

   await env.reset()

   await test()



   # end all

asyncio.run(main())




