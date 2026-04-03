<h1 align="center"> auto-ascii </h1>

<p align="center">
  <b>A powerful, flexible, and easy-to-use Python package that converts images and videos into customizable ASCII art!</b>
</p>

## ✨ Features
- **Images and Videos:** Convert static images or entire videos to ASCII art.
- **Terminal Playback:** Watch videos in real-time as an ASCII stream within your terminal.
- **Over 100 Presets:** Choose from numerous languages and visual representations. From traditional `standard` ASCII, block characters, Braille, Japanese, Chinese, Cyrillic, or Emojis.
- **Exporting Options:** Dump ASCII directly into `.txt`, auto-upscale results directly to `.png`/`.jpg`, or render an `.mp4` video out of ASCII frames.
- **Aspect Ratio & Resolution Keeping:** Keep the original picture aspect ratio or output native resolution text mappings up to 4K parity images explicitly.

## Installation

Install directly via `pip`:

```bash
pip install auto-ascii
```

## Quick Start

### CLI Usage

```bash
# Convert an image and output to terminal
auto-ascii test_image.jpg -w 120

# Convert an image using Japanese Kanji and save as a high-res PNG image
auto-ascii input.jpg -c japanese_kanji -o ascii_art.png

# Play a video in the terminal as ASCII blocks with a 30 FPS cap
auto-ascii input.mp4 --video --fps 30 -c blocks

# Render an entire video into an ASCII MP4 output natively
auto-ascii input.mp4 --video -o output_ascii.mp4
```

*Note: You can view all available charsets by running `auto-ascii --help`.*

### Python API Usage

Use `auto-ascii` directly in your Python code:

```python
from auto_ascii import image_to_ascii, video_to_ascii

# Convert image to a raw ASCII string
ascii_art = image_to_ascii("image.jpg", new_width=100, char_set="emoji_faces")
print(ascii_art)

# Playback a video in the terminal (runs synchronously until finished)
video_to_ascii("video.mp4", new_width=80, char_set="braille")

# Output ASCII text back into an image programmatically
from auto_ascii.converter import ascii_to_image_obj
img = ascii_to_image_obj(ascii_art)
img.show()
```

## License
MIT License
