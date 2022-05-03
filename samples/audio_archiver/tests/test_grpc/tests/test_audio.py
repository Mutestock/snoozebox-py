import unittest
import sys
import os

#from test_grpc.client.audio import create_audio

test_dir_directory: str = os.path.dirname(__file__)
test_dir_directory = os.path.dirname(test_dir_directory)
test_dir_directory = test_dir_directory + "/test_grpc"

sys.path.append(test_dir_directory)

from client import audio
from protogen import audio_pb2

class TestAudio(unittest.TestCase):

    def test_create(self):
        new_audio_object = audio_pb2.NewAudioObject(
            title="some_title_from_integration_testing",
            channel_id=3,
            status="some status from integration testing",
            duration="some duration from integration testing",
            url="some url from integration testing",
        )
        create_audio_request = audio_pb2.CreateAudioRequest(
            new_audio_object=new_audio_object
        )
        
        response = audio.create_audio(create_audio_request)
        print(response.msg)
        self.assertTrue("err" not in response.msg.lower())
        
        
    
    def test_read(self):
        stub = audio._create_stub()
        self.assertTrue(stub!=None)
        self.assertTrue(2==1)

    def test_update(self):
        pass

    def test_delete(self):
        pass

    def test_read_list(self):
        pass
