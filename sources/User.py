import base64
import os

from DigitalCheck import *


class User:

    def __init__(self):
        pass

    def generate_keys(self):
        """
        Generate the public and private key
        """
        private_k_byte, public_k_byte = generate_keys()

        self.private_k = RSA.import_key(private_k_byte)
        self.public_k = RSA.import_key(public_k_byte)

    def private_k_utf8(self):
        """
        Returns the private key in utf8 format
        """
        return self.private_k_bytes().decode("utf-8")

    def public_k_utf8(self):
        """
        Returns the public key in utf8 format
        """
        return self.public_k_bytes().decode("utf-8")

    def private_k_bytes(self):
        """
        Returns the private key in bytes format
        """
        return self.private_k.export_key()

    def public_k_bytes(self):
        """
        Returns the public key in bytes format
        """
        return self.public_k.export_key()

    def set_user_info(self, user_path):
        """
        Set the user information.

        user_path : the path of the user where all info can be found
        """
        path, file = os.path.split(user_path)
        self.username = file
        self.private_k = import_key(os.path.join(user_path, "private_k.pem"))
        self.public_k = import_key(os.path.join(user_path, "public_k.pem"))

    def sign_transaction(self, data_hash):
        """
        Sign the transaction with the hash of the data and the private key

        data_hash : the hash of the data (message + public of the receiver)
        """
        data_sign = generate_signature(data_hash, self.private_k)
        return data_sign, data_hash

    def display_keys(self):
        """
        Display private and public key
        """
        print(self.private_k_utf8())
        print("\n\n")
        print(self.public_k_utf8())
