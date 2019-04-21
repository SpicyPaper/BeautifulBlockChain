import os

from DigitalCheck import *


class User:

    def __init__(self):
        pass

    def generate_keys(self):
        private_k_byte, public_k_byte = generate_keys()

        self.private_k = RSA.import_key(private_k_byte)
        self.public_k = RSA.import_key(public_k_byte)

    def private_k_utf8(self):
        return self.private_k_bytes().decode("utf-8")

    def public_k_utf8(self):
        return self.public_k_bytes().decode("utf-8")

    def private_k_bytes(self):
        return self.private_k.export_key()

    def public_k_bytes(self):
        return self.public_k.export_key()

    def set_user_info(self, user_path):
        """
        Set the user information.

        user_path : the path of the user where all info can be found
        """
        path, file = os.path.split(user_path)
        self.username = file
        self.private_k = self._import_key(os.path.join(user_path, "private_k.pem"))
        self.public_k = self._import_key(os.path.join(user_path, "public_k.pem"))
        print(self.private_k_bytes(), self.public_k_bytes())

    def sign_transaction(self):
        pass

    def display_keys(self):
        print(self.private_k_utf8())
        print("\n\n")
        print(self.public_k_utf8())

    def _import_key(self, key_file_path):
        """
        Import a key to RSA from a file
        """
        with open(key_file_path, "r") as keyfile:
            return RSA.import_key(keyfile.read())
