import os
from PIL import Image

def recolor_sprites(start_num, end_num, target_hex):
    # Convert hex to RGB tuple
    hex_color = target_hex.lstrip('#')
    new_rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    for i in range(start_num, end_num + 1):
        file_path = f"sprites/sprite.{i}.png"
        
        if not os.path.exists(file_path):
            print(f"Skipping: {file_path} not found.")
            continue

        # Open image and ensure it's in RGBA mode
        img = Image.open(file_path).convert("RGBA")
        datas = img.getdata()

        new_data = []
        for item in datas:
            # item[3] is the Alpha channel (0 is fully transparent)
            if item[3] > 0:
                # Replace RGB, keep original Alpha
                new_data.append((new_rgb[0], new_rgb[1], new_rgb[2], item[3]))
            else:
                new_data.append(item)

        img.putdata(new_data)
        img.save(file_path)
        print(f"Processed: {file_path}")

if __name__ == "__main__":
    recolor_sprites(15, 15, "48A12D")