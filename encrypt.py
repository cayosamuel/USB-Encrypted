import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import sys

try:
    # Check if file path is provided
    if len(sys.argv) < 2:
        print("Error: No file path provided.")
        exit(1)

    # Get the file path from command line argument
    file_path = sys.argv[1]

    # Get the current working directory
    cwd = os.path.dirname(os.path.abspath(__file__))

    # Build the file paths for key and password
    key_file_path = os.path.join(cwd, 'key.key')
    password_file_path = os.path.join(cwd, 'password.txt')

    # Read the key from the file
    key_data = b''
    try:
        with open(key_file_path, 'rb') as file:
            key_data = file.read()
    except IOError:
        print("Error: Could not read from key file.")
        exit(1)

    # Split the key data into key_salt and key
    key_salt = key_data[:16]
    key = key_data[16:]

    # Derive the encryption key from the key_salt and key
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=key_salt,
        iterations=100000
    )
    encryption_key = kdf.derive(key)

    # Encode the encryption key to make it urlsafe
    encoded_key = base64.urlsafe_b64encode(encryption_key)

    # Read the data from the file
    data = b''
    try:
        with open(file_path, 'rb') as file:
            data = file.read()
    except IOError:
        print(f"Error: Could not read from file {file_path}.")
        exit(1)

    # Encrypt the data
    fernet_key = Fernet(encoded_key)
    encrypted_data = fernet_key.encrypt(data)

    # Save the encrypted data back to the same file
    try:
        with open(file_path, 'wb') as file:
            file.write(encrypted_data)
    except IOError:
        print(f"Error: Could not write to file {file_path}.")
        exit(1)

except Exception as e:
    print(f"An error occurred: {str(e)}")