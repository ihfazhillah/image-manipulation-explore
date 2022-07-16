# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import csv
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
            bottom + descent + margin
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


def main():
    img = Image.open("image.png")
    w, h = img.size
    half_width = w // 2
    half_height = h // 2

    print(img.info)
    print(img.im)
    print(img.size)
    font = ImageFont.truetype("Crayon pastel.otf", 100)
    print(font.getmetrics())
    draw = ImageDraw.Draw(img)

    for char in ascii_letters:
        print(font.getbbox(char))

    # get max char count
    avg_char_width = sum([font.getbbox(char)[2] for char in ascii_letters]) / len(ascii_letters)
    max_char_count = int(w * .80 / avg_char_width)

    text = textwrap.fill("Kaum muslimin teringat dengan perkataan Rosululloh shollallohu ‘alaihi wa sallam tentang Al Barro’", width=max_char_count)
    wrapped_texts = textwrap.wrap("Kaum muslimin teringat dengan perkataan Rosululloh shollallohu ‘alaihi wa sallam tentang Al Barro’", width=max_char_count)

    space_box = font.getbbox(" ")
    y, line_heights = get_y_and_heights(wrapped_texts, img.size, 10, font)
    page_data = []
    for idx, line in enumerate(wrapped_texts):
        line_width = font.getbbox(line)[2]
        x = (img.width - line_width) // 2  # center
        draw.text((x, y), line, font=font, fill="black")

        box_line = draw.textbbox((x, y), line, font=font)
        # draw.rectangle(box_line, outline="black")

        box_left, box_top, box_right, box_bottom = box_line

        # get bbox for each word
        words = line.split(" ")
        for word in words:
            word_box = font.getbbox(word)

            word_final_box = (word_box[0] + x, box_top, word_box[2] + x, box_bottom)

            # draw.rectangle(word_final_box, outline="red")

            # increase x
            x += word_box[2] + space_box[2]
            page_data.append([word] + list(word_final_box))

        y += line_heights[idx]

    img.show()
    img.save("test_result.png")
    with open("test_result_data.csv", "w") as data:
        writer = csv.writer(data)
        writer.writerows(page_data)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
