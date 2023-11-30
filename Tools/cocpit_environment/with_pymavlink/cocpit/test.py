#!/usr/bin/env python3

import torch 
import numpy as np
from time import sleep
import time

import sys
sys.path.append("/ardupilot/Tools/cocpit_environment/with_pymavlink")

from utils.prints import cool_print , reminder_print , report_to_file

from gym import CopterGym

from drl.pi_network import PI_Network

def test(obs):
    total_penalty = 0
    with torch.no_grad():
        while True:

            print(f"\nnet : obs = {obs}")
            
            obs_torch = torch.unsqueeze(torch.tensor(obs, dtype=torch.float32), 0)

            action = pi_net(obs_torch)

            action_numpy = action[0].detach().numpy()

            roll, pitch, throttle, yaw = action_numpy

            action_numpy_pro = [roll,pitch,throttle,0]

            print(f"net : action = {action_numpy_pro}")
            
            next_obs, penalty, done = env.step(action_numpy_pro)

            total_penalty -= penalty

            if done:
                return total_penalty

            obs = next_obs


if __name__ == "__main__":

    try: 

        env = CopterGym(max_steps=300)
        pi_net = PI_Network(obs_dim=3,action_dim=4,action_lower_bound=1000,action_upper_bound=2000)

        cool_print()
        reminder_print()
        
        pretrained_state_dict = torch.load('saved_network/pi_network.pth')
        pi_net.load_state_dict(pretrained_state_dict)

        start = time.time()
        attitude = env.reset()
        total_penalty = test(obs=attitude)
        end = time.time()

        episode_duration = int(end-start)
        # report_to_file(0,env.angle_of_attack,total_penalty,env.current_step,episode_duration)

    except ValueError as e:
         print(e)
         
    except KeyboardInterrupt:
         print("\n shutting down . . .  \n")
         env.close()