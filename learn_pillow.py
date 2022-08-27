import csv
import math
import random
import string

from PIL import Image, ImageDraw, ImageFont
import textwrap

image = Image.new("RGBA", (960, 1080), (255, 255, 255, 255))

draw = ImageDraw.Draw(image)

text = "Pillow is the friendly PIL fork by Alex Clark and Contributors. PIL is the Python Imaging Library by Fredrik Lundh and Contributors."
font = ImageFont.truetype("Crayon pastel.otf", 50)

chars = string.ascii_letters
widhts = [font.getbbox(char)[2] for char in chars]
rata_rata = sum(widhts) / len(widhts)

max_width = image.width * 0.8
max_char = math.floor(max_width / rata_rata)

wrapped_text = textwrap.fill(text, max_char)
print(wrapped_text)
print(textwrap.wrap(text, max_char))

line_bounding_boxes = []
for line in textwrap.wrap(text, max_char):
    line_bounding_boxes.append(font.getbbox(line))

print(line_bounding_boxes)

# draw.multiline_text((100, 100), text=text, fill="red", font=font)

# bbox = draw.textbbox((100, 100), wrapped_text, font=font)
# draw.rectangle(bbox, fill="black")

# draw.text((100, 100), wrapped_text, fill="red", font=font)


colors = ["yellow", "blue"]

x, y = 100, 100
ascender, descender = font.getmetrics()
space_x1, space_y1, space_x2, space_y2 = font.getbbox(" ")
space_width = space_x2 - space_x1

words = []

for bounding_box, line in zip(line_bounding_boxes, textwrap.wrap(text, max_char)):
    x_adder = 0
    l, t, r, b = bounding_box

    bbox = draw.textbbox((x, y), text=line, font=font)

    y1 = y
    y2 = y + ascender + descender

    # draw.rectangle(((x, y1), ((r - l + x), y2)), outline="black")
    draw.text((x, y), line, fill="red", font=font)

    for word in line.split(" "):
        x1_word, y1_word, x2_word, y2_word = draw.textbbox((x, y), text=word, font=font)
        # draw.rectangle((x1_word + x_adder, y1, x2_word + x_adder, y2), outline="red")
        words.append([word, x1_word + x_adder, y1, x2_word + x_adder, y2])

        word_width = x2_word - x1_word + space_width
        x_adder += word_width

    y += ascender + descender + 10



image.save("contoh_gambar.png")
with open("contoh_gambar_bbox.csv", "w") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(words)

# image.show()