from PIL import Image
from .presets import ASCII_PRESETS

def resize_image(image, new_width=None, new_height=None, maintain_aspect_ratio=True):
    """Resizes an image. If new_width and new_height are None, original size is kept."""
    width, height = image.size
    
    if new_width is None and new_height is None:
        # Keep original resolution
        return image
        
    if new_width is not None and new_height is None:
        if maintain_aspect_ratio:
            ratio = height / width * 0.55 
            new_height = max(1, int(new_width * ratio))
        else:
            new_height = height
    elif new_height is not None and new_width is None:
        if maintain_aspect_ratio:
            ratio = width / height / 0.55
            new_width = max(1, int(new_height * ratio))
        else:
            new_width = width
            
    return image.resize((new_width, new_height))

def grayify(image):
    """Converts an image to grayscale."""
    return image.convert("L")

def pixels_to_ascii(image, char_set="standard"):
    """Maps grayscale pixel values to ASCII characters."""
    chars = ASCII_PRESETS.get(char_set, ASCII_PRESETS["standard"])
    pixels = image.getdata()
    # pixel_value * len(chars) // 256
    characters = "".join([chars[pixel * len(chars) // 256] for pixel in pixels])
    return characters

def image_obj_to_ascii(image, new_width=None, new_height=None, char_set="standard"):
    """Converts a loaded PIL Image into an ASCII art string."""
    image = resize_image(image, new_width, new_height)
    image = grayify(image)
    ascii_str = pixels_to_ascii(image, char_set)
    
    # Format the string with line breaks
    img_width = image.width
    ascii_str_len = len(ascii_str)
    ascii_img = ""
    for i in range(0, ascii_str_len, img_width):
        ascii_img += ascii_str[i:i+img_width] + "\n"
        
    return ascii_img

def image_to_ascii(image_path, new_width=None, new_height=None, char_set="standard"):
    """Converts the image at `image_path` to an ASCII art string."""
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"Unable to open image file {image_path}: {e}")
        return ""
    
    return image_obj_to_ascii(image, new_width, new_height, char_set)

def ascii_to_image_obj(ascii_str, char_width=10, char_height=20, bg_color="black", fg_color="white"):
    """Renders an ASCII text block back into a PIL Image, effectively upscaling it."""
    from PIL import ImageDraw, ImageFont
    
    lines = ascii_str.splitlines()
    if not lines:
        return Image.new("RGB", (1, 1), color=bg_color)
        
    img_width = len(lines[0]) * char_width
    img_height = len(lines) * char_height
    
    img = Image.new("RGB", (img_width, img_height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    try:
        # Load a default monospaced font if possible, else standard internal
        font = ImageFont.load_default()
    except:
        font = None
        
    y_text = 0
    for line in lines:
        if font:
            draw.text((0, y_text), line, font=font, fill=fg_color)
        else:
            draw.text((0, y_text), line, fill=fg_color)
        y_text += char_height
        
    return img
