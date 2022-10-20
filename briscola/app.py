import gym

from modules import *
from agents.human import Human
from agents.random import RandomAI

NUM_EPISODES = 1

playersNameList = ['Kazuma', 'Aqua', 'Megumin', 'Darkness']
agent_list = [0, 0, 0, 0]


# Human vs Random
"""
agent_list[0] = Human(playersNameList[0], {})
agent_list[1] = RandomAI(playersNameList[1], {'print_info': False})
agent_list[2] = RandomAI(playersNameList[2], {'print_info': False})
agent_list[3] = RandomAI(playersNameList[3], {'print_info': False})
"""

# Random play
agent_list[0] = RandomAI(playersNameList[0], {'print_info': False})
agent_list[1] = RandomAI(playersNameList[1], {'print_info': False})
agent_list[2] = RandomAI(playersNameList[2], {'print_info': False})
agent_list[3] = RandomAI(playersNameList[3], {'print_info': False})


env = gym.make('Briscola-v2', playerNames=playersNameList)
batch_size = 32
output_dir = 'learning/model_output'

for i_episode in range(NUM_EPISODES):
    
    observation = env.reset()
    actions = {}
    states = {}
    
    while True:
        env.render()

        now_event = observation['event_name']
        if now_event == 'PlayTurn':
            playName = observation['data']['playerName']
            states[playName] = observation['data']['state']
        IsBroadcast = observation['broadcast']
        action = None
        
        if IsBroadcast == True:
            for agent in agent_list:
                agent.act(observation)
        else:
            playName = observation['data']['playerName']
            for agent in agent_list:
                if agent.name == playName:
                    action = agent.act(observation)
                    actions[agent.name] = action


        observation, reward, done, info = env.step(action)
        
        if observation['event_name'] == 'ShowTurnEnd':
            for agent in agent_list:
                if agent.type == 'learning':
                    agent.remember(states[agent.name], actions[agent.name], reward[agent.name], observation['data']['state'], done)
        
        if reward != None:
            print('\nreward: {0}\n'.format(reward))

        if done:
            print('\nGame Over!!\n')
            break

    for agent in agent_list:
        if agent.type == 'learning':
            if len(agent.memory) > batch_size:
                agent.train(batch_size)
    
    if i_episode % 50 == 0:
        agent.save(output_dir + 'weights_' + '{:04d}'.format(i_episode) + '.hdf5')