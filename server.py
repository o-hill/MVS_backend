'''

    Provide API endpoints for the MVS backend.

'''

import sys
import os

# Flask server stuff.
from flask import Flask, request, abort, send_from_directory
from flask_restful import abort, Api, Resource, reqparse
from flask_cors import *

# But let's use WSGIServer for actually putting the host up.
import eventlet
from eventlet import wsgi

import os
from werkzeug.utils import secure_filename
from subprocess import Popen

from database import MongoDatabase
from serial import *

from ipdb import set_trace as debug


# -------------------------------------------------------------

DEV = True

# Specify the port number.
PORT = 1496

# Directory to save videos to.
ROOT_DIR = os.getcwd()
SAVE_DIR = f'{os.getcwd()}/videos'

# Create the server.
app = Flask(__name__)
api = Api(app)
valid_headers = ['Content-Type', 'Access-Control-Allow-Origin', '*']
cors = CORS(app, allow_headers=valid_headers)

# Connect to the database.
mongo = MongoDatabase()

# Do a little server-side checking.
ALLOWED_EXTENSIONS = set(['webm', 'mp4', 'mp3', 'wav', 'jpeg', 'gif', 'png'])

def allowed_file(filename):
    '''Ensure we want to keep this file.'''
    return True


def validate_filepath(func):
    '''Decorator to validate a filepath from the frontend.'''
    def wrapper(obj, video_filename):

        # Disallow anything but pure filenames - no messing with other directories.
        if video_filename.find('/'):
            old_filename = video_filename
            split = video_filename.split('/')
            video_filename = split[-1]
            print(f'Modified filename from {old_filename} to {video_filename}.')

        if not os.path.exists(os.path.join(SAVE_DIR, video_filename)):
            print(f'Filename: {video_filename} does not exist in directory {SAVE_DIR}. Aborting request.')
            abort(404)

        func(obj, video_filename)

    return wrapper

# --------------------------------------------------------------


class Video(Resource):

    @validate_filepath
    def get(self, video_filename):
        '''Return the video for the user to download.'''
        print(f'Sending file {video_filename} from {SAVE_DIR}')
        response = send_from_directory(directory=SAVE_DIR, filename=video_filename)
        return respone

    @validate_filepath
    def delete(self, video_filename):
        '''Delete a video from the database and the server.'''
        print(f'Deleting file {video_filename} from {SAVE_DIR} and from the database.')
        os.remove(os.path.join(SAVE_DIR, video_filename))
        mongo.delete_video(video_filename)



class Videos(Resource):

    def get(self):
        '''Return a list of the avilable videos in the database.'''
        return mongo.list_videos()

    def post(self):
        '''Add video files to the database.'''
        posts = dict(request.files)

        if 'videos' not in posts:
            print('No videos in the request...')
            return self.get()

        for video in posts['videos']:
            if video.filename and allowed_file(video.filename):
                filename = secure_filename(video.filename)
                print(f'Saving {filename} to {SAVE_DIR}...')

                video.save(os.path.join(SAVE_DIR, filename))
                mongo.add_video(filename, SAVE_DIR)

        return self.get()





# ----------------------------------------------------------------

api.add_resource(Videos, '/videos', methods=['GET', 'POST'])
api.add_resource(Video, '/video/<video_filename>', methods=['GET', 'DELETE'])

# -----------------------------------------------------------------


def start_video_server():
    '''Start a simple HTTP video server for dealing with downloads.'''
    os.chdir(SAVE_DIR)
    print('> Launching simple HTTP server for video downloads.')
    video_server = Popen('http-server', '-p', '2007')

    # Now go back to the original root.
    os.chdir(ROOT_DIR)



if __name__ == '__main__':

    # Launch the server.
    if DEV:
        app.run(port=PORT, debug=True)
    else:
        wsgi.server(eventlet.listen(('localhost', PORT)), app)


