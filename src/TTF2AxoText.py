from tkinter import *
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk
import ia4
import makeglyph
import os
import re

class TTF2LetterRack:
    def __init__(self, root):
        self.root = root
        self.root.title("TTF2LetterRack")
        ico = PhotoImage(file="faviDark.png")
        self.root.iconphoto(False, ico)

        self.font_path = None
        self.font_size = 16

        self.select_button = tk.Button(root, text="Select Font", command=self.load_font)
        self.select_button.pack()

        self.canvas = tk.Canvas(root, width=300, height=100, bg="white")
        self.canvas.pack()

        self.size_slider = tk.Scale(root, from_=1, to=64, orient="horizontal", label="Font Size", command=self.update_size)
        self.size_slider.set(self.font_size)
        self.size_slider.pack()

        self.convert_button = tk.Button(root, text="Convert", command=self.convert)
        self.convert_button.pack()

        self.tk_image = None

    def load_font(self):
        self.font_path = filedialog.askopenfilename(filetypes=[("Font Files", "*.ttf;*.otf")])
        if self.font_path:
            self.update_preview()

    def update_size(self, value):
        self.font_size = int(value)
        self.update_preview()

    def update_preview(self):
        if not self.font_path:
            return

        img = Image.new("RGB", (300, 100), "white")
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype(self.font_path, self.font_size)
            draw.text((10, 30), "The quick brown fox jumps over the lazy dog.", font=font, fill="black")
            
            # img.show()

            self.tk_image = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        except Exception as e:
            print("Error loading font:", e)

    def convert(self):
        if self.font_path and self.font_size:
            font_name = os.path.basename(self.font_path).replace(".ttf", "").replace(".otf", "")
            font_name = re.sub(r'\W+', '', font_name)
            print(f"{self.font_path} : {self.font_size}")
            makeglyph.makeGlyphFolder(self.font_path, self.font_size, "output")
            with open(f"{font_name}.inc.c", "w", encoding="utf-8") as f:
                f.write('// This font was converted with TTF2AxoText, for use with AxoText.\n// Made with ♥ from Fallden4\n// Shoutouts to SimpleFlips\n\n#include "game/axotext.h"\n\n')
                for letter in range(33, 127):
                    img_str = ia4.img2ia4(os.path.join("output", f"{letter}.png"), f"{font_name}_texture_{letter}")
                    f.write(img_str + "\n")
                f.write(f"u8 *{font_name}_texture_table[] = {{\n    // unprintables\n    NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,\n    NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,\n\n    /*   */ NULL,\n    ")
                for letter in range(33,127):
                    separator = "," if letter < 126 else ""
                    f.write(f"/* {chr(letter)} */ {font_name}_texture_{letter}{separator}\n    ")
                f.write("};\n\n")
                
                f.write(f'''u8 {font_name}_kerning_table[] = {{
	// unprintable characters
	8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
	8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    
    
''')
                for letter in range(32,127):
                    kerning = makeglyph.get_glyph_advance(Image.open(os.path.join("output", f"{letter}.png")))
                    separator = "," if letter < 126 else ""
                    f.write(f"/* {chr(letter)} */ {str(int(kerning + 2))}{separator}\n    ")
                f.write("};\n\n")
        
                f.write(f"AxotextFont {font_name} = {{\n    64,\n    128,\n    1.0f,\n    {font_name}_texture_table,\n    {font_name}_kerning_table,\n    AXOTEXT_FILTER_BILERP\n}};")

        else:
            messagebox.showerror("Error", "Select a font and a size")

if __name__ == "__main__":
    root = tk.Tk()
    app = TTF2LetterRack(root)
    root.mainloop()
