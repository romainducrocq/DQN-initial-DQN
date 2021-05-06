import os

import torch as T
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

import msgpack
from .utils import msgpack_numpy_patch
msgpack_numpy_patch()


class Network(nn.Module):
    def __init__(self, device):
        super(Network, self).__init__()

        self.device = device

    def save(self, save_path, step, episode_count, rew_mean, len_mean):
        params_dict = {
            'parameters': {k: v.detach().cpu().numpy() for k, v in self.state_dict().items()},
            'step': step, 'episode_count': episode_count, 'rew_mean': rew_mean, 'len_mean': len_mean
        }

        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'wb') as f:
            f.write(msgpack.dumps(params_dict))

    def load(self, load_path):
        if not os.path.exists(load_path):
            raise FileNotFoundError(load_path)

        with open(load_path, 'rb') as f:
            params_dict = msgpack.loads(f.read())

        parameters = {k: T.as_tensor(v, device=self.device) for k, v in params_dict['parameters'].items()}
        self.load_state_dict(parameters)

        return params_dict['step'], params_dict['episode_count'], params_dict['rew_mean'], params_dict['lean_mean']


class DeepQNetwork(Network):
    def __init__(self, device, lr, input_dim, output_dim, hidden_dim=(256, 256, 256)):
        super(DeepQNetwork, self).__init__(device)

        self.fc1 = nn.Linear(input_dim, hidden_dim[0])
        self.fc2 = nn.Linear(hidden_dim[0], hidden_dim[1])
        self.fc3 = nn.Linear(hidden_dim[1], hidden_dim[2])
        self.fc4 = nn.Linear(hidden_dim[2], output_dim)

        self.optimizer = optim.Adam(self.parameters(), lr=lr)
        self.loss = nn.SmoothL1Loss()

        self.to(self.device)

    def forward(self, x_state):
        z1 = self.fc1(x_state)
        a1 = F.elu(z1)
        z2 = self.fc2(a1)
        a2 = F.elu(z2)
        z3 = self.fc3(a2)
        a3 = F.elu(z3)
        y_action = self.fc4(a3)

        return y_action
