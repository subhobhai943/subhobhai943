from PIL import Image, ImageDraw, ImageFont
import numpy as np
import imageio
import sys
import os

ASCII_CHARS = "@%#*+=-:. "

def image_to_ascii_lines(img, width=55):
    if img.mode == 'RGBA':
        bg = Image.new('RGB', img.size, (13, 17, 23))
        bg.paste(img, mask=img.split()[3])
        img = bg
    else:
        img = img.convert('RGB')
    aspect = img.height / img.width
    height = int(width * aspect * 0.5)
    img = img.resize((width, height))
    gray = img.convert('L')
    pixels = np.array(gray)
    lines = []
    for row in pixels:
        line = ''.join(ASCII_CHARS[int(p * (len(ASCII_CHARS)-1) / 255)] for p in row)
        lines.append(line)
    return lines

def ascii_lines_to_frame(lines, char_size=9, reveal_rows=None):
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
                brightness = ASCII_CHARS.index(ch) / (len(ASCII_CHARS) - 1)
                r = int(169 + (255-169) * brightness)
                g = int(96 + (255-96) * brightness)
                b = 255
                draw.text((10 + j*char_size, 10 + i*char_size), ch, fill=(r,g,b), font=font)
    return frame

def generate(image_path, output_path="assets/ascii_logo.gif"):
    img = Image.open(image_path)
    lines = image_to_ascii_lines(img, width=55)
    rows = len(lines)
    frames = []
    for i in range(rows + 8):
        reveal = min(i + 1, rows)
        frame = ascii_lines_to_frame(lines, char_size=9, reveal_rows=reveal)
        frames.append(np.array(frame))
    frames += [frames[-1]] * 15
    durations = [0.06] * (rows + 8) + [0.1] * 15
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    imageio.mimsave(output_path, frames, duration=durations, loop=0)
    print(f"Saved: {output_path} ({os.path.getsize(output_path)/1024:.1f} KB)")

if __name__ == "__main__":
    image_path = sys.argv[1] if len(sys.argv) > 1 else "assets/logo_SUB.png"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "assets/ascii_logo.gif"
    generate(image_path, output_path)
