# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
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
    line_heights = [
        font.getbbox(text_line)[3] + descent + margin
        for text_line in text_wrapped
    ]
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
    font = ImageFont.truetype("Playful Koala.ttf", 120)
    print(font.getmetrics())
    draw = ImageDraw.Draw(img)

    for char in ascii_letters:
        print(font.getbbox(char))

    # get max char count
    avg_char_width = sum([font.getbbox(char)[2] for char in ascii_letters]) / len(ascii_letters)
    max_char_count = int(w * .80 / avg_char_width)

    text = textwrap.fill("Kaum muslimin teringat dengan perkataan Rosululloh shollallohu ‘alaihi wa sallam tentang Al Barro’.", width=max_char_count)
    wrapped_texts = textwrap.wrap("Kaum muslimin teringat dengan perkataan Rosululloh shollallohu ‘alaihi wa sallam tentang Al Barro’.", width=max_char_count)

    # draw.text(
    #     (half_width, half_height),
    #     text,
    #     fill="black",
    #     anchor="mm",
    #     font=font
    # )
    y, line_heights = get_y_and_heights(wrapped_texts, img.size, 20, font)
    for idx, line in enumerate(wrapped_texts):
        # TODO: get the bbox each word
        line_width = font.getbbox(line)[2]
        x = (img.width - line_width) // 2  # center
        draw.text((x, y), line, font=font, fill="black")

        y += line_heights[idx]

    img.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
