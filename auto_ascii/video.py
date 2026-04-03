import sys
import time
try:
    import cv2
except ImportError:
    cv2 = None
from PIL import Image

from .converter import image_obj_to_ascii, ascii_to_image_obj

def video_to_ascii(video_path, new_width=None, new_height=None, char_set="standard", max_fps=None, out_path=None):
    """
    Plays a video in the terminal as ASCII art or saves it to an output file.
    Requires opencv-python to be installed.
    """
    if cv2 is None:
        print("Error: opencv-python is not installed. Please install it using `pip install opencv-python` to use video support.")
        return

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error opening video file {video_path}")
        return

    # Determine FPS
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    fps = video_fps if video_fps > 0 else 30
    if max_fps is not None and max_fps > 0:
        fps = min(fps, max_fps)
        
    frame_delay = 1.0 / fps

    out_video = None
    if out_path:
        # Get frame sample to figure out size
        ret, frame = cap.read()
        if not ret:
            print("Cannot read video frames.")
            return
            
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_frame)
        ascii_frame = image_obj_to_ascii(pil_image, new_width=new_width, new_height=new_height, char_set=char_set)
        img_rendered = ascii_to_image_obj(ascii_frame)
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out_video = cv2.VideoWriter(out_path, fourcc, fps, (img_rendered.width, img_rendered.height))
        # Reset position
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    else:
        # Clear terminal screen
        sys.stdout.write('\033[2J')
        sys.stdout.flush()

    try:
        while cap.isOpened():
            start_time = time.time()
            ret, frame = cap.read()
            if not ret:
                break
            
            # Convert BGR to RGB then to PIL Image
            idx = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb_frame)
            
            # Convert to ASCII
            ascii_frame = image_obj_to_ascii(pil_image, new_width=new_width, new_height=new_height, char_set=char_set)
            
            if out_video:
                # Output to video file by rendering ASCII strings
                rendered = ascii_to_image_obj(ascii_frame)
                out_video.write(cv2.cvtColor(np.array(rendered), cv2.COLOR_RGB2BGR))
                print(f"\rProcessed frame {idx}", end="")
            else:
                # Move cursor top-left
                sys.stdout.write('\033[H')
                sys.stdout.write(ascii_frame)
                sys.stdout.flush()
                
                # Wait to maintain FPS
                elapsed_time = time.time() - start_time
                time_to_wait = frame_delay - elapsed_time
                if time_to_wait > 0:
                    time.sleep(time_to_wait)
    except KeyboardInterrupt:
        print("\nVideo playback interrupted by user.")
    finally:
        cap.release()
        if out_video:
            out_video.release()
            print("\nSaved video:", out_path)
