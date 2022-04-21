import unittest
import sys
import os

test_dir_directory: str = os.path.dirname(__file__)
test_dir_directory = os.path.dirname(test_dir_directory)
test_dir_directory = os.path.dirname(test_dir_directory)
test_dir_directory = test_dir_directory + "/audio_archiver"

sys.path.append(test_dir_directory)

from models.audio import Audio
from logic.handlers.audio_handler import AudioHandler
from connection.pg_connection import db_init, engine
from sqlalchemy_utils import create_database, drop_database, database_exists
from tests.dummy_data.dummy_data_execution import create_dummy_data


class TestAudioArchiver(unittest.TestCase):

    audio_handler = AudioHandler()

    def setUp(self):
        if not database_exists(engine.url):
            create_database(engine.url)
        db_init()
        create_dummy_data(engine, "channel")
        create_dummy_data(engine, "audio")

    def tearDown(self):
        if database_exists(engine.url):
            drop_database(engine.url)

    def test_create_audio(self):
        audio = Audio(
            title="some_inserted_audio01",
            channel_id=3,
            status="some_status01",
            duration="some_duration01",
            url="some_inserted_url_01",
        )

        self.audio_handler.create(audio)
        audio_from_database = (
            engine.connect()
            .execute("SELECT * FROM audio WHERE url='some_inserted_url_01'")
            .fetchone()
        )
        self.assertEqual(audio_from_database.title, "some_inserted_audio01")

    def test_read_audio(self):
        audio_tracks = self.assertEqual(self.audio_handler.crud_components.read_list())
        self.assertEqual(len(audio_tracks), 9)

    def test_update_audio(self):
        self.audio_handler.crud_component.update(
            5,
            Audio(
                title="some_updated_audio01",
                channel_id=7,
                status="some_updated_status01",
                duration="some_updated_duration01",
                url="some_url_01",
            ),
        )
        audio_from_database = (
            engine.connect()
            .execute("SELECT * FROM audio WHERE url='some_updated_audio01'")
            .fetchone()
        )
        self.assertEqual("some_updated_audio01", audio_from_database.title)

    def test_delete_audio(self):
        self.audio_handler.crud_component.delete(5)

        audio_from_database = (
            engine.connect()
            .execute("SELECT * FROM audio WHERE url='some_url_08'")
            .fetchone()
        )

        self.assertEqual(audio_from_database)

    def test_read_audio_list(self):
        audio_tracks = self.audio_handler.crud_component.read_list()
        self.assertEqual(len(audio_tracks), 9)
