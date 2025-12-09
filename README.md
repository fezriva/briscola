# 🃏 Briscola RL

AI agents that learn to play Briscola (Italian card game) through Deep Reinforcement Learning.

## 📖 About

Briscola is a popular Italian trick-taking card game. This project implements the game environment and multiple DQN (Deep Q-Network) agents that learn optimal strategies through reinforcement learning.

**Game Rules**: [Briscola Rules](https://www.casualarena.com/briscola/rules)

## ✨ Features

- **Custom Gymnasium Environment** - Full Briscola game implementation (2-4 players)
- **Multiple AI Agents**:
  - 🎲 Random AI (baseline)
  - 🧠 DQN v1 (basic deep Q-learning)
  - 🚀 DQN v2 (target network + improved Q-learning)
  - 🎯 DQN v3 (multi-input architecture: separates hand cards from game context)
- **Intelligent Reward System** - Rewards strategic play (winning valuable turns) not just points
- **Self-Play Training** - Agents learn by playing against themselves
- **Comprehensive Testing** - Compare agent versions head-to-head

## 🏗️ Architecture

### DQN v3 (Latest)
Multi-input neural network with separated concerns:
- **Input 1**: Cards in hand (LSTM) - handles variable-length sequences
- **Input 2**: Game context (Dense) - briscola, table cards, turn info
- **Output**: Q-values for each action

**Why Multi-Input?**
- Clearer separation between "what I have" vs "game state"
- Faster learning - network doesn't waste capacity figuring out structure
- Better handles variable hand sizes (0-3 cards)

### Reward System
Encourages strategic play:
```python
# Turn reward
if win_turn:
    reward = (points_won - card_value_played) * 0.5
else:
    reward = -card_value_played * 0.2

# Round bonus
if win_round:
    reward += 100
```

**Example**: Playing a low-value card to win 21 points = +10.5 reward ✅  
Playing an Asso to win 0 points = -5.5 reward ❌

## 🚀 Quick Start

### Installation
```bash
# Clone repository
git clone https://github.com/yourusername/briscola.git
cd briscola

# Create virtual environment with uv
uv venv --python 3.12
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -e .
```

### Training
```bash
cd briscola

# Train DQN v3 (recommended)
python train.py
```

**Configuration** (`train.py`):
```python
TRAINING_MODE = 'v3'           # Agent version
NUM_EPISODES = 500             # Training duration
RESUME_MODE = 'auto'           # Continue from checkpoint
```

**Training Modes**:
- `'v1'`, `'v2'`, `'v3'` - Single agent vs 3 random
- `'self_play_v2'`, `'self_play_v3'` - Self-play (AlphaGo style)
- `'multi_v3'` - 4 agents learning together

### Testing
```bash
python test.py
```

**Configuration** (`test.py`):
```python
TEST_MODE = 'v3'               # Test single agent
# TEST_MODE = 'v2_vs_v3'       # Head-to-head comparison
NUM_GAMES = 100                # Evaluation games
DEBUG_MODE = False             # Detailed output
```

### Play vs AI
```bash
python play.py
```

Choose cards by entering 1, 2, or 3 when it's your turn!

## 📊 Results

| Agent | Training | Win Rate vs Random | Notes |
|-------|----------|-------------------|-------|
| Random | - | 25% | Baseline |
| DQN v1 | 20 episodes | ~30% | Basic Q-learning |
| DQN v2 | 1000 episodes | ~25% | Needs more training |
| DQN v3 | TBD | TBD | Multi-input architecture |

*Note: 25% is random baseline in 4-player game*

## 📁 Project Structure
```
briscola/
├── briscola/
│   ├── agents/
│   │   ├── dqn_v1.py         # Original DQN
│   │   ├── dqn_v2.py         # Improved DQN with target network
│   │   ├── dqn_v3.py         # Multi-input DQN (latest)
│   │   ├── random.py         # Random AI
│   │   └── human.py          # Human player
│   ├── modules/
│   │   ├── briscola.py       # Gymnasium environment
│   │   └── classes.py        # Card and Player classes
│   ├── train.py              # Training script
│   ├── test.py               # Testing/evaluation script
│   └── play.py               # Human vs AI gameplay
├── learning/                 # Saved model weights
├── pyproject.toml            # Dependencies (uv)
└── README.md
```

## 🛠️ Technical Details

### Environment
- **Observation Space**: Dict with game state (cards, briscola, table)
- **Action Space**: Discrete(3) - play card at index 0, 1, or 2
- **Reward**: Turn-based + round winner bonus

### Training Hyperparameters (v3)
```python
memory_size = 10000
gamma = 0.95              # Discount factor
epsilon_start = 1.0       # Initial exploration
epsilon_decay = 0.995     # Decay rate
epsilon_min = 0.01        # Minimum exploration
learning_rate = 0.001
batch_size = 32
target_update = 10        # Update target network every N training steps
```

## 🔬 Experiments

### Current Focus
- **Multi-input architecture** (v3) - Does separating hand from context improve learning?
- **Self-play training** - Can agents develop advanced strategies by playing themselves?
- **Longer training** - Does v2 improve with 5000+ episodes?

### Planned
- Attention mechanism for card importance
- Team play (2v2 mode)
- Transfer learning from v2 to v3

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Alternative network architectures (Attention, Transformer)
- Curriculum learning (start simple, increase difficulty)
- Multi-agent training strategies
- Better state representation

## 📚 References

- [OpenAI Gym Hearts Implementation](https://github.com/zmcx16/OpenAI-Gym-Hearts)
- [Deep Reinforcement Learning Guide](https://www.dominodatalab.com/blog/deep-reinforcement-learning)
- [Gymnasium Documentation](https://gymnasium.farama.org/)

## 📝 License

MIT License - feel free to use this code for learning and experimentation!

---

Built with ❤️ and lots of ☕ by someone who loves both card games and ML