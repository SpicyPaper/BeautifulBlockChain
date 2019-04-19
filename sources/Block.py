import hashlib

class Block:

    blockNumber = 0

    def __init__(self, header=None, transactions=None):
        self.blockNumber = Block.blockNumber
        Block.blockNumber += 1
        self.header = header
        self.transactions = transactions
        self.nonce = None
        self.hash = None


    def __str__(self):
        string = ""
        string += "/**************Block %d***************\\\n" % self.blockNumber
        string += str(self.header) + "\n"
        string += "-----------------------------------\n"

        for transaction in self.transactions:
            string += str(transaction) + "\n"

        string += "-----------------------------------\n"
        string += str(self.nonce) + "\n"
        string += "-----------------------------------\n"
        string += str(self.hash) + "\n"
        string += "\**********************************/\n"

        return string


    def try_hash(self, nonce):
        plain = ""
        plain += str(self.header)

        for transaction in self.transactions:
            plain += transaction

        plain += str(nonce)

        #print(plain)

        h = hashlib.sha256()
        h.update(plain.encode())

        return h.hexdigest()


    def validate(self, nonce): # TODO : add signature
        self.nonce = nonce
        self.hash = self.try_hash(nonce)
        return self.hash


    def get_hash(self):
        return self.hash


if __name__ == "__main__":
    block = Block("coucou", ["a 4 to b", "v 5 to x", "c 100 to b"])

    print(block)

    print(block.try_hash("1"))

    block.validate("test_nonce")

    print(block)
