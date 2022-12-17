import os
from sys import argv
from bitFileStream import BitFileStream
from huffmanTree import HuffmanTree

class Encoder:
    def __init__(self):
        self.tree = HuffmanTree(1)

    def encodeFile(self, fileName, outFileName):
        if not os.path.exists(fileName):
            print('File is not found')
            return
        readFile = open(fileName, 'rb')
        writeFile = BitFileStream(outFileName, 'wb')
        writeFile.write('{0:032b}'.format(os.stat(fileName).st_size))
        while True:
            code = self.tree.encode(readFile)
            if not code:
                break
            writeFile.write(code)
        readFile.close()
        writeFile.close()

if __name__ == '__main__':
    script, fileName = argv
    #fileName = './' + str(input("File name: "))
    fileName = './' + fileName
    outputFileName = fileName + '_encoded'
    encoder = Encoder()
    encoder.encodeFile(fileName, outputFileName)
    print('Completed')