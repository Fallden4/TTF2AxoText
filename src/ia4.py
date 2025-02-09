from PIL import Image
import numpy as np

def img2ia4(image_path, var_name="image_data"):
    image = Image.open(image_path).convert("LA")
    width, height = image.size
    pixels = np.array(image)
    
    ia4_data = bytearray()
    
    for y in range(height):
        for x in range(0, width, 2):
            p1 = pixels[y, x]
            ia1 = ((p1[0] >> 4) & 0xF) | ((p1[1] >> 4) << 4)
            
            if x + 1 < width:
                p2 = pixels[y, x + 1]
                ia2 = ((p2[0] >> 4) & 0xF) | ((p2[1] >> 4) << 4)
            else:
                ia2 = 0
            
            ia4_data.append((ia1 << 4) | ia2)
    
    output = []
    output.append(f"u8 {var_name}[] = {{\n")
    
    for i, byte in enumerate(ia4_data):
        if i % 12 == 0:
            output.append("    ")
        output.append(f"0x{byte:02X}, ")
        if (i + 1) % 12 == 0:
            output.append("\n")
    
    output.append("\n};\n")
    
    return "".join(output)

# with open(r"C:\Users\htauk\Downloads\LetterRack\test.inc.c", "w") as f:
#     f.write(img2ia4(r"output\64.png"))