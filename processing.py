'''

    Control of video processing for the MVS backend.

'''

from collections import deque
from database import MongoDatabase
import multiprocessing

# Video reading and writing.
import cv2

# Define some video processing globals.
FRAME_RATE = 20.0
FILE_TYPE = '.avi'
FRAME_SIZE = (640, 480)
COLOR = True
OUTPUT_CODE = cv2.VideoWriter_fourcc(*'XVID')


class Processor:

    def __init__(self):
        self.processing_queue = deque()
        self.actively_processing = { }
        self.mongo = MongoDatabase()


    def add_video(self, request: dict = { }):
        '''Add a video to the processing queue.

        @request: dictionary containing the video filename and specified options.
        '''

        self.processing_queue.append(request)
        if not self.actively_processing:
            self.actively_processing = self.processing_queue.popleft()
            self.process()


    def get_status(self):
        '''Get the status of each video in the processing pipeline.'''
        status = {
            el['filename']: 'Waiting...' for el in self.processing_queue
        }
        status[self.actively_processing['filename']] = 'Processing'

        return status


    def process(self):
        '''Process a video.'''
        print(f'Processing video {self.actively_processing["filename"]}...')
        print('Add processing code here.......')
        self.mongo.add_processed_video(self.actively_processing)
        self.actively_processing = { }



def process_video(functions: list = [], video_filename: str = '', new_filename: str = ''):
    '''Process a single video with the given processing functions.'''

    if not functions or not video_filename or not new_filename:
        print('> Processing error: invalid input...')

    video = cv2.VideoCapture(video_filename)
    output = cv2.VideoWriter(f'{new_filename}{FILE_TYPE}', OUTPUT_CODE, FRAME_RATE, FRAME_SIZE, COLOR)

    # Logging progress.
    num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    logging_id = mongo.begin_logging_processing(new_filename)

    ret = True
    while ret:
        ret, frame = video.read()

        # Process the frame of data.
        for f in functions:
            frame = f(frame)

        # Write to the file.
        output.write(frame)












