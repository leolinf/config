# -*- coding: utf-8 -*-
from Crypto.PublicKey import RSA
from Crypto import Random
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import (
    NoEncryption, Encoding, PrivateFormat, PublicFormat
)


def generate_rsa_keys():
    """crpyto install need gcc and python-devel
    pip install pycrypto
    """
    random_generator = Random.new().read
    key = RSA.generate(1024, random_generator)
    pub_key = key.publickey()

    public_key = pub_key.exportKey("PEM")
    private_key = key.exportKey("PEM")
    return public_key, private_key


def generate_keys():
    """
    pip install cryptography
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=1024,
        backend=default_backend(),
    )

    serialized_private_key = private_key.private_bytes(
        Encoding.PEM,
        PrivateFormat.PKCS8,
        NoEncryption()
    )

    public_key = private_key.public_key()

    serialized_public_key = public_key.public_bytes(
        Encoding.PEM,
        PublicFormat.SubjectPublicKeyInfo,
    )

    return serialized_public_key, serialized_private_key


if __name__ == "__main__":
    print("------------pycrypto------------")
    pub_key, pri_key = generate_rsa_keys()
    print(pub_key)
    print(pri_key)

    print("\n------------cryptography------------")
    pub_key, pri_key = generate_keys()
    print(pub_key)
    print(pri_key)
