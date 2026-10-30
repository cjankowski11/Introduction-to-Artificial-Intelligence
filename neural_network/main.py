import math
import random
import statistics
import matplotlib.pyplot as plt

B = 1
MU = 0
ITERATIONS = 100000
LEARNING_RATE = 0.20
EXPERIMENT_REPEATS = 25


def sigmoid_function(x):
    return 1/(1+math.exp(-x))


def sigmoid_derivative(x):
    return x * (1 - x)


def laplace_function(x, mu=MU, b=B):
    exponent = -abs(x - mu) / b
    return (1 / (2 * b)) * math.exp(exponent)


class Neuron:
    def __init__(self, num_of_inputs):
        self.weights = [random.uniform(-1, 1) for _ in range(num_of_inputs + 1)]
        self.output = None
        self.inputs = None
        self.delta = 0

    def calculate_output(self, data, is_final_neuron):
        data_with_bias = data + [1]
        self.inputs = data_with_bias
        weighted_sum = 0
        for x, w in zip(data_with_bias, self.weights):
            weighted_sum += x*w
        if is_final_neuron:
            self.output = weighted_sum
        else:
            self.output = sigmoid_function(weighted_sum)
        return self.output

    def update_weights(self, lr):
        for i in range(len(self.weights)):
            self.weights[i] -= lr * self.delta * self.inputs[i]


class Network:
    def __init__(self, n_of_hidden_neurons, learning_step):
        self.hiddenlayer = [Neuron(1) for _ in range(n_of_hidden_neurons)]
        self.outputneuron = Neuron(n_of_hidden_neurons)
        self.learning_step = learning_step

    def test(self, input_data):
        inputs_for_output_neuron = []
        for neuron in self.hiddenlayer:
            y = neuron.calculate_output(input_data, False)
            inputs_for_output_neuron.append(y)
        return self.outputneuron.calculate_output(inputs_for_output_neuron, True)

    def train(self, input_data, target):
        output = self.test(input_data)
        error = output - target
        self.outputneuron.delta = error

        for i, neuron in enumerate(self.hiddenlayer):
            w_out = self.outputneuron.weights[i]
            neuron.delta = error * w_out * sigmoid_derivative(neuron.output)

        self.outputneuron.update_weights(self.learning_step)

        for n in self.hiddenlayer:
            n.update_weights(self.learning_step)


def run_single_experiment(n_hidden, iterations, lr):
    net = Network(n_hidden, lr)

    for _ in range(iterations):
        x = random.uniform(-8, 8)
        y = laplace_function(x)
        net.train([x], y)

    test_x = [i * 0.1 for i in range(-80, 81)]
    y_real = [laplace_function(x) for x in test_x]
    y_pred = [net.test([x]) for x in test_x]

    mse = sum((r - p)**2 for r, p in zip(y_real, y_pred)) / len(test_x)
    mae = sum(abs(r - p) for r, p in zip(y_real, y_pred)) / len(test_x)

    return mse, mae, net


def print_table_row(param_val, data):
    print(f"{param_val:<10} | {min(data):.6f} | {statistics.mean(data):.6f} | {statistics.stdev(data):.6f} | {max(data):.6f}")


def plot_results(net, title):
    test_x = [i * 0.05 for i in range(-160, 161)]
    y_real = [laplace_function(x) for x in test_x]
    y_pred = [net.test([x]) for x in test_x]

    plt.figure(figsize=(10, 6))
    plt.plot(test_x, y_real, label='Funkcja Rzeczywista (Laplace)', color='blue', linewidth=2)
    plt.plot(test_x, y_pred, label='Aproksymacja Sieci', color='red', linestyle='--', linewidth=2)
    plt.title(title)
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    neurons_to_test = [20]

    print("-" * 70)
    print(f"{'Neurony':<10} | {'Min MSE':<10} | {'Śr MSE':<10} | {'Std MSE':<10} | {'Max MSE':<10}")
    print("-" * 70)

    best_network = None
    best_mse = float('inf')

    for n_neurons in neurons_to_test:
        mse_results = []
        mae_results = []

        for _ in range(EXPERIMENT_REPEATS):
            mse, mae, net = run_single_experiment(n_neurons, ITERATIONS, LEARNING_RATE)
            mse_results.append(mse)
            mae_results.append(mae)

            if mse < best_mse:
                best_mse = mse
                best_network = net

        print_table_row(n_neurons, mse_results)

    print("-" * 70)

    if best_network:
        print(f"Generowanie wykresu dla sieci z najlepszym wynikiem (MSE: {best_mse:.6f})...")
        plot_results(best_network, f"Aproksymacja Rozkładu Laplace'a (MSE: {best_mse:.5f})")