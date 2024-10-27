import cv2
import time
import datetime

# Desired settings
# desired_width = 3840   # 4K width
# desired_height = 2160  # 4K height
desired_width = 1920   
desired_height = 1080  
desired_fps = 60       # Target FPS

# Open a connection to the first available camera (0 is typically the default camera)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Use CAP_DSHOW backend on Windows

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

# Attempt to set custom resolution and frame rate
cap.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)
cap.set(cv2.CAP_PROP_FPS, desired_fps)

# Get the actual resolutions and frame rate after setting
actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
actual_fps = cap.get(cv2.CAP_PROP_FPS)

print(f"Requested resolution: {desired_width}x{desired_height} at {desired_fps} fps")
print(f"Actual resolution: {actual_width}x{actual_height} at {actual_fps:.2f} fps")

# For calculating frame rate
prev_frame_time = 0
new_frame_time = 0

while True:
    # Read a frame from the camera
    ret, frame = cap.read()
    
    # Check if the frame was read correctly
    if not ret:
        print("Error: Could not read frame.")
        break
    
    # Calculate frame rate
    new_frame_time = time.time()
    fps = 1 / (new_frame_time - prev_frame_time) if prev_frame_time else 0
    prev_frame_time = new_frame_time
    fps_text = f'FPS: {fps:.2f}'
    
    # Get current time
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Add metadata text to the frame
    resolution_text = f'Resolution: {actual_width}x{actual_height}'
    metadata_text = f'{fps_text} | {resolution_text} | Time: {current_time}'
    cv2.putText(frame, metadata_text, (10, frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    # Display the frame in a window named 'Camera Feed'
    cv2.imshow('Camera Feed', frame)
    
    # Press 'q' to exit the loop and close the window
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close any open windows
cap.release()
cv2.destroyAllWindows()
