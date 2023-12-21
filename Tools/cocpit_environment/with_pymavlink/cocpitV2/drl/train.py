import sys
sys.path.append("/ardupilot/Tools/cocpit_environment/with_pymavlink/cocpitV2/env")
import os

from gyms.base_env import CopterGym
from gyms.althold_reward_wrapper import Alt_hold_wrapper
from callbacks.total_timesteps import Total_timesteps
from gymnasium.wrappers import TimeLimit
from stable_baselines3 import PPO




base_env = CopterGym()
timeLimit_env = TimeLimit(base_env, max_episode_steps=300)
env = Alt_hold_wrapper(timeLimit_env)
total_timesteps = 32770

# Instantiate the agent
model = PPO("MultiInputPolicy", env, verbose=2,tensorboard_log="/ardupilot/Tools/cocpit_environment/with_pymavlink/cocpitV2/drl/trained_models/logs/ppo_althold_tensorboard_05s/",n_steps=1024)
# Train the agent and display a progress bar
callback = Total_timesteps(num=total_timesteps)

model.learn(total_timesteps=total_timesteps,callback=callback,reset_num_timesteps=False)

model.save(f"/ardupilot/Tools/cocpit_environment/with_pymavlink/cocpitV2/drl/trained_models/ppo_althold_{total_timesteps}steps_05s")

# model_path = "/ardupilot/Tools/cocpit_environment/with_pymavlink/cocpitV2/drl/trained_models/ppo_althold_1e4steps.zip" 

# if os.path.exists(model_path):

#     model.load("/ardupilot/Tools/cocpit_environment/with_pymavlink/cocpitV2/drl/trained_models/ppo_althold_1e4steps")

#     model.learn(total_timesteps=total_timesteps,callback=callback,reset_num_timesteps=False)

#     model.save(f"/ardupilot/Tools/cocpit_environment/with_pymavlink/cocpitV2/drl/trained_models/ppo_althold_{total_timesteps}steps")

# else: assert False, "path to model is not exist"



print("*"*10,"after train")


