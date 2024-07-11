import numpy as np
import cv2 
import os

def calc_color_hist(image):
    # Calculates color histogram for a given image.

    # Args:
    #     image: The image to analyze.

    # Returns:
    #     A list containing the BGR histograms.
    
    chans = cv2.split(image)
    hists = []
    for chan in chans:
        hist = cv2.calcHist([chan], [0], None, [256], [0, 256])
        hists.append(hist.flatten()) 
    return hists

def get_peak_color(hist):
    # Finds the peak intensity value in a histogram.

    # Args:
    #     hist: The histogram to analyze.

    # Returns:
    #     The index of the peak intensity value.
    
    return np.argmax(hist)

def save_test_features(image, filename="test.data"):
    # Calculates and saves color histogram features of a test image.

    # Args:
    #     image: The test image.
    #     filename: The filename to save the features .
    
    hists = calc_color_hist(image)
    peak_colors = [get_peak_color(h) for h in hists]
    features = ",".join(map(str, peak_colors))

    with open(filename, "w") as f:
        f.write(features)

def save_training_features(image, color_label, filename="training.data"):
   
    hists = calc_color_hist(image)
    peak_colors = [get_peak_color(h) for h in hists]
    features = ",".join(map(str, peak_colors))

    with open(filename, "a") as f:
        f.write(features + "," + color_label + "\n")

def train_color_classifier(training_dir):
    # Trains a color classifier using color histograms of training images.

    # Args:
    #     training_dir: The directory containing subdirectories of training images
    #                    labeled by color (e.g., "red", "yellow").
    
    for color in os.listdir(training_dir):
        color_path = os.path.join(training_dir, color)
        for image_file in os.listdir(color_path):
            image_path = os.path.join(color_path, image_file)
            save_training_features(cv2.imread(image_path), color)


train_color_classifier("training_dataset")

def predict_color(test_image):
    # Predicts the color of a test image based on the trained classifier.

    # This function assumes a trained color classifier using the `train_color_classifier` function.

    # Args:
    #     test_image: The image to predict the color for.

    # Returns:
    #     The predicted color label (e.g., "red", "yellow").
    
    print("Color prediction logic (kNN, etc.) not implemented yet. ")
    return None

test_image = cv2.imread("test.jpg")
predicted_color = predict_color(test_image)
if predicted_color:
    print("Predicted color:", predicted_color)


