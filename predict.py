import sys
import argparse
import numpy as np
from PIL import Image
import requests
from io import BytesIO
from pprint import pprint
import matplotlib.pyplot as plt

from keras.preprocessing import image
from keras.models import load_model
from keras.applications.inception_v3 import preprocess_input

from config import ConfigStore

# TODO: Fix keras 2 api error, Rewrite some functions.
# Note that the tensorflow-gpu is only enabled with python2, not 3.

target_size = (229, 229)  # Fixed size for InceptionV3 architecture


def predict(model, img, target_size):
    """Run model prediction on image
  Args:
    model: keras model
    img: PIL format image
    target_size: (w,h) tuple
  Returns:
    list of predicted labels and their probabilities
  """
    if img.size != target_size:
        img = img.resize(target_size)

    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    preds = model.predict(x)
    return preds[0]


def plot_preds(image, preds, labels):
    """Displays image and the top-n predicted probabilities in a bar graph
  Args:
    image: PIL image
    preds: list of predicted labels and their probabilities
  """
    plt.imshow(image)
    plt.axis('off')

    plt.figure()
    plt.barh([0, 1], preds, alpha=0.5)
    plt.yticks([0, 1], labels)
    plt.xlabel('Probability')
    plt.xlim(0, 1.01)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    a = argparse.ArgumentParser()
    a.add_argument("--image", help="path to image")
    a.add_argument("--image_url", help="url to image")
    a.add_argument("--model")
    a.add_argument('--config', help='Config key')
    args = a.parse_args()

    if not args.image and not args.image_url:
        a.print_help()
        sys.exit(1)

    if args.image:
        img = Image.open(args.image)
    else:
        response = requests.get(args.image_url)
        img = Image.open(BytesIO(response.content))

    cfg_store = ConfigStore()
    config = cfg_store.get(args.config)

    model = load_model(config['model'])
    labels = config['labels']

    preds = predict(model, img, target_size)
    result = [(x, y) for (x, y) in zip(labels, preds)]
    pprint(result)
