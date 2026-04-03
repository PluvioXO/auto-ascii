import argparse
import sys
import os
from .converter import image_to_ascii, ascii_to_image_obj
from .video import video_to_ascii
from .presets import ASCII_PRESETS

def main():
    parser = argparse.ArgumentParser(description="Convert an image or video to ASCII art.")
    parser.add_argument("input_path", help="Path to the input image or video")
    parser.add_argument("-w", "--width", type=int, default=None, help="Width of the output ASCII art (if omitted, keeps original)")
    parser.add_argument("-H", "--height", type=int, default=None, help="Height of the output ASCII art (if omitted, keeps original aspect)")
    parser.add_argument("-c", "--charset", type=str, default="standard", 
                        choices=list(ASCII_PRESETS.keys()),
                        help="CharacterSet preset to use (default: standard)")
    parser.add_argument("--video", action="store_true", help="Process the input as a video")
    parser.add_argument("--fps", type=int, default=None, help="Framerate cap for output playback/file")
    parser.add_argument("-o", "--out", type=str, default=None, help="Output file path (.txt, .png/.jpg, or .mp4) to save instead of print")
    
    args = parser.parse_args()
    
    if args.video:
        video_to_ascii(args.input_path, args.width, args.height, args.charset, args.fps, args.out)
    else:
        ascii_art = image_to_ascii(args.input_path, args.width, args.height, args.charset)
        if ascii_art:
            if args.out:
                ext = os.path.splitext(args.out)[1].lower()
                if ext in ['.txt', '.log']:
                    with open(args.out, "w", encoding="utf-8") as f:
                        f.write(ascii_art)
                    print(f"Saved text to {args.out}")
                elif ext in ['.png', '.jpg', '.jpeg']:
                    img = ascii_to_image_obj(ascii_art)
                    img.save(args.out)
                    print(f"Saved image to {args.out}")
                else:
                    print(f"Unsupported image output extension {ext}")
            else:
                print(ascii_art)
        else:
            sys.exit(1)

if __name__ == "__main__":
    main()
