import sys
sys.path.append("/ardupilot/Tools/cocpit_environment/with_pymavlink/cocpitV2/env")

from gyms.base_env import CopterGym
from gyms.althold_reward_wrapper import Alt_hold_wrapper
from callbacks.total_timesteps import Total_timesteps
from gymnasium.wrappers import TimeLimit
from stable_baselines3 import PPO




base_env = CopterGym(with_mp=True)
timeLimit_env = TimeLimit(base_env, max_episode_steps=30)
env = Alt_hold_wrapper(timeLimit_env)

num_iter_file = 32770

model_path = f"/ardupilot/Tools/cocpit_environment/with_pymavlink/cocpitV2/drl/trained_models/ppo_althold_{num_iter_file}steps"

model = PPO.load(model_path, env=env, print_system_info=True)



vec_env = model.get_env()
obs = vec_env.reset()
for i in range(1000):
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, dones, info = vec_env.step(action)
    print(action)
    if dones: break
print("done")