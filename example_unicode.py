import os
from PIL import Image
from auto_ascii import image_to_ascii

def create_sample_image(path):
    img = Image.new('L', (100, 100))
    pixels = img.load()
    for i in range(img.width):
        for j in range(img.height):
            pixels[i, j] = int((i + j) / 200 * 255)
    img.save(path)

def main():
    sample_path = "sample_test_image.jpg"
    create_sample_image(sample_path)
    
    print("Testing Japanese Kanji...")
    print(image_to_ascii(sample_path, new_width=60, char_set="japanese_kanji"))
    
    print("Testing Chinese...")
    print(image_to_ascii(sample_path, new_width=60, char_set="chinese"))
    
    print("Testing Cyrillic...")
    print(image_to_ascii(sample_path, new_width=60, char_set="cyrillic"))

    if os.path.exists(sample_path):
        os.remove(sample_path)

if __name__ == "__main__":
    main()
