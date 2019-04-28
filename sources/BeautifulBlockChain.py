import base64
import os

from Blockchain import Blockchain
from User import User
from DigitalCheck import *


class BeautifulBlockChain:

    def __init__(self):
        rootName = "bbc_data"
        rootPath = os.path.join(rootName)
        self.usersPath = os.path.join(rootPath, "users")
        self.blockChainPath = os.path.join(rootPath, "block_chain")
        self.extra = ""
        self.command_force = "--force"
        self.part_splitter = ";"
        self.type_splitter = "!\n"

    def command_manager(self, argument, extra):
        """
        Manage all the command enter by the user

        argument : the argument that references a method
        extra : for extra arguments, used in some command
        """
        self.extra = extra
        print(self._display_title())
        # Switcher is a dict with key = command, value = function to call
        switcher = {
            "-u": self._create_user,
            "-h": self._display_help,
            "-i": self._init_struct_folders,
            "-t": self._add_transaction,
            "-v": self._verify_transaction,
            "-d": self._display_blockchain
        }
        # Get the function from switcher dictionary
        func = switcher.get(argument, lambda: "*** Invalid command! type : -h for help")
        # Execute the function and print the result
        res = func()
        if res != None:
            print(res)

    def _init_struct_folders(self):
        """
        Create the base folders structure for the block chain to work fine
        """
        # Create target Directory if don't exist
        if not os.path.exists(self.usersPath):
            os.makedirs(self.usersPath)
            print("Directory ", self.usersPath, " Created ")
        else:
            print("Directory '", self.usersPath, "' already exists")

        if not os.path.exists(self.blockChainPath):
            os.makedirs(self.blockChainPath)
            print("Directory ", self.blockChainPath, " Created ")
        else:
            print("Directory ", self.blockChainPath, " already exists")
            
        blockchain = Blockchain()

    def _create_user(self, username = None):
        """
        Create a new user if he doesn't already exists.
        Create the folder, private and public key.
        """
        try:
            isAllOpStandard = True
            if username == None:
                username = input("Enter the username : ")
            
            user = User()
            user.generate_keys()

            # Create user path
            newUserPath = os.path.join(self.usersPath, username)

            if not os.path.exists(newUserPath):
                os.makedirs(newUserPath)
            else:
                isAllOpStandard = False

                if self.extra == self.command_force:
                    print("User was overwrite!")
                else:
                    print("User already exists! Add --force to overwrite the user!")

            # Write private and public key in user files
            privateKeyFile = os.path.join(newUserPath, "private_k.pem")
            publicKeyFile = os.path.join(newUserPath, "public_k.pem")

            exists = os.path.isfile(privateKeyFile)
            if exists and self.extra != self.command_force:
                isAllOpStandard = False
                print("User private key already exists!")
            else:
                f = open(privateKeyFile, "wb+")
                f.write(user.private_k_bytes())
                f.close()

            exists = os.path.isfile(publicKeyFile)
            if exists and self.extra != self.command_force:
                isAllOpStandard = False
                print("User public key already exists!")
            else:
                f = open(publicKeyFile, "wb+")
                f.write(user.public_k_bytes())
                f.close()
            
            if isAllOpStandard:
                return "*** User created successfully!"
            else:
                return ""
        except Exception as e:
            return "*** An error occured during user creation! " + str(e)

    def _add_transaction(self):
        """
        Make a new transaction between 2 users and add it to the blockchain.
        """
        # Get users info
        username1 = input("Enter the client user : ")
        username2 = input("Enter the operator user : ")
        content = input("Enter the transaction content : ")

        # Check if both users exists
        if self._check_user_exists(username1) and self._check_user_exists(username2):
            # Create both users
            sender = User()
            sender.set_user_info(os.path.join(self.usersPath, username1))

            reciever = User()
            reciever.set_user_info(os.path.join(self.usersPath, username2))

            # Create signature
            content_sign = bytes(content, 'utf-8') + reciever.public_k_bytes()
            h = generate_hash(content_sign)
            sender_sign, sender_hash = sender.sign_transaction(h)
            sender_sign_enc = self._enc_sign_b64(sender_sign)

            # Prepare transaction
            data_transaction = str(sender.public_k_bytes()) + self.part_splitter + str(reciever.public_k_bytes()) + self.part_splitter + content + self.part_splitter + sender_sign_enc
            #data_transaction = username1 + self.part_splitter + username2 + self.part_splitter + content + self.part_splitter + sender_sign_enc

            # Create transaction
            #transaction = str(base64.b64encode(bytes(data_transaction, 'utf-8'))) + self.type_splitter + data_transaction
            transaction = data_transaction
            blockchain = Blockchain()
            blockchain.add_transaction(transaction)

    def _verify_transaction(self):
        """
        Verify if a transaction encoded in base64 is valid.
        Check signature with given information in the transaction.
        """
        transaction = self.extra
        #transaction = transaction.split(self.type_splitter)[0]
        #transaction = base64.b64decode(eval(transaction)).decode('utf-8')
        transaction = transaction.split(self.part_splitter)

        content = bytes(transaction[2], 'utf-8')
        sender_pu_k = import_key_bytes(eval(transaction[0]))
        reciever_pu_k_bytes = eval(transaction[1])
        signature = self._dec_sign_b64(transaction[3])
        content_sign = content + reciever_pu_k_bytes

        h = generate_hash(content_sign)

        if verify_signature(h, sender_pu_k, signature):
            print("The signature is valid!")
        else:
            print("The signature is NOT valid!")

    def _enc_sign_b64(self, sign):
        return str(base64.b64encode(sign))

    def _dec_sign_b64(self, enc_sign):
        return bytes(base64.b64decode(eval(enc_sign)))

    def _check_user_exists(self, username):
        """
        Check if a user already exists.
        Create the user if the --force is used.
        """
        userPath = os.path.join(self.usersPath, username)

        if not os.path.exists(userPath):

            if self.extra == self.command_force:
                print("The user {} was created because you add --force".format(username))
                self._create_user(username)

                return True
            else:
                print("The user {} doesn't exists, create it to make transaction with it or add --force to this command to create all the needed users!".format(username))
        else:
            return True

        return False

    def _display_blockchain(self):
        """
        Display the blockchain.
        """
        blockchain = Blockchain()
        print(blockchain)
            
    def _display_help(self):
        """
        Returns the help page
        """

        helpText = """
        Welcome in the BeautifulBlockChain help part.

        ------ How To Use ------

        To use one of this command call this python script following with one of this command, example :
        ./BeautifulBlockChain.py -h

        *** WARNING *** Don't forget to initialize the block chain by doing ./BeautifulBlockChain.py -i

        ------ Commands ------

        -h : display this page
        -u : create a new user
        -i : initialize the base structure of the block chain (create usefull folders and files)
        -t : make a transaction between 2 user and add it to the blockchain when enough transactions were done
        -v : verify the transaction given in parameter (put the transaction between quotation marks)
        -d : display the blockchain

        --force : used in some command to force an action
        """
        return helpText

    def _display_title(self):
        """
        Returns the title
        """
        return """
        (    (     (
        ( )\ ( )\    )\\
        )((_))((_) (((_)
        ((_)_((_)_  )\___
        | _ )| _ )((/ __|
        | _ \| _ \ | (__
        |___/|___/  \___|
        """
