import hashlib
import time
import datetime

class Block:

    blockNumber = 0

    def __init__(self, prev_hash=None, transactions=None):
        self.blockNumber = Block.blockNumber
        Block.blockNumber += 1
        self.prev_hash = prev_hash
        ts = time.time()
        self.timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        self.merkle_root = None
        #self.difficulty = 0
        self.nonce = None
        self.transactions = transactions
        self.hash = None
        # TODO : total hash = hash du header
        if (self.transactions != None):
            self.compute_merkle_root()


    def __str__(self):
        string = ""
        string += "/**************Block %d***************\\\n" % self.blockNumber
        string += str(self.prev_hash) + "\n"
        string += str(self.timestamp) + "\n"
        string += str(self.merkle_root) + "\n"
        string += str(self.nonce) + "\n"
        string += "-----------------------------------\n\n"

        for transaction in self.transactions:
            string += str(transaction) + "\n\n"

        string += "-----------------------------------\n"
        string += str(self.hash) + "\n"
        string += "\**********************************/\n"

        return string


    def try_hash(self, nonce):
        plain = ""
        plain += str(self.prev_hash)
        plain += str(self.timestamp)
        plain += str(self.merkle_root)
        plain += str(nonce)

        #print(plain)

        h = hashlib.sha256()
        h.update(plain.encode())

        return h.hexdigest()


    def validate(self, nonce): # TODO : add signature ??????
        self.nonce = nonce
        self.hash = self.try_hash(nonce)
        return self.hash


    def get_hash(self):
        return self.hash


    def compute_merkle_root(self):
        merkle_hashes = self.transactions.copy()
        merkle_hashes_length = len(merkle_hashes)

        h = hashlib.sha256()
        for i in range(merkle_hashes_length):
            h.update(merkle_hashes[i].encode())
            merkle_hashes[i] = h.hexdigest()

        while merkle_hashes_length > 1:
            if merkle_hashes_length % 2 != 0:
                merkle_hashes.append("0")
                merkle_hashes_length += 1

            for i in range(int(merkle_hashes_length/2)):
                merkle_hashes[i] = merkle_hashes[2*i] + merkle_hashes[2*i+1]
                h.update(merkle_hashes[i].encode())
                merkle_hashes[i] = h.hexdigest()
            merkle_hashes_length /= 2

        self.merkle_root =  merkle_hashes[0]


if __name__ == "__main__":
    block = Block("coucou", ["a 4 to b", "v 5 to x", "c 100 to b", "c 100 to b"])

    print(block)

    print(block.try_hash("1"))

    block.compute_merkle_root()
    block.validate("test_nonce")

    print(block)
