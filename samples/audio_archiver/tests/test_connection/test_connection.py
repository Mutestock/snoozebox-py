import unittest
import sys
import os
import nose2


#test_dir_directory: str = os.path.dirname(__file__)
#for _ in range(2):
#    test_dir_directory = os.path.dirname(test_dir_directory)
#test_dir_directory = test_dir_directory + "/audio_archiver"
#
#from connection.pg_connection import db_init, engine
#from sqlalchemy_utils import create_database, drop_database, database_exists
#
#sys.path.append(test_dir_directory)
#
#class TestConnection(unittest.TestCase):
#    
#    
#    def setUp(self):
#        if not database_exists(engine.url):
#            create_database(engine.url)
#        db_init()
#
#    def tearDown(self):
#        drop_database(engine.url)
#    
#    def test_pg_connection(self):
#        self.assertTrue(database_exists(engine.url))
#        
#    def test_redis_connection(self):
#        pass
    
    