from Cryptodome.PublicKey import RSA
from Cryptodome.Hash import SHA256
from Cryptodome import Random

def generate_keys():
    """
    Generate the public and the private key
    """
    random_generator = Random.new().read
    key = RSA.generate(2048, random_generator)
    return (key.exportKey(), key.publickey().exportKey())

def generate_hash(data):
    return SHA256.new(data).digest()

def generate_signature(hash, key):
    return key.sign(hash, '')

def verify_signature(hash, public_key, signature):
    return public_key.verify(hash, signature)
