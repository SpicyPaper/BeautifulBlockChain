import os

from Blockchain import Blockchain
from User import User


class BeautifulBlockChain:

    def __init__(self):
        rootName = "bbc_data"
        rootPath = os.path.join("..", rootName)
        self.usersPath = os.path.join(rootPath, "users")
        self.blockChainPath = os.path.join(rootPath, "block_chain")
        self.extra = ""
        self.command_force = "--force"

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

    def _create_user(self, username = None):
        """
        Create a new user if he doesn't already exists.
        Create the folder, private and public key.
        """
        try:
            if username == None:
                username = input("Enter the username : ")
            
            user = User()
            user.generate_keys()

            # Create user path
            newUserPath = os.path.join(self.usersPath, username)

            if not os.path.exists(newUserPath):
                os.makedirs(newUserPath)
            else:
                if self.extra == self.command_force:
                    print("User was overwrite!")
                else:
                    print("User already exists! Add --force to overwrite the user!")

            # Write private and public key in user files
            privateKeyFile = os.path.join(newUserPath, "private_k.pem")
            publicKeyFile = os.path.join(newUserPath, "public_k.pem")

            exists = os.path.isfile(privateKeyFile)
            if exists and self.extra != self.command_force:
                print("User private key already exists!")
            else:
                f = open(privateKeyFile, "wb+")
                f.write(user.private_k_bytes())
                f.close()

            exists = os.path.isfile(publicKeyFile)
            if exists and self.extra != self.command_force:
                print("User public key already exists!")
            else:
                f = open(publicKeyFile, "wb+")
                f.write(user.public_k_bytes())
                f.close()
            return "*** User created successfully!"
        except Exception as e:
            return "*** An error occured during user creation! " + str(e)

    def _add_transaction(self):
        """
        Make a new transaction between 2 users.
        Add the transaction when enough of them were done.
        """
        username1 = input("Enter the sender user : ")
        username2 = input("Enter the reciever user : ")
        content = input("Enter the transaction content : ")

        if self._check_user_exists(username1) and self._check_user_exists(username2):
            user1 = User()
            user1.set_user_info(os.path.join(self.usersPath, username1))

        transaction = content
        blockchain = Blockchain()
        blockchain.add_transaction(transaction)

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
