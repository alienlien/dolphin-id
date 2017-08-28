#!/usr/bin/env python3
# Ref: predict.py
import numpy as np
from keras.preprocessing import image
from keras.models import load_model
from keras.applications.inception_v3 import preprocess_input

DEFAULT_CONFIG = {
    'target_size': (229, 229),
    'top_n':
    5,
    'model':
    './model/dolphin.h5',
    'labels': [
        '20110607_04', '20110607_06', '20110607_07', '20110607_08',
        '20110607_10', '20110607_11', '20110607_12', '20110607_13',
        '20110607_14', '20110607_15', '20110607_16', '20110607_19',
        '20110607_20', '20110607_21', '20110607_22', '20110607_23',
        '20110607_24', '20110607_25', '20110607_27', '20110607_28',
        '20110704_03', '20110704_10', '20110704_11', '20110704_12',
        '20110704_13', '20110704_14', '20110704_15', '20110704_16',
        '20110704_17', '20110704_18', '20130801_004', '20130801_010',
        '20130801_011', '20130801_012', '20130801_014', '20140811_06',
        '20140811_07', '20140811_09', '20140811_10', '20140811_12',
        '20140811_13', '20140811_14', '20140811_15', '20140811_16',
        '20140813_006', '20140813_007', '20140813_010', '20140813_012',
        'ku_000', 'ku_014', 'ku_015', 'ku_016', 'ku_017', 'ku_018', 'ku_020',
        'ku_022', 'ku_114', 'ku_178'
    ],
}


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

    img_array = preprocess_input(
        np.expand_dims(image.img_to_array(img), axis=0))
    preds = model.predict(img_array)
    return preds[0]


class Classifier(object):
    def __init__(self, config=DEFAULT_CONFIG):
        self.config = config
        self.model = load_model(config['model'])

    def predict(self, img):
        """It returns the result predicted.
        """
        preds = predict(self.model, img, self.config['target_size'])
        result = zip(self.config['labels'], preds)
        # Sort by probability and only choose top n
        result = sorted(
            result, key=lambda item: item[1],
            reverse=True)[:self.config['top_n']]
        return [pred_label_for(label, prob) for (label, prob) in result]


def pred_label_for(label, prob):
    """It returns the prediction label for input.
    TODO: Define a common prediction label object?
    """
    return {
        'label': label,
        'prob': prob,
    }
