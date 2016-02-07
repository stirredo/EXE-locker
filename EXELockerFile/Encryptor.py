import os
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random


class EncryptedFile(object):
    def __init__(self, checksum=None, fileName=None, IV=None, encryptedData=None):
        self.encryptedData = encryptedData
        self.checksum = checksum
        self.fileName = fileName
        self.IV = IV


    def _encryptText(self, message, key, iv):
        # iv = Random.new().read(AES.block_size)
        aes = AES.new(key, AES.MODE_CBC, iv)
        return aes.encrypt(message)

    @staticmethod
    def decryptText(ciphertext, key, iv):
        aes = AES.new(key, AES.MODE_CBC, iv)
        return aes.decrypt(ciphertext)

    @staticmethod
    def createEncryptedFile(key, infile, outfile):
        encryptedFile = EncryptedFile()
        encryptedFile.setFileName(infile)

        try:
            chunksize = 64 * 1024  # read 64kb from file at one time
            hashedKey = encryptedFile.getHashedKey(key)
            checksum = SHA256.new()
            iv = EncryptedFile.getIV()
            aes = AES.new(key, AES.MODE_CBC, iv)

            infileHandle = open(infile, 'rb')
            outfileHandle = open(outfile, 'wb')
            data = infileHandle.read(chunksize)
            while data != "":
                checksum.update(data)


        except IOError as e:
            print "I/O error ({0}: {1})".format(e.errno, e.strerror)


    def setFileName(self, fileName):
        if os.path.exists(fileName):
            self.fileName = fileName
        else:
            raise Exception("File does not exist")
 
    def setChecksum(self, hexDigest):
        self.checksum = hexDigest


