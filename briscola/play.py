"""
Play Briscola against trained DQN agents
Human player vs AI
"""
import gymnasium as gym
import os
from modules import *
from agents.human import Human
from agents.random import RandomAI
from agents.dqn_v1 import DQNAgent as DQNv1
from agents.dqn_v2 import ImprovedDQNAgent as DQNv2

# ============================================================
# CONFIGURATION - CHANGE THESE
# ============================================================

# Agent version to play against: 'v1' or 'v2'
OPPONENT_VERSION = 'v2'

# Model paths
MODEL_PATH_V1 = 'learning/model_output_v1/4_players/agent0_weights_final.weights.h5'
MODEL_PATH_V2 = 'learning/model_output_v2/4_players/agent0_weights_final.weights.h5'

# Other opponents: 'random' or 'ai' (if 'ai', uses same version as main opponent)
OTHER_OPPONENTS = 'random'  # Can be 'random' or 'ai'

# ============================================================

playersNameList = ['You (Human)', 'DQN Agent', 'Player 3', 'Player 4']

print(f"\n{'='*60}")
print("BRISCOLA - Human vs AI")
print(f"{'='*60}")
print(f"\nOpponent Version: DQN {OPPONENT_VERSION.upper()}")
print(f"You are playing as: {playersNameList[0]}")
print()

# Create agents based on configuration
agent_list = [Human(playersNameList[0], {})]

# Main opponent
if OPPONENT_VERSION == 'v1':
    main_opponent = DQNv1(playersNameList[1], {'print_info': False})
    model_path = MODEL_PATH_V1
elif OPPONENT_VERSION == 'v2':
    main_opponent = DQNv2(playersNameList[1], {'print_info': False})
    model_path = MODEL_PATH_V2
else:
    raise ValueError(f"Unknown opponent version: {OPPONENT_VERSION}")

agent_list.append(main_opponent)

# Other opponents
if OTHER_OPPONENTS == 'random':
    agent_list.append(RandomAI(playersNameList[2], {'print_info': False}))
    agent_list.append(RandomAI(playersNameList[3], {'print_info': False}))
elif OTHER_OPPONENTS == 'ai':
    if OPPONENT_VERSION == 'v1':
        agent_list.append(DQNv1(playersNameList[2], {'print_info': False}))
        agent_list.append(DQNv1(playersNameList[3], {'print_info': False}))
    else:
        agent_list.append(DQNv2(playersNameList[2], {'print_info': False}))
        agent_list.append(DQNv2(playersNameList[3], {'print_info': False}))
else:
    raise ValueError(f"Unknown opponent type: {OTHER_OPPONENTS}")

print("Your opponents:")
for i, agent in enumerate(agent_list[1:], 1):
    agent_type = agent.__class__.__name__ if hasattr(agent, '__class__') else type(agent).__name__
    print(f"  Player {i+1}: {agent.name} ({agent_type})")
print()

# Load trained weights
if os.path.exists(model_path):
    print(f"Loading trained model from: {model_path}\n")
    if hasattr(main_opponent, 'load'):
        main_opponent.load(model_path)
    else:
        main_opponent.model.load_weights(model_path)
    main_opponent.epsilon = 0.01  # Use trained model
    
    # Load weights for other AI opponents if applicable
    if OTHER_OPPONENTS == 'ai':
        for agent in agent_list[2:]:
            if agent.type == 'learning':
                if hasattr(agent, 'load'):
                    agent.load(model_path)
                else:
                    agent.model.load_weights(model_path)
                agent.epsilon = 0.01
else:
    print(f"Warning: Trained model not found at {model_path}")
    print("DQN Agent will play untrained\n")

env = gym.make('Briscola-v2', playerNames=playersNameList, disable_env_checker=True)

observation, _ = env.reset()
actions = {}
states = {}

print("Game starting!\n")
print("When it's your turn, you'll see your hand and can choose a card by entering 1, 2, or 3")
print("="*60 + "\n")

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
                if action:
                    actions[action['data']['playerName']] = action['data']['action']['card']
    
    observation, reward, done, info = env.step(action)
    
    if reward != None:
        print('\nPoints earned this turn:')
        for player_name, points in reward.items():
            if points > 0:
                print(f'  {player_name}: {points} points')
        print()
    
    if done:
        env.render()
        print('\n' + '='*60)
        print('GAME OVER!')
        print('='*60)
        
        # Get winner from GameOver observation
        if observation is not None and observation.get('event_name') == 'GameOver':
            if 'data' in observation and 'game_winner' in observation['data']:
                winner = observation['data']['game_winner']
                print(f'\nWinner: {winner}')
                
                if winner == playersNameList[0]:
                    print("🎉 Congratulations! You won! 🎉")
                elif winner == playersNameList[1]:
                    print(f"The AI beat you this time. Better luck next round!")
                else:
                    print(f"{winner} won the game!")
        
        print()
        
        # Ask to play again
        play_again = input("Play another game? (y/n): ").lower()
        if play_again == 'y':
            print("\n" + "="*60)
            print("Starting new game...")
            print("="*60 + "\n")
            observation, _ = env.reset()
            actions = {}
            states = {}
        else:
            print("\nThanks for playing! 👋\n")
            break