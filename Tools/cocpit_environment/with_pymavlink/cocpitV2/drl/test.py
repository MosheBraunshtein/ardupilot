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

path = "/ardupilot/Tools/cocpit_environment/with_pymavlink/cocpitV2/drl/trained_models/ppo_cocpit"

model = PPO.load(path, env=env, print_system_info=True)



vec_env = model.get_env()
obs = vec_env.reset()
for i in range(1000):
    action, _states = model.predict(obs, deterministic=True)
    obs, rewards, dones, info = vec_env.step(action)
    print(action)