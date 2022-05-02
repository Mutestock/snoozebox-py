from snoozelib import __version__
import os
import sys
import unittest

src_dir = os.path.dirname(os.path.dirname(__file__))+"/snoozelib"

sys.path.append(src_dir)

from interpret import _get_table_name


class TestSnoozeLib(unittest.TestCase):
    

    def test_get_table_name(self):
        test_sql = f"""
        CREATE TABLE some_table_name(
            id SERIAL UNIQUE NOT NULL
        );
        """
        self.assertEqual(_get_table_name(test_sql), "some_table_name")
        
        
        

