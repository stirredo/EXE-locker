from Crypto.Hash import SHA256
from Crypto import Random
from Crypto.Cipher import AES


class EncryptionHelper(object):
    @staticmethod
    def padString(message, length = 16):
        filler_char = "\0"
        filler_length = length - (len(message) % length)
        return message + filler_char * filler_length

    @staticmethod
    def stripPadding(message):
        return message.rstrip("\0")

    @staticmethod
    def generateKeyHash(key):
        h = SHA256.new()
        h.update(key)
        return h.digest()


    @staticmethod
    def generateIV():
        return Random.new().read(AES.block_size)

