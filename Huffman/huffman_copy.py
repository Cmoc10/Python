import os
import sys
import marshal
import array
import heapq

try:
    import cPickle as pickle
except:
    import pickle

class huffNode:
    def __init__(self,char,freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def huffSearch(huffTree, target):
    #get root outa there
    root = heapq.heappop(huffTree)
    queue = [(root,"")]
    while queue:
        curNode = queue[0][0]
        curString = queue[0][1]
        if curNode.char == None:
            if curNode.left:
                queue.append((curNode.left, curString + "0"))
            if curNode.right:
                queue.append((curNode.right, curString + "1"))
        elif curNode.char == target:
            heapq.heappush(huffTree, root)
            return curString
        else:
            if curNode.left:
                queue.append((curNode.left, curString + "0"))
            if curNode.right:
                queue.append((curNode.right, curString + "1"))
        queue.pop(0)
    #put root back in there
    heapq.heappush(huffTree, root)
    print(target + "not found")
    return ""
    
def copyArray(arr):
    myArray = array.array("B")
    for item in arr:
        myArray.append(item)
    return myArray

def binHuffSearch(huffTree, target):
    #get root outa there
    root = heapq.heappop(huffTree)
    compressed = array.array('B')
    queue = [(root,compressed)]
    while queue:
        curNode = queue[0][0]
        curString = queue[0][1]
        if curNode.char == None:
            if curNode.left:
                curString.append(0b0)
                queue.append((curNode.left, copyArray(curString)))
                curString.pop(-1)
            if curNode.right:
                curString.append(0b1)
                queue.append((curNode.right, copyArray(curString)))
                curString.pop(-1)
        elif curNode.char == target:
            heapq.heappush(huffTree, root)
            return curString
        else:
            if curNode.left:
                curString.append(0b0)
                queue.append((curNode.left, curString))
                curString.pop(-1)
            if curNode.right:
                curString.append(0b1)
                queue.append((curNode.right, curString))
                curString.pop(-1)
        queue.pop(0)
    #put root back in there
    heapq.heappush(huffTree, root)
    print(target + "not found")
    return array.array("B")

def createHuffTree(msg):
    huffmanTree = []
    heapq.heapify(huffmanTree)
    # Initializes an array to hold the compressed message.
    frequencies = {}
    #get frequencies of every character
    for char in msg:
        if char in frequencies:
            frequencies[char] += 1
        else:
            frequencies[char] = 1
    sortedFrequencies = {}
    for key in sorted(frequencies, key=frequencies.get): 
        sortedFrequencies[key] = frequencies[key]
    #construct min heap
    for key in sortedFrequencies:
        node = huffNode(key, sortedFrequencies[key])
        heapq.heappush(huffmanTree, node)    
    while len(huffmanTree) > 1:
        leftChild = heapq.heappop(huffmanTree)
        rightChild = heapq.heappop(huffmanTree)
        #constructNewNode
        newNode = huffNode(None, leftChild.freq + rightChild.freq)
        newNode.left = leftChild
        newNode.right = rightChild
        heapq.heappush(huffmanTree, newNode)
    return huffmanTree

def code(msg):
    codedString = ""
    huffmanTree = createHuffTree(msg)
    seen = {}
    for char in msg:
        if char not in seen:
            seen[char] = huffSearch(huffmanTree, char)
        codedString += seen[char]

    return codedString, huffmanTree

def decode(msg, decoderRing):
    decodedString = ""
    root = heapq.heappop(decoderRing)
    heapq.heappush(decoderRing,root)
    curNode = root
    for char in msg:
        if curNode.left == None and curNode.right == None:
            decodedString += curNode.char
            curNode = root
        if char == "0":
            curNode = curNode.left
        elif char == "1":
            curNode = curNode.right
    if curNode.left == None and curNode.right == None:
            decodedString += curNode.char
            curNode = root
    return decodedString

def compress(msg):
    compressed = array.array('B')
    huffmanTree = createHuffTree(msg)
    seen = {}
    for char in msg:
        if char not in seen:
            seen[char] = binHuffSearch(huffmanTree, char)
        compressed.extend(seen[char])
    return compressed, huffmanTree

def decompress(msg, decoderRing):

    # Represent the message as an array
    byteArray = array.array('B',msg)

    decodedString = ""
    root = heapq.heappop(decoderRing)
    heapq.heappush(decoderRing,root)
    finalArray = array.array("B")
    curNode = root
    for byte in byteArray:
        if curNode.left == None and curNode.right == None:
            decodedString += chr(curNode.char)
            finalArray.append(curNode.char)
            curNode = root
        if byte == 0b0:
            curNode = curNode.left
        elif byte == 0b1:
            curNode = curNode.right
    if curNode.left == None and curNode.right == None:
            decodedString += chr(curNode.char)
            finalArray.append(curNode.char)
            curNode = root
    return finalArray

def usage():
    sys.stderr.write("Usage: {} [-c|-d|-v|-w] infile outfile\n".format(sys.argv[0]))
    exit(1)

if __name__=='__main__':
    if len(sys.argv) != 4:
        usage()
    opt = sys.argv[1]
    compressing = False
    decompressing = False
    encoding = False
    decoding = False
    if opt == "-c":
        compressing = True
    elif opt == "-d":
        decompressing = True
    elif opt == "-v":
        encoding = True
    elif opt == "-w":
        decoding = True
    elif opt == "-n":
        enc, tree = code("hello world I am colin and this is my encoded message")
        print(enc)
        dec = decode(enc, tree)
        print(dec)
        compr, tree = compress("hello world I am colin and this is my encoded message")
        print(compr)
        msg = decompress(compr, tree)
        print(msg)
    else:
        usage()

    infile = sys.argv[2]
    outfile = sys.argv[3]
    assert os.path.exists(infile)

    if compressing or encoding:
        fp = open(infile, 'rb')
        msg = fp.read()
        fp.close()
        if compressing:
            compr, tree = compress(msg)
            fcompressed = open(outfile, 'wb')
            marshal.dump((pickle.dumps(tree), compr), fcompressed)
            fcompressed.close()
        else:
            enc, tree = code(msg)
            print(msg)
            fcompressed = open(outfile, 'wb')
            marshal.dump((pickle.dumps(tree), enc), fcompressed)
            fcompressed.close()
    elif decompressing or decoding:
        fp = open(infile, 'rb')
        pickleRick, compr = marshal.load(fp)
        tree = pickle.loads(pickleRick)
        fp.close()
        if decompressing:
            msg = decompress(compr, tree)
        else:
            msg = decode(compr, tree)
            print(msg)
        fp = open(outfile, 'wb')
        fp.write(msg)
        fp.close()