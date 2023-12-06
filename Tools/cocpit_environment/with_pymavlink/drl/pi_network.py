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
        action = ((action + 1) * (self.upper_bound-self.lower_bound) / 2 + self.lower_bound)
        return action
    

    def initialize_weights(self):
        weghits = np.random.uniform(-0.05, 0.05, size=self.fc1.weight.shape)
        self.fc1.weight.data = torch.tensor(weghits, dtype=torch.float32)





























############################################################

                #checking diferent initial wheights

# pi_net = PI_Network(1,1,1000,2000)

# # weights = pi_net.fc1.weight

# # print(weights)

# obs = torch.tensor([1],dtype=torch.float32)

# with torch.no_grad():
#     out = pi_net(obs)


# print(out)

############################################################

                # see net dict

# pi_network = PI_Network(obs_dim=2, action_dim=4, lower_bound=1, upper_bound=100)


# with torch.no_grad():
#     obs = (100,1)

#     obs_torch = torch.tensor(obs,dtype=torch.float32)

#     # obs_torch = torch.unsqueeze(torch.tensor(obs, dtype=torch.float32), 0)

#     action = pi_network(obs_torch)

#     dict = pi_network.state_dict()

#     keys = [key for key in dict]

#     fc1_bias = pi_network[0].bias

#     print(fc1_bias)