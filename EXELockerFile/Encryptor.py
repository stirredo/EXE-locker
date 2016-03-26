import os

import shutil

import time

from EncryptionHelper import EncryptionHelper
import ntpath
import _winreg


_ISPRODUCTION_ = False

class EncryptedFile(object):
    MAGIC_NUMBER = "EXELocker1"
    _CHUNK_SIZE = 64 * 1024 # 64 kilo bytes
    if _ISPRODUCTION_:
        key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\WOW6432Node\EXELocker\Settings', 0, _winreg.KEY_READ)
        installLocation = _winreg.QueryValueEx(key, "InstallPath")[0] # returns C:\Program Files (x86)\EXELocker
        UNLOCK_DIALOG_LOCATION = str(installLocation).strip() + '\\base\\UnlockDialog.exe'
        CALLER_LOCATION = str(installLocation).strip() + '\\base\\caller.exe'
    else:
        UNLOCK_DIALOG_LOCATION = r'.\base\UnlockDialog.exe'
        CALLER_LOCATION = r'.\base\caller.exe'

    def __init__(self, encryptedFileName):
        if os.path.exists(encryptedFileName) and EncryptedFile.isValidFile(encryptedFileName):
            self.encryptedFileName = encryptedFileName
            self._handle = open(encryptedFileName, "rb")
            self._handle.read(10) # skip reading magic number
            self._checksum = self._handle.read(32) # read 32 bytes checksum from file
            self._filename = EncryptionHelper.stripPadding(self._handle.read(255)) # read filename
            # and then strip padding
            self._iv = self._handle.read(16) # read 16 bytes IV
            self._cycles = (os.stat(encryptedFileName).st_size) / (64 * 1024) # divided by 64kbytes
        else:
            raise Exception("File does not exist or not a valid EXELocker File.")


    def getEncryptedFileName(self):
        return self.encryptedFileName

    def getOriginalFileName(self):
            # return just the filename without the original directory
            return ntpath.basename(self._filename)

    def decryptFile(self,  key, sameLocation = False):
        if sameLocation == False:
            outfile = open(self.getOriginalFileName(), "wb")
        else:
            outfileName = os.path.join(os.path.dirname(self.encryptedFileName), self.getOriginalFileName())
            outfile = open(outfileName, "wb")
            # change the name of the encryptedFileName because right now it will be .exelocker file, change it to original extension
        data = self._handle.read(EncryptedFile._CHUNK_SIZE)
        cycle = 1
        while data != "":
            message = EncryptionHelper.decryptCipher(data, key, self._iv)
            if cycle == self._cycles:
                message = EncryptionHelper.stripPadding(message)
            outfile.write(message)
            cycle = cycle + 1
            data = self._handle.read(EncryptedFile._CHUNK_SIZE)
        outfile.close()



    def _moveHandleToData(self):
        headerSize = 10 + 32 + 255 + 16 # magic number + checksum + file name + iv
        self._handle.seek(headerSize + 1, os.SEEK_SET)


    # destructor
    def __del__(self):
        self._handle.close()

    @staticmethod
    def isValidFile(fileName):
        if os.path.isfile(fileName):
            handle = open(fileName, "rb")
            magic = handle.read(10)
            handle.close()
            return magic == EncryptedFile.MAGIC_NUMBER
        else:
            return False

    @staticmethod
    def createEncryptedFile(unencryptedFileName, key, baseFileLocation, makeBackup = False, deleteOriginal= False):
        if os.path.exists(unencryptedFileName):
            checksum = EncryptionHelper.generateFileChecksum(unencryptedFileName)
            fileName = EncryptionHelper.padString(unencryptedFileName, 255)
            iv = EncryptionHelper.generateIV()
            key = EncryptionHelper.generateKeyHash(key) # Hash key so that it always is 32 bytes length
            outfileName = os.path.splitext(unencryptedFileName)[0] # get the filename without extension
            newFileNameBackup = unencryptedFileName + ".old"
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

            if makeBackup:
                if not os.path.exists(newFileNameBackup):
                    os.rename(unencryptedFileName, newFileNameBackup)
                EncryptedFile.replaceWithUnlockDialog(baseFileLocation, newFileNameBackup)
            else:
                EncryptedFile.replaceWithUnlockDialog(baseFileLocation, unencryptedFileName, removeOriginal=True)


            # if makeBackup and deleteOriginal:
            #     pass
            # elif makeBackup:
            #     os.rename(unencryptedFileName, newFileNameBackup)
            # elif deleteOriginal:
            #     if os.path.exists(outfileName):
            #         EncryptedFile.replaceWithUnlockDialog(baseFileLocation, outfileName)



            # if everything is successful, return EncryptedFile object
            return EncryptedFile(outfileName)

        else:
            raise Exception("File does not exist")

    @staticmethod
    def replaceWithUnlockDialog(baseFileLocation, toLocationFile, removeOriginal = False):
        baseFileChecksum = EncryptionHelper.generateFileChecksum(baseFileLocation)
        toFileChecksum = EncryptionHelper.generateFileChecksum(toLocationFile)
        if baseFileChecksum != toFileChecksum:
            toDirLocation = os.path.dirname(toLocationFile)
            shutil.copy2(baseFileLocation, toDirLocation)
            fileToBeRenamed = toDirLocation + "/" + os.path.basename(baseFileLocation)
            fileNameWanted = toDirLocation + "/" + os.path.basename(toLocationFile)
            # if not removed, os.rename throws up error
            if removeOriginal:
                os.remove(fileNameWanted)
            os.rename(fileToBeRenamed, fileNameWanted)

    def getChecksum(self):
        return self._checksum
