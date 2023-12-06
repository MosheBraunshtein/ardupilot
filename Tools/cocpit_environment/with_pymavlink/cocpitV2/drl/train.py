import sys
sys.path.append("/ardupilot/Tools/cocpit_environment/with_pymavlink/cocpitV2/env")

from gyms.base_env import CopterGym
from gyms.reward_wrapper import Reward_wrapper
from callbacks.total_timesteps import Total_timesteps
from gymnasium.wrappers import TimeLimit
from stable_baselines3 import PPO




base_env = CopterGym()
timeLimit_env = TimeLimit(base_env, max_episode_steps=30)
env = Reward_wrapper(timeLimit_env)

# Instantiate the agent
model = PPO("MultiInputPolicy", env, verbose=2)
# Train the agent and display a progress bar
callback = Total_timesteps()


model.learn(total_timesteps=10,callback=callback)

model.save("/ardupilot/Tools/cocpit_environment/with_pymavlink/cocpitV2/drl/trained_models/ppo_cocpit")

print("*"*10,"after train")