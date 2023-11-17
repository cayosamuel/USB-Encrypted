import os
import bcrypt
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

# Get the directory of the script
scrip_dir = os.path.dirname(os.path.abspath(__file__))

# Get the paths of the key and password files
key_file = os.path.join(scrip_dir, 'key.key')
password_file = os.path.join(scrip_dir, 'password.txt')

try:
    # Ask the user to enter a password
    password = input('Set a password: ')

    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    salt_length = len(salt)
    hashed_password = bcrypt.hashpw(password.encode(), salt)

    # Store the hashed password and salt in a file
    try:
        with open('password.txt', 'wb') as file:
            file.write(salt_length.to_bytes(1,'big')+salt+hashed_password)  # Store the salt along with the hashed password
    except IOError:
        print("Error: Could not write to password file.")
        exit(1)

    # Retrieve the stored salt and password from the file
    stored_salt_length = 0
    stored_salt = b''
    stored_password = b''
    try:
        with open('password.txt', 'rb') as file:
            stored_data = file.read()
            stored_salt_length = int.from_bytes(stored_data[:1], 'big')  # Extract the salt length from the stored data
            stored_salt = stored_data[1:1+stored_salt_length]  # Extract the salt from the stored data
            stored_password = stored_data[1+stored_salt_length:]  # Extract the hashed password from the stored data
    except IOError:
        print("Error: Could not read from password file.")
        exit(1)

    # Ask the user to enter the password again
    entered_password = input('Enter password: ')

    # Compare the entered password with the stored password
    if bcrypt.checkpw(entered_password.encode(), stored_password):
        print('Password is correct')

        # Generate a key for encryption
        key_salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=key_salt,
            iterations=100000
        )
        key = kdf.derive(entered_password.encode())

        # Store the key and key_salt in a file
        stored_key = key_salt + key
        try:
            with open('key.key', 'wb') as file:
                file.write(stored_key)
        except IOError:
            print("Error: Could not write to key file.")
            exit(1)
    else:
        print('Password did not match stored password. Password is not set.')

except Exception as e:
    print(f"An error occurred: {str(e)}")