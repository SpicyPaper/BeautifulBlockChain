from Cryptodome import Random
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA


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
    return SHA256.new(data).digest()

def generate_signature(hash, key):
    """
    Generate the signature for a given hash and private key
    """
    return key.sign(hash, '')

def verify_signature(hash, public_key, signature):
    """
    Verify if a given signature is valid for a given public_key and hash
    """
    return public_key.verify(hash, signature)
