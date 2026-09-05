from PIL import Image, ImageDraw, ImageFont, ImageOps
import numpy as np
import imageio
import sys
import os

# Sparse to dense — light pixels = spaces, dark pixels = dense chars
ASCII_CHARS = " .:=+*#%@"

def image_to_ascii_lines(img, width=60):
    if img.mode == 'RGBA':
        # White background composite — logo is dark on white
        bg = Image.new('RGB', img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[3])
        img = bg
    else:
        img = img.convert('RGB')

    aspect = img.height / img.width
    height = int(width * aspect * 0.45)  # correct for monospace char ratio
    img = img.resize((width, height), Image.LANCZOS)

    gray = img.convert('L')
    # Invert: dark logo areas → dense chars, white bg → spaces
    gray = ImageOps.invert(gray)

    pixels = np.array(gray)
    lines = []
    for row in pixels:
        line = ''.join(ASCII_CHARS[int(p * (len(ASCII_CHARS) - 1) / 255)] for p in row)
        lines.append(line)
    return lines

def ascii_lines_to_frame(lines, char_size=10, reveal_rows=None):
    cols = max(len(l) for l in lines)
    rows = len(lines)
    fw = cols * char_size + 20
    fh = rows * char_size + 20
    frame = Image.new('RGB', (fw, fh), (13, 17, 23))
    draw = ImageDraw.Draw(frame)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", char_size)
    except:
        font = ImageFont.load_default()

    show_rows = reveal_rows if reveal_rows is not None else rows
    for i, line in enumerate(lines[:show_rows]):
        for j, ch in enumerate(line):
            if ch != ' ':
                # Density-based color: sparse = dim purple, dense = bright white
                density = ASCII_CHARS.index(ch) / (len(ASCII_CHARS) - 1)
                r = int(80 + (255 - 80) * density)
                g = int(40 + (255 - 40) * density)
                b = int(200 + (55) * density)
                draw.text((10 + j * char_size, 10 + i * char_size), ch, fill=(r, g, b), font=font)
    return frame

def generate(image_path, output_path="assets/ascii_logo.gif"):
    img = Image.open(image_path)
    lines = image_to_ascii_lines(img, width=60)
    rows = len(lines)

    frames = []
    # Scanline reveal: top to bottom
    for i in range(rows):
        frame = ascii_lines_to_frame(lines, char_size=10, reveal_rows=i + 1)
        frames.append(np.array(frame))

    # Hold full frame at end
    for _ in range(20):
        frames.append(frames[-1])

    durations = [0.07] * rows + [0.1] * 20
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    imageio.mimsave(output_path, frames, duration=durations, loop=0)
    print(f"Saved: {output_path} ({os.path.getsize(output_path) / 1024:.1f} KB)")

if __name__ == "__main__":
    image_path = sys.argv[1] if len(sys.argv) > 1 else "assets/logo_SUB.png"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "assets/ascii_logo.gif"
    generate(image_path, output_path)
