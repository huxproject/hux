import logging

try:
    from asyncio import BufferedProtocol
except ImportError:
    BufferedProtocol = None
    from asyncio import Protocol
from asyncio import BaseProtocol
from enum import Enum
from enum import auto

DEFAULT_BUFFER_SIZE = 1452 * 10  # TCP 14K
ARBITRARY_BUFFER_SIZE = -1


class Stage(Enum):
    INIT = auto()
    ADDR = auto


class SunshinesocksBaseProtocol(BaseProtocol):

    def __init__(self):
        self.stage: Stage = Stage.INIT
        self.transport = None
        self.buffer = None

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        logging.debug(f"Connection from {peername} made.")
        self.transport = transport

    def _data_received(self, data):
        if self.stage == Stage.INIT:
            self._method_selection(data)
        elif self.stage == Stage.ADDR:
            self._addressing(data)

    def _method_selection(self, data):
        if data[0] != 5:
            return
        if 0 not in data[2:]:
            return
        self.transport.write(b'\x05\x00')
        self.stage = Stage.ADDR


if BufferedProtocol:
    class SunshinesocksProtocol(BufferedProtocol, SunshinesocksBaseProtocol):

        def get_buffer(self, sizehint):
            if sizehint == ARBITRARY_BUFFER_SIZE:
                sizehint = DEFAULT_BUFFER_SIZE
            self.buffer = bytearray(sizehint)
            return self.buffer

        def buffer_updated(self, nbytes):
            self._data_received(self.buffer[:nbytes])
else:
    class SunshinesocksProtocol(Protocol, SunshinesocksBaseProtocol):

        def data_received(self, data):
            self._data_received(data)
