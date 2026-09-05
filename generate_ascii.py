from PIL import Image
import sys
import os

# ASCII characters from dense to sparse
ASCII_CHARS = "@%#*+=-:. "

def resize_image(image, new_width=100):
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(new_width * aspect_ratio * 0.55)  # 0.55 corrects for font aspect ratio
    return image.resize((new_width, new_height))

def to_grayscale(image):
    return image.convert("L")

def pixels_to_ascii(image):
    pixels = image.getdata()
    chars = "".join([ASCII_CHARS[pixel * len(ASCII_CHARS) // 256] for pixel in pixels])
    return chars

def convert(image_path, output_path="assets/ascii.txt", width=100):
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"Error opening image: {e}")
        sys.exit(1)

    image = resize_image(image, width)
    image = to_grayscale(image)
    ascii_str = pixels_to_ascii(image)

    img_width = image.width
    ascii_lines = [ascii_str[i:i+img_width] for i in range(0, len(ascii_str), img_width)]
    ascii_art = "\n".join(ascii_lines)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        f.write(ascii_art)

    print(f"ASCII art saved to {output_path}")
    return ascii_art

if __name__ == "__main__":
    image_path = sys.argv[1] if len(sys.argv) > 1 else "assets/logo_SUB.png"
    convert(image_path)
