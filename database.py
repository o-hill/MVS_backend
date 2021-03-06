'''

    Direct access to the database for the MVS backend server.

'''

import pymongo
from pymongo import MongoClient
from mongoengine import *

from ipdb import set_trace as debug

# Global database client.
client = MongoClient()

CELL_TYPES = ['WBC', 'RBC', 'Stem Cell']

PROCESSING_OPTIONS = [
    { 'name': 'Cell Segmentation', 'options': [
        { 'name': 'Cell Type', 'fields': ('LIST', CELL_TYPES) },
        { 'name': 'Distance', 'fields': ('DOUBLE', 0.0) }
    ]},
    { 'name': 'Cell Count', 'options': [
        { 'name': 'Cell Type', 'fields': ('LIST', CELL_TYPES) }
    ]},
    { 'name': 'Clean', 'options': [{ 'name': 'Uniform Elimination', 'fields': ('BOOLEAN', False) }]}
]


class MongoDatabase:

    def __init__(self):
        '''Initialize access to the database.'''

        self.db = client.MVS
        self.videos = self.db.videos
        self.processed = self.db.processed
        self.logging = self.db.logging
        self.experiments = self.db.experiments

    def list_videos(self):
        '''Return a list of filenames for available videos.'''
        videos = list(self.videos.find({}, {'_id': 0}))
        return sorted(videos, key=lambda x: x['filename'])


    def add_video(self, filename: str = '', save_dir: str = ''):
        '''Add a video filename to the database.'''

        self.videos.insert_one({
            'filename': filename,
            'save_directory': save_dir,
            'processing_options': PROCESSING_OPTIONS
        })


    def delete_video(self, filename: str = ''):
        '''Delete a video from the database.'''
        self.videos.delete_one({ 'filename': filename })


    def add_processed_video(self, request: dict = { }):
        '''Add a processed video to the database.'''
        filename = request.pop('filename')
        self.processed.insert_one({
            'filename': filename,
            'processing_options': dict(request)
        })


    def begin_logging_processing(self, filename: str = ''):
        '''Log distributed video processing progress.'''
        return self.logging.insert_one({
            'filename': filename,
            'progress': 0,
            'completed': False,
            'error': { }
        })


<<<<<<< HEAD
    def add_experiment(self, experiment):
        '''Add an experiment to the database.'''
        self.experiments.insert_one(experiment)
=======
    def update_video_progress(self, video_id, progress: int = 0):
        '''Update the progress of a video processing task.'''
        return self.logging.update_one(
                { '_id': video_id },
                { '$set': {'progress': progress} },
                upsert = False
        )


    def complete_video_processing(self, video_id):
        '''Mark the video processing task as complete.'''
        return self.logging.update_one(
                { '_id': video_id },
                { '$set': {'completed': True} },
                upsert = False
        )

    def report_processing_error(self, video_id, error: dict = { }):
        '''Report an error with a video processing task.

            @error: dictionary containing keys 'error_type' and 'message'.
        '''
        return self.logging.update_one(
                { '_id': video_id },
                { '$set': {'error': error} },
                upsert = False
        )



>>>>>>> 470f7dc16486330c4241d237b27d5f504caa27e5


'''class Dish(Document):
    dish_number = IntField()
    start_date = DateTimeField()
    end_date = DatetimeField()
'''
