

import unittest
import sys
import os

test_dir_directory: str = os.path.dirname(__file__)
test_dir_directory = os.path.dirname(test_dir_directory)
test_dir_directory = test_dir_directory + "/test_grpc"

sys.path.append(test_dir_directory)

from client import channel

class TestChannel(unittest.TestCase):

    def test_create(self):
        obj: dict = {
            "title": "some_title_from_integration_testing",
            "channel_is_alive": True,
            "url": "some url from integration testing",
        }

        response = channel.create_channel(obj)
        self.assertTrue("err" not in response.msg.lower())

    def test_read(self):
        response = channel.read_channel(id=2)
        self.assertTrue(response.channel_object.title != None)
        self.assertTrue("err" not in response.msg)

    def test_update(self):
        obj: dict = {
            "title": "some_updated_channel_from_integration_testing",
            "channel_is_alive": True,
            "url": "no"
        }

        response = channel.update_channel(id=5, channel=obj)
        self.assertTrue("err" not in response.msg)

    def test_delete(self):
        response = channel.delete_channel(id=7)
        self.assertTrue("err" not in response.msg)

    def test_read_list(self):
        response = channel.read_channel_list()
        self.assertTrue("err" not in response.msg)
        self.assertTrue(len(response.channel_objects) > 0)
