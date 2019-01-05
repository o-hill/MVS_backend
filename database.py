'''

    Direct access to the database for the MVS backend server.

'''

import pymongo
from pymongo import MongoClient

from ipdb import set_trace as debug

# Global database client.
client = MongoClient()

CELL_TYPES = ['WBC', 'RBC', 'Stem Cell']

PROCESSING_OPTIONS = {
    'Cell Segmentation': { 'Cell Type': ('LIST', CELL_TYPES), 'Distance': ('DOUBLE') },
    'Cell Count': { 'Cell Type': ('LIST', CELL_TYPES) }
    'Clean': { 'Uniform Elimination': ('BOOLEAN') }
}


class MongoDatabase:

    def __init__(self):
        '''Initialize access to the database.'''

        self.db = client.MVS
        self.videos_collection = self.db.videos


    def list_videos(self):
        '''Return a list of filenames for available videos.'''
        return [ x['filename'] for x in self.videos_collection.find() ]


    def add_video(self, filename, save_dir):
        '''Add a video filename to the database.'''

        self.videos_collection.insert_one({
            'filename': filename,
            'save_directory': save_dir
        })


    def delete_video(self, filename):
        '''Delete a video from the database.'''
        self.videos_collection.delete_one({ 'filename': filename })


