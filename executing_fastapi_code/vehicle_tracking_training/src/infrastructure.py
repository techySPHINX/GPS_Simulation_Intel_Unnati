import cv2
import numpy as np

# Define colors
DIVIDER_COLOUR = (0, 0, 0)
BOUNDING_BOX_COLOUR = (0, 255, 0)  # Green
CENTROID_COLOUR = (255, 0, 0)  # Blue
CAR_COLOURS = [(0, 255, 255)]  # Yellow


def detect_vehicles(frame, background_model):
    """
    Detects vehicles in a frame using background subtraction.

    Args:
        frame: The current frame as a NumPy array.
        background_model: The background model used for subtraction.

    Returns:
        A list of bounding boxes for detected vehicles.
    """
    foreground_mask = cv2.subtract(frame, background_model)
    _, contours, _ = cv2.findContours(
        foreground_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    bounding_boxes = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        bounding_boxes.append((x, y, w, h))
    return bounding_boxes


def draw_boxes(frame, bounding_boxes):
    """
    Draws bounding boxes around detected vehicles on the frame.

    Args:
        frame: The current frame as a NumPy array.
        bounding_boxes: A list of bounding boxes for detected vehicles.
    """
    for x, y, w, h in bounding_boxes:
        cv2.rectangle(frame, (x, y), (x + w, y + h), BOUNDING_BOX_COLOUR, 2)


def count_vehicles(bounding_boxes, exit_line):
    """
    Counts vehicles that have crossed the exit line.

    Args:
        bounding_boxes: A list of bounding boxes for detected vehicles.
        exit_line: A horizontal line representing the exit point.

    Returns:
        The number of vehicles that have crossed the exit line.
    """
    vehicle_count = 0
    for x, y, w, h in bounding_boxes:
        centroid_y = y + h // 2
        if centroid_y > exit_line:
            vehicle_count += 1
    return vehicle_count


def main():

    background_model = cv2.imread("background.png")
    exit_line = 200

    cap = cv2.VideoCapture("video.mp4")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Detect vehicles
        bounding_boxes = detect_vehicles(frame, background_model)

        # Draw bounding boxes
        draw_boxes(frame, bounding_boxes)

        # Count vehicles
        vehicle_count = count_vehicles(bounding_boxes, exit_line)
        print(f"Vehicle count: {vehicle_count}")

        # Display frame
        cv2.imshow("Vehicle Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
