import unittest
from unittest.mock import mock_open, patch
import password

class TestPassword(unittest.TestCase):
    # test to Get the paths of the key and password files
    def test_filepath(self):
        
        self.assertEqual(password.key_file, 'key.key')
        self.assertEqual(password.password_file, 'password.txt')

    # test salt length generation
    def test_salt_length(self):
        salt_length = len(password.salt)
        self.assertEqual(salt_length, 29) # salt length should be 12 bytes
    # test password hashing 
    def test_password_hashing(self):
        password1 = password.bcrypt.hashpw(b'password', password.salt)
        password2 = password.bcrypt.hashpw(b'password', password.salt)
        # test to make sure that the password generated twice is not equal 
        self.assertNotEqual(password1, password2)

    # test File writing for password
    @patch ('password.bcrypt.gensalt')
    @patch ('password.bcrypt.hashpw')
    @patch ('builtins.open', new_callable=mock_open)
    def test_file_write(self, mock_file,mock_hashpw, mock_gensalt):

        # mock the return value of bcrypt.gensalt()
        mock_salt = b'mock_salt'
        mock_salt_length = len(mock_salt)
        mock_hashed_password = b'mock_hashed_password'

        # Set up the return values for the mocked functions
        mock_gensalt.return_value = mock_salt
        mock_hashpw.return_value = mock_hashed_password

        # logic to trigger the file writing in password.py
        password.password_file_write()
        # test to make sure that the correct file and more was opened
        mock_file.assert_called_once_with('password.txt', 'wb')
        # test to make sure that the correct content was written to the file
        except_content = mock_salt_length.to_bytes(1, 'big') + mock_salt + mock_hashed_password
        # test to make sure that the correct content was written to the file
        mock_file().write.assert_called_once_with(except_content)

    # Test File Reading for Password
    @patch ('builtins.open', new_callable=mock_open, read_data=b'\x05salt_hashedpassword')
    def test_file_read(self, mock_file):
        # logic to trigger the file reading in password.py
        password.password_file_read()
        # test to make sure that the correct file and more was opened
        mock_file.assert_called_once_with('password.txt', 'rb')
    
        # test to make sure that the correct content was read from the file
        self.assertEqual(password.stored_salt_length, 5)
        self.assertEqual(password.stored_salt,b'salt_')
        self.assertEqual(password.stored_password, b'hashedpassword')




if __name__ == '__main__':
    unittest.main()
