import os
from EncryptionHelper import EncryptionHelper


class EncryptedFile(object):
    MAGIC_NUMBER = "EXELocker1"
    _CHUNK_SIZE = 64 * 1024 # 64 kilo bytes
    def __init__(self, encryptedFileName):
        if os.path.exists(encryptedFileName) and EncryptedFile.isValidFile(encryptedFileName):
            self._handle = open(encryptedFileName, "rb")
            self._handle.read(10) # skip reading magic number
            self._checksum = self._handle.read(32) # read 32 bytes checksum from file
            self._filename = EncryptionHelper.stripPadding(self._handle.read(255)) # read filename
            # and then strip padding
            self._iv = self._handle.read(16) # read 16 bytes IV
            self._cycles = (os.stat(encryptedFileName).st_size) / (64 * 1024) # divided by 64kbytes
        else:
            raise Exception("File does not exist or not a valid EXELocker File.")

    def getOriginalFileName(self):
        return self._filename

    def decryptFile(self, key):
        #self._moveHandleToData()
        outfile = open(self.getOriginalFileName(), "wb")
        data = self._handle.read(EncryptedFile._CHUNK_SIZE)
        cycle = 1
        while data != "":
            message = EncryptionHelper.decryptCipher(data, key, self._iv)
            if cycle == self._cycles:
                message = EncryptionHelper.stripPadding(message)
            outfile.write(message)
            cycle = cycle + 1
            data = self._handle.read(EncryptedFile._CHUNK_SIZE)


    def _moveHandleToData(self):
        headerSize = 10 + 32 + 255 + 16 # magic number + checksum + file name + iv
        self._handle.seek(headerSize + 1, os.SEEK_SET)


    # destructor
    def __del__(self):
        self._handle.close()

    @staticmethod
    def isValidFile(fileName):
        handle = open(fileName, "rb")
        magic = handle.read(10)
        handle.close()
        return magic == EncryptedFile.MAGIC_NUMBER


    @staticmethod
    def createEncryptedFile(unencryptedFileName, key):
        if os.path.exists(unencryptedFileName):
            checksum = EncryptionHelper.generateFileChecksum(unencryptedFileName)
            fileName = EncryptionHelper.padString(unencryptedFileName, 255)
            iv = EncryptionHelper.generateIV()
            key = EncryptionHelper.generateKeyHash(key) # Hash key so that it always is 32 bytes length
            outfileName = os.path.splitext(unencryptedFileName)[0] # get the filename without extension
            outfileName = outfileName + ".exelocker"
            outfile = open(outfileName, "wb")
            outfile.write(EncryptedFile.MAGIC_NUMBER)  # 10 bytes that will help detect file
            outfile.write(checksum)  # 32 bytes SHA256 checksum
            outfile.write(fileName)  # 255 bytes of padded filename
            outfile.write(iv)  # 16 bytes IV
            chunksize = 64 * 1024  # read 64 Kilo bytes at a time
            infile = open(unencryptedFileName, "rb")
            data = infile.read(chunksize)
            while data != "":
                if len(data) % 16 != 0:
                    data = EncryptionHelper.padString(data, chunksize)
                cipher = EncryptionHelper.encryptText(data, key, iv)
                outfile.write(cipher)
                data = infile.read(chunksize)

            outfile.close()
            infile.close()

            # if everything is successful, return EncryptedFile object


        else:
            raise Exception("File does not exist")
