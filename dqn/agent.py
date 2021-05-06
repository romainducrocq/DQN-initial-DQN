from .utils import ABCMeta, abstract_attribute
from .replay_memory import ReplayMemory
from .network import DeepQNetwork

import os
import time
import math
import random
import numpy as np
from collections import deque

import torch as T
from torch.utils.tensorboard import SummaryWriter


class Agent(metaclass=ABCMeta):
    def __init__(self, n_env, lr, gamma, epsilon_start, epsilon_min, epsilon_decay, input_dim, output_dim, batch_size,
                 min_buffer_size, buffer_size, update_target_frequency, save_frequency, log_frequency, save_dir, log_dir, load, algo, gpu):
        self.n_env = n_env
        self.lr = lr
        self.gamma = gamma
        self.epsilon_start = epsilon_start
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.batch_size = batch_size
        self.min_buffer_size = min_buffer_size
        self.buffer_size = buffer_size
        self.update_target_frequency = update_target_frequency
        self.save_frequency = save_frequency
        self.log_frequency = log_frequency
        self.load = load

        self.resume_step = 0
        self.episode_count = 0
        self.ep_info_buffer = deque([], maxlen=100)

        path = algo + '_lr' + str(lr)
        self.save_path = save_dir + path + '_' + 'model.pack'
        self.summary_writer = SummaryWriter(log_dir + path + '/')

        self.device = T.device(("cuda:"+gpu) if T.cuda.is_available() else "cpu")

        self.start_time = time.time()

    @abstract_attribute
    def replay_memory_buffer(self):
        pass

    @abstract_attribute
    def online_network(self):
        pass

    @abstract_attribute
    def target_network(self):
        pass

    def store_transitions(self, obses, actions, rews, dones, new_obses, infos):
        raise NotImplementedError

    def sample_transitions(self):
        raise NotImplementedError

    def choose_actions(self, step, obses):
        raise NotImplementedError

    def learn(self):
        raise NotImplementedError

    def epsilon(self, step):
        return np.interp(step * self.n_env, [0, self.epsilon_decay], [self.epsilon_start, self.epsilon_min])

    def transitions_to_tensor(self, transitions):
        obses_t = T.as_tensor(np.asarray([t[0] for t in transitions]), dtype=T.float32).to(self.device)
        actions_t = T.as_tensor(np.asarray([t[1] for t in transitions]), dtype=T.int64).to(self.device).unsqueeze(-1)
        rews_t = T.as_tensor(np.asarray([t[2] for t in transitions]), dtype=T.float32).to(self.device).unsqueeze(-1)
        dones_t = T.as_tensor(np.asarray([t[3] for t in transitions]), dtype=T.float32).to(self.device).unsqueeze(-1)
        new_obses_t = T.as_tensor(np.asarray([t[4] for t in transitions]), dtype=T.float32).to(self.device)

        return obses_t, actions_t, rews_t, dones_t, new_obses_t

    def update_target_network(self, step=0):
        if step % self.update_target_frequency == 0:
            self.target_network.load_state_dict(self.online_network.state_dict())

    def load_model(self):
        if self.load and os.path.exists(self.save_path):
            print()
            print("Resume training from " + self.save_path + "...")
            self.resume_step, self.episode_count, rew_mean, len_mean = self.online_network.load(self.save_path)
            [self.ep_info_buffer.append({'r': rew_mean, 'l': len_mean}) for _ in range(np.min([self.episode_count, self.ep_info_buffer.maxlen]))]
            print("Step: ", self.resume_step, ", Episodes: ", self.episode_count, ", Avg Rew: ", rew_mean, ", Avg Ep Len: ", len_mean)

            self.update_target_network()

    def save_model(self, step):
        if step % self.save_frequency == 0 and step > self.resume_step:
            print()
            print("Saving model...")
            self.online_network.save(self.save_path, step, self.episode_count, self.info_mean('r'), self.info_mean('l'))
            print("OK!")

    def log(self, step):
        if step % self.log_frequency == 0 and step > self.resume_step:
            rew_mean, len_mean = self.info_mean('r'), self.info_mean('l')

            print()
            print('Step: ', step)
            print('Avg Rew: ', rew_mean)
            print('Avg Ep Len: ', len_mean)
            print('Episodes: ', self.episode_count)
            print('---', round((time.time() - self.start_time), 2), '---')

            self.summary_writer.add_scalar('AvgRew', rew_mean, global_step=step)
            self.summary_writer.add_scalar('AvgEpLen', len_mean, global_step=step)
            self.summary_writer.add_scalar('Episodes', self.episode_count, global_step=step)

    def info_mean(self, i):
        i_mean = np.mean([e[i] for e in self.ep_info_buffer])
        return i_mean if not math.isnan(i_mean) else 0.


class DQNAgent(Agent):
    def __init__(self, *args, **kwargs):
        super(DQNAgent, self).__init__(*args, **kwargs)

        self.replay_memory_buffer = ReplayMemory(self.buffer_size, self.batch_size)

        self.online_network = DeepQNetwork(self.device, self.lr, self.input_dim, self.output_dim)
        self.target_network = DeepQNetwork(self.device, self.lr, self.input_dim, self.output_dim)

        self.update_target_network()

    def store_transitions(self, obses, actions, rews, dones, new_obses, infos):
        for i in self.replay_memory_buffer.store_transitions(obses, actions, rews, dones, new_obses):
            if infos:
                self.ep_info_buffer.append({'r': infos[i]['r'], 'l': infos[i]['l']})
                self.episode_count += 1

    def sample_transitions(self):
        return self.transitions_to_tensor(self.replay_memory_buffer.sample_transitions())

    def choose_action(self, step, obses):
        obses_t = T.as_tensor(obses, dtype=T.float32).to(self.device)
        q_values = self.online_network(obses_t)

        max_q_indices = T.argmax(q_values, dim=1)
        actions = max_q_indices.detach().tolist()

        for i in range(len(actions)):
            if random.random() <= self.epsilon(step):
                actions[i] = random.randint(0, self.output_dim - 1)

        return actions

    def learn(self):
        # Compute loss
        obses_t, actions_t, rews_t, dones_t, new_obses_t = self.replay_memory_buffer.sample_transitions()

        with T.no_grad():
            target_q_values = self.target_network(new_obses_t)
            max_target_q_values = target_q_values.max(dim=1, keepdim=True)[0]

            targets = rews_t + (1 - dones_t) * self.gamma * max_target_q_values

        online_q_values = self.online_network(obses_t)
        action_q_values = T.gather(input=online_q_values, dim=1, index=actions_t)

        loss = self.online_network.loss(action_q_values, targets).to(self.device)

        # Gradient descent
        self.online_network.optimizer.zero_grad()
        loss.backward()
        self.online_network.optimizer.step()
