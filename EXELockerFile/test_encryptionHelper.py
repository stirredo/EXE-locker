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
        self.fail()


if __name__ == "__main__":
    unittest.main()