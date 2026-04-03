import os
try:
    import cv2
    import numpy as np
except ImportError:
    cv2 = None
    np = None

from auto_ascii.video import video_to_ascii

def create_sample_video(path, width=320, height=240, fps=30, duration_sec=3):
    """Creates a simple test video with a moving bouncing circle."""
    if cv2 is None or np is None:
        print("Error: opencv-python and numpy are required to generate the sample video.")
        return False

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(path, fourcc, fps, (width, height))
    
    total_frames = fps * duration_sec
    for i in range(total_frames):
        # Create a black background
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Add a subtle animated gradient background
        bg_intensity = int((np.sin(i * 0.05) + 1) * 60)
        frame[:] = (bg_intensity, bg_intensity, bg_intensity)
        
        # Calculate circle position (moving left to right, bouncing up and down)
        x = int(width * (i / total_frames))
        y = int(height / 2 + np.sin(i * 0.3) * (height / 3))
        
        # Draw the circle (white)
        cv2.circle(frame, (x, y), 40, (255, 255, 255), -1)
        
        out.write(frame)
        
    out.release()
    return True

def main():
    sample_path = "sample_test_video.mp4"
    
    print("Creating a 3-second sample video using OpenCV... (this might take a moment)")
    success = create_sample_video(sample_path)
    
    if not success:
        return

    print("\nPlaying video in terminal as ASCII art in 3 seconds! (Press Ctrl+C to stop early)")
    # Optional delay to let the user read the message
    import time
    time.sleep(3)
    
    # Play the video in terminal!
    try:
        video_to_ascii(sample_path, new_width=60, char_set="blocks", max_fps=15)
    except KeyboardInterrupt:
        pass
    
    # Cleanup
    if os.path.exists(sample_path):
        os.remove(sample_path)
        print("\nCleaned up sample video.")

if __name__ == "__main__":
    main()
