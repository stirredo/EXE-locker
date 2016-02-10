from Crypto.Hash import SHA256
from Crypto import Random
from Crypto.Cipher import AES


class EncryptionHelper(object):
    @staticmethod
    def padString(message, length=16):
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

    @staticmethod
    def generateFileChecksum(fileName):
        """ Generates checksum of the files' content """
        infile = open(fileName, "rb")
        checksum = SHA256.new()
        chunksize = 64 * 1024  # read 64kbytes at a time

        data = infile.read(chunksize)

        while data != "":
            checksum.update(data)
            data = infile.read(chunksize)

        return checksum.digest()

    @staticmethod
    def encryptText(message, key, iv):
        a = AES.new(key, AES.MODE_CBC, iv)
        cipher = a.encrypt(message)
        return cipher

    @staticmethod
    def decryptCipher(cipher, key, iv):
        a = AES.new(key, AES.MODE_CBC, iv)
        message = a.decrypt(cipher)
        return message

    @staticmethod
    def getIV(cipher):
        return cipher[:16]
