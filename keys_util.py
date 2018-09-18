# -*- coding: utf-8 -*-
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

def write2file(file_name, data):
    with open(file_name, "wb+") as f:
        f.write(data)

def genrate_keys(private_outfile, public_outfile):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
        )
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
        )
    write2file(private_outfile, private_pem)

    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    write2file(public_outfile, public_pem)

def load_private_key(filepath):
    with open(filepath, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
            )
    return private_key

def load_public_key(filepath):
    with open(filepath, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
            )
    return public_key

def encrypt_data(public_key):
    message = 'the code must be like a piece of music'
    print(len(message))
    message_bytes = bytes(message, encoding='utf8') if not isinstance(message, bytes) else message
    ciphertext = public_key.encrypt(
          message,
          padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
          )
    )
    ciphertext  = base64.b64encode(ciphertext)
    return ciphertext

if __name__ == "__main__":
    public_key = load_public_key("keys/rsa_pub.pem")
    print(len(encrypt_data(public_key)))