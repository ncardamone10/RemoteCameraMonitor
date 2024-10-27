import cv2
import numpy as np

def main():
    # Initialize the video capture object
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Use CAP_DSHOW backend for Windows

    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return

    # Create background subtractor with adjusted parameters
    back_sub = cv2.createBackgroundSubtractorMOG2(history=200, varThreshold=25, detectShadows=False)

    # Allow the camera to warm up and the background model to initialize
    for i in range(30):
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            return
        back_sub.apply(frame)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # Apply background subtractor to get the foreground mask
        fg_mask = back_sub.apply(frame)

        # Remove noise and fill in holes using morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel, iterations=1)
        fg_mask = cv2.dilate(fg_mask, kernel, iterations=2)

        # Find contours in the foreground mask
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            # Adjusted contour area threshold for smaller objects
            if cv2.contourArea(contour) < 100:  # Lowered from 500 to 100
                continue
            x, y, w, h = cv2.boundingRect(contour)
            # Draw a green rectangle around the detected object
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display the result
        cv2.imshow('Motion Detection', frame)
        # cv2.imshow('Foreground Mask', fg_mask)  # Uncomment to see the foreground mask

        # Exit when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
