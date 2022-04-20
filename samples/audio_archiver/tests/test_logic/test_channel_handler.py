
import unittest
import sys
import os

test_dir_directory = os.path.dirname(__file__)
test_dir_directory = os.path.dirname(test_dir_directory)
test_dir_directory = os.path.dirname(test_dir_directory)
test_dir_directory = test_dir_directory + "/audio_archiver"

sys.path.append(test_dir_directory)

from models.channel import Channel
from logic.handlers.audio_handler import AudioHandler


class TestChannelArchiver(unittest.TestCase):
    
    audio_handler = AudioHandler()
    
    def test_create_channel(self):
        channel = Channel(title="stuff", channel_is_alive=True, url=True)
        self.audio_handler.crud_component.create(channel.__dict__)
    
    
    def test_read_channel(self):
        pass
    
    
    def test_update_channel(self):
        pass
    
    
    def test_delete_channel(self):
        pass
    
    
    def test_read_channel_list(self):
        pass