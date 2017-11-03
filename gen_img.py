#!/usr/bin/env python3
# This is used to generate a test image for regressions test.
from PIL import Image

SIZE = 3

# Generate an image like this:
# B B W
# B W W
# W W W
if __name__ == '__main__':
    img = Image.new('RGB', (SIZE, SIZE))
    pix = img.load()
    for i in range(SIZE):
        for j in range(SIZE):
            if (i + j) <= 1:
                pix[i, j] = (0, 0, 255)
            else:
                pix[i, j] = (255, 255, 255)

    img.save('./regression_test/test.jpg', 'JPEG')
