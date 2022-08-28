from base64 import b64encode
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
from Crypto.PublicKey import RSA

class Encrypt():
    def __init__(self, public_key=''):
        self.public_key = public_key
        if public_key=='':
            self.public_key = "-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQD5uIDebA2qU746e/NVPiQSBA0Q3J8/G23zfrwMz4qoip1vuKaVZykuMtsAkCJFZhEcmuaOVl8nAor7cz/KZe8ZCNInbXp2kUQNjJiOPwEhkGiVvxvU5V5vCK4mzGZhhawF5cI/pw2GJDSKbXK05YHXVtOAmg17zB1iJf+ie28TbwIDAQAB\n-----END PUBLIC KEY-----"
        self.rsa_key = RSA.importKey(self.public_key)
        self.cipher = Cipher_pksc1_v1_5.new(self.rsa_key)

    def encrypt(self, password):
        cipher_text = b64encode(self.cipher.encrypt(password.encode()))
        return cipher_text.decode()