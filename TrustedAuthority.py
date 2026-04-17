import pyaes, pbkdf2, binascii, os, secrets
import base64

class TrustedAuthority:

    def getKey(self): #generating public and private key
        password = "s3cr3t*c0d3"
        passwordSalt = '76895'
        key = pbkdf2.PBKDF2(password, passwordSalt).read(32)
        return key

    def encrypt(self,plaintext): #data encryption
        aes = pyaes.AESModeOfOperationCTR(self.getKey(), pyaes.Counter(31129547035000047302952433967654195398124239844566322884172163637846056248223))
        ciphertext = aes.encrypt(plaintext)
        return ciphertext

    def decrypt(self,enc): #data decryption
        aes = pyaes.AESModeOfOperationCTR(self.getKey(), pyaes.Counter(31129547035000047302952433967654195398124239844566322884172163637846056248223))
        decrypted = aes.decrypt(enc)
        return decrypted
