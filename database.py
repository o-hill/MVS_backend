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
    { 'name': 'Cell Segmentation', options: [
        { 'name': 'Cell Type', fields: ('LIST', CELL_TYPES) },
        { 'name': 'Distance', fields: ('DOUBLE') }
    ]},
    { 'name: 'Cell Count', options: [
        { name: 'Cell Type', fields: ('LIST', CELL_TYPES) }
    ]},
    { name: 'Clean', options: [{ name: 'Uniform Elimination', fields: ('BOOLEAN') }]}
]


class MongoDatabase:

    def __init__(self):
        '''Initialize access to the database.'''

        self.db = client.MVS
        self.videos = self.db.videos


    def list_videos(self):
        '''Return a list of filenames for available videos.'''
        videos = list(self.videos.find({}, {'_id': 0}))
        return sorted(videos, key=lambda x: x['filename'])


    def add_video(self, filename, save_dir):
        '''Add a video filename to the database.'''

        self.videos.insert_one({
            'filename': filename,
            'save_directory': save_dir,
            'processing_options': PROCESSING_OPTIONS
        })


    def delete_video(self, filename):
        '''Delete a video from the database.'''
        self.videos.delete_one({ 'filename': filename })

    def something(x):
    print(x)



