import sys
sys.path.append("/ardupilot/Tools/cocpit_environment/with_pymavlink/cocpitV2/env")
import os
import argparse


from gyms.base_env import CopterGym
from gyms.althold_reward_wrapper import Alt_hold_wrapper
from callbacks.total_timesteps import Total_timesteps
from gymnasium.wrappers import TimeLimit
from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy

base_env = CopterGym()
timeLimit_env = TimeLimit(base_env, max_episode_steps=30)
env = Alt_hold_wrapper(timeLimit_env)

parser = argparse.ArgumentParser()
parser.add_argument("-num",help="N_iterations")
args = parser.parse_args()

num_iter_file = args.num

model_path = f"/ardupilot/Tools/cocpit_environment/with_pymavlink/cocpitV2/drl/trained_models/ppo_althold_{num_iter_file}steps"

model = PPO.load(model_path, env=env, print_system_info=True)


if __name__ == '__main__':

    # Evaluate the trained agent
    mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=10, deterministic=True)

    print(f"mean_reward={mean_reward:.2f} +/- {std_reward}")


