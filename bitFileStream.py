class BitFileStream:
    
    def __init__(self, fileName, mode):
        self.file = open(fileName, mode)
        self.word = 0
        if mode[0] == 'r':
            self.position = -1
        elif mode[0] == 'w':
            self.position = 7
        self.mode = mode

    def read(self, size):
        retVal = ''
        for i in range(size):
            if self.position == -1:
                self.word = self.file.read(1)
                if self.word == b'':
                    return ''
                else:
                    self.word = ord(self.word)
                    self.position = 7
            if self.word & (1 << self.position):
                retVal += '1'
            else:
                retVal += '0'
            self.position -= 1
        return retVal

    def write(self, string):
        for char in string:
            if char == '0':
                self.word <<= 1
                self.position -= 1
            elif char == '1':
                self.word <<= 1
                self.word += 1
                self.position -= 1
            else:
                continue
            if self.position == -1:
                self.flush()
                
    def flush(self):
        if self.position != 7:
            while self.position > -1:
                self.word <<= 1
                self.position -= 1
            self.file.write(self.word.to_bytes(1, byteorder='little'))
        self.word = 0
        self.position = 7
        
    def close(self):
        if self.mode[0] == 'w':
            self.flush()
        self.file.close()