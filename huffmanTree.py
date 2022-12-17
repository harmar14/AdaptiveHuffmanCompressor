from queue import Queue

class HuffmanTree:
    def __init__(self, order = 1):
        self.root = Node()
        self.emptyNode = self.root
        self.bytes = {}
        self.order = order
        self.counter = 0

    def addChar(self, char):
        node = Node(char)
        self.bytes[char] = node
        self.emptyNode.setLeft(Node())
        self.emptyNode.setRight(node)
        self.emptyNode = self.emptyNode.left  

    def encode(self, file):
        char = b''
        char = file.read(self.order)
        if char == b'':
            return b''
        if not (char in self.bytes):
            code = self.huffmanCode(self.emptyNode)
            for i in range(len(char)):
                code += '{0:08b}'.format(char[i])
            self.addChar(char)
        else:
            node = self.bytes[char]
            code = self.huffmanCode(node)
        self.updateHuffmanTree(self.bytes[char])
        return code

    def endOfFile(self):
        return self.huffmanCode(self.emptyNode)

    def huffmanCode(self, node):
        code = ''
        if node == self.root:
            return '0'
        parent = node.parent
        while parent:
            if parent.left == node:
                code += '0'
            else:
                code += '1'
            node = parent
            parent = node.parent
        return code[::-1]

    def findTheFarthestNode(self, weight):
        q = Queue()
        q.put(self.root)
        while not q.empty():
            node = q.get()
            if node.weight == weight:
                return node
            if node.right:
                q.put(node.right)
            if node.left:
                q.put(node.left)

    def updateHuffmanTree(self, node):
        while node:
            node.swap(self.findTheFarthestNode(node.weight))
            node.weight += 1
            node = node.parent

    def decode(self, file):
        if self.counter <= 0:
            return ''
        node = self.reHuffmanCode(file)
        if node == self.emptyNode:
            code = ''
            for i in range(self.order):
                code += file.read(8)
            char = b''
            for i in range(int(len(code)/8)):
                ch = int(code[i*8:i*8+8], 2)
                char += ch.to_bytes(1, byteorder='little')
            self.addChar(char)
        else:
            char = node.char
        self.updateHuffmanTree(self.bytes[char])
        self.counter -= len(char)
        return char

    def reHuffmanCode(self, file):
        if self.root.hasNoChild():
            file.read(1)
            return self.root
        node = self.root
        while not node.hasNoChild():
            ch = file.read(1)
            if ch == '1':
                node = node.right
            elif ch == '0':
                node = node.left
            else:
                return self.emptyNode
        return node
    
class Node:
    def __init__(self, char=None):
        self.weight = 0
        self.parent = None
        self.right = None
        self.left = None
        self.level = 0
        if char == None:
            self.char = b'*'
        else:
            self.char = char

    def setLeft(self, node):
        self.left = node
        node.parent = self
        node.updateLevel()

    def setRight(self, node):
        self.right = node
        node.parent = self
        node.updateLevel()

    def replaceChild(self, child, node):
        if self.left == child:
            self.setLeft(node)
        elif self.right == child:
            self.setRight(node)

    def updateLevel(self):
        self.level = self.parent.level+1
        if self.right:
            self.right.updateLevel()
        if self.left:
            self.left.updateLevel()

    def hasNoChild(self):
        return self.left == None and self.right == None

    def checkIfAncestor(self, node):
        ancestor = self.parent
        while ancestor:
            if ancestor == node:
                return True
            ancestor = ancestor.parent
        return False

    def swap(self, node):
        if self == node or node.checkIfAncestor(self) or self.checkIfAncestor(node):
            return
        parent1 = self.parent
        parent2 = node.parent
        parent2.replaceChild(node, self)
        parent1.replaceChild(self, node)