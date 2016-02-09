import unittest
from unittest import TestCase
from Encryptor import EncryptedFile
from EncryptionHelper import EncryptionHelper
from Crypto import Random
from Crypto.Cipher import AES
class TestEncryptedFile(TestCase):

    def test_encryption(self):
        message = EncryptionHelper.padString("hello")
        key = EncryptionHelper.generateKeyHash("mykey")
        iv = EncryptionHelper.generateIV()
        cipher = EncryptedFile.encryptText(message, key, iv)
        message = EncryptedFile.decryptText(cipher, key, iv)
        self.assertEquals(EncryptedFile.stripPadding(message), "hello")





if __name__ == "__main__":
    unittest.main()
