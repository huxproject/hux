import asyncio
import socket
from unittest import skipIf

from sunshinesocks.socks import SunshinesocksProtocol
from sunshinesocks.test import TestCase


class SocksTestCase(TestCase):
    server = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        async def start_server(loop):
            server = await loop.create_server(
                SunshinesocksProtocol, 'localhost', 0
            )

            await server.start_serving()
            return server

        cls.server = cls.loop.run_until_complete(start_server(cls.loop))

    def test_socks(self):
        async def test(server_socket):
            s = socket.socket(server_socket.family)
            with s:
                s.setblocking(False)
                await self.loop.sock_connect(s, server_socket.getsockname())
                await self.loop.sock_sendall(s, b'\x05\x01\x00')
                d = await self.loop.sock_recv(s, 100)
                self.assertEqual(d, b'\x05\x00')

        for ss in self.server.sockets:
            self.loop.run_until_complete(test(ss))

    @skipIf(
        hasattr(asyncio, 'BufferedProtocol'),
        'asyncio has BufferedProtocol')
    def test_buffered_protocol_missing(self):
        self.assertTrue(issubclass(SunshinesocksProtocol, asyncio.Protocol))
        self.assertFalse(hasattr(SunshinesocksProtocol, 'get_buffer'))
        self.assertFalse(hasattr(SunshinesocksProtocol, 'buffer_updated'))

    @classmethod
    def tearDownClass(cls):

        async def close_server(server):
            server.close()
            await server.wait_closed()
        cls.loop.run_until_complete(close_server(cls.server))
        super().tearDownClass()
