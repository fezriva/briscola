"""
Unified Testing Script for Briscola DQN Agents
Simple player-based configuration
"""
import gymnasium as gym
import os
from modules import *
from agents.random import RandomAI
from agents.dqn_v1 import DQNAgent as DQNv1
from agents.dqn_v2 import ImprovedDQNAgent as DQNv2
from agents.dqn_v3 import DQNv3Agent as DQNv3

# ============================================================
# CONFIGURATION - CHANGE THESE
# ============================================================

# Configure each player - types: 'DQNv1', 'DQNv2', 'DQNv3', 'Random'
PLAYERS = [
    {'type': 'DQNv3', 'name': 'DQN v3', 'weights': 'learning/model_output_dqnv3/4_players/agent0_weights_final.weights.h5'},
    {'type': 'DQNv2', 'name': 'DQN v2', 'weights': 'learning/model_output_dqnv2/4_players/agent0_weights_final.weights.h5'},
    {'type': 'Random', 'name': 'Random 1'},
    {'type': 'Random', 'name': 'Random 2'}
]

# Number of test games
NUM_GAMES = 100

# Debug mode - run single game with detailed output
DEBUG_MODE = False  # Set to True to see detailed agent behavior

# ============================================================

def create_agent(player_config, debug=False):
    """Create agent based on configuration"""
    agent_type = player_config['type']
    name = player_config['name']
    
    if agent_type == 'DQNv1':
        return DQNv1(name, {'print_info': debug})
    elif agent_type == 'DQNv2':
        return DQNv2(name, {'print_info': debug})
    elif agent_type == 'DQNv3':
        return DQNv3(name, {'print_info': debug})
    elif agent_type == 'Random':
        return RandomAI(name, {'print_info': False})
    else:
        raise ValueError(f"Unknown agent type: {agent_type}")

# Override settings if debug mode
if DEBUG_MODE:
    NUM_GAMES = 1
    print("\n" + "="*60)
    print("DEBUG MODE ENABLED - Running 1 game with detailed output")
    print("="*60 + "\n")

# Validate configuration
if len(PLAYERS) < 2 or len(PLAYERS) > 4:
    raise ValueError("Briscola requires 2-4 players")

# Create agents
player_names = [p['name'] for p in PLAYERS]
agent_list = [create_agent(p, debug=DEBUG_MODE) for p in PLAYERS]

# Load trained weights
print("="*60)
print("LOADING MODELS")
print("="*60)

for idx, (agent, config) in enumerate(zip(agent_list, PLAYERS)):
    if agent.type == 'learning':
        weight_path = config.get('weights')
        
        if weight_path and os.path.exists(weight_path):
            print(f"✓ Loading {agent.name} from: {weight_path}")
            if hasattr(agent, 'load'):
                agent.load(weight_path)
            else:
                agent.model.load_weights(weight_path)
            agent.epsilon = 0.01  # Minimal exploration during testing
        else:
            if weight_path:
                print(f"✗ Warning: Model not found at {weight_path}")
            else:
                print(f"✗ Warning: No weights specified for {agent.name}")
            print(f"  {agent.name} will play untrained")

env = gym.make('Briscola-v2', playerNames=player_names, disable_env_checker=True)

# Statistics
wins = {name: 0 for name in player_names}
total_points = {name: 0 for name in player_names}
total_rewards = {agent.name: [] for agent in agent_list if agent.type == 'learning'}

print()
print("="*60)
print("TESTING AGENTS")
print("="*60)
print(f"Games: {NUM_GAMES}")
print("\nPlayers:")
for i, (agent, config) in enumerate(zip(agent_list, PLAYERS)):
    print(f"  {i+1}. {agent.name}: {config['type']}")
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
        
        if now_event == 'PlayTurn':
            playName = observation['data']['playerName']
            # Store appropriate state based on agent type
            for agent in agent_list:
                if agent.name == playName:
                    if agent.__class__.__name__ == 'DQNv3Agent':
                        states[playName] = observation['data']['state_v3']
                    else:
                        states[playName] = observation['data']['state']
                    break
        
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
                            print(f"{agent.name} chose card index: {action['data']['action']['card']}")
        
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

for idx, (name, config) in enumerate(zip(player_names, PLAYERS)):
    win_rate = (wins[name] / NUM_GAMES) * 100
    avg_points = total_points[name] / NUM_GAMES
    
    print(f"{name} ({config['type']}):")
    print(f"  Wins: {wins[name]} ({win_rate:.1f}%)")
    print(f"  Avg Points: {avg_points:.1f}")
    
    # Show average reward for learning agents
    if name in total_rewards and total_rewards[name]:
        avg_reward = sum(total_rewards[name]) / len(total_rewards[name])
        print(f"  Avg Reward: {avg_reward:.2f}")
    print()

# Performance analysis
print("="*60)
print("PERFORMANCE ANALYSIS")
print("="*60)

learning_agents = [agent for agent in agent_list if agent.type == 'learning']

if learning_agents:
    random_baseline = NUM_GAMES / len(PLAYERS)  # Equal distribution
    
    print(f"Random baseline: {random_baseline:.0f} wins ({100/len(PLAYERS):.1f}%)\n")
    
    for agent in learning_agents:
        agent_wins = wins[agent.name]
        improvement = (agent_wins / random_baseline - 1) * 100
        
        print(f"{agent.name}:")
        print(f"  Actual: {agent_wins} wins ({agent_wins/NUM_GAMES*100:.1f}%)")
        
        if improvement > 0:
            print(f"  vs Baseline: +{improvement:.1f}% 🎉")
        else:
            print(f"  vs Baseline: {improvement:.1f}%")
        print()

# Head-to-head comparison if 2 learning agents
if len(learning_agents) == 2:
    print("="*60)
    print(f"HEAD-TO-HEAD: {learning_agents[0].name} vs {learning_agents[1].name}")
    print("="*60)
    
    wins_0 = wins[learning_agents[0].name]
    wins_1 = wins[learning_agents[1].name]
    
    print(f"{learning_agents[0].name}: {wins_0} wins ({wins_0/NUM_GAMES*100:.1f}%)")
    print(f"{learning_agents[1].name}: {wins_1} wins ({wins_1/NUM_GAMES*100:.1f}%)")
    
    if wins_0 > wins_1:
        print(f"\n🏆 {learning_agents[0].name} wins by {wins_0 - wins_1} games!")
    elif wins_1 > wins_0:
        print(f"\n🏆 {learning_agents[1].name} wins by {wins_1 - wins_0} games!")
    else:
        print(f"\n🤝 It's a tie!")

print("\n" + "="*60 + "\n")