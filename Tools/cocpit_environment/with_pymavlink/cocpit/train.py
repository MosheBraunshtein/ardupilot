#!/usr/bin/env python3
from colorama import init, Fore, Style
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
    with torch.no_grad():
        while True:
            
            obs_torch = torch.unsqueeze(torch.tensor(obs, dtype=torch.float32), 0)

            action = pi_net(obs_torch)

            action_numpy = action[0].detach().numpy()

            roll, pitch, throttle, yaw = action_numpy

            action_numpy_pro = [roll,pitch,throttle,0]

            print(f"net : action = {action_numpy_pro}")
            
            next_obs, penalty, done = env.step(action_numpy_pro)

            if done:
                break

            obs = next_obs

            print(f"net : obs = {obs}")


if __name__ == "__main__":

    try: 

        init() #coloroma

        env = CopterGym(max_steps=100)
        pi_net = PI_Network(obs_dim=3,action_dim=4,action_lower_bound=1000,action_upper_bound=2000)

        cool_print()
        reminder_print()

        for i in np.arange(10):
            start = time.time()

            attitude = env.reset()
            test(obs=attitude)

            end = time.time()
            episode_duration = int(end-start)
            report_to_file(i,env.angle_of_attack,env.total_penalty,env.current_step,episode_duration)

    except ValueError as e:
         print(e)
         
    except KeyboardInterrupt:
         print("\n shutting down . . .  \n")
         env.close()



