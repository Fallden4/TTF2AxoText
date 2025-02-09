from PIL import Image, ImageDraw, ImageFont
import os

def makeGlyphFolder(font, size, outputFolder):
    os.makedirs(outputFolder, exist_ok=True)
    
    for ascii in range(32, 127):
        fnt = ImageFont.truetype(font, size)
        image = Image.new("RGBA", (64, 128), (0, 0, 0, 0))  # Final image size (64x128)
        draw = ImageDraw.Draw(image)
        
        # Get text size
        text_width, text_height = draw.textbbox((0, 0), chr(ascii), font=fnt)[2:]
        
        # Create a temporary image to draw text
        temp_image = Image.new("RGBA", (text_width, text_height), (0, 0, 0, 0))
        temp_draw = ImageDraw.Draw(temp_image)
        temp_draw.text((0, 0), chr(ascii), font=fnt, fill=(255, 255, 255, 255))  # White text with full opacity
        
        # Stretch only the text vertically (double the height)
        stretched_image = temp_image.resize((text_width, text_height * 2), Image.Resampling.NEAREST)  # Double the height
        
        # Create a final image with a 64x128 canvas
        final_image = Image.new("RGBA", (64, 128), (0, 0, 0, 0))  # Transparent background
        
        # Paste the stretched image starting from the top
        final_image.paste(stretched_image, (0, 0))  # Center horizontally

        # Save the final image
        final_image.save(f"{outputFolder}/{ascii}.png")


def get_glyph_advance(img_input):
    arr = []
    earliest_start = []
    img = img_input.convert('RGBA')
    width, height = img.size
    
    for i in range(height):
        a1 = [img.getpixel((o, i)) for o in range(width)]
        a2 = a1[::-1]
        start = -1
        end = -1
        
        for l in range(width):
            if a1[l][-1] != 0:
                earliest_start.append(l)
                start = l
                break
        
        for l in range(width):
            if a2[l][-1] != 0:
                end = width - l
                break
        
        if start == -1 or end == -1:
            arr.append(0)
        else:
            arr.append(end - start)
    
    toReturn = max(arr)
    if toReturn == 0:
        return width / 2
    
    return toReturn
