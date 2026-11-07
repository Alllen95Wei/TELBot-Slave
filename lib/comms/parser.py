try:
    from micropython import const
except ImportError:
    def const(x):
        return x

from comms.protocol import (
    HEADER_SIZE,
    MAGIC_HEADER,
    MAX_PAYLOAD_SIZE,
    MIN_PACKET_SIZE,
    Packet,
    calc_crc8,
)

_INITIAL_BUFFER_SIZE = const(1024)


class PacketParser:
    """
    Sliding-window binary packet parser for MicroPython UART streams.
    Recovers frame alignment and validates CRC-8 with minimal heap allocations.
    """

    def __init__(self, buffer_size: int = _INITIAL_BUFFER_SIZE) -> None:
        if buffer_size < MIN_PACKET_SIZE:
            buffer_size = _INITIAL_BUFFER_SIZE
        self._buffer = bytearray(buffer_size)
        self._mv = memoryview(self._buffer)
        self._head = 0
        self._tail = 0

    def _append(self, chunk: bytes | bytearray | memoryview) -> None:
        chunk_len = len(chunk)
        if self._head == self._tail:
            self._head = 0
            self._tail = 0

        cap = len(self._buffer)
        if self._tail + chunk_len > cap:
            # Compact unread bytes to the front of the buffer first
            if self._head > 0:
                rem = self._tail - self._head
                self._mv[:rem] = self._mv[self._head : self._tail]
                self._head = 0
                self._tail = rem

            # Grow backing buffer only if compacted space is still insufficient
            needed = self._tail + chunk_len
            if needed > cap:
                new_cap = cap * 2
                if new_cap < needed:
                    new_cap = needed
                new_buf = bytearray(new_cap)
                new_mv = memoryview(new_buf)
                if self._tail > 0:
                    new_mv[: self._tail] = self._mv[: self._tail]
                self._buffer = new_buf
                self._mv = new_mv

        new_tail = self._tail + chunk_len
        self._mv[self._tail : new_tail] = chunk
        self._tail = new_tail

    def feed(self, chunk: bytes | bytearray | memoryview) -> list[Packet]:
        """
        Feed incoming serial bytes into the parser.
        Returns a list of complete, CRC-validated Packet instances.
        """
        if not chunk:
            return []

        self._append(chunk)
        packets = []

        buf = self._buffer
        mv = self._mv
        head = self._head
        tail = self._tail

        while tail - head >= MIN_PACKET_SIZE:
            # 1. Slide window to locate frame sync header (0xAA 0x55)
            if buf[head] != MAGIC_HEADER[0] or buf[head + 1] != MAGIC_HEADER[1]:
                head += 1
                continue

            # 2. Check payload length bounds
            payload_len = buf[head + 2]
            if payload_len > MAX_PAYLOAD_SIZE:
                # Corrupted length, slide past false positive header
                head += 1
                continue

            total_len = HEADER_SIZE + payload_len + 1  # Header + Payload + CRC8

            # Wait for entire packet to arrive
            if tail - head < total_len:
                break

            # 3. Validate CRC-8 over [LENGTH, SEQ, CMD, PART, PAYLOAD]
            crc_idx = head + total_len - 1
            body = mv[head + 2 : crc_idx]
            received_crc = buf[crc_idx]

            if calc_crc8(body) == received_crc:
                # Extract header fields directly without slice allocation
                seq = buf[head + 3]
                cmd = buf[head + 4]
                part = buf[head + 5]
                payload = bytes(mv[head + HEADER_SIZE : crc_idx]) if payload_len > 0 else b""

                packets.append(Packet(cmd=cmd, part=part, payload=payload, seq=seq))
                head += total_len
            else:
                # CRC failed; false positive header or corrupted bytes
                head += 1

        if head == tail:
            self._head = 0
            self._tail = 0
        else:
            self._head = head

        return packets

    def clear(self) -> None:
        """Clears the internal parse buffer."""
        self._head = 0
        self._tail = 0

