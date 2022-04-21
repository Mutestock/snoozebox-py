import unittest
import sys
import os
import nose2


test_dir_directory: str = os.path.dirname(__file__)
# for _ in range(2):
#    test_dir_directory = os.path.dirname(test_dir_directory)
test_dir_directory = os.path.dirname(test_dir_directory)
test_dir_directory = os.path.dirname(test_dir_directory)

test_dir_directory = test_dir_directory + "/audio_archiver"

print(test_dir_directory)

sys.path.append(test_dir_directory)

from models.channel import Channel
from logic.handlers.channel_handler import ChannelHandler
from connection.pg_connection import db_init, engine
from sqlalchemy_utils import create_database, drop_database, database_exists
from tests.dummy_data.dummy_data_execution import create_dummy_data
import time


class TestChannelArchiver(unittest.TestCase):

    channel_handler = ChannelHandler()

    def setUp(self):
        if not database_exists(engine.url):
            create_database(engine.url)
        db_init()
        create_dummy_data(engine, "channel")

    def tearDown(self):

        if database_exists(engine.url):
            drop_database(engine.url)

    def test_delete_channel(self):
        self.channel_handler.crud_component.delete(5)

        channel_from_database = (
            engine.connect().execute("SELECT * FROM channel WHERE id=5").fetchone()
        )
        self.assertEqual(
            channel_from_database,
        )

    def test_read_channel_list(self):
        channels = self.channel_handler.crud_component.read_list()
        self.assertEqual(len(channels), 9)

    def test_update_channel(self):
        self.channel_handler.crud_component.update(
            4,
            Channel(
                title="updated_channel", channel_is_alive=False, url="some_updated_url"
            ),
        )

        channel_from_database = (
            engine.connect()
            .execute("SELECT * FROM channel WHERE title='updated_channel'")
            .fetchone()
        )
        self.assertEqual(channel_from_database.url, "some_updated_url")

    def test_create_channel(self):
        channel = Channel(title="stuff", channel_is_alive=True, url="some url")

        self.channel_handler.crud_component.create(channel)

        channel_from_database = (
            engine.connect()
            .execute("SELECT * FROM channel WHERE url='some url'")
            .fetchone()
        )
        self.assertEqual(channel_from_database.title, "stuff")

    def test_read_channel(self):
        self.assertEqual(
            self.channel_handler.crud_component.read(3).title, "some_title_03"
        )
