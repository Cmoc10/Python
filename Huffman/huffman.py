import os
import sys
import marshal
import array
import heapq

try:
    import cPickle as pickle
except:
    import pickle

'''
    INVARIANTS: 
    HUFFMAN ALGORITHM SPECIFIC:
    1. The encoded message is a more compact representation of the original. 
    INITIALIZATION: At the start of the encoding process, the encoded message is empty, and the original message is unchanged, making the empty message smaller than the original one.
    MAINTENANCE: During each step of the encoding process, characters from the original message are replaced with their corresponding Huffman codes, which are shorter bit sequences. This replacement reduces the overall size of the message.
    TERMINATION: Once all characters have been encoded, the process is complete, the encoded message is finalized, and is more compact than the original.
   
    2. The more frequent characters in the original message have shorter codes in the encoded message.
    INITIALIZATION: At the start of the encoding process, no characters have any assigned codes, making them automatically shorter than any potential code (since 'empty')
    MAINTENANCE: During each step of the encoding process, characters are assigned codes based on their frequencies, with the more frequent characters receiving the shorter codes.
    TERMINATION: At the end of the encoding process, all characters have been assigned codes, and the more frequent characters have shorter codes in the encoded message.
    
    3. The less frequent characters in the original message have longer codes in the encoded message.
    INITIALIZATION: At the start of the encoding process, no characters have any assigned codes, making them automatically longer than any potential code (since 'empty')
    MAINTENANCE: During each step of the encoding process, characters are assigned codes based on their frequencies, with the less frequent characters receiving the longer codes.
    TERMINATION: At the end of the encoding process, all characters have been assigned codes, and the less frequent characters have longer codes in the encoded message.
    
    HEAP IMPLEMENTATION SPECIFIC:
    4. The priorities of the children of the node are always greater than or equal to the priority of the node itself.
    INITIALIZATION: At the start of the program, the heap is empty and will satisfy the heap property automatically.
    MAINTENANCE: During each insertion or deletion operation, the heap property is maintained by ensuring that the priorities of the children of any node are always greater than or equal to the priority of the node itself.
    TERMINATION: At the end of the program, the heap property is preserved, ensuring that the priorities of the children of each node are always greater than or equal to the priority of the node itself.
    
    5. The different paths from root to leaf deviate in height by at most one. At the bottom of the tree there may be some missing leaves, these are to the right to all of the leaves that are present.
    INITIALIZATION: At the start of the program, the tree is empty and will satisfy the balanced tree property automatically.
    MAINTENANCE: During each insertion or deletion operation, the balanced tree property is maintained by ensuring that the heights of the two child subtrees of any node differ by at most one.
    TERMINATION: At the end of the program, the balanced tree property is preserved, ensuring that the heights of the two child subtrees of each node differ by at most one.
'''

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
    huffmanTree = createHuffTree(msg)
    seen = {}
    bitstring = ""
    for char in msg:
        if char not in seen:
            seen[char] = huffSearch(huffmanTree, char)
        bitstring += seen[char]
    
    # Pack bits into bytes
    compressed = array.array('B')
    for i in range(0, len(bitstring), 8):
        byte = bitstring[i:i+8]
        byte = byte.ljust(8, '0')  # Pad last byte if needed
        compressed.append(int(byte, 2))
    
    # Store the number of valid bits in the last byte
    num_padding = (8 - len(bitstring) % 8) % 8
    
    return (compressed, num_padding), huffmanTree

def decompress(msg, decoderRing):
    compressed, num_padding = msg
    byteArray = array.array('B', compressed)
    
    # Convert bytes back to bit string
    bitstring = ""
    for byte in byteArray:
        bitstring += format(byte, '08b')
    
    # Remove padding from the last byte
    if num_padding > 0:
        bitstring = bitstring[:-num_padding]
    
    decodedString = ""
    root = heapq.heappop(decoderRing)
    heapq.heappush(decoderRing, root)
    finalArray = array.array("B")
    curNode = root
    
    for bit in bitstring:
        if curNode.left == None and curNode.right == None:
            decodedString += chr(curNode.char)
            finalArray.append(curNode.char)
            curNode = root
        if bit == "0":
            curNode = curNode.left
        elif bit == "1":
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