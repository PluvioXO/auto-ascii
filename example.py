import os
from PIL import Image
from auto_ascii import image_to_ascii

def create_sample_image(path):
    """Creates a simple test image if you don't have one handy."""
    # Create a simple gradient image to show different ASCII characters
    img = Image.new('L', (100, 100))
    pixels = img.load()
    for i in range(img.width):
        for j in range(img.height):
            # Gradient pattern
            pixels[i, j] = int((i + j) / 200 * 255)
    img.save(path)

def main():
    sample_path = "sample_test_image.jpg"
    
    print("Creating sample image...")
    create_sample_image(sample_path)
    
    print("Converting image to ASCII art (Standard)...\n")
    # Convert it!
    ascii_art = image_to_ascii(sample_path, new_width=60, char_set="standard")
    print(ascii_art)
    
    print("Converting image to ASCII art (Blocks)...\n")
    # Convert it with Blocks!
    ascii_art_blocks = image_to_ascii(sample_path, new_width=60, char_set="blocks")
    print(ascii_art_blocks)
    
    print("Converting image to ASCII art (Binary)...\n")
    # Convert it with Binary!
    ascii_art_binary = image_to_ascii(sample_path, new_width=60, char_set="binary")
    print(ascii_art_binary)
    
    # Cleanup
    if os.path.exists(sample_path):
        os.remove(sample_path)
        print("\nCleaned up sample image.")

if __name__ == "__main__":
    main()
