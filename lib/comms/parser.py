try:
    import ustruct as struct
except ImportError:
    import struct

from comms.protocol import (
    HEADER_SIZE,
    MAGIC_HEADER,
    MAX_PAYLOAD_SIZE,
    MIN_PACKET_SIZE,
    Packet,
    calc_crc8,
)


class PacketParser:
    """
    Sliding-window binary packet parser for MicroPython UART streams.
    Recovers frame alignment and validates CRC-8 with minimal heap allocations.
    """

    def __init__(self) -> None:
        self._buffer = bytearray()

    def feed(self, chunk: bytes) -> list:
        """
        Feed incoming serial bytes into the parser.
        Returns a list of complete, CRC-validated Packet instances.
        """
        self._buffer.extend(chunk)
        packets = []

        while len(self._buffer) >= MIN_PACKET_SIZE:
            # 1. Slide window to locate frame sync header (0xAA 0x55)
            if self._buffer[0] != MAGIC_HEADER[0] or self._buffer[1] != MAGIC_HEADER[1]:
                del self._buffer[0]
                continue

            # 2. Check payload length bounds
            payload_len = self._buffer[2]
            if payload_len > MAX_PAYLOAD_SIZE:
                # Corrupted length, slide past false positive header
                del self._buffer[0]
                continue

            total_len = HEADER_SIZE + payload_len + 1  # Header + Payload + CRC8

            # Wait for entire packet to arrive
            if len(self._buffer) < total_len:
                break

            # 3. Validate CRC-8 over [LENGTH, SEQ, CMD, PART, PAYLOAD]
            body = self._buffer[2 : total_len - 1]
            received_crc = self._buffer[total_len - 1]

            if calc_crc8(body) == received_crc:
                # Extract header fields
                _, seq, cmd, part = struct.unpack("<BBBB", self._buffer[2:6])
                payload = bytes(self._buffer[6 : total_len - 1])

                packets.append(Packet(cmd=cmd, part=part, payload=payload, seq=seq))
                del self._buffer[:total_len]
            else:
                # CRC failed; false positive header or corrupted bytes
                del self._buffer[0]

        return packets

    def clear(self) -> None:
        """Clears the internal parse buffer."""
        self._buffer = bytearray()

