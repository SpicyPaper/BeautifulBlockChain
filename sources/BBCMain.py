import sys

from BeautifulBlockChain import BeautifulBlockChain

if __name__ == "__main__":

    bbc = BeautifulBlockChain()

    print(bbc.display_title())

    try:
        extra = sys.argv[2]
    except:
        extra = None

    try:
        command = sys.argv[1]
        bbc.command_manager(command, extra)
    except:
        bbc.command_manager("-h", extra)
