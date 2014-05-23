import unittest
from mock import patch

import journalist

class TestDelete(unittest.TestCase):

    @patch('datetime.datetime')
    def test_delayed_delete(self, datetime):
        datetime.now.return_value = 123

        journalist.delayed_delete("some-id")

        self.assertIn(("some-id", 123), journalist.to_delete)

    @patch('datetime.datetime')
    def test_deleting_thread(self, datetime):
        datetime.now.return_value = 
        deleting_thread = journalist.DeletingThread()
        journalist.to_delete = [("some-id", timestamp)]
        deleting_thread.run()
        #verify journalist.delete_collection("some-id")
