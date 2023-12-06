from gymV2 import CopterGym
from gymV2Extended import EpisodeReward
from gymnasium.wrappers import TimeLimit
from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.callbacks import BaseCallback
import os

# current_file_path = os.path.abspath(__file__)

# # Print the current file path
# print("Current File Path:", current_file_path)
# exit(0)

# Create environment
base_env = CopterGym()
timeLimit_env = TimeLimit(base_env, max_episode_steps=30)
env = EpisodeReward(timeLimit_env)

class StepCallback(BaseCallback):
    def __init__(self, verbose=0):
        super(StepCallback, self).__init__(verbose)
        self.total_steps = 0

    def _on_step(self):
        self.total_steps += 1
        if self.total_steps >= 5:
            self.model.save("/ardupilot/Tools/cocpit_environment/with_pymavlink/cocpitV2/trained_models/ppo_cocpit")
            return False  # Stop training
        return True

# Instantiate the agent
model = PPO("MultiInputPolicy", env, verbose=2)
print("\n*"*15 ,"before train","*"*15)

# Train the agent and display a progress bar
callback = StepCallback()
model.learn(total_timesteps=10,callback=callback)

print("*"*15 ,"after train","*"*15)
del model  # delete trained model to demonstrate loading

# Load the trained agent
# NOTE: if you have loading issue, you can pass `print_system_info=True`
# to compare the system on which the model was trained vs the current one
# model = DQN.load("dqn_lunar", env=env, print_system_info=True)


# Enjoy trained agent
# vec_env = model.get_env()
# obs = vec_env.reset()
# for i in range(1000):
#     action, _states = model.predict(obs, deterministic=True)
#     obs, rewards, dones, info = vec_env.step(action)
    
    # vec_env.render("human")


'''
if __name__ == '__main__':

    obs,info = env.reset()
    itter = 0
    while True:
        copter_state,reward,terminate,truncated,info = env.step([1500,1500,1000,1500])
        print("reward", reward)
        done = terminate or truncated
        print("step ", itter)
        itter += 1
        if done:
            print("episode end")
            break
'''            