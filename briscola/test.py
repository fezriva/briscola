"""
Unified Testing Script for Briscola DQN Agents
Supports testing different agent versions and head-to-head comparisons
"""
import gymnasium as gym
import os
from modules import *
from agents.random import RandomAI
from agents.dqn_v1 import DQNAgent as DQNv1
from agents.dqn_v2 import ImprovedDQNAgent as DQNv2

# ============================================================
# CONFIGURATION - CHANGE THESE
# ============================================================

# Test mode: 'v1', 'v2', 'v1_vs_v2', 'v1_vs_random', 'v2_vs_random', 'debug'
TEST_MODE = 'v2'

# Debug mode - run single game with detailed output
DEBUG_MODE = False  # Set to True to see detailed agent behavior

# Model paths (adjust based on your training)
MODEL_PATH_V1 = 'learning/model_output_v1/4_players/agent0_weights_final.weights.h5'
MODEL_PATH_V2 = 'learning/model_output_v2/4_players/agent0_weights_final.weights.h5'

# Number of test games
NUM_GAMES = 100  # Will be set to 1 if DEBUG_MODE is True

# ============================================================

playersNameList = ['Player 1', 'Player 2', 'Player 3', 'Player 4']

# Override settings if debug mode
if DEBUG_MODE:
    NUM_GAMES = 1
    print("\n" + "="*60)
    print("DEBUG MODE ENABLED - Running 1 game with detailed output")
    print("="*60 + "\n")

# Setup based on test mode
if TEST_MODE == 'v1':
    agent_list = [
        DQNv1(playersNameList[0], {'print_info': DEBUG_MODE}),
        RandomAI(playersNameList[1], {'print_info': False}),
        RandomAI(playersNameList[2], {'print_info': False}),
        RandomAI(playersNameList[3], {'print_info': False})
    ]
    models_to_load = [(0, MODEL_PATH_V1)]
    
elif TEST_MODE == 'v2':
    agent_list = [
        DQNv2(playersNameList[0], {'print_info': DEBUG_MODE}),
        RandomAI(playersNameList[1], {'print_info': False}),
        RandomAI(playersNameList[2], {'print_info': False}),
        RandomAI(playersNameList[3], {'print_info': False})
    ]
    models_to_load = [(0, MODEL_PATH_V2)]
    
elif TEST_MODE == 'v1_vs_v2':
    agent_list = [
        DQNv1(playersNameList[0], {'print_info': False}),
        DQNv2(playersNameList[1], {'print_info': False}),
        RandomAI(playersNameList[2], {'print_info': False}),
        RandomAI(playersNameList[3], {'print_info': False})
    ]
    models_to_load = [(0, MODEL_PATH_V1), (1, MODEL_PATH_V2)]
    
elif TEST_MODE == 'v1_vs_random':
    agent_list = [
        DQNv1(playersNameList[0], {'print_info': False}),
        RandomAI(playersNameList[1], {'print_info': False}),
        RandomAI(playersNameList[2], {'print_info': False}),
        RandomAI(playersNameList[3], {'print_info': False})
    ]
    models_to_load = [(0, MODEL_PATH_V1)]
    
elif TEST_MODE == 'v2_vs_random':
    agent_list = [
        DQNv2(playersNameList[0], {'print_info': False}),
        RandomAI(playersNameList[1], {'print_info': False}),
        RandomAI(playersNameList[2], {'print_info': False}),
        RandomAI(playersNameList[3], {'print_info': False})
    ]
    models_to_load = [(0, MODEL_PATH_V2)]
else:
    raise ValueError(f"Unknown test mode: {TEST_MODE}")

# Load trained weights
print("="*60)
print("LOADING MODELS")
print("="*60)
for idx, model_path in models_to_load:
    if os.path.exists(model_path):
        print(f"✓ Loading {agent_list[idx].name} from: {model_path}")
        if hasattr(agent_list[idx], 'load'):
            agent_list[idx].load(model_path)
        else:
            agent_list[idx].model.load_weights(model_path)
        agent_list[idx].epsilon = 0.01  # Minimal exploration during testing
    else:
        print(f"✗ Warning: Model not found at {model_path}")
        print(f"  {agent_list[idx].name} will play untrained")

env = gym.make('Briscola-v2', playerNames=playersNameList, disable_env_checker=True)

# Statistics
wins = {name: 0 for name in playersNameList}
total_points = {name: 0 for name in playersNameList}
total_rewards = {agent.name: [] for agent in agent_list if agent.type == 'learning'}

print()
print("="*60)
print(f"TESTING: {TEST_MODE.upper()}")
print("="*60)
print(f"Games: {NUM_GAMES}")
print("\nAgents:")
for agent in agent_list:
    agent_type = agent.__class__.__name__ if hasattr(agent, '__class__') else agent.type
    print(f"  {agent.name}: {agent_type}")
print("="*60)
print()

