import unittest
import zerome

class TestZerome(unittest.TestCase):

    def test_zerome_erases_memory(self):
        secret_string = "super secret stuff"

        zerome.zerome_string(secret_string)

        self.assertEquals(secret_string, '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

    def test_zerome_works_for_unicode_strings(self):
        secret_string = u"super secret stuff"

        zerome.zerome_unicode_string(secret_string)

        self.assertEquals(secret_string, '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

