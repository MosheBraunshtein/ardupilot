#!/usr/bin/python3

import sys
sys.path.append("/ardupilot/Tools/cocpit_environment/with_pymavlink")

from pathlib import Path

import torch
from torch import nn
import torch.nn.functional as F

from time import time 
import numpy as np
import gymnasium as gym

import matplotlib.pyplot as plt

from drl.policy import PPOPolicy
from drl.ppobuffer import PPOBuffer

from drl.pi_network import PI_Network
from drl.v_network import V_Network

from cocpit.gym import CopterGym
from colorama import init, Fore, Style


from utils.prints import cool_print , reminder_print , report_to_file , print_episode  




NUM_STEPS = 100  # 2048                    # Timesteps data to collect before updating
BATCH_SIZE = 64                     # Batch size of training data
TOTAL_TIMESTEPS = NUM_STEPS * 2  # 500   # Total timesteps to run
GAMMA = 0.99                        # Discount factor
GAE_LAM = 0.95                      # For generalized advantage estimation
NUM_EPOCHS = 10                     # Number of epochs to train
REPORT_STEPS = 3                 # Number of timesteps between reports


if __name__ == "__main__":
    """
    Using reinforcement learning, you can train a network to directly map state to actuator commands.
    """

    env = CopterGym(max_steps=150)
    obs_dim = env.observation_space.shape[0]
    action_dim = env.action_space.shape[0]
    lower_bound = env.action_space.low
    upper_bound = env.action_space.high

    pi_network = PI_Network(obs_dim=obs_dim, action_dim=action_dim, action_lower_bound=lower_bound, action_upper_bound=upper_bound)
    v_network = V_Network(obs_dim=obs_dim)

    learning_rate = 3e-4

    buffer = PPOBuffer(obs_dim, action_dim, NUM_STEPS)

    policy = PPOPolicy(
        pi_network,
        v_network,
        learning_rate,
        clip_range=0.2,
        value_coeff=0.5,
        obs_dim=obs_dim,
        action_dim=action_dim,
        initial_std=1.0,
        max_grad_norm=0.5,
    )

    episode_penalty = 0.0
    episode_count = 0
    episode_start_time = 0
    season_count = 0

    pi_losses, v_losses, total_losses, approx_kls, stds = [], [], [], [], []
    mean_rewards = []

    init() #coloroma

    cool_print()
    reminder_print()

    obs = env.reset()

    for t in range(TOTAL_TIMESTEPS):

        
        print(t, '/', TOTAL_TIMESTEPS)

        action_np, log_prob_np, values_np = policy.get_action(obs)

        roll, pitch, throttle, yaw = action_np

        action_on_env = [roll,pitch,throttle,0]

        env.print_current_step()

        print(f"net : action = {action_on_env}")

        next_obs, penalty, done = env.step(action_on_env)

        episode_penalty -= penalty

        # Add to buffer TODO: consider to store only the values whose change over time and not store yaw=0 for example  
        buffer.record(obs, action_on_env, -penalty, values_np, log_prob_np)
        
        obs = next_obs

        # Calculate advantage and returns if it is the end of episode or
        # its time to update
        if done or (t + 1) % NUM_STEPS == 0:
            if done:
                episode_count += 1
                print_episode(episode_count)

            # Value of last time-step
            last_value = policy.get_values(obs)

            # Compute returns and advantage and store in buffer
            buffer.process_trajectory(
                gamma=GAMMA,
                gae_lam=GAE_LAM,
                is_last_terminal=done,
                last_v=last_value)

            if (t + 1) % NUM_STEPS == 0:
                print("in num_steps")
                season_count += 1
                # Update for epochs
                for ep in range(NUM_EPOCHS):
                    batch_data = buffer.get_mini_batch(BATCH_SIZE)
                    num_grads = len(batch_data)

                    print("num_grads = ",num_grads)

                    # Iterate over minibatch of data
                    for k in range(num_grads):
                        (
                            obs_batch,
                            action_batch,
                            log_prob_batch,
                            advantage_batch,
                            return_batch,
                        ) = (
                            batch_data[k]['obs'],
                            batch_data[k]['action'],
                            batch_data[k]['log_prob'],
                            batch_data[k]['advantage'],
                            batch_data[k]['return'],
                        )

                        # Normalize advantage
                        advantage_batch = (
                            advantage_batch -
                            np.squeeze(np.mean(advantage_batch, axis=0))
                        ) / (np.squeeze(np.std(advantage_batch, axis=0)) + 1e-8)

                        # Convert to torch tensor
                        (
                            obs_batch,
                            action_batch,
                            log_prob_batch,
                            advantage_batch,
                            return_batch,
                        ) = (
                            torch.tensor(obs_batch, dtype=torch.float32),
                            torch.tensor(action_batch, dtype=torch.float32),
                            torch.tensor(log_prob_batch, dtype=torch.float32),
                            torch.tensor(advantage_batch, dtype=torch.float32),
                            torch.tensor(return_batch, dtype=torch.float32),
                        )

                        # Update the networks on minibatch of data
                        (
                            pi_loss,
                            v_loss,
                            total_loss,
                            approx_kl,
                            std,
                        ) = policy.update(obs_batch, action_batch,
                                        log_prob_batch, advantage_batch,
                                        return_batch)

                        pi_losses.append(pi_loss.numpy())
                        v_losses.append(v_loss.numpy())
                        total_losses.append(total_loss.numpy())
                        approx_kls.append(approx_kl.numpy())
                        stds.append(std.numpy())

                buffer.clear()

                episode_penalty= 0.0

                pi_losses, v_losses, total_losses, approx_kls, stds = (
                        [], [], [], [], [])
                
            obs = env.reset()

    # Save policy and value network
    directory_path = Path('/ardupilot/Tools/cocpit_environment/with_pymavlink/saved_data/networks').mkdir(parents=True, exist_ok=True)
    torch.save(pi_network.state_dict(), directory_path / 'pi_network.pth')
    torch.save(v_network.state_dict(), directory_path / 'v_network.pth')

    # Plot episodic reward
    # _, ax = plt.subplots(1, 1, figsize=(5, 4), constrained_layout=True)
    # ax.plot(range(season_count), mean_rewards)
    # ax.set_xlabel("season")
    # ax.set_ylabel("episodic reward")
    # ax.grid(True)
    # plt.show()
