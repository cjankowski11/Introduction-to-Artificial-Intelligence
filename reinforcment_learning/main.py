import gymnasium as gym
import random
import json
LEARNING_RATE = 0.5


class Agent:
    def __init__(self, learning_rate,
                 posibble_moves, epsilon_start, epsilon_end,
                 epsilon_decay, discount_factor=0.95):
        self.temp = {}
        self.epsilon = epsilon_start
        self.epsilondecay = epsilon_decay
        self.final_epsilon = epsilon_end
        self.discount_factor = discount_factor
        self.lr = learning_rate
        self.possible_moves = posibble_moves

    def _check_state(self, state):
        if state not in self.temp:
            self.temp[state] = [0.0] * self.possible_moves

    def move(self, place, islearning):
        self._check_state(place)
        number = random.uniform(0, 1.0)
        if number <= self.epsilon and islearning:
            print("random")
            return random.randint(0, self.possible_moves-1)
        else:
            first_best = max(self.temp[place])
            possible_moves = []
            for move, move_value in enumerate(self.temp[place]):
                if move_value == first_best:
                    possible_moves.append(move)
            print(place, possible_moves)
            return random.choice(possible_moves)

    def learn(self, reward, new_place, old_place, move):
        # print(reward, new_place, old_place)
        self._check_state(new_place)
        cos = reward + self.discount_factor * max(self.temp[new_place]) - self.temp[old_place][move]
        self.temp[old_place][move] += self.lr * cos

    def update_epsilon(self):
        self.epsilon = max(self.epsilon - self.epsilondecay, self.final_epsilon)


env = gym.make('CliffWalking-v1', render_mode="human", max_episode_steps=200)
agent = Agent(LEARNING_RATE, env.action_space.n, 1, 0.05, 0.001)
print(agent.temp)

# learning
for epoka in range(1000):
    print(agent.temp)
    print("---------------------")
    print("epoka:"+str(epoka))
    new_place, info = env.reset()
    # print(new_place)
    episode_over = False
    total_reward = 0
    while not episode_over:
        action = agent.move(new_place, True)
        place = new_place
        new_place, reward, terminated, truncated, info = env.step(action)
        if new_place == 47:
            print("SUKCES")

        total_reward += reward
        agent.learn(reward, new_place, place, action)
        episode_over = terminated or truncated

    agent.update_epsilon()

with open("data.json", "w") as f:
    json.dump(agent.temp, f)
for epoka in range(5):
    print("TESTY")
    print(agent.temp)
    print("---------------------")
    print("epoka:"+str(epoka))
    new_place, info = env.reset()
    # print(new_place)
    episode_over = False
    total_reward = 0
    while not episode_over:
        action = agent.move(new_place, False)
        place = new_place
        new_place, reward, terminated, truncated, info = env.step(action)
        if new_place == 47:
            print("SUKCES")

        total_reward += reward
        episode_over = terminated or truncated
    agent.update_epsilon()
env.close()


# print(f"Action space: {env.action_space}")
# print(f"Sample action: {env.action_space.sample()}")
# print(f"Observation space: {env.observation_space}")
# print(f"Sample observation: {env.observation_space.sample()}")
