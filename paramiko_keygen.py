# -*- coding: utf-8 -*-
from paramiko import RSAKey

def genrate_keys(private_outfile, public_outfile):
    private_key = RSAKey.generate(bits=2048, progress_func=None)
    private_key.write_private_key_file(private_outfile)

    public_key = RSAKey(filename=private_outfile)
    with open(public_outfile, "w+") as f:
        f.write(f"{public_key.get_name()} {public_key.get_base64()}")

def load_public_key(public_key_path):
    with open(public_key_path, "rb") as f:
        public_key = f.read()
    return public_key.split(b" ")[1]

if __name__ == "__main__":
    private_outfile = "ars_ssh/test_rsa.key"
    public_outfile = "ars_ssh/test_rsa.pub"
    genrate_keys(private_outfile, public_outfile)