import cv2
import numpy as np
import skvideo.io


# Define video source and frame size
VIDEO_SOURCE = "bradley_input.mp4"
SHAPE = (352, 640)  # Height, Width

# Define exit regions (modify these points for your video)
EXIT_PTS = np.array([
    [[120, 100], [380, 0], [510, 0], [385, 150]],
])


def train_bg_subtractor(bg_subtractor, cap, num_frames=2400):
    """
    Trains the background subtractor using video frames.

    Args:
        bg_subtractor: Background subtractor object.
        cap: Video capture object.
        num_frames: Number of frames to use for training (default: 2400).

    Returns:
        The video capture object.
    """
    print("Training background subtractor...")
    for _ in range(num_frames):
        _, frame = cap.read()
        bg_subtractor.apply(frame)
    return cap


def main():
    # Create background subtractor
    bg_subtractor = cv2.createBackgroundSubtractorMOG2()

    # Open video capture
    cap = skvideo.io.vreader(VIDEO_SOURCE)
    cap = train_bg_subtractor(bg_subtractor, cap)  # Train before processing

    for frame in cap:
        if not frame.any():
            print("Frame capture failed, stopping...")
            break

        # Perform background subtraction (using the trained bg_subtractor)
        foreground_mask = bg_subtractor.apply(frame)

        # Implement your vehicle detection and counting logic here (using foreground_mask)
        # You can use techniques like contour analysis or pre-trained models.

        # (Optional) Display the frame with foreground mask (for debugging)
        # cv2.imshow("Foreground Mask", foreground_mask)
        # cv2.waitKey(1)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
