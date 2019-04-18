from DigitalCheck import *

class User:

    def __init__(self):
        self.private_k, self.public_k = generate_keys()

    def private_k_utf8(self):
        return self.private_k.decode("utf-8")

    def public_k_utf8(self):
        return self.public_k.decode("utf-8")
    
    def displayKeys(self):
        print(self.private_k)
        print("\n\n")
        print(self.public_k)