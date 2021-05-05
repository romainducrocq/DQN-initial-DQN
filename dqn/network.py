import os

import torch as T
import torch.nn as nn
import torch.optim as optim

import msgpack
from .utils import msgpack_numpy_patch
msgpack_numpy_patch()


class DeepQNetwork(nn.Module):
    def __init__(self, lr, input_dim, output_dim, hidden_dim=(256, 256, 256)):
        super(DeepQNetwork, self).__init__()

        self.model = nn.Sequential(
            nn.Linear(input_dim, hidden_dim[0]),
            nn.ELU(),
            nn.Linear(hidden_dim[0], hidden_dim[1]),
            nn.ELU(),
            nn.Linear(hidden_dim[1], hidden_dim[2]),
            nn.ELU(),
            nn.Linear(hidden_dim[2], output_dim)
        )

        self.optimizer = optim.Adam(self.parameters(), lr=lr)
        self.loss = nn.SmoothL1Loss()

        self.device = T.device("cuda:0" if T.cuda.is_available() else "cpu")
        self.to(self.device)

        print(self.model)

    def forward(self, x):
        return self.model(x)

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
