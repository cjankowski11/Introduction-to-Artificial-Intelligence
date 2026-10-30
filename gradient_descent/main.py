import matplotlib.pyplot as plt
import numpy as np
from autograd import grad
import random


def function_1(point):
    return point[0]**2 + point[1]**2


def matyas_function(point):
    return 0.26*(point[0]**2+point[1]**2) - 0.48*point[0]*point[1]


def simple_gradient_algorithm(max_iteration: int, starting_point, step_size, function):
    starting_point = np.array(starting_point, dtype=float)
    points = [starting_point]
    function_values = [function(starting_point)]
    gradient_fn = grad(function)
    epsilon = 1e-6
    final_iteration = 0
    for _ in range(max_iteration):
        gra = gradient_fn(starting_point)
        
        if np.linalg.norm(gra) < epsilon:
            break
        new_point = starting_point - step_size * gra
        points.append(new_point)
        value = function(new_point)
        function_values.append(value)
        
        starting_point = new_point
        final_iteration += 1
    
    return np.array(points), function_values, final_iteration


def visualize_fun(obj_fun: callable, trajectory: np.ndarray):
    min_x, min_y = trajectory[-1]
    MIN_X = 10
    MAX_X = 10
    PLOT_STEP = 100

    x1 = np.linspace(-MIN_X, MAX_X, PLOT_STEP)
    x2 = np.linspace(-MIN_X, MAX_X, PLOT_STEP)
    X1, X2 = np.meshgrid(x1, x2)
    Z = obj_fun((X1, X2))

    plt.figure(figsize=(8, 6))
    plt.pcolormesh(X1, X2, Z, cmap='viridis', shading='auto')
    plt.colorbar(label='Objective Function Value')
    plt.xlabel('x1')
    plt.ylabel('x2')
    plt.title('Objective Function Visualization')

    plt.scatter(min_x, min_y, color='yellow',
                label='Minimum found by gradient descent alg.')
    plt.plot(trajectory[:, 0], trajectory[:, 1],
             marker='o', color='red',
             label='Gradient Descent Steps', alpha=0.5)

    plt.legend()
    plt.show()


def find_best_step_size(function):
    step_size_plot = []
    average_value_for_step = []
    for step in range(1, 201, 1):
        # print(step)
        step_size = step * 0.01
        step_size_plot.append(step_size)
        average_list = []
        suma = 0
        number_of_points = 100
        for _ in range(number_of_points):
            starting_point_global = (random.uniform(-10, 10), random.uniform(-10, 10))
            points = simple_gradient_algorithm(300, starting_point_global, step_size, function)[0]
            final_point = points[-1]
            value = function(final_point)
            average_list.append(value)
            
        suma = sum(average_list) / number_of_points
        average_value_for_step.append(suma)
    plt.plot(step_size_plot, average_value_for_step)
    plt.title("Average function value for various size of learning step for 100 different points")
    plt.xlabel("learning step size")
    plt.ylabel("average function value")
    plt.yscale("log")
    plt.show()

           
def checking_specific_step_size(function, step_size):
    values_plot = [0] * 400
    indexes = list(range(400))
    n = 100
    for _ in range(n):
        
        starting_point_global = (random.uniform(-10, 10), random.uniform(-10, 10))
        _, values, final_iteration = simple_gradient_algorithm(399, starting_point_global, step_size, function)
        for j in range(len(values)):
            values_plot[j] = values_plot[j] + values[j]
    for i in range(len(values_plot)):
        values_plot[i] = values_plot[i] / n
    # plt.plot(indexes[:final_iteration+1], values_plot[:final_iteration+1])
    # plt.title("Average value of a function for iteration for 100 runs")
    # plt.yscale("log")
    # plt.xlabel("iteration")
    # plt.ylabel("value of function")
    # plt.show()
    
    return values_plot[:final_iteration+1], indexes[:final_iteration+1]
    

def plotter_for_various_step_sizes(function, step_sizes):
    plt.title("Average value of a function for iteration for 100 runs")
    plt.yscale("log")
    plt.xlabel("iteration")
    plt.ylabel("value of function")
    for i in step_sizes:
        print(i)
        values, indexes = checking_specific_step_size(function, i)
        plt.plot(indexes, values, label=str(i))
    plt.legend(title="step size")
    plt.show()


if __name__ == "__main__":
    
    # find_best_step_size(matyas_function)

    # starting_point_global = (random.uniform(-10, 10), random.uniform(-10, 10))
    starting_point_global = (9, 8)
    points, _, _ = simple_gradient_algorithm(399, starting_point_global, 1.5, matyas_function)
    visualize_fun(function_1, points)
    # plotter_for_various_step_sizes(function_1, [0.01, 0.25, 0.5, 1])
    # checking_specific_step_size(matyas_function, 0.7)