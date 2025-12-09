"""
DQN v3 Agent for Briscola - Multi-Input Architecture
Separates hand cards from global game context for better learning
"""
import tensorflow as tf
import numpy as np
import collections
import random


class DQNv3Agent:
    """
    Deep Q-Network with multi-input architecture:
    - Input 1: Cards in hand (LSTM) - variable length
    - Input 2: Game context (Dense) - fixed length
    """
    
    def __init__(self, name, params=None):
        random.seed()
        self.name = name
        self.type = 'learning'
        
        # Parse parameters
        if params is not None:
            self.print_info = params.get('print_info', False)
        else:
            self.print_info = False
        
        # State and action space
        self.max_hand_size = 3  # Maximum cards in hand
        self.card_features = 3  # [suit, value, points]
        self.context_size = 15  # Fixed context features
        self.action_size = 3  # Can play card 0, 1, or 2
        
        # Hyperparameters
        self.memory = collections.deque(maxlen=10000)
        self.gamma = 0.95  # Discount factor
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        self.learning_rate = 0.001
        self.batch_size = 32
        
        # Target network update frequency
        self.target_update_frequency = 10
        self.training_count = 0
        
        # Build networks
        self.model = self._build_model()
        self.target_model = self._build_model()
        self.update_target_model()
    
    def _build_model(self):
        """
        Build multi-input Q-network:
        - Input 1: Hand cards (variable length, LSTM)
        - Input 2: Game context (fixed length, Dense)
        - Output: Q-values for 3 actions
        """
        # Input 1: Hand cards (variable length)
        hand_input = tf.keras.Input(shape=(None, self.card_features), name='hand_input')
        
        # Process hand with LSTM
        hand_lstm = tf.keras.layers.LSTM(32, name='hand_lstm')(hand_input)
        
        # Input 2: Global context (fixed length)
        context_input = tf.keras.Input(shape=(self.context_size,), name='context_input')
        
        # Process context with Dense layers
        context_dense = tf.keras.layers.Dense(32, activation='relu', name='context_dense1')(context_input)
        context_dense = tf.keras.layers.Dense(32, activation='relu', name='context_dense2')(context_dense)
        
        # Combine both streams
        combined = tf.keras.layers.Concatenate(name='combine')([hand_lstm, context_dense])
        
        # Shared layers
        hidden = tf.keras.layers.Dense(64, activation='relu', name='hidden1')(combined)
        hidden = tf.keras.layers.Dense(64, activation='relu', name='hidden2')(hidden)
        
        # Output: Q-values for each action
        q_values = tf.keras.layers.Dense(self.action_size, activation='linear', name='q_values')(hidden)
        
        # Create model
        model = tf.keras.Model(inputs=[hand_input, context_input], outputs=q_values)
        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=self.learning_rate),
                     loss='mse')
        
        return model
    
    def update_target_model(self):
        """Copy weights from main model to target model"""
        self.target_model.set_weights(self.model.get_weights())
    
    def _pad_hand(self, hand):
        """Pad hand to max_hand_size with zeros"""
        hand = np.array(hand)
        if len(hand) == 0:
            # Empty hand - return array of zeros
            return np.zeros((self.max_hand_size, self.card_features))
        
        if len(hand) < self.max_hand_size:
            padding = np.zeros((self.max_hand_size - len(hand), self.card_features))
            hand = np.vstack([hand, padding])
        
        return hand
    
    def _prepare_state(self, state):
        """
        Prepare state dict for model input
        Returns: (hand_array, context_array)
        """
        hand = self._pad_hand(state['hand'])
        context = np.array(state['context'])
        return hand, context
    
    def remember(self, state, action, reward, next_state, done):
        """Store experience in replay memory"""
        self.memory.append((state, action, reward, next_state, done))
    
    def act(self, observation):
        """
        Choose action based on epsilon-greedy policy
        """
        event_name = observation['event_name']
        
        if event_name == 'PlayTurn':
            player_name = observation['data']['playerName']
            
            if player_name == self.name:
                # Get multi-input state (use state_v3 key)
                state = observation['data']['state_v3']
                hand_size = len(state['hand'])
                
                # Epsilon-greedy action selection
                if np.random.rand() <= self.epsilon:
                    # Explore: random valid action
                    action_index = random.randrange(hand_size)
                    if self.print_info:
                        print(f"{self.name}'s turn")
                        print(f"  Exploring (ε={self.epsilon:.3f}): chose card {action_index}")
                else:
                    # Exploit: choose best action
                    hand, context = self._prepare_state(state)
                    
                    # Predict Q-values
                    q_values = self.model.predict([
                        np.array([hand]),
                        np.array([context])
                    ], verbose=0)[0]
                    
                    # Only consider valid actions (cards in hand)
                    valid_q_values = q_values[:hand_size]
                    action_index = np.argmax(valid_q_values)
                    
                    if self.print_info:
                        print(f"{self.name}'s turn")
                        print(f"  Exploiting: Q-values={valid_q_values}, chose card {action_index}")
                
                # Decay epsilon
                if self.epsilon > self.epsilon_min:
                    self.epsilon *= self.epsilon_decay
                
                # Return action
                return {
                    'event_name': 'PlayTurn_Action',
                    'broadcast': False,
                    'data': {
                        'playerName': self.name,
                        'action': {'card': action_index}
                    }
                }
        
        return None
    
    def train(self, batch_size):
        """
        Train the network using experience replay
        """
        if len(self.memory) < batch_size:
            return
        
        # Sample random minibatch
        minibatch = random.sample(self.memory, batch_size)
        
        # Prepare batch data
        hands_batch = []
        contexts_batch = []
        targets_batch = []
        
        for state, action, reward, next_state, done in minibatch:
            hand, context = self._prepare_state(state)
            
            # Get current Q-values
            current_q_values = self.model.predict([
                np.array([hand]),
                np.array([context])
            ], verbose=0)[0]
            
            # Calculate target Q-value using Bellman equation
            if done:
                target_q_value = reward
            else:
                next_hand, next_context = self._prepare_state(next_state)
                next_q_values = self.target_model.predict([
                    np.array([next_hand]),
                    np.array([next_context])
                ], verbose=0)[0]
                target_q_value = reward + self.gamma * np.max(next_q_values)
            
            # Update Q-value for the action taken
            current_q_values[action] = target_q_value
            
            # Add to batch
            hands_batch.append(hand)
            contexts_batch.append(context)
            targets_batch.append(current_q_values)
        
        # Train on batch
        self.model.fit(
            [np.array(hands_batch), np.array(contexts_batch)],
            np.array(targets_batch),
            epochs=1,
            verbose=0
        )
        
        # Update target network periodically
        self.training_count += 1
        if self.training_count % self.target_update_frequency == 0:
            self.update_target_model()
    
    def save(self, filepath):
        """Save model weights"""
        self.model.save_weights(filepath)
    
    def load(self, filepath):
        """Load model weights"""
        self.model.load_weights(filepath)
        self.update_target_model()