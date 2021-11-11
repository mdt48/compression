from math import sin
import numpy as np
import math
from PIL import Image

def SNR(original_signal, quantized_signal):
    return float(10 * np.log10( np.sum(np.square(original_signal)) / np.sum(np.square(original_signal - quantized_signal)) ))

def MSE(original_signal, quantized_signal):
    return float((1/len(original_signal)) * np.sum( np.square(original_signal - quantized_signal) ))

def ENT(signal):
    probabilities = {}
    for x in signal:
        if x not in probabilities:
            probabilities[x] = int(np.count_nonzero(signal == x)) / len(signal)
    H = 0
    for p in probabilities.values():
        H += p*math.log10(p)
    return -H

def open_vectorize_image(path):
    image = np.asarray(Image.open(path))
    return image, np.ndarray.flatten(image)