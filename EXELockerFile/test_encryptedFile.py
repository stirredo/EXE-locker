import unittest
from unittest import TestCase
from Encryptor import EncryptedFile
from EncryptionHelper import EncryptionHelper
from Crypto import Random
from Crypto.Cipher import AES
import os


class TestEncryptedFile(TestCase):
    def test_createEncryptedFile(self):
        filePath = r"G:\work\EXE locker\EXE_locker\test_file\prog.py"
        encryptedFilePath = r"G:\work\EXE locker\EXE_locker\test_file\prog.exelocker"
        file = EncryptedFile.createEncryptedFile(filePath, "password")
        self.assertTrue(os.path.exists(encryptedFilePath))
        self.assertIsInstance(file, EncryptedFile)


    def test_isValidFile(self):
        validFilePath = r"G:\work\EXE locker\EXE_locker\test_file\prog.exelocker"
        invalidFile = r"G:\work\EXE locker\EXE_locker\test_file\prog.py"
        self.assertTrue(EncryptedFile.isValidFile(validFilePath))
        self.assertFalse(EncryptedFile.isValidFile(invalidFile))

    def test_decryptFile(self):
        validFilePath = r"G:\work\EXE locker\EXE_locker\test_file\BTSync.exelocker"
        eFile = EncryptedFile(validFilePath)
        password = EncryptionHelper.generateKeyHash("password")
        eFile.decryptFile(password)
        self.assertTrue(os.path.exists(eFile.getOriginalFileName()))

if __name__ == "__main__":
    unittest.main()

