import torch.nn as nn
import torch.optim as optim

# """CHANGE HYPER PARAMETERS HERE"""
HYPER_PARAMS = {
    'gpu': '0',                          # GPU #
    'n_env': 4,                          # Multi-processing environments
    'lr': 5e-05,                         # Learning rate
    'gamma': 0.99,                       # Discount factor
    'eps_start': 1.,                     # Epsilon start
    'eps_min': 0.01,                     # Epsilon min
    'eps_dec': 1e7,                      # Epsilon decay
    'eps_dec_exp': True,                 # Epsilon exponential decay
    'bs': 32,                            # Batch size
    'min_mem': 500000,                   # Replay memory buffer min size
    'max_mem': 1000000,                  # Replay memory buffer max size
    'target_update_freq': 50000,         # Target network update frequency
    'save_freq': 10000,                  # Save frequency
    'log_freq': 1000,                    # Log frequency
    'save_dir': './save/',               # Save directory
    'log_dir': './logs/',                # Log directory
    'load': True,                        # Load model
    'repeat': 2,                         # Repeat action
    'max_episode_steps': 5000,           # Time limit episode steps
    'max_total_steps': 0,                # Max total training steps if > 0, else inf training
    'algo': 'PerDuelingDoubleDQNAgent'   # DQNAgent
                                         # DoubleDQNAgent
                                         # DuelingDoubleDQNAgent
                                         # PerDuelingDoubleDQNAgent
}


# """CHANGE NETWORK CONFIG HERE"""
def network_config(input_dim):
    hidden_dims = (256, 256)

    activation = nn.ELU()

    net = nn.Sequential(
        nn.Linear(input_dim, hidden_dims[0]),
        activation,
        nn.Linear(hidden_dims[0], hidden_dims[1]),
        activation
    )

    optim_func = (lambda params, lr: optim.Adam(params, lr=lr))
    loss_func = (lambda reduction: nn.SmoothL1Loss(reduction=reduction))

    fc_out_dim = hidden_dims[-1]

    return net, optim_func, loss_func, fc_out_dim
