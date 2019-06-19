import asyncio
import unittest


class TestCase(unittest.TestCase):
    loop = None

    @classmethod
    def setUpClass(cls):
        cls.loop = asyncio.new_event_loop()

    @classmethod
    def tearDownClass(cls):
        cls.loop.close()
