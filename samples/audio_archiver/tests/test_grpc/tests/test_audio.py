

import unittest
import sys
import os

test_dir_directory: str = os.path.dirname(__file__)
test_dir_directory = os.path.dirname(test_dir_directory)
test_dir_directory = test_dir_directory + "/test_grpc"

sys.path.append(test_dir_directory)

from client import audio

class TestAudio(unittest.TestCase):

    def test_create(self):
        obj: dict = {
            "title": "some_title_from_integration_testing",
            "channel_id": 3,
            "status": "some status from integration testing",
            "duration": "some duration from integration testing",
            "url": "some url from integration testing",
        }

        response = audio.create_audio(obj)
        self.assertTrue("err" not in response.msg.lower())

    def test_read(self):
        response = audio.read_audio(id=2)
        self.assertTrue(response.audio_object.title != None)
        self.assertTrue("err" not in response.msg)

    def test_update(self):
        obj: dict = {
            "title": "some_updated_audio_from_integration_testing",
            "channel_id": 2,
            "status": "some updated audio status from integration testing",
            "duration": "more than two seconds",
            "url": "no"
        }

        response = audio.update_audio(id=5, audio=obj)
        self.assertTrue("err" not in response.msg)

    def test_delete(self):
        response = audio.delete_audio(id=7)
        self.assertTrue("err" not in response.msg)

    def test_read_list(self):
        response = audio.read_audio_list()
        self.assertTrue("err" not in response.msg)
        self.assertTrue(len(response.audio_objects) > 0)
