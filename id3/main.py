import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
from id3tree import ID3TREE


def import_data_pandas(file_name):
    data = pd.read_csv(file_name)
    # data = data.sample(frac=1).reset_index(drop=True)
    return data


def split_data(data, a, b):
    train_data, temp_data = train_test_split(data, test_size=0.01 * a, shuffle=True, random_state=None)
    validation_data, test_data = train_test_split(temp_data, test_size=0.01 * b, shuffle=True, random_state=None)
    return train_data, validation_data, test_data


def validate_tree(training_data, validation_data, depths_to_test):
    best_depth = None
    biggest_prob_of_correct = -1
    prob_of_depths = []
    for depth in depths_to_test:
        prob = test_tree(training_data, validation_data, depth)[0]
        # print(prob, depth)
        prob_of_depths.append(prob)
        if prob > biggest_prob_of_correct:
            best_depth = depth
            biggest_prob_of_correct = prob
    # print(biggest_prob_of_correct)
    return best_depth, prob_of_depths


def test_tree(training_data, test_data, depth):
    tree = ID3TREE(training_data, depth)
    results = tree.get_possible_results()
    correct_result = 0
    true_results = {}
    false_results = {}
    
    for r in results:
        true_results[r] = 0
        false_results[r] = 0
    for id_test in range(len(test_data)):
        test = test_data.iloc[id_test]
        result = tree.test_result(test)
        if result == test["result"]:
            correct_result += 1
            true_results[test["result"]] += 1
        else:
            false_results[test["result"]] += 1
    # print(f"prawidlowe: {true_results}")
    # print(f"falszywe: {false_results}")
    return correct_result/len(test_data), true_results, false_results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file")
    args = parser.parse_args()
    data = import_data_pandas(args.data_file)
    # for i in range(19,0,-1):
    #     print(i)
    #     results = []
    #     train_data, validate_data, test_data = split_data(data)
    depths = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    for depth in depths:
        train, validate, test = split_data(data, 30, 50)
        tree = ID3TREE(train, depth)
        print(test_tree(tree))




            
            
