"""
Improved DQN Agent for Briscola
- Proper Q-learning with Bellman equation
- Target network for stability
- Better feedforward architecture
- Experience replay
"""
import tensorflow as tf
import numpy as np
import collections
import random
from datetime import datetime


class ImprovedDQNAgent:
    """
    Deep Q-Network agent with modern best practices
    """
    
    def __init__(self, name, params=None):
        random.seed()  # Use system time for randomness
        self.name = name
        self.type = 'learning'
        
        # Parse parameters
        if params is not None:
            self.print_info = params.get('print_info', False)
        else:
            self.print_info = False
        
        # State and action space
        self.state_size = (None, 3)  # Variable number of cards, each with 3 features
        self.action_size = 3  # Can play card 0, 1, or 2
        
        # Hyperparameters
        self.memory = collections.deque(maxlen=10000)  # Increased from 2000
        self.gamma = 0.95  # Discount factor for future rewards
        self.epsilon = 1.0  # Exploration rate (start with full exploration)
        self.epsilon_decay = 0.995  # Decay exploration over time
        self.epsilon_min = 0.01  # Minimum exploration rate
        self.learning_rate = 0.001
        self.batch_size = 32
        
        # Target network update frequency
        self.target_update_frequency = 10  # Update target network every N training calls
        self.training_count = 0
        
        # Build main and target networks
        self.model = self._build_model()
        self.target_model = self._build_model()
        self.update_target_model()  # Initially, both networks are the same
    
    def _build_model(self):
        """
        Build a feedforward neural network for Q-value approximation
        
        Architecture:
        - Input: State representation (variable-length sequence of cards)
        - Dense layers: Process the state
        - Output: Q-values for each action (3 actions)
        
        Why this architecture:
        - Simple feedforward is faster and often better than LSTM for this task
        - Multiple dense layers allow learning complex patterns
        - Final layer has 3 outputs (Q-value for each card choice)
        """
        model = tf.keras.Sequential([
            # Input layer - accepts variable-length card sequences
            tf.keras.layers.Input(shape=self.state_size),
            
            # First hidden layer - 64 neurons to learn patterns
            tf.keras.layers.Dense(64, activation='relu'),
            
            # LSTM to process the sequence of cards
            # This helps because order of cards matters
            tf.keras.layers.LSTM(32),
            
            # Second hidden layer - 32 neurons for more abstraction
            tf.keras.layers.Dense(32, activation='relu'),
            
            # Output layer - 3 Q-values (one per action)
            # Linear activation because Q-values can be any real number
            tf.keras.layers.Dense(self.action_size, activation='linear')
        ])
        
        # Compile with MSE loss (standard for Q-learning)
        model.compile(
            loss='mse',
            optimizer=tf.keras.optimizers.Adam(learning_rate=self.learning_rate)
        )
        
        return model
    
    def update_target_model(self):
        """
        Copy weights from main model to target model
        
        Why: Target network provides stable Q-value estimates during training
        The main network is constantly updated, but the target network is frozen
        for several training steps, preventing the "moving target" problem
        """
        self.target_model.set_weights(self.model.get_weights())
    
    def remember(self, state, action, reward, next_state, done):
        """
        Store experience in replay memory
        
        Args:
            state: Current state
            action: Action taken
            reward: Reward received
            next_state: State after action
            done: Whether episode ended
        """
        self.memory.append((state, action, reward, next_state, done))
    
    def train(self, batch_size=None):
        """
        Train the network using experience replay
        
        This is where the magic happens - proper Q-learning!
        
        Key improvements over old version:
        1. Uses Bellman equation: Q(s,a) = r + γ * max(Q(s',a'))
        2. Uses target network for stable learning
        3. Only updates Q-value for the action taken (not all actions)
        """
        if batch_size is None:
            batch_size = self.batch_size
        
        # Need enough samples to train
        if len(self.memory) < batch_size:
            return
        
        # Sample random batch from memory
        minibatch = random.sample(self.memory, batch_size)
        
        # Prepare batch data - need to pad states to same length
        states = []
        targets = []
        
        # Find max state length in batch for padding
        max_len = max(len(state) for state, _, _, _, _ in minibatch)
        
        for state, action, reward, next_state, done in minibatch:
            # Pad state to max_len
            padded_state = self._pad_state(state, max_len)
            padded_next_state = self._pad_state(next_state, max_len)
            
            # Current Q-values from main network
            current_q_values = self.model.predict(np.array([padded_state]), verbose=0)[0]
            
            if done:
                # If episode ended, there's no future reward
                target_q_value = reward
            else:
                # Use TARGET network to get Q-values for next state
                # This is the key to stability!
                next_q_values = self.target_model.predict(np.array([padded_next_state]), verbose=0)[0]
                
                # Bellman equation: Q(s,a) = reward + gamma * max(Q(next_state, a'))
                target_q_value = reward + self.gamma * np.max(next_q_values)
            
            # Update only the Q-value for the action that was taken
            current_q_values[action] = target_q_value
            
            states.append(padded_state)
            targets.append(current_q_values)
        
        # Train on the batch
        self.model.fit(
            np.array(states),
            np.array(targets),
            batch_size=batch_size,
            epochs=1,
            verbose=0
        )
        
        # Decay exploration rate
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        
        # Update target network periodically
        self.training_count += 1
        if self.training_count % self.target_update_frequency == 0:
            self.update_target_model()
            if self.print_info:
                print(f"Target network updated (training count: {self.training_count})")
    
    def _pad_state(self, state, target_len):
        """
        Pad state to target length with zeros
        
        Args:
            state: List of cards (each card is [suit, value, position])
            target_len: Desired length
        
        Returns:
            Padded state as numpy array
        """
        state = np.array(state)
        if len(state) < target_len:
            # Pad with zeros
            padding = np.zeros((target_len - len(state), 3))
            state = np.vstack([state, padding])
        return state
    
    def act(self, observation):
        """
        Choose an action based on the current observation
        
        Uses epsilon-greedy strategy:
        - With probability epsilon: explore (random action)
        - With probability 1-epsilon: exploit (use learned Q-values)
        """
        
        # Handle different game events
        if observation['event_name'] == 'GameStart':
            if self.print_info:
                print(observation)
        elif observation['event_name'] == 'NewRound':
            if self.print_info:
                print(observation)
        elif observation['event_name'] == 'ShowPlayerHand':
            if self.print_info:
                print(observation)
        elif observation['event_name'] == 'PlayTurn':
            if self.print_info:
                print(f"\n{self.name}'s turn")
            
            state = observation['data']['state']
            hand_size = len(observation['data']['hand'])
            
            # Epsilon-greedy action selection
            if np.random.rand() <= self.epsilon:
                # Explore: choose random valid action
                choose_card = random.randrange(hand_size)
                if self.print_info:
                    print(f"  Exploring (ε={self.epsilon:.3f}): chose card {choose_card}")
            else:
                # Exploit: use Q-values to choose best action
                q_values = self.model.predict(np.array([state]), verbose=0)[0]
                
                # Only consider valid actions (cards in hand)
                valid_q_values = q_values[:hand_size]
                choose_card = np.argmax(valid_q_values)
                
                if self.print_info:
                    print(f"  Exploiting: Q-values={valid_q_values}, chose card {choose_card}")
            
            return {
                "event_name": "PlayTurn_Action",
                "data": {
                    'playerName': self.name,
                    'action': {'card': choose_card}
                }
            }
        
        elif observation['event_name'] == 'ShowTurnAction':
            if self.print_info:
                print(observation)
        elif observation['event_name'] == 'ShowTurnEnd':
            if self.print_info:
                print(observation)
        elif observation['event_name'] == 'RoundEnd':
            if self.print_info:
                print(observation)
        elif observation['event_name'] == 'GameOver':
            if self.print_info:
                print(observation)
    
    def save(self, filepath):
        """Save model weights"""
        self.model.save_weights(filepath)
        if self.print_info:
            print(f"Model saved to {filepath}")
    
    def load(self, filepath):
        """Load model weights"""
        self.model.load_weights(filepath)
        self.update_target_model()  # Sync target network
        if self.print_info:
            print(f"Model loaded from {filepath}")