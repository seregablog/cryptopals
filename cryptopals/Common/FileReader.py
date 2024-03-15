import base64
import os


class FileReader:
    def readLines(self, dir: str, filename: str) -> list:
        with open(self.__getFullPath(dir, filename)) as f:
            lines = f.read().splitlines()
        return lines

    def readBase64Lines(self, dir: str, filename: str) -> list:
        with open(self.__getFullPath(dir, filename)) as f:
            lines = f.read().splitlines()

        decodedLines = []
        for line in lines:
            decodedLines.append(bytearray(base64.b64decode(line)))
        return decodedLines

    def readBase64Line(self, dir: str, filename: str) -> bytearray:
        with open(self.__getFullPath(dir, filename), 'r') as file:
            data = file.read()

        return bytearray(base64.b64decode(data))

    def __getFullPath(self, dir: str, filename: str) -> str:
        return os.path.join(os.path.join(os.path.dirname(dir), filename))
