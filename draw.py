#!/usr/bin/env python3
# It is used to draw the boxes on the pic.
from docopt import docopt
from PIL import Image, ImageDraw, ImageFont
from parser import from_xml

DEFAULT_FONT_PATH = '/Library/Fonts/Arial.ttf'
DEFAULT_FONT_SIZE = 100
DEFAULT_BOX_WIDTH = 20  # Width for the boxes.
DEFAULT_BOX_COLOR = 'white'


class BoxDrawer():
    def __init__(self,
                 font_path=DEFAULT_FONT_PATH,
                 font_size=DEFAULT_FONT_SIZE):
        self.font = ImageFont.truetype(font=font_path, size=font_size)

    def draw(self, img, boxes, width, color):
        """
        Args:
            img: PIL Image object.

        Returns:
            PIL Image object.
        """
        draw = ImageDraw.Draw(img)

        for box in boxes:
            # Render the bounding box.
            (ulx, uly), (lrx, lry) = box.upper_left(), box.lower_right()
            for shift in range(0, width):
                draw.rectangle(
                    [(ulx + shift, uly + shift), (lrx + shift, lry + shift)],
                    outline=color)

            # Render the label.
            label = box.label()
            _, height = self.font.getsize(label)
            draw.text(
                (ulx, uly - height), box.label(), fill=color, font=self.font)

        return img

    def draw_file(self,
                  img_in,
                  img_out,
                  boxes,
                  width=DEFAULT_BOX_WIDTH,
                  color=DEFAULT_BOX_COLOR):
        """It draws boxes on the image input.

        Args:
            img_in: The path of the image input.
        """
        img = self.draw(Image.open(img_in), boxes, width, color)
        img.save(img_out)


usage = """
Usage:
    draw.py [options]

Options:
    --img=FILE  The file to draw.
    --anno=FILE The annotation file (.xml).
    --out=FILE  Output file [default: ./test.png].
"""
if __name__ == '__main__':
    args = docopt(usage, help=True)
    drawer = BoxDrawer()

    with open(args['--anno'], 'r') as f:
        boxes = from_xml(f).boxes

    drawer.draw_file(args['--img'], args['--out'], boxes, color='yellow')
