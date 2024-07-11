# KNN Classifier

import csv
import random
from math import sqrt


def euclid_distance(point1, point2):
    """

    Args:
        point1: A list of coordinates representing the first point.
        point2: A list of coordinates representing the second point.

    Returns:
        The Euclidean distance between the two points.
    """
    distance = 0
    for i in range(len(point1)):
        distance += (point1[i] - point2[i])**2
    return sqrt(distance)


def k_nearest_neighbors(training_data, test_instance, k):

    distances = []
    for point in training_data:
        distance = euclid_distance(test_instance[:-1], point[:-1])
        distances.append((point, distance))
    distances.sort(key=lambda x: x[1])
    return distances[:k]


def majority_vote(neighbors):
    """Determines the most frequent class label among the k nearest neighbors.

    Args:
        neighbors: A list of k nearest neighbors, where each neighbor is a list
                   representing a data point with features and class label.
    """
    class_counts = {}
    for neighbor in neighbors:
        class_label = neighbor[-1]
        class_counts[class_label] = class_counts.get(class_label, 0) + 1
    return max(class_counts, key=class_counts.get)


def load_data(filename, data):
    """
     Args:
         filename: The path to the CSV file.
         data: An empty list to store the loaded data.
     """
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:

            data.append([float(x) for x in row])


def classify(training_data, test_data, k):
    """Classifies a test instance using k-Nearest Neighbors.

    Args:
        training_data: A list of lists representing the training data.
        test_data: A list representing the features of the test instance.
        k: The number of nearest neighbors to use.

    Returns:
        The predicted class label for the test instance.
    """
    neighbors = k_nearest_neighbors(training_data, test_data, k)
    predicted_class = majority_vote(neighbors)
    return predicted_class


training_file = "training.data"
test_file = "test.data"
k = 3

training_data = []
test_data = []
load_data(training_file, training_data)
load_data(test_file, test_data)

predicted_class = classify(training_data, test_data[0], k)
print("Predicted class for first test instance:", predicted_class)
