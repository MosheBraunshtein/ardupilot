import torch
from pathlib import Path  
import sys
sys.path.append("/ardupilot/Tools/cocpit_environment/with_pymavlink")


import torch 
from torch import nn
import torch.nn.functional as F
import numpy as np
import torch.nn.init as init



class PI_Network(nn.Module):

    def __init__(self,obs_dim,action_dim,action_lower_bound,action_upper_bound) -> None: 
        super().__init__()
        (
            self.lower_bound,
            self.upper_bound
        ) = (
            torch.tensor(action_lower_bound, dtype=torch.float32),
            torch.tensor(action_upper_bound, dtype=torch.float32),
        )
        self.fc1 = nn.Linear(obs_dim,64)
        self.fc2 = nn.Linear(64,64)
        self.fc3 = nn.Linear(64,action_dim)

        self.initialize_weights()

    def forward(self, obs):
        x = F.tanh(self.fc1(obs))
        x = F.tanh(self.fc2(x))
        action = self.fc3(x)
        action = ((action + 1) * (self.upper_bound-self.lower_bound) / 2 +self.lower_bound)
        return action
    

    def initialize_weights(self):
        weghits = np.random.uniform(-0.05, 0.05, size=self.fc1.weight.shape)
        self.fc1.weight.data = torch.tensor(weghits, dtype=torch.float32)

pi_network = PI_Network(3,4,100,200)

directory_path = Path('/ardupilot/Tools/cocpit_environment/with_pymavlink/saved_data/networks/')
# directory_path.mkdir(parents=True,exist_ok=True)
torch.save(pi_network.state_dict(), directory_path / 'pi_network.pth')
# torch.save(v_network.state_dict(), 'saved_network/v_network.pth')