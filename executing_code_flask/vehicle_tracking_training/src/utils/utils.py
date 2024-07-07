import cv2 
import numpy as np

def skeletonize(image):
  """
  Performs skeletonization on a binary image.

  Args:
      image: The binary image to be skeletonized.

  Returns:
      A binary image representing the skeleton of the input image.
  """

  # Convert image to binary format (black and white)
  thresh, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

  # Define structuring element for erosion and dilation
  element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))

  # Initialize variables for loop
  done = False
  skeleton = np.zeros(image.shape, np.uint8)  # Create empty image for skeleton

  while not done:
    # Erode the image (thinning boundaries)
    eroded = cv2.erode(image, element)

    # Dilate the eroded image (thickening)
    temp = cv2.dilate(eroded, element)

    # Subtract the dilated image from the original to get skeleton parts
    temp = cv2.subtract(image, temp)

    # Update the skeleton with the extracted parts
    skeleton = cv2.bitwise_or(skeleton, temp)

    # Update the image for next iteration
    image = eroded.copy()

    # Check if there are no foreground pixels left
    total_pixels = image.size  # Total number of pixels of image
    foreground_pixels = cv2.countNonZero(image)
    if foreground_pixels == 0:
      done = True

  # Return the final skeleton image
  return skeleton
