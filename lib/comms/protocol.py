try:
    from micropython import const
except ImportError:
    def const(x):
        return x

try:
    import ustruct as struct
except ImportError:
    import struct

# ==============================================================================
# Protocol Constants
# ==============================================================================
MAGIC_HEADER = b"\xaa\x55"
HEADER_SIZE = const(6)
MIN_PACKET_SIZE = const(7)  # HEADER_SIZE + 1 CRC
MAX_PAYLOAD_SIZE = const(240)

# Command Types
CMD_STOP = const(0)
CMD_PING = const(1)
CMD_RUN = const(2)
CMD_ACK = const(3)
CMD_TELEMETRY = const(4)
CMD_CONFIG = const(5)

# Subsystem Part Types
PART_ALL = const(0)
PART_CHASSIS = const(1)
PART_CONVEYOR = const(2)
PART_SHOOTER = const(3)
PART_SENSORS = const(4)

# ==============================================================================
# CRC-8 Lookup Table (Polynomial 0x07, Initial 0x00)
# Stored as bytes object (256 bytes) for zero-heap memory efficiency
# ==============================================================================
CRC8_TABLE = (
    b"\x00\x07\x0e\t\x1c\x1b\x12\x158?61$#*-pw~ylkbeHOFATSZ]"
    b"\xe0\xe7\xee\xe9\xfc\xfb\xf2\xf5\xd8\xdf\xd6\xd1\xc4\xc3\xca\xcd"
    b"\x90\x97\x9e\x99\x8c\x8b\x82\x85\xa8\xaf\xa6\xa1\xb4\xb3\xba\xbd"
    b"\xc7\xc0\xc9\xce\xdb\xdc\xd5\xd2\xff\xf8\xf1\xf6\xe3\xe4\xed\xea"
    b"\xb7\xb0\xb9\xbe\xab\xac\xa5\xa2\x8f\x88\x81\x86\x93\x94\x9d\x9a"
    b"' ).;<52\x1f\x18\x11\x16\x03\x04\r\nWPY^KLEBohafst}z"
    b"\x89\x8e\x87\x80\x95\x92\x9b\x9c\xb1\xb6\xbf\xb8\xad\xaa\xa3\xa4"
    b"\xf9\xfe\xf7\xf0\xe5\xe2\xeb\xec\xc1\xc6\xcf\xc8\xdd\xda\xd3\xd4"
    b"ing`ur{|QV_XMJCD\x19\x1e\x17\x10\x05\x02\x0b\x0c!&/(=:34"
    b"NI@GRU\\[vqx\x7fjmdc>907\"%,+\x06\x01\x08\x0f\x1a\x1d\x14\x13"
    b"\xae\xa9\xa0\xa7\xb2\xb5\xbc\xbb\x96\x91\x98\x9f\x8a\x8d\x84\x83"
    b"\xde\xd9\xd0\xd7\xc2\xc5\xcc\xcb\xe6\xe1\xe8\xef\xfa\xfd\xf4\xf3"
)


def calc_crc8(data: bytes | bytearray | memoryview) -> int:
    """Calculate CRC-8 checksum over bytes, bytearray, or memoryview."""
    crc = 0
    for b in data:
        crc = CRC8_TABLE[crc ^ b]
    return crc


# ==============================================================================
# MicroPython Packet Class
# ==============================================================================
class Packet:
    """
    Lightweight packet representation for MicroPython:
    [MAGIC: 2B][LENGTH: 1B][SEQ: 1B][CMD: 1B][PART: 1B][PAYLOAD: NB][CRC8: 1B]
    """

    __slots__ = ("cmd", "part", "payload", "seq")

    def __init__(self, cmd: int, part: int, payload: bytes = b"", seq: int = 0) -> None:
        self.cmd = cmd
        self.part = part
        self.payload = payload
        self.seq = seq & 0xFF

    def encode(self) -> bytes:
        """Serializes the packet into framed binary wire format."""
        body = struct.pack("<BBBB", len(self.payload), self.seq, self.cmd, self.part) + self.payload
        crc = calc_crc8(body)
        return MAGIC_HEADER + body + bytes([crc])

    def __repr__(self) -> str:
        return f"<Packet seq={self.seq} cmd={self.cmd} part={self.part} len={len(self.payload)}>"

