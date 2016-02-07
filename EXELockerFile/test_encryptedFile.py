import unittest
from unittest import TestCase
from Encryptor import EncryptedFile
from Crypto import Random
from Crypto.Cipher import AES
class TestEncryptedFile(TestCase):

    def test_encryption(self):
        message = EncryptedFile.padding("hello")
        key = EncryptedFile.getHashedKey("mykey")
        iv = Random.new().read(AES.block_size)
        cipher = EncryptedFile.encryptText(message, key, iv)
        message = EncryptedFile.decryptText(cipher, key, iv)
        self.assertEquals(EncryptedFile.stripPadding(message), "hello")





if __name__ == "__main__":
    unittest.main()
