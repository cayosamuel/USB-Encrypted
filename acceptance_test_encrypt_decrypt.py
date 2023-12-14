import os
from cryptography.fernet import Fernet
import unittest
import encrypt
import decrypt
import random
import string

class TestEcryptDEcrypt(unittest.TestCase):

    def setUp(self):

        self.medium_content = random_string(10000)  # 10,000 characters in the file
        self.large_content = random_string(1000000)  # 1,000,000 characters in the file

        # Create a mock key file
        self.key_file_path = 'mock_key.key'
        with open(self.key_file_path, 'wb') as key_file:
          key_file.write(Fernet.generate_key())  

        # Create mock files for general testing
          self.mock_files_general =['test1.txt', 'test2.txt', 'test3.txt']
        for file in self.mock_files_general:
            with open(file, 'wb') as f:
                f.write(("This is a test file for " + file).encode())
                f.close()

        # Create mock files for different file types
        self.mock_files = [
                            # Different file sizes
                            'small_file.txt',
                            'medium_file.txt',
                            'large_file.txt',
                            #Different file types
                            'test2.jpg',
                            'test3.bin', 
                            'test4.pdf']
        
        for file in self.mock_files:
            with open(file, 'wb') as f:
                if file =='small_file.txt':
                    content = "This is a test file for " + file
                    #f.write(("This is a test file for ").encode())
                    f.write(content.encode())
                    #print("\n\nContent of small file:", content)
                    f.close()
                elif file =='medium_file.txt':
                    f.write(self.medium_content.encode())
                    f.close()
                elif file =='large_file.txt':
                    f.write(self.large_content.encode())
                    f.close()
                elif file.endswith('.jpg'):
                    f.write(b'\xff\xd8\xff' *10)
                    f.close()
                else: # for .bin and .pdf files
                    f.write(os.urandom(1024)) # 1KB of random data
                    f.close()

    def tearDown(self):
    # Clean up - delete the mock files
         for file_set in [self.mock_files_general, self.mock_files]:
            for file in file_set:
              if os.path.exists(file):
                os.remove(file)

    # Remove the mock key file
            if os.path.exists(self.key_file_path):
             os.remove(self.key_file_path)

    # Code for testing the encryption and decryption general files
    def test_encryption_decryption(self):
          
        # First, encrypt the files
        for file in self.mock_files_general:
            encrypt.encrypt_file(file)

        # Check if file content is encrypted
            with open(file,'rb') as f:
                encrypted_data = f.read()
                self.assertNotEqual(encrypted_data, ("This is a test file for " + file).encode())

        # Now, decrypt the files
        for file in self.mock_files_general:
            decrypt.decrypt_file(file)

        # Check if the original files are restored correctly
        for file in self.mock_files_general:
            with open(file, 'r') as f:
                content = f.read()
                self.assertEqual(content, "This is a test file for " + file)

  # Code for testing the encryption and decryption with different file size 
    def test_file_size_encryption_decryption(self):
        import time
        
        for file in ['small_file.txt', 'medium_file.txt', 'large_file.txt']:
         # Check the original content of the file !!!!!!!!!
         with open(file, 'rb') as f:
            original_content = f.read()
           # print(f"\nOriginal content of {file}:", original_content)

    # ---------------------Encryption-------------------------
         start_time = time.time()
         encrypt.encrypt_file(file)
         end_time = time.time()
        # Check that the file has been encrypted
         encrypted_data = b''
         with open(file, 'rb') as f:
            if file =='small_file.txt':
                encrypted_data = f.read()
                #print("\n\nEncrypted:", encrypted_data)
                self.assertNotEqual(encrypted_data,("This is a test file for ").encode())
            elif file =='medium_file.txt':
                encrypted_data = f.read()
                self.assertNotEqual(encrypted_data,self.medium_content.encode())
            elif file =='large_file.txt':
                encrypted_data = f.read()
                self.assertNotEqual(encrypted_data,self.large_content.encode())

            #Encryption time
         encrypt_time = end_time - start_time
    # ---------------------Decryption-------------------------
         start_time = time.time()
         decrypt.decrypt_file(file)
         end_time = time.time()
        # Check that the file has been decrypted
         decrypted_data = b''
         with open(file, 'rb') as f:
            if file =='small_file.txt':
                decrypted_data = f.read()
                #print("\n\nDecrypted:", decrypted_data)
                self.assertEqual(decrypted_data,("This is a test file for "+file).encode())
            elif file =='medium_file.txt':
                decrypted_data = f.read()
                self.assertEqual(decrypted_data,self.medium_content.encode())
            elif file =='large_file.txt':
                decrypted_data = f.read()
                self.assertEqual(decrypted_data,self.large_content.encode())

            #Decryption time
         decrypt_time = end_time - start_time

         print(f"{file}: Encryption time {encrypt_time}s, Decryption time {decrypt_time}s")
    
    # Code for testing the encryption and decryption with different file types
    def test_binary_data_encryption_decryption(self):

        for file in ['test2.jpg', 'test3.bin', 'test4.pdf']:

         with open(file, 'rb') as f:
          original_data = f.read()
         encrypt.encrypt_file(file)
         decrypt.decrypt_file(file)
         with open(file, 'rb') as f:
            decrypted_data = f.read()
        
        self.assertEqual(original_data, decrypted_data, f"Binary data mismatch in {file}")

def random_string(length):
     return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


if __name__ == '__main__':
    unittest.main(verbosity=2)