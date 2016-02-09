import os
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random


class EncryptedFile(object):
    def __init__(self, encryptedFileName):
        pass



    @staticmethod
    def createEncryptedFile(unencryptedFileName, key):
        if os.path.exists(unencryptedFileName):
            checksum = SHA256.new()
            chunksize = 64 * 1024 # read 64 Kilo bytes at a time

            infile = open(unencryptedFileName, "rb")
            data = infile.read(chunksize)
            while data != "":
                checksum




        else:
            raise Exception("File does not exist")


