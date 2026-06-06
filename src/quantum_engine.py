import time
from kryptoon.quantum.kem import Algorithm as KEM_Alg, KeyPair as KEM_KeyPair
from kryptoon.quantum.dsa import Algorithm as DSA_Alg, KeyPair as DSA_KeyPair


class QuantumEngine:
    def __init__(self):

        self.kem_alg = KEM_Alg.MLKEM.MLKEM1024
        self.kem_sk, self.kem_pk = KEM_KeyPair(self.kem_alg)


        self.dsa_alg = DSA_Alg.MLDSA.MLDSA87
        self.dsa_sk, self.dsa_pk = DSA_KeyPair(self.dsa_alg)

    def encapsulate_key(self):
        time.sleep(1.5)
        shared_secret, key_ciphertext = self.kem_pk.encapsulate()
        return shared_secret, key_ciphertext

    def decapsulate_key(self, key_ciphertext):
        time.sleep(1.0)
        return self.kem_sk.decapsulate(key_ciphertext)

    def sign_data(self, data):
        time.sleep(1.2)
        return self.dsa_sk.sign(data)

    def verify_signature(self, data, signature):
        time.sleep(1.0)
        return self.dsa_pk.verify(signature=signature, message=data)