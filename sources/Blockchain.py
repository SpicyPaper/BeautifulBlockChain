from Block import Block
import os

class Blockchain:

    def __init__(self):
        rootName = "bbc_data"
        rootPath = os.path.join("..", rootName, "block_chain")
        self.blockchainPath = os.path.join(rootPath, "blockchain.txt")
        print(self.blockchainPath)

        try:
            self.load_blockchain()
        except Exception as e:
            genesis_block = Block(0, ["genesis block"])
            genesis_block.validate("no nonce")
            self.blocks = [genesis_block]
            self.transactions = []

            with open(self.blockchainPath, "w") as f:
                f.write("/**********************************BlockChain**********************************\\\n")
                f.write(self.blocks[-1].__str__())


    def __str__(self):
        """
        return a string version of the blockchain
        """
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
        """
        add a transaction to the BlockChain
        read the text file to figure out if we now have 4 transaction and if so, it delete them and creates a new block with them
        if there is less than 4 transactions in total, it just append this one to the text file
        """
        self.transactions.append(transaction)

        if len(self.transactions) >= 4:
            blockchain = ""
            line_index = 0
            with open(self.blockchainPath, "r") as f:
                blockchain = f.readlines()
                while line_index < len(blockchain):
                    if "/**********************************BlockChain**********************************\\" in blockchain[line_index]:
                        line_index += 10
                    elif "/**************Block" in blockchain[line_index]:
                        line_index += 12
                    else :
                        break
            with open(self.blockchainPath, "w") as f:
                for i in range(line_index):
                    f.write(blockchain[i])

            self.mining_block()
        else :
            with open(self.blockchainPath, "a") as f:
                f.write(transaction + "\n")


    def mining_block(self):
        prev_hash = self.blocks[-1].get_hash()
        new_block = Block(prev_hash, self.transactions)
        new_block.validate("test nonce")
        self.add_block(new_block)
        self.transactions = []


    def add_block(self, block):
        self.blocks.append(block)

        with open(self.blockchainPath, "a") as f:
            f.write(self.blocks[-1].__str__())


    def load_blockchain(self):
        self.blocks = []
        self.transactions = []

        try:
            file = open(self.blockchainPath, "r")

            blockchain = file.readlines()
            line_index = 1

            while line_index < len(blockchain):
                if "/**************Block 0" in blockchain[line_index]:
                    new_block = Block()
                    new_block.header = blockchain[line_index+1].replace("\n", "")
                    new_block.transactions = [blockchain[line_index+3].replace("\n", "")]
                    new_block.nonce = blockchain[line_index+5].replace("\n", "")
                    new_block.hash = blockchain[line_index+7].replace("\n", "")
                    self.blocks.append(new_block)
                    line_index += 9
                elif "/**************Block" in blockchain[line_index]:
                    new_block = Block()
                    new_block.header = blockchain[line_index+1].replace("\n", "")
                    new_block.transactions = []
                    new_block.transactions.append(blockchain[line_index+3].replace("\n", ""))
                    new_block.transactions.append(blockchain[line_index+4].replace("\n", ""))
                    new_block.transactions.append(blockchain[line_index+5].replace("\n", ""))
                    new_block.transactions.append(blockchain[line_index+6].replace("\n", ""))
                    new_block.nonce = blockchain[line_index+8].replace("\n", "")
                    new_block.hash = blockchain[line_index + 10].replace("\n", "")
                    self.blocks.append(new_block)
                    line_index += 12
                else:
                    transaction = blockchain[line_index].replace("\n", "")
                    self.transactions.append(transaction)
                    line_index += 1

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
    blockchain.add_transaction("transaction XXX")

    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    
    print(blockchain)
