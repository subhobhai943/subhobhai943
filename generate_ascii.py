from PIL import Image
import sys
import os
import re

ASCII_CHARS = "@%#*+=-:. "

def convert(image_path, width=80):
    image = Image.open(image_path).convert("L")
    w, h = image.size
    new_h = int(h / w * width * 0.55)
    image = image.resize((width, new_h))
    pixels = list(image.getdata())
    chars = [ASCII_CHARS[p * (len(ASCII_CHARS) - 1) // 255] for p in pixels]
    lines = ["".join(chars[i:i+width]) for i in range(0, len(chars), width)]
    return "\n".join(lines)

def inject_into_readme(ascii_art, readme_path="README.md"):
    block = f'<pre align="center">\n{ascii_art}\n</pre>'
    with open(readme_path, "r") as f:
        content = f.read()
    # Replace existing <pre> block if present, else insert after first <h1>
    pre_pattern = re.compile(r'<pre align="center">.*?</pre>', re.DOTALL)
    if pre_pattern.search(content):
        content = pre_pattern.sub(block, content)
    else:
        content = re.sub(r'(<h1[^>]*>.*?</h1>)', r'\1\n\n' + block, content, count=1)
    with open(readme_path, "w") as f:
        f.write(content)
    print("Injected ASCII art into README.md")

if __name__ == "__main__":
    image_path = sys.argv[1] if len(sys.argv) > 1 else "assets/logo_SUB.png"
    ascii_art = convert(image_path)
    # Save txt
    os.makedirs("assets", exist_ok=True)
    with open("assets/ascii.txt", "w") as f:
        f.write(ascii_art)
    inject_into_readme(ascii_art)
