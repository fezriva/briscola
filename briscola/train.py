"""
Unified Training Script for Briscola DQN Agents
Supports multiple agent versions and training modes
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

# Agent version to train: 'v1', 'v2', 'v3', 'v1_vs_v2', 'multi_v1', 'multi_v2', 'multi_v3', 'self_play_v2', 'self_play_v3'
TRAINING_MODE = 'v2'

# Training parameters
NUM_EPISODES = 500
SAVE_FREQUENCY = 100
PRINT_FREQUENCY = 50
BATCH_SIZE = 32

# Resume training from existing weights (set to None to start fresh)
RESUME_FROM_WEIGHTS = None  # e.g., 'learning/model_output_v2/4_players/agent0_weights_final.weights.h5'
# Or set to 'auto' to automatically find latest checkpoint
RESUME_MODE = 'auto'  # 'auto' or None

# ============================================================

# Training modes explained:
# 'v1' - Train single DQN v1 agent vs 3 random
# 'v2' - Train single DQN v2 agent vs 3 random
# 'v3' - Train single DQN v3 agent (multi-input) vs 3 random
# 'v1_vs_v2' - Train v1 and v2 against each other + 2 random
# 'multi_v1' - Train 4 DQN v1 agents together
# 'multi_v2' - Train 4 DQN v2 agents together
# 'multi_v3' - Train 4 DQN v3 agents together
# 'self_play_v2' - Train 1 DQN v2 against 3 copies of itself (shared learning)
# 'self_play_v3' - Train 1 DQN v3 against 3 copies of itself (shared learning)

playersNameList = ['Player 1', 'Player 2', 'Player 3', 'Player 4']

# Setup based on training mode
if TRAINING_MODE == 'v1':
    agent_list = [
        DQNv1(playersNameList[0], {'print_info': False}),
        RandomAI(playersNameList[1], {'print_info': False}),
        RandomAI(playersNameList[2], {'print_info': False}),
        RandomAI(playersNameList[3], {'print_info': False})
    ]
    output_dir = 'learning/model_output_v1'
    
elif TRAINING_MODE == 'v2':
    agent_list = [
        DQNv2(playersNameList[0], {'print_info': False}),
        RandomAI(playersNameList[1], {'print_info': False}),
        RandomAI(playersNameList[2], {'print_info': False}),
        RandomAI(playersNameList[3], {'print_info': False})
    ]
    output_dir = 'learning/model_output_v2'

elif TRAINING_MODE == 'v3':
    agent_list = [
        DQNv3(playersNameList[0], {'print_info': False}),
        RandomAI(playersNameList[1], {'print_info': False}),
        RandomAI(playersNameList[2], {'print_info': False}),
        RandomAI(playersNameList[3], {'print_info': False})
    ]
    output_dir = 'learning/model_output_v3'
    
elif TRAINING_MODE == 'v1_vs_v2':
    agent_list = [
        DQNv1(playersNameList[0], {'print_info': False}),
        DQNv2(playersNameList[1], {'print_info': False}),
        RandomAI(playersNameList[2], {'print_info': False}),
        RandomAI(playersNameList[3], {'print_info': False})
    ]
    output_dir = 'learning/model_output_v1_vs_v2'
    
elif TRAINING_MODE == 'multi_v1':
    agent_list = [
        DQNv1(playersNameList[0], {'print_info': False}),
        DQNv1(playersNameList[1], {'print_info': False}),
        DQNv1(playersNameList[2], {'print_info': False}),
        DQNv1(playersNameList[3], {'print_info': False})
    ]
    output_dir = 'learning/model_output_multi_v1'
    
elif TRAINING_MODE == 'multi_v2':
    agent_list = [
        DQNv2(playersNameList[0], {'print_info': False}),
        DQNv2(playersNameList[1], {'print_info': False}),
        DQNv2(playersNameList[2], {'print_info': False}),
        DQNv2(playersNameList[3], {'print_info': False})
    ]
    output_dir = 'learning/model_output_multi_v2'

elif TRAINING_MODE == 'multi_v3':
    agent_list = [
        DQNv3(playersNameList[0], {'print_info': False}),
        DQNv3(playersNameList[1], {'print_info': False}),
        DQNv3(playersNameList[2], {'print_info': False}),
        DQNv3(playersNameList[3], {'print_info': False})
    ]
    output_dir = 'learning/model_output_multi_v3'
    
elif TRAINING_MODE == 'self_play_v2':
    # Create one main agent
    main_agent = DQNv2(playersNameList[0], {'print_info': False})
    
    # Create 3 "shadow" agents that share the same model
    agent_list = [main_agent]
    for i in range(1, 4):
        shadow = DQNv2(playersNameList[i], {'print_info': False})
        # Share the model and target_model references (not copies!)
        shadow.model = main_agent.model
        shadow.target_model = main_agent.target_model
        shadow.memory = main_agent.memory  # Share experience replay too
        agent_list.append(shadow)
    
    output_dir = 'learning/model_output_v2'  # Use same output as 'v2' mode

elif TRAINING_MODE == 'self_play_v3':
    # Create one main agent
    main_agent = DQNv3(playersNameList[0], {'print_info': False})
    
    # Create 3 "shadow" agents that share the same model
    agent_list = [main_agent]
    for i in range(1, 4):
        shadow = DQNv3(playersNameList[i], {'print_info': False})
        # Share the model and target_model references (not copies!)
        shadow.model = main_agent.model
        shadow.target_model = main_agent.target_model
        shadow.memory = main_agent.memory  # Share experience replay too
        agent_list.append(shadow)
    
    output_dir = 'learning/model_output_v3'  # Use same output as 'v3' mode
    
else:
    raise ValueError(f"Unknown training mode: {TRAINING_MODE}")

# Create output directory
os.makedirs(output_dir + '/4_players/', exist_ok=True)

# Load existing weights if resume is enabled
def find_latest_weights(output_dir, agent_idx):
    """Find the latest weights file for an agent"""
    weights_dir = output_dir + '/4_players/'
    if not os.path.exists(weights_dir):
        return None
    
    import glob
    pattern = f"{weights_dir}agent{agent_idx}_weights_*.weights.h5"
    weight_files = glob.glob(pattern)
    
    if not weight_files:
        # Try final weights
        final_path = f"{weights_dir}agent{agent_idx}_weights_final.weights.h5"
        if os.path.exists(final_path):
            return final_path
        return None
    
    # Sort by episode number
    weight_files.sort()
    return weight_files[-1]  # Return latest

if RESUME_MODE == 'auto' or RESUME_FROM_WEIGHTS is not None:
    print("="*60)
    print("LOADING EXISTING WEIGHTS (RESUME TRAINING)")
    print("="*60)
    
    for idx, agent in enumerate(agent_list):
        if agent.type == 'learning':
            if RESUME_FROM_WEIGHTS is not None:
                # Specific path provided
                weight_path = RESUME_FROM_WEIGHTS
            else:
                # Auto-find latest
                weight_path = find_latest_weights(output_dir, idx)
            
            if weight_path and os.path.exists(weight_path):
                print(f"✓ Loading {agent.name} from: {weight_path}")
                if hasattr(agent, 'load'):
                    agent.load(weight_path)
                else:
                    agent.model.load_weights(weight_path)
                print(f"  Epsilon: {agent.epsilon:.3f}")
            else:
                print(f"✗ No weights found for {agent.name}, starting fresh")
    print()

env = gym.make('Briscola-v2', playerNames=playersNameList, disable_env_checker=True)

# Statistics tracking
episode_rewards = {agent.name: [] for agent in agent_list if agent.type == 'learning'}
episode_wins = {agent.name: [] for agent in agent_list if agent.type == 'learning'}

print("="*60)
print("TRAINING BRISCOLA DQN AGENTS")
print("="*60)
print(f"Mode: {TRAINING_MODE}")
print(f"Episodes: {NUM_EPISODES}")
print(f"Batch size: {BATCH_SIZE}")
print(f"Save frequency: every {SAVE_FREQUENCY} episodes")
print(f"Output directory: {output_dir}")
print()
print("Agents:")
for i, agent in enumerate(agent_list):
    agent_type = agent.__class__.__name__ if hasattr(agent, '__class__') else agent.type
    print(f"  {agent.name}: {agent_type}")
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
                epsilon = agent.epsilon
                
                print(f"  {agent.name}:")
                print(f"    Avg Reward: {avg_reward:.2f}")
                print(f"    Win Rate: {win_rate:.1f}%")
                print(f"    Epsilon: {epsilon:.3f}")
                print(f"    Memory: {len(agent.memory)}")
        print()
    
    # Save models periodically
    if (i_episode + 1) % SAVE_FREQUENCY == 0:
        if TRAINING_MODE in ['self_play_v2', 'self_play_v3']:
            # Only save the main agent (agent 0), others share the same model
            save_path = output_dir + '/4_players/' + f'agent0_weights_{i_episode+1:04d}.weights.h5'
            agent_list[0].save(save_path)
            print(f"✓ Saved self-play model: {save_path}")
        else:
            for idx, agent in enumerate(agent_list):
                if agent.type == 'learning':
                    save_path = output_dir + '/4_players/' + f'agent{idx}_weights_{i_episode+1:04d}.weights.h5'
                    agent.save(save_path)
                    print(f"✓ Saved {agent.name}: {save_path}")
        print()

# Save final models
print("="*60)
print("SAVING FINAL MODELS")
print("="*60)

if TRAINING_MODE in ['self_play_v2', 'self_play_v3']:
    # Only save the main agent
    final_path = output_dir + '/4_players/' + f'agent0_weights_final.weights.h5'
    agent_list[0].save(final_path)
    print(f"✓ Self-play model: {final_path}")
else:
    for idx, agent in enumerate(agent_list):
        if agent.type == 'learning':
            final_path = output_dir + '/4_players/' + f'agent{idx}_weights_final.weights.h5'
            agent.save(final_path)
            print(f"✓ {agent.name}: {final_path}")

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
        
        print(f"\n{agent.name}:")
        print(f"  Average Reward: {overall_avg_reward:.2f}")
        print(f"  Win Rate: {overall_win_rate:.1f}%")
        print(f"  Final Epsilon: {agent.epsilon:.3f}")

print("\n" + "="*60)
print("\nTo test the trained agents, run:")
print(f"  python test.py")
print()