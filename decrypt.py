import os
import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import sys

def decrypt_file(file_path):
    # Get the current working directory
    cwd = os.path.dirname(os.path.abspath(__file__))
    # Get the directory for key file
    key_file_path = os.path.join(cwd, 'key.key')
    # Read the key from the file
    try:
        with open(key_file_path, 'rb') as file:
            key_data = file.read()
    except IOError:
        raise IOError("Error: Could not read from key file.")

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
    try:
        with open(file_path, 'rb') as file:
            encrypted_data = file.read()
    except IOError:
        raise IOError(f"Error: Could not read from file {file_path}.")

    # Decrypt the data
    fernet_key = Fernet(encoded_key)
    try:
        decrypted_data = fernet_key.decrypt(encrypted_data)
    except cryptography.fernet.InvalidToken as e:
        raise cryptography.fernet.InvalidToken(f"Error: Invalid token. {str(e)}")

    # Save the decrypted data back to the same file
    try:
        with open(file_path, 'wb') as file:
            file.write(decrypted_data)
    except IOError:
        raise IOError(f"Error: Could not write to file {file_path}.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: No file path provided.")
        sys.exit(1)

    file_path = sys.argv[1]
    
    decrypt_file(file_path)