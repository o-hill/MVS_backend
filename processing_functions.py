'''

    Video processing functionality. A little data science for ya.

'''

import numpy as np
import cv2
from mathtools.fit import Fit

from skimage import feature


def uniform_elimination(frame: np.ndarray = np.zeros(0), num_bases: int = 10, penalty: list = [0,0,0]):
    '''Remove uneven lighting given a single frame.'''

    # Remove color channels if necessary.
    if frame.ndim >= 3:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    nrows, dcols = frame.shape
    f = Fit(np.arange(nrows), num_bases, reg_coefs=penalty)
    new_frame = np.zeros_like(frame, dtype=float)

    for column in range(dcols):
        regression = f.fit(frame[:, column])

        # Subtract off the polynomial.
        new_frame[:, column] = frame[:, column] - regression.y

    return new_frame


def edge_detection(frame):
    '''Attempt to find/count cells in a frame.'''

    # Remove color channels if necessary.
    if frame.ndim >= 3:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    return feature.canny(frame)




