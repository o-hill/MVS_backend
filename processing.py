'''

    Control of video processing for the MVS backend.

'''

from collections import deque
from database import MongoDatabase

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
        self.mongo.add_processed_video(self.actively_processing)
        self.actively_processing = { }

