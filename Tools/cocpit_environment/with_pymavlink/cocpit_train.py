#!/usr/bin/env python3
from colorama import init, Fore, Style
import torch 
import numpy as np
from env import Sitl
from time import sleep
import time
import sys

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
            
            next_obs, penalty, done = env.step(action_numpy_pro)

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
        set parameters values in "sitl parameters list":
            - angle_max
            - sim_rate 
            - msg mavlink rate
            - vehicle parameters
        """)

def report_to_file(episode_N, angle_of_attack,total_penalty,steps,time):    
    filename = "/ardupilot/Tools/cocpit_environment/with_pymavlink/saved_data/reports/output.txt"
    with open(filename, "a") as file:
        sys.stdout = file  # Redirect standard output to the file
        print(f"""
    ╔════════════════════════╗
    ║   report {episode_N}         ║
    ╚════════════════════════╝
                """)
        print("{:15} {:<20} {:<15} {:<15} {:<15}".format("Episode","Angle of Attack", "Total penalty", "Steps","time"))
        print("="*60)
        print("{:<15} {:<20} {:<15} {:<15} {:<15} ".format(episode_N, angle_of_attack, total_penalty, steps, time))
        sys.stdout = sys.__stdout__  # Reset standard output to the console

        print(f"""{Fore.GREEN}
    ╔════════════════════════╗
    ║   episode {episode_N} reported to file       ║
    ╚════════════════════════╝
                {Style.RESET_ALL}""")


if __name__ == "__main__":

    try: 

        init() #coloroma

        env = CopterGym(out_of_bound_penalty=100, max_steps=100)
        pi_net = PI_Network(obs_dim=3,action_dim=4,lower_bound=1000,upper_bound=2000)

        cool_print()
        reminder_print()

        for i in np.arange(10):
            start_time = time.time()
            attitude = env.reset()
            test(obs=attitude)
            end_time = time.time()
            duration = end_time - start_time
            report_to_file(i,env.angle_of_attack,env.total_penalty,env.current_step,duration)

    except ValueError as e:
         print(e)
         
    except KeyboardInterrupt:
         print("\n shutting down . . .  \n")
         env.close()



