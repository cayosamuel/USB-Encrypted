import os
from cryptography.fernet import Fernet
import unittest
import encrypt
import decrypt

class TestEcryptDEcrypt(unittest.TestCase):

    def setUp(self):

        # Create a mock key file
        self.key_file_path = 'mock_key.key'
        with open(self.key_file_path, 'wb') as key_file:
          key_file.write(Fernet.generate_key())  
        # Create mock files for testing
        self.mock_files = ['test1.txt', 'test2.txt', 'test3.txt']
        for file in self.mock_files:
            with open(file, 'w') as f:
                f.write("This is a test file for " + file)

    def tearDown(self):
        # Clean up - delete the mock files and any encrypted/decrypted versions
        for file in self.mock_files:
            if os.path.exists(file):
                os.remove(file)
            encrypted_file = file # Assuming encrypted files have '.enc' extension
            if os.path.exists(encrypted_file):
                os.remove(encrypted_file)
        if os.path.exists(self.key_file_path):
            os.remove(self.key_file_path)

    def test_encryption_decryption(self):
        # Code for testing the encryption and decryption

        # First, encrypt the files
        for file in self.mock_files:
            encrypt.encrypt_file(file)

        # Check if file content is encrypted
            with open(file,'rb') as f:
                encrypted_data = f.read()
                self.assertNotEqual(encrypted_data, b"This is a test file for " + file.encode())

        # Now, decrypt the files
        for file in self.mock_files:
            decrypt.decrypt_file(file)

        # Check if the original files are restored correctly
        for file in self.mock_files:
            with open(file, 'r') as f:
                content = f.read()
                self.assertEqual(content, "This is a test file for " + file)

if __name__ == '__main__':
    unittest.main(verbosity=2)