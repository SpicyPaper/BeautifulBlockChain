from Cryptodome import Random
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15


def generate_keys():
    """
    Generate the public and the private key
    """
    random_generator = Random.new().read
    key = RSA.generate(2048, random_generator)
    return (key.exportKey(), key.publickey().exportKey())

def generate_hash(data):
    """
    Generate the hash for a given data
    """
    return SHA256.new(data)

def generate_signature(h, key):
    """
    Generate the signature for a given hash and private key
    """
    return pkcs1_15.new(key).sign(h)

def import_key(key_file_path):
    """
    Import a key to RSA from a file
    """
    with open(key_file_path, "r") as keyfile:
        return RSA.import_key(keyfile.read())

def import_key_bytes(key_bytes):
    """
    Import a key bytes in an RSA type
    """
    return RSA.import_key(key_bytes)

def verify_signature(h, public_key, signature):
    """
    Verify if a given signature is valid for a given public_key and hash
    """
    try:
        pkcs1_15.new(public_key).verify(h, signature)
        return True
    except:
        return False
