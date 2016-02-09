import os
import unittest
from unittest import TestCase

from Crypto.Cipher import AES
from Crypto.Hash import SHA256

from EncryptionHelper import EncryptionHelper


class TestEncryptionHelper(TestCase):
    def test_padString(self):
        self.assertEquals(16, len(EncryptionHelper.padString("hello")))
        self.assertEquals(18, len(EncryptionHelper.padString("hello", 18)))

    def test_stripPadding(self):
        originalString = "hello"
        paddedString = EncryptionHelper.padString("hello")
        self.assertNotEqual(originalString, paddedString)
        self.assertEquals(originalString, EncryptionHelper.stripPadding(paddedString))

    def test_generateKeyHash(self):
        key = "password"
        hashedKey = EncryptionHelper.generateKeyHash(key)
        self.assertNotEqual(key, hashedKey)
        self.assertEquals(32, len(hashedKey))

    def test_generateIV(self):
        iv = EncryptionHelper.generateIV()
        self.assertEquals(16, len(iv))

    def test_generateFileChecksum(self):
        text = "Hello world"
        outfile = open("testfile", "wb+")
        outfile.write(text)
        fileHash = SHA256.new()
        textHash = EncryptionHelper.generateKeyHash(text)
        outfile.seek(0, os.SEEK_SET) # bring file pointer to the beginning
        chunksize = 64 * 1024 # read 64 kilo bytes at a time
        data = outfile.read(chunksize)
        self.assertEquals(text, data)

        while data != "":
            fileHash.update(data)
            data = outfile.read(chunksize)


        outfile.close()
        self.assertEquals(textHash, fileHash.digest())


    def test_encryption(self):
        originalMessage = EncryptionHelper.padString("Hello")
        key = EncryptionHelper.generateKeyHash("world")
        iv = EncryptionHelper.generateIV()
        cipher = EncryptionHelper.encryptText(originalMessage, key, iv)
        self.assertNotEqual(originalMessage, cipher)
        message = EncryptionHelper.decryptCipher(cipher, key, iv)
        self.assertEqual(EncryptionHelper.stripPadding(message), EncryptionHelper.stripPadding(originalMessage))

#
# if __name__ == "__main__":
#     unittest.main()


