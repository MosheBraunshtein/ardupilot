#!/usr/bin/env python3

import torch 
import numpy as np
from env import Sitl
from time import sleep

from copter_gym import CopterGym

from pi_network import PI_Network

def test(obs):
    with torch.no_grad():
        while True:
            
            obs_torch = torch.unsqueeze(torch.tensor(obs, dtype=torch.float32), 0)

            action = pi_net(obs_torch)

            action_numpy = action[0].detach().numpy()

            roll, pitch, throttle, yaw = action_numpy

            action_numpy_pro = [roll,pitch,throttle,0]

            print(f"net : action = {action_numpy_pro}")
            
            next_obs, reward, done = env.step(action_numpy_pro)

            if done:
                break

            obs = next_obs

            print(f"net : obs = {obs}")


def cool_print():
        print("""
╔════════════════════════╗
║   Welcome to Drone Gym ║
╚════════════════════════╝
* by moshe braunshtein ! *
            """)
        sleep(2)

def reminder_print():
        print("""
        set parameters values:
            - angle_max
            - sim_rate 
            - msg mavlink rate
            - vehicle parameters
        """)


if __name__ == "__main__":

    try: 

        env = CopterGym(out_of_bound_penalty=100, max_steps=100)

        pi_net = PI_Network(obs_dim=3,action_dim=4,lower_bound=1000,upper_bound=2000)

        cool_print()
        reminder_print()

        attitude = env.reset()

        test(obs=attitude)

    except ValueError as e:
         print(e)
         
    except KeyboardInterrupt:
         print("\n shutting down . . .  \n")
         env.close()














































# sitl = Sitl()

# sitl.run()

# rc_channel_values = [1500, 1550, 1500, 1500, 0, 0, 0, 0]


# while True:
#     sleep(0.1)
#     sitl.set_rc(rc_channels=rc_channel_values)

