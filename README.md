# Briscola

My attempt to create an AI capable to play the Italian card game Briscola.
The Agent will be trained through Reinforcement Learning.

## Description

I used to play this game a lot at university with my Computer Science and Engineering classmates.
I therefore decided to recreate the game and implement an AI through ML algorithms that could learn how to play.

The game is fairly easy and it can be played by 2, 3, 4 or even 5 people at each time.
If you want to know more about the rules you can find them at this link https://www.casualarena.com/briscola/rules.

## v2.1.0

Created an environment with OpenAI gym to mimic the game dynamics.
Game is playable from 2 to 4 players (no teams allowed).
Human, Random and Learning Agents have been created.
Training of 4 player Learning DQN Agent is done (run the code with less players to train the others).

### Next steps

- Better Training function
- Bug fixing: AI can't choose ooh range

## References

- https://github.com/zmcx16/OpenAI-Gym-Hearts
- https://github.com/nicknochnack/OpenAI-Reinforcement-Learning-with-Custom-Environment
- https://www.dominodatalab.com/blog/deep-reinforcement-learning
