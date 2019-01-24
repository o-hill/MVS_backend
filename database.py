'''

    Direct access to the database for the MVS backend server.

'''

import pymongo
from pymongo import MongoClient

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

    def something(x):
        print("something not x")



    def add_processed_video(self, request: dict = { }):
        '''Add a processed video to the database.'''
        filename = request.pop('filename')
        self.processed.insert_one({
            'filename': filename,
            'processing_options': dict(request)
        })


    def begin_logging_processing(self, filename):
        '''Log distributed video processing progress.'''
        return self.logging.insert_one({
            'filename': filename,
            'progress': 0,
            'completed': False,
            'error': ''
        })




