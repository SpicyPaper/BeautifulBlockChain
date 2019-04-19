from Block import Block

class Blockchain:

    def __init__(self):
        try:
            self.load_blockchain()
        except Exception as e:
            print(e)
            genesis_block = Block(0, ["genesis block"])
            genesis_block.validate("no nonce")
            self.blocks = [genesis_block]
            self.transactions = []

            # with open("../bbc/../bbc/blockchain.txt", "w") as f:
            #     f.write("/**********************************BlockChain**********************************\\\n")
            #     f.write(self.blocks[-1].__str__())



    def __str__(self):
        string = ""
        string += "/**********************************BlockChain**********************************\\\n"

        for block in self.blocks:
            string += block.__str__()
            string += "\n"

        for transaction in self.transactions:
            string += transaction
            string += "\n"

        string += "\n"

        string += "\******************************************************************************/\n"

        return string

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

        if len(self.transactions) >= 4:

            self.mining_block()

    def mining_block(self):
        prev_hash = self.blocks[-1].get_hash()
        new_block = Block(prev_hash, self.transactions)
        new_block.validate("test nonce")
        self.add_block(new_block)
        self.transactions = []


    def add_block(self, block):
        self.blocks.append(block)

        with open("../bbc/blockchain.txt", "a") as f:
            f.write(self.blocks[-1].__str__())


    def load_blockchain(self):
        self.blocks = []
        self.transactions = []

        try:
            file = open("../bbc/blockchain.txt", "r")

            line = file.readline()
            line = file.readline()
            while line:
                if "/**************Block" in line:
                    print(self.transactions)

                    new_block = Block()
                    print("title line : " + line)
                    line = file.readline()
                    print("next line : " + line)
                    new_block.header = line.replace("\n", "")
                    print("header : " + new_block.header)

                    file.readline()
                    line = file.readline()
                    block_transactions = []

                    while line != "-----------------------------------\n":
                        block_transaction = line.replace("\n", "")
                        block_transactions.append(block_transaction)
                        line = file.readline()
                    new_block.transactions = block_transactions
                    print(new_block.transactions)

                    line = file.readline()
                    new_block.nonce = line.replace("\n", "")

                    file.readline()
                    line = file.readline()
                    new_block.hash = line.replace("\n", "")
                    # print(new_block.hash)

                    self.blocks.append(new_block)

                    line = file.readline()
                    # print(line)
                else:
                    line = file.readline()
                    transaction = file.readline().replace("\n", "")
                    self.transactions.append(transaction)
            file.close()

        except Exception as e:
            print(e)
            file.close()
            raise


if __name__ == "__main__":
    blockchain = Blockchain()

    # blockchain.add_transaction("transaction 1")
    # blockchain.add_transaction("transaction 2")
    # blockchain.add_transaction("transaction 3")
    # blockchain.add_transaction("transaction 4")
    # blockchain.add_transaction("transaction 5")
    # blockchain.add_transaction("transaction 6")
    # blockchain.add_transaction("transaction 7")
    # blockchain.add_transaction("transaction 8")
    # blockchain.add_transaction("transaction 9")
    # blockchain.add_transaction("transaction 10")
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print(blockchain)
