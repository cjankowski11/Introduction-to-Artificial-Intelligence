import math


class ID3TREE:
    def __init__(self, training_data, depth):
        self.results = set(training_data["result"].tolist())
        signs = set()
        for col in training_data.columns:
            if col != "result":
                signs.update(training_data[col].tolist())
        dividers = training_data.columns.tolist()[:-1]
        self.root = Node(training_data, None, depth, dividers, None, signs, self.results)
        self.create_recursion(self.root)

    def create_recursion(self, node):
        if not node.isleaf():
            node.find_best_divider()
            node.create_children()
            for child in node.children:
                self.create_recursion(child)

    def test_result(self, individual):
        if self.root.isleaf():
            return self.root.result
        value = individual[self.root.question]
        for child in self.root.children:
            if child.answer == value:
                return child.test_result(individual)
        print("nie znaleziono dziecka") #do debugowania
        return -1  # nie znaleziono drogi
    
    def get_possible_results(self):     # do liczenia macierzy pomyłek
        return self.results

    
class Node:

    def __init__(self, collection, answer, depth, dividers, parent_result, signs, results):
        self.collection = collection
        self.question = None
        self.answer = answer
        self.children = []
        self.depth = depth
        self.possible_dividers = dividers
        self.signs = signs
        self.results = results
        
        if self.isleaf(): 
            if len(self.collection) > 0:
                self.result = self.collection["result"].iloc[0]
            else:
                self.result = parent_result
        else:
            self.result = self.calculate_most_frequent_result()

    def isleaf(self):
        return self.collection["result"].is_unique or self.depth == 0 or len(self.possible_dividers) == 0
                # zalatwia tez warunek kiedy collection jest puste
    def calculate_entrophy(self, data):
        entrophy = 0
        results_e = data["result"]
        data_size = len(results_e)
        if data_size > 0:
            counts = results_e.value_counts()
            for result_count in counts:
                result_probability = result_count/data_size
                entrophy -= result_probability*math.log(result_probability, len(self.results))
        return entrophy
    
    def find_best_divider(self):
        own_entrophy = self.calculate_entrophy(self.collection)
        best_divider = self.possible_dividers[0]
        best_information_gain = -1
        for divider in self.possible_dividers:
            divider_entrophy = 0
            for sign in self.signs:
                filtered_data = self.collection[self.collection[divider] == sign]
                posibility_of_sign = len(filtered_data)/len(self.collection)
                sign_entropy = self.calculate_entrophy(filtered_data)
                divider_entrophy += posibility_of_sign*sign_entropy
            information_gain = own_entrophy - divider_entrophy
            if information_gain > best_information_gain:
                best_information_gain = information_gain
                best_divider = divider
        self.question = best_divider
        return best_divider

    def calculate_most_frequent_result(self):
        counts = self.collection["result"].value_counts()
        most_frequent = counts.idxmax()
        return most_frequent
    
    def create_children(self):
        child_dividers = self.possible_dividers.copy()
        child_dividers.remove(self.question)
        for sign in self.signs:
            filtered_data = self.collection[self.collection[self.question] == sign]  # wiersze z poszczegolnym znakiem "x","b","o"
            self.children.append(Node(filtered_data, sign, self.depth - 1,
                                      child_dividers, self.result,self.signs,self.results))

    
    def test_result(self, individual):
        if self.isleaf():
            return self.result
        value = individual[self.question]
        for child in self.children:
            if child.answer == value:
                return child.test_result(individual)
        print("nie znaleziono dziecka") #do debugowania
        return -1  # nie znaleziono drogi