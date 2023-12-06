from stable_baselines3 import PPO
from env.gyms.gymV2Extended import EpisodeReward
from env.gyms.gymV2


base_env = CopterGym()
timeLimit_env = TimeLimit(base_env, max_episode_steps=30)
env = EpisodeReward(timeLimit_env)

model = PPO.load("/ardupilot/Tools/cocpit_environment/with_pymavlink/cocpitV2/trained_models/ppo_cocpit", env=env)

exit(0)

# Evaluate the agent
# NOTE: If you use wrappers with your environment that modify rewards,
#       this will be reflected here. To evaluate with original rewards,
#       wrap environment in a "Monitor" wrapper before other wrappers.
mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=10)