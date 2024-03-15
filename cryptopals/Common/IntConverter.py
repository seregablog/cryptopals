class IntConverter:
    def bytesToInt(self, bytes: bytearray) -> int:
        return int.from_bytes(bytes, 'big')

    def intToBytes(self, value: int, bytes: int = 128) -> bytearray:
        return bytearray(value.to_bytes(bytes, 'big'))
