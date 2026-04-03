import unittest
from PIL import Image
import os

from auto_ascii.converter import resize_image, grayify, pixels_to_ascii, image_to_ascii

class TestConverter(unittest.TestCase):
    def setUp(self):
        # Create a tiny 10x10 dummy image for testing
        self.image = Image.new('RGB', (10, 10), color='white')

    def test_resize_image(self):
        resized = resize_image(self.image, new_width=5)
        self.assertEqual(resized.width, 5)
        
        # original ratio is 1 (10/10) * 0.55 = 0.55
        # new_height = int(5 * 0.55) = int(2.75) = 2
        self.assertEqual(resized.height, 2)

    def test_grayify(self):
        gray = grayify(self.image)
        self.assertEqual(gray.mode, 'L')

    def test_pixels_to_ascii(self):
        gray = grayify(self.image)
        ascii_chars = pixels_to_ascii(gray)
        
        # Original dummy is 10x10, so 100 pixels
        self.assertEqual(len(ascii_chars), 100)
        self.assertIsInstance(ascii_chars, str)

        # White pixels (255) should map to the lightest ASCII character (e.g. " " or ".")
        # Let's just make sure it's valid
        self.assertTrue(len(ascii_chars) > 0)

    def test_image_to_ascii(self):
        # We need to save a temporary image to test the full pipeline
        test_path = "test_temp_img.jpg"
        self.image.save(test_path)
        
        ascii_art = image_to_ascii(test_path, new_width=10)
        self.assertIsInstance(ascii_art, str)
        self.assertTrue(len(ascii_art) > 0)
        
        # Cleanup
        if os.path.exists(test_path):
            os.remove(test_path)
            
    def test_image_to_ascii_invalid_path(self):
        ascii_art = image_to_ascii("non_existent_image.png")
        self.assertEqual(ascii_art, "")

if __name__ == '__main__':
    unittest.main()