for game_num in range(NUM_GAMES):
    if not DEBUG_MODE and (game_num + 1) % 10 == 0:
        print(f"Playing game {game_num + 1}/{NUM_GAMES}...")
    
    if DEBUG_MODE:
        print(f"\n{'='*60}")
        print(f"GAME START")
        print(f"{'='*60}")
    
    observation, _ = env.reset()
    actions = {}
    states = {}
    game_reward = {agent.name: 0 for agent in agent_list if agent.type == 'learning'}
    
    step_count = 0
    
    while True:
        now_event = observation['event_name']
        
        if DEBUG_MODE and now_event == 'PlayTurn':
            step_count += 1
            print(f"\n--- Step {step_count} ---")
            print(f"Event: {now_event}")
            print(f"Current Player: {observation['data']['playerName']}")
            print(f"Hand: {observation['data']['hand']}")
            print(f"Table: {observation['data'].get('table', [])}")
            print(f"Briscola: {observation['data'].get('briscola', 'N/A')}")
            print(f"State shape: {len(observation['data']['state'])} cards")
        
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
                        
                        if DEBUG_MODE and agent.type == 'learning':
                            print(f"DQN chose card index: {action['data']['action']['card']}")
        
        observation, reward, done, info = env.step(action)
        
        if DEBUG_MODE and reward is not None:
            print(f"Rewards: {reward}")
        
        # Track rewards for learning agents
        if reward is not None:
            for agent in agent_list:
                if agent.type == 'learning' and agent.name in reward:
                    game_reward[agent.name] += reward[agent.name]
        
        # Capture game over data
        if done and observation is not None:
            if observation.get('event_name') == 'GameOver' and 'data' in observation:
                if DEBUG_MODE:
                    print(f"\n{'='*60}")
                    print("GAME OVER")
                    print(f"{'='*60}")
                
                if 'game_winner' in observation['data']:
                    winner = observation['data']['game_winner']
                    wins[winner] += 1
                    
                    if DEBUG_MODE:
                        print(f"Winner: {winner}")
                
                if 'players' in observation['data']:
                    for player_data in observation['data']['players']:
                        name = player_data['playerName']
                        points = player_data['playerPoints']
                        total_points[name] += points
                        
                        if DEBUG_MODE:
                            print(f"{name}: {points} points")
        
        if done:
            break
    
    # Record rewards
    for agent in agent_list:
        if agent.type == 'learning':
            total_rewards[agent.name].append(game_reward[agent.name])
            
            if DEBUG_MODE:
                print(f"\nTotal reward for {agent.name}: {game_reward[agent.name]}")


# Print statistics
print()
print("="*60)
print("RESULTS")
print("="*60)
print(f"Games played: {NUM_GAMES}\n")

for name in playersNameList:
    win_rate = (wins[name] / NUM_GAMES) * 100
    avg_points = total_points[name] / NUM_GAMES
    
    # Get agent info
    agent_info = ""
    for agent in agent_list:
        if agent.name == name:
            agent_type = agent.__class__.__name__ if hasattr(agent, '__class__') else type(agent).__name__
            agent_info = f" ({agent_type})"
            break
    
    print(f"{name}{agent_info}:")
    print(f"  Wins: {wins[name]} ({win_rate:.1f}%)")
    print(f"  Avg Points: {avg_points:.1f}")
    
    # Show average reward for learning agents
    if name in total_rewards and total_rewards[name]:
        avg_reward = sum(total_rewards[name]) / len(total_rewards[name])
        print(f"  Avg Reward: {avg_reward:.2f}")
    print()

# Compare with random baseline
print("="*60)
print("PERFORMANCE ANALYSIS")
print("="*60)
random_baseline = NUM_GAMES / 4  # 25% if all equal

for agent in agent_list:
    if agent.type == 'learning':
        agent_wins = wins[agent.name]
        improvement = (agent_wins / random_baseline - 1) * 100
        
        print(f"\n{agent.name}:")
        print(f"  Expected (random): {random_baseline:.0f} wins (25%)")
        print(f"  Actual: {agent_wins} wins ({agent_wins/NUM_GAMES*100:.1f}%)")
        
        if improvement > 0:
            print(f"  Improvement: +{improvement:.1f}% 🎉")
        else:
            print(f"  Improvement: {improvement:.1f}%")

# Head-to-head comparison for v1 vs v2
if TEST_MODE == 'v1_vs_v2':
    print("\n" + "="*60)
    print("HEAD-TO-HEAD: DQN v1 vs DQN v2")
    print("="*60)
    v1_wins = wins[playersNameList[0]]
    v2_wins = wins[playersNameList[1]]
    
    print(f"DQN v1: {v1_wins} wins ({v1_wins/NUM_GAMES*100:.1f}%)")
    print(f"DQN v2: {v2_wins} wins ({v2_wins/NUM_GAMES*100:.1f}%)")
    
    if v1_wins > v2_wins:
        print(f"\n🏆 DQN v1 wins by {v1_wins - v2_wins} games!")
    elif v2_wins > v1_wins:
        print(f"\n🏆 DQN v2 wins by {v2_wins - v1_wins} games!")
    else:
        print(f"\n🤝 It's a tie!")

print("\n" + "="*60 + "\n")