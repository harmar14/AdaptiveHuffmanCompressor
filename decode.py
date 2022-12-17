import os
from sys import argv
from bitFileStream import BitFileStream
from huffmanTree import HuffmanTree

class Decoder:
    def __init__(self):
        self.tree = HuffmanTree(1)

    def decodeFile(self, fileName, outFileName):
        if not os.path.exists(fileName):
            print('File is not found')
            return
        readFile = BitFileStream(fileName, 'rb')
        writeFile = open(outFileName, 'wb')
        self.tree.counter = int(readFile.read(32), 2)
        while True:
            char = self.tree.decode(readFile)
            if not char:
                break
            writeFile.write(char)
        readFile.close()
        writeFile.close()

if __name__ == '__main__':
    script, fileName = argv
    fileName = './' + fileName
    outputFileName = fileName + '_decoded'
    decoder = Decoder()
    decoder.decodeFile(fileName, outputFileName)
    print('Completed')