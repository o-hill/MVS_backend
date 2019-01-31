'''

    Testing, notes, and investigation for the video processing.

'''

import cv2
import numpy as np
from matplotlib import pyplot as plt

from processing_functions import *

from tqdm import tqdm
from ipdb import set_trace as debug

import imageio

OUTPUT_CODE = cv2.VideoWriter_fourcc(*'MJPG')

def edge_detection_video():
    '''Create video of edge detection.'''

    video = cv2.VideoCapture('xdfo.m4v')
    output_filename = 'edges.mp4'
    output_fps = 10
    width, height = int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    output = imageio.get_writer('edges2.mp4', fps=10, mode='I')

    num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    full_video = np.zeros((num_frames, height, width), dtype=np.uint8)

    for i in tqdm(range(num_frames)):
        ret, frame = video.read()
        eliminated = uniform_elimination(
                        frame = frame,
                        num_bases = 8,
                        penalty = [0, 0, 0.01]
                    )

        edges = edge_detection(eliminated)
        edges = edges.astype(np.uint8) * 255
        output.append_data(edges)

    output.close()
    print('All done!')

def test_uniform_elimination():
    '''Notes:
        Looks like 8 bases with a 0.01 penalty on the second derivative is nice for uniform elimination.
    '''

    video = cv2.VideoCapture('xdfo.m4v')
    _, frame = video.read()
    gframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    plt.figure()

    for i, nb in enumerate([8, 9, 10]):
        for j, penalty in enumerate([10**-3, 10**-2, 10**-1]):
            ax = plt.subplot(3, 3, (3*i)+j+1)
            ax.imshow(uniform_elimination(
                frame = gframe,
                num_bases = nb,
                penalty = [0, 0, penalty]
            ), cmap=plt.cm.viridis)
            plt.title(f'bases: {nb}, penalty: {penalty}')

    # for i in range(5, 16):
    #     ax = plt.subplot(3, 4, i - 3)
    #     ax.imshow(p.uniform_elimination(frame = gframe, num_bases = i), cmap=plt.cm.bone)
    #     plt.title(f'Num bases: {i}')

    plt.show()

if __name__ == '__main__':
    edge_detection_video()
