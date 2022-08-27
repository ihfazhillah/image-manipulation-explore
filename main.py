# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import csv
import itertools
import pprint
import re
import textwrap
from string import ascii_letters

from PIL import Image, ImageFont, ImageDraw


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

    
def get_y_and_heights(text_wrapped, dimensions, margin, font):
    """Get the first vertical coordinate at which to draw text and the height of each line of text"""
    # https://stackoverflow.com/a/46220683/9263761
    ascent, descent = font.getmetrics()

    # Calculate the height needed to draw each line of text (including its bottom margin)
    line_heights = []

    for line in text_wrapped:
        left, top, right, bottom = font.getbbox(line)
        line_heights.append(
            ascent + descent
        )

    # line_heights = [
    #     # bottom - top
    #     (font.getbbox(text_line)[3] - font.getbbox(text_line)[1])  + descent + margin
    #     for text_line in text_wrapped
    # ]
    # The last line doesn't have a bottom margin
    line_heights[-1] -= margin

    # Total height needed
    height_text = sum(line_heights)

    # Calculate the Y coordinate at which to draw the first line of text
    y = (dimensions[1] - height_text) // 2

    # Return the first Y coordinate and a list with the height of each line
    return y, line_heights


def split_words(special_words, text):
    special_words_pattern = "|".join(special_words)
    separators = "[,.?!]?"
    text_pattern = f"(?P<final>({special_words_pattern}|[\w\-]+){separators})"
    pattern = re.compile(text_pattern)

    final_words = []
    for match in re.finditer(pattern, text):
        res = match.groupdict().get("final")
        if res:
            final_words.append(res)
    return final_words


text = "Ketika sampai, mereka semua langsung turun dari tunggangannya dan menemui Rosululloh shollallohu 'alaihi wa sallam, kecuali Al-Asyaj"

def generate_image(size, font_size):
    img = Image.new("RGBA", size, (255, 0, 0, 0))
    w, h = img.size

    font = ImageFont.truetype("Crayon pastel.otf", font_size)
    draw = ImageDraw.Draw(img)

    # get max char count
    avg_char_width = sum([font.getbbox(char)[2] for char in ascii_letters]) / len(ascii_letters)
    max_char_count = int(w * .80 / avg_char_width)

    wrapped_texts = textwrap.wrap(text, width=max_char_count)

    space_box = font.getbbox(" ")
    y, line_heights = get_y_and_heights(wrapped_texts, img.size, 10, font)
    page_data = []
    for idx, line in enumerate(wrapped_texts):
        line_width = font.getbbox(line)[2]
        # x = (img.width - line_width) // 2  # center
        x = img.width // 2
        draw.text((x, y), line, font=font, fill="black", anchor="ma")

        box_line = draw.textbbox((x, y), line, font=font, anchor="ma")
        draw.rectangle(box_line, outline="black")

        box_left, box_top, box_right, box_bottom = box_line

        # get bbox for each word
        words = line.split(" ")

        word_x = box_left
        for word in words:
            word_left, word_top, word_right, word_bottom = font.getbbox(word)

            word_final_box = (word_left + word_x, box_top, word_right + word_x, box_bottom)

            draw.rectangle(word_final_box, outline="red")

            # increase x
            word_x += word_right + space_box[2]

            page_data.append([word] + list(word_final_box))

        y += line_heights[idx]

    img.show()
    return page_data


def main():
    sizes = [
        ((480, 320), 25),
        # ((800, 480), 38),
        # ((1280, 720), 50),
        # ((1440, 960), 75),
        # ((1920, 1280), 100),
    ]
    for image_size, font_size in sizes:
        page_data = generate_image(image_size, font_size)
        splitted_text = split_words(["shollallohu 'alaihi wa sallam"], text)

        # dapatkan splitted text with empty list
        final = [(word, []) for word in splitted_text]

        # dapatkan index by words
        words_and_index = []
        for index, line in enumerate(splitted_text):
            for word in line.split(" "):
                words_and_index.append((word, index))

        for data, word_and_index in zip(page_data, words_and_index):
            word, left, top, right, bottom = data
            word_1, index = word_and_index

            final[index][1].append([left, top, right, bottom])

        normalize_lines = []
        for word, bboxes in final:
            if len(bboxes) == 1:
                normalize_lines.append((word, bboxes))
                continue

            final_bboxes = []
            line_groups = itertools.groupby(bboxes, key=lambda bbox: bbox[1] and bbox[3])
            for _, g_bboxes in line_groups:
                g_bboxes = list(g_bboxes)
                if len(g_bboxes) == 1:
                    final_bboxes += g_bboxes
                    continue

                left = min([b[0] for b in g_bboxes])
                right = max([b[2] for b in g_bboxes])
                top = g_bboxes[0][1]
                bottom = g_bboxes[0][3]
                final_bboxes.append([left, top, right, bottom])

            normalize_lines.append((word, final_bboxes))

        pprint.pprint(normalize_lines, indent=2)
    # img = Image.new("RGBA", (480, 320), (255, 0, 0, 0))
    # w, h = img.size
    #
    # print(img.info)
    # print(img.im)
    # print(img.size)
    # font = ImageFont.truetype("Crayon pastel.otf", 25)
    # print(font.getmetrics())
    # draw = ImageDraw.Draw(img)
    #
    # for char in ascii_letters:
    #     print(font.getbbox(char))
    #
    # # get max char count
    # avg_char_width = sum([font.getbbox(char)[2] for char in ascii_letters]) / len(ascii_letters)
    # max_char_count = int(w * .80 / avg_char_width)
    #
    # wrapped_texts = textwrap.wrap("Ketika sampai, mereka semua langsung turun dari tunggangannya dan menemui Rosululloh shollallohu 'alaihi wa sallam, kecuali Al-Asyaj", width=max_char_count)
    #
    # space_box = font.getbbox(" ")
    # y, line_heights = get_y_and_heights(wrapped_texts, img.size, 10, font)
    # page_data = []
    # for idx, line in enumerate(wrapped_texts):
    #     line_width = font.getbbox(line)[2]
    #     x = (img.width - line_width) // 2  # center
    #     draw.text((x, y), line, font=font, fill="black")
    #
    #     box_line = draw.textbbox((x, y), line, font=font)
    #     # draw.rectangle(box_line, outline="black")
    #
    #     box_left, box_top, box_right, box_bottom = box_line
    #
    #     # get bbox for each word
    #     words = line.split(" ")
    #     for word in words:
    #         word_box = font.getbbox(word)
    #
    #         word_final_box = (word_box[0] + x, box_top, word_box[2] + x, box_bottom)
    #
    #         # draw.rectangle(word_final_box, outline="red")
    #
    #         # increase x
    #         x += word_box[2] + space_box[2]
    #         page_data.append([word] + list(word_final_box))
    #
    #     y += line_heights[idx]
    #
    # img.show()
    # # img.save("test_result-xxhdpi.png")
    # # with open("test_result_data-xxhdpi.csv", "w") as data:
    # #     writer = csv.writer(data)
    # #     writer.writerows(page_data)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
