#!/usr/bin/env python3

import torch 
import gymnasium as gym
import numpy as np
import asyncio
from gym import DroneGym

from drl import pi_network as drl



async def test():
    with torch.no_grad():
        while True:
            
            obs = np.array([1,1,1])
            

            obs_torch = torch.unsqueeze(torch.tensor(obs, dtype=torch.float32), 0)

            action = pi_net(obs_torch)

            action_numpy = action[0].detach().numpy()
            
            next_obs, reward, done = await env.step(action_numpy)

            if done:
                break

            obs = next_obs


            
async def main():
   await env.reset()
   await test()


if __name__ == "__main__":

    env = DroneGym(max_angle=45, out_of_bound_penalty=100, bounds=10, max_steps=100)
    obs_dim = env.observation_space.shape[0]
    action_dim = env.action_space.shape[0]
    lower_bound = env.action_space.low
    upper_bound = env.action_space.high
    pi_net = drl.PI_Network(obs_dim=3,action_dim=4,lower_bound=-1,upper_bound=1)

    print("############################################")
    print(" Drone Gym")
    print("Observation Dimension:", obs_dim)
    print("Action Dimension:", action_dim)
    print("Lower Bound for Actions:", lower_bound)
    print("Upper Bound for Actions:", upper_bound)
    print("############################################")

    asyncio.run(main())




