"""
Logic to encrypt and decrypt values. This can be replaced at some point for some stronger protocol.
"""
from base64 import urlsafe_b64encode, urlsafe_b64decode


def encrypt_value(value):
    return urlsafe_b64encode(bytes(value, 'utf-8')).decode()


def decrypt_value(value):
    return urlsafe_b64decode(value).decode()
