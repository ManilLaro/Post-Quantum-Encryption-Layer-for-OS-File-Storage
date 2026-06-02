import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class AESEngine:
    def generate_key(self):

        return AESGCM.generate_key(bit_length=256)

    def encrypt_data(self, key, plaintext):

        aesgcm = AESGCM(key)
        nonce = os.urandom(12) # Random initialization vector (12 bytes)
        # Encrypt the data
        ciphertext = aesgcm.encrypt(nonce, plaintext.encode('utf-8'), None)
        return nonce, ciphertext

    def decrypt_data(self, key, nonce, ciphertext):

        aesgcm = AESGCM(key)
        # Decrypt and decode
        return aesgcm.decrypt(nonce, ciphertext, None).decode('utf-8')