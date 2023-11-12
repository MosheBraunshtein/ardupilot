import numpy as np


def compute_return_advantage(
            rewards, values, is_last_terminal, gamma, gae_lambda, last_value):
    """
    computes returns and adventage based on generalized advantage estimation.
    """

    N = rewards.shape[0]
    advantages = np.zeros((N,1), dtype=np.float32)

    tmp = 0.0
    for k in reversed(range(N)):
        if k == N-1:
            next_non_terminal = 1 - is_last_terminal
            next_values = last_value
        else:
            next_non_terminal = 1
            next_values = values[k+1]

        delta = (rewards[k] + 
                 gamma*next_non_terminal*next_values-values[k])


