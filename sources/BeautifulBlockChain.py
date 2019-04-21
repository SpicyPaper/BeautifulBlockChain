from User import User
from Blockchain import Blockchain
import sys
import os

rootName = "bbc_data"
rootPath = os.path.join("..", "bbc_data")
usersPath = os.path.join(rootPath, "users")
blockChainPath = os.path.join(rootPath, "block_chain")
extra = ""
command_force = "--force"

def init_struct_folders():
    """
    Create the base folders structure for the block chain to work fine
    """
    # Create target Directory if don't exist
    if not os.path.exists(usersPath):
        os.makedirs(usersPath)
        print("Directory ", usersPath, " Created ")
    else:
        print("Directory '", usersPath, "' already exists")

    if not os.path.exists(blockChainPath):
        os.makedirs(blockChainPath)
        print("Directory ", blockChainPath, " Created ")
    else:
        print("Directory ", blockChainPath, " already exists")

def command_manager(argument):
    """
    Manage all the command enter by the user
    """
    # Switcher is a dict with key = command, value = function to call
    switcher = {
        "-u": create_user,
        "-h": display_help,
        "-i": init_struct_folders,
        "-t": add_transaction,
        "-d": display_blockchain
    }
    # Get the function from switcher dictionary
    func = switcher.get(argument, lambda: "*** Invalid command! type : -h for help")
    # Execute the function and print the result
    res = func()
    if res != None:
        print(res)

def create_user():
    """
    Create a new user if he doesn't already exists.
    Create the folder, private and public key.
    """
    try:
        username = input("Enter the username : ")
        user = User()

        # Create user path
        newUserPath = os.path.join(usersPath, username)

        if not os.path.exists(newUserPath):
            os.makedirs(newUserPath)
        else:
            if extra == command_force:
                print("User was overwrite!")
            else:
                print("User already exists! Add --force to overwrite the user!")

        # Write private and public key in user files
        privateKeyFile = os.path.join(newUserPath, "private_k")
        publicKeyFile = os.path.join(newUserPath, "public_k")

        exists = os.path.isfile(privateKeyFile)
        if exists and extra != command_force:
            print("User private key already exists!")
        else:
            f = open(privateKeyFile, "w+")
            f.write(user.private_k_utf8())
            f.close()

        exists = os.path.isfile(publicKeyFile)
        if exists and extra != command_force:
            print("User public key already exists!")
        else:
            f = open(publicKeyFile, "w+")
            f.write(user.public_k_utf8())
            f.close()
        return "*** User created successfully!"
    except Exception as e:
        return "*** An error occured during user creation! " + str(e)

def display_help():
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

def display_title():
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

def add_transaction():
    """
    Make a new transaction between 2 users.
    Add the transaction when enough of them were done.
    """
    user1 = input("Enter the sender user : ")
    user2 = input("Enter the reciever user : ")
    content = input("Enter the transaction content : ")

    transaction = content
    blockchain = Blockchain()
    blockchain.add_transaction(transaction)

def display_blockchain():
    """
    Display the blockchain.
    """
    blockchain = Blockchain()
    print(blockchain)

if __name__ == "__main__":

    print(display_title())

    try:
        extra = sys.argv[2]
    except:
        pass

    try:
        command = sys.argv[1]
        command_manager(command)
    except:
        command_manager("-h")