"""
Unified Training Script for Briscola DQN Agents
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
    {'type': 'DQNv1', 'name': 'Player 1'},
    {'type': 'DQNv2', 'name': 'Player 2'},
    {'type': 'DQNv3', 'name': 'Player 3'},
    {'type': 'Random', 'name': 'Player 4'}
]

# Training parameters
NUM_EPISODES = 1000
SAVE_FREQUENCY = 100
PRINT_FREQUENCY = 50
BATCH_SIZE = 32

# Share weights between agents of same type (self-play style)
# If True, all DQNv2 agents share one model, all DQNv3 share another
SHARE_WEIGHTS = False

# Higher exploration for more diverse experiences
EPSILON_OVERRIDE = None  # Set to 0.3 for 30% exploration, None to use default

# Resume training from existing weights (set to None to start fresh)
# 'auto' will find latest checkpoint for each agent type
RESUME_MODE = None  # 'auto', None, or dict with paths

# Model paths for resuming (used if RESUME_MODE is dict)
# Example: RESUME_MODE = {
#     'DQN v3': 'learning/model_output_v3/4_players/agent0_weights_final.weights.h5'
# }

# ============================================================

def create_agent(player_config):
    """Create agent based on configuration"""
    agent_type = player_config['type']
    name = player_config['name']
    
    if agent_type == 'DQNv1':
        return DQNv1(name, {'print_info': False})
    elif agent_type == 'DQNv2':
        return DQNv2(name, {'print_info': False})
    elif agent_type == 'DQNv3':
        return DQNv3(name, {'print_info': False})
    elif agent_type == 'Random':
        return RandomAI(name, {'print_info': False})
    else:
        raise ValueError(f"Unknown agent type: {agent_type}")

def get_output_dir(players, share_weights=False):
    """Generate output directory name based on player configuration"""
    learning_agents = [p for p in players if p['type'] in ['DQNv1', 'DQNv2', 'DQNv3']]
    
    if len(learning_agents) == 0:
        raise ValueError("No learning agents configured")
    
    # Always use simple naming based on agent types present
    if len(learning_agents) == 1:
        agent_type = learning_agents[0]['type'].lower()
        return f'learning/model_output_{agent_type}'
    else:
        # Multiple learning agents - not used for saving when share_weights=True
        agent_types = '_'.join([p['type'].lower() for p in learning_agents])
        return f'learning/model_output_{agent_types}'

def find_latest_weights(base_dir, agent_name):
    """Find the latest weights file for an agent"""
    weights_dir = base_dir + '/4_players/'
    if not os.path.exists(weights_dir):
        return None
    
    import glob
    
    # Try to find checkpoint files
    pattern = f"{weights_dir}*weights_*.weights.h5"
    weight_files = glob.glob(pattern)
    
    if not weight_files:
        # Try final weights
        final_path = f"{weights_dir}agent0_weights_final.weights.h5"
        if os.path.exists(final_path):
            return final_path
        return None
    
    # Sort by episode number
    weight_files.sort()
    return weight_files[-1]  # Return latest

# Validate configuration
if len(PLAYERS) < 2 or len(PLAYERS) > 4:
    raise ValueError("Briscola requires 2-4 players")

# Create agents
player_names = [p['name'] for p in PLAYERS]

if SHARE_WEIGHTS:
    # Create agents with shared weights per type
    agent_list = []
    shared_agents = {}  # Track first agent of each type
    
    for p in PLAYERS:
        agent_type = p['type']
        
        if agent_type in ['DQNv1', 'DQNv2', 'DQNv3']:
            if agent_type not in shared_agents:
                # First agent of this type - create normally
                agent = create_agent(p)
                shared_agents[agent_type] = agent
                agent_list.append(agent)
            else:
                # Subsequent agents - share weights with first
                main_agent = shared_agents[agent_type]
                agent = create_agent(p)
                
                # Share model, target_model, memory
                agent.model = main_agent.model
                agent.target_model = main_agent.target_model
                agent.memory = main_agent.memory
                
                # Mark as shadow agent
                agent._is_shadow = True
                agent._main_agent = main_agent
                
                agent_list.append(agent)
        else:
            # Random agents don't share
            agent_list.append(create_agent(p))
    
    print("\n" + "="*60)
    print("WEIGHT SHARING ENABLED")
    print("="*60)
    for agent_type, main_agent in shared_agents.items():
        count = sum(1 for p in PLAYERS if p['type'] == agent_type)
        print(f"{agent_type}: {count} agents sharing weights")
    print("="*60 + "\n")
else:
    # Normal mode - separate weights
    agent_list = [create_agent(p) for p in PLAYERS]

# Determine output directory (only used when not sharing weights)
if SHARE_WEIGHTS:
    output_dir = None  # Each agent type saves to its own folder
else:
    # When not sharing, still save each agent type to its own folder
    output_dir = None

# Load existing weights if resume is enabled
if RESUME_MODE is not None:
    print("="*60)
    print("LOADING EXISTING WEIGHTS (RESUME TRAINING)")
    print("="*60)
    
    if SHARE_WEIGHTS:
        # Load one model per agent type
        loaded_types = set()
        
        for idx, (agent, config) in enumerate(zip(agent_list, PLAYERS)):
            agent_type = config['type']
            
            if agent.type == 'learning' and agent_type not in loaded_types:
                if isinstance(RESUME_MODE, dict) and agent.name in RESUME_MODE:
                    # Specific path provided
                    weight_path = RESUME_MODE[agent.name]
                elif RESUME_MODE == 'auto':
                    # Auto-find latest
                    base_dir = f'learning/model_output_{agent_type.lower()}'
                    weight_path = find_latest_weights(base_dir, agent.name)
                else:
                    weight_path = None
                
                if weight_path and os.path.exists(weight_path):
                    print(f"✓ Loading {agent_type} from: {weight_path}")
                    if hasattr(agent, 'load'):
                        agent.load(weight_path)
                    else:
                        agent.model.load_weights(weight_path)
                    print(f"  Epsilon: {agent.epsilon:.3f}")
                    
                    # Override epsilon if specified
                    if EPSILON_OVERRIDE is not None:
                        agent.epsilon = EPSILON_OVERRIDE
                        print(f"  Epsilon overridden to: {agent.epsilon:.3f}")
                    
                    loaded_types.add(agent_type)
                else:
                    print(f"✗ No weights found for {agent_type}, starting fresh")
                    loaded_types.add(agent_type)
    else:
        # Load each agent separately
        for idx, agent in enumerate(agent_list):
            if agent.type == 'learning':
                if isinstance(RESUME_MODE, dict) and agent.name in RESUME_MODE:
                    # Specific path provided
                    weight_path = RESUME_MODE[agent.name]
                elif RESUME_MODE == 'auto':
                    # Auto-find latest
                    agent_type = PLAYERS[idx]['type'].lower()
                    base_dir = f'learning/model_output_{agent_type}'
                    weight_path = find_latest_weights(base_dir, agent.name)
                else:
                    weight_path = None
                
                if weight_path and os.path.exists(weight_path):
                    print(f"✓ Loading {agent.name} from: {weight_path}")
                    if hasattr(agent, 'load'):
                        agent.load(weight_path)
                    else:
                        agent.model.load_weights(weight_path)
                    print(f"  Epsilon: {agent.epsilon:.3f}")
                    
                    # Override epsilon if specified
                    if EPSILON_OVERRIDE is not None:
                        agent.epsilon = EPSILON_OVERRIDE
                        print(f"  Epsilon overridden to: {agent.epsilon:.3f}")
                else:
                    print(f"✗ No weights found for {agent.name}, starting fresh")
    print()

# Override epsilon if specified (AFTER resume so it applies to everyone)
if EPSILON_OVERRIDE is not None:
    print(f"Overriding epsilon to {EPSILON_OVERRIDE} for all learning agents")
    for agent in agent_list:
        if agent.type == 'learning':
            agent.epsilon = EPSILON_OVERRIDE
            # Also update main agent if this is a shadow
            if hasattr(agent, '_is_shadow') and hasattr(agent, '_main_agent'):
                agent._main_agent.epsilon = EPSILON_OVERRIDE
    print()

env = gym.make('Briscola-v2', playerNames=player_names, disable_env_checker=True)

# Statistics tracking
episode_rewards = {agent.name: [] for agent in agent_list if agent.type == 'learning'}
episode_wins = {agent.name: [] for agent in agent_list if agent.type == 'learning'}

print("="*60)
print("TRAINING BRISCOLA AGENTS")
print("="*60)
print(f"Episodes: {NUM_EPISODES}")
print(f"Batch size: {BATCH_SIZE}")
print(f"Save frequency: every {SAVE_FREQUENCY} episodes")

# Show output directories for each agent type
print("Output directories:")
agent_types = set([p['type'] for p in PLAYERS if p['type'] in ['DQNv1', 'DQNv2', 'DQNv3']])
for agent_type in sorted(agent_types):
    print(f"  {agent_type}: learning/model_output_{agent_type.lower()}/4_players/")

print()
print("Players:")
for i, (agent, config) in enumerate(zip(agent_list, PLAYERS)):
    print(f"  {i+1}. {agent.name}: {config['type']}")
print("="*60)
print()

for i_episode in range(NUM_EPISODES):
    observation, _ = env.reset()
    actions = {}
    states = {}
    
    episode_reward = {agent.name: 0 for agent in agent_list if agent.type == 'learning'}
    episode_winner = None
    
    while True:
        now_event = observation['event_name']
        
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
        
        observation, reward, done, info = env.step(action)
        
        # Store experiences for learning agents
        if observation is not None and observation['event_name'] == 'ShowTurnEnd':
            for agent in agent_list:
                if agent.type == 'learning' and agent.name in states:
                    # Get appropriate next_state based on agent type
                    if agent.__class__.__name__ == 'DQNv3Agent':
                        next_state = observation['data']['state_v3']
                    else:
                        next_state = observation['data']['state']
                    
                    agent.remember(
                        states[agent.name],
                        actions[agent.name],
                        reward[agent.name],
                        next_state,
                        done
                    )
                    episode_reward[agent.name] += reward[agent.name]
        
        # Capture game winner
        if done and observation is not None:
            if observation.get('event_name') == 'GameOver' and 'data' in observation:
                if 'game_winner' in observation['data']:
                    episode_winner = observation['data']['game_winner']
        
        if done:
            break
    
    # Train all learning agents
    for agent in agent_list:
        if agent.type == 'learning':
            if len(agent.memory) > BATCH_SIZE:
                agent.train(BATCH_SIZE)
    
    # Track statistics for learning agents
    for agent in agent_list:
        if agent.type == 'learning':
            episode_rewards[agent.name].append(episode_reward[agent.name])
            episode_wins[agent.name].append(1 if episode_winner == agent.name else 0)
    
    # Print progress
    if (i_episode + 1) % PRINT_FREQUENCY == 0:
        print(f"Episode {i_episode + 1}/{NUM_EPISODES}")
        
        for agent in agent_list:
            if agent.type == 'learning':
                recent_rewards = episode_rewards[agent.name][-PRINT_FREQUENCY:]
                recent_wins = episode_wins[agent.name][-PRINT_FREQUENCY:]
                
                avg_reward = sum(recent_rewards) / len(recent_rewards)
                win_rate = sum(recent_wins) / len(recent_wins) * 100
                
                # Get epsilon from main agent if sharing weights
                if hasattr(agent, '_main_agent'):
                    epsilon = agent._main_agent.epsilon
                else:
                    epsilon = agent.epsilon
                
                print(f"  {agent.name}:")
                print(f"    Avg Reward: {avg_reward:.2f}")
                print(f"    Win Rate: {win_rate:.1f}%")
                print(f"    Epsilon: {epsilon:.3f}")
                print(f"    Memory: {len(agent.memory)}")
        print()
    
    # Save models periodically
    if (i_episode + 1) % SAVE_FREQUENCY == 0:
        # Always save each agent type to its own folder
        saved_types = set()
        for idx, (agent, config) in enumerate(zip(agent_list, PLAYERS)):
            if agent.type == 'learning' and config['type'] not in saved_types:
                agent_type = config['type'].lower()
                type_output_dir = f'learning/model_output_{agent_type}'
                os.makedirs(type_output_dir + '/4_players/', exist_ok=True)
                
                save_path = type_output_dir + '/4_players/' + f'agent0_weights_{i_episode+1:04d}.weights.h5'
                agent.save(save_path)
                print(f"✓ Saved {config['type']}: {save_path}")
                saved_types.add(config['type'])
        print()

# Save final models
print("="*60)
print("SAVING FINAL MODELS")
print("="*60)

# Always save each agent type to its own folder
saved_types = set()
for idx, (agent, config) in enumerate(zip(agent_list, PLAYERS)):
    if agent.type == 'learning' and config['type'] not in saved_types:
        agent_type = config['type'].lower()
        type_output_dir = f'learning/model_output_{agent_type}'
        os.makedirs(type_output_dir + '/4_players/', exist_ok=True)
        
        final_path = type_output_dir + '/4_players/' + f'agent0_weights_final.weights.h5'
        agent.save(final_path)
        print(f"✓ {config['type']}: {final_path}")
        saved_types.add(config['type'])

print()
print("="*60)
print("TRAINING COMPLETE!")
print("="*60)
print(f"Total episodes: {NUM_EPISODES}")
print()

# Print overall statistics
print("OVERALL STATISTICS:")
for agent in agent_list:
    if agent.type == 'learning':
        overall_avg_reward = sum(episode_rewards[agent.name]) / len(episode_rewards[agent.name])
        overall_win_rate = sum(episode_wins[agent.name]) / len(episode_wins[agent.name]) * 100
        
        # Get epsilon from main agent if sharing weights
        if hasattr(agent, '_main_agent'):
            final_epsilon = agent._main_agent.epsilon
        else:
            final_epsilon = agent.epsilon
        
        print(f"\n{agent.name}:")
        print(f"  Average Reward: {overall_avg_reward:.2f}")
        print(f"  Win Rate: {overall_win_rate:.1f}%")
        print(f"  Final Epsilon: {final_epsilon:.3f}")

print("\n" + "="*60)
print("\nTo test the trained agents, run:")
print(f"  python test.py")
print()