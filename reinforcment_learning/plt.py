from pl import Agent
import gymnasium as gym
import matplotlib.pyplot as plt


def test_quality(agent, env):
    number_of_tests = 25
    sum_of_total_rewards = 0
    for _ in range(number_of_tests):
        new_place, _ = env.reset()
        episode_over = False
        total_reward = 0
        while not episode_over:
            action = agent.move(new_place, False)
            new_place, reward, terminated, truncated, _ = env.step(action)
            total_reward -= reward

            episode_over = terminated or truncated
            if episode_over:
                sum_of_total_rewards += total_reward

    return sum_of_total_rewards/number_of_tests


if __name__ == "__main__":
    env = gym.make('CliffWalking-v1', max_episode_steps=1000)
    learning_rates = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1]
    number_of_echoes = 1000
    epoches_for_tests = list(range(0, number_of_echoes, 10))
    results_for_lr = {lr: [] for lr in learning_rates}
    for learning_rate in learning_rates:
        print(learning_rate)
        decay = 1/number_of_echoes
        agent = Agent(learning_rate, env.observation_space.n, env.action_space.n,
                      epsilon_start=1, epsilon_end=0.05, epsilon_decay=decay,
                      json_data=None, discount_factor=0.98)
        for epoka in range(number_of_echoes):
            if epoka in epoches_for_tests:
                result = test_quality(agent, env)
                results_for_lr[learning_rate].append(result) 
            new_place, info = env.reset()
            episode_over = False

            while not episode_over:
                action = agent.move(new_place, True)
                place = new_place
                new_place, reward, terminated, truncated, info = env.step(action)
                agent.learn(reward, new_place, place, action)
                episode_over = terminated or truncated
            agent.update_epsilon()

    env.close()
    plt.figure(figsize=(12, 7))

    for lr in learning_rates:
        y_values = results_for_lr[lr]
        plt.plot(
            epoches_for_tests,
            y_values,
            label=f'LR = {lr}',
            # marker='o',
            # markersize=5,
            # markerfacecolor='none',
            linewidth=1.4,
            alpha=0.8
        )

    plt.title("Average cost for various learning rates")
    plt.xlabel("epoch number")
    plt.ylabel("average cost")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.yscale("log")
    filename = "image.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.show()
