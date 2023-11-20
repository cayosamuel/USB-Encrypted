import os
import bcrypt
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

# Function to write the hashed password and salt to a file
def write_password_file(salt_length, salt, hashed_password, password_file_path):
    try:
        with open(password_file_path, 'wb') as file:
            file.write(salt_length.to_bytes(1, 'big') + salt + hashed_password)
    except IOError:
        print("Error: Could not write to password file.")
        exit(1)

# Function to read the hashed password and salt from a file
def read_password_file(password_file_path):
    try:
        with open(password_file_path, 'rb') as file:
            stored_data = file.read()
            stored_salt_length = int.from_bytes(stored_data[:1], 'big')
            stored_salt = stored_data[1:1+stored_salt_length]
            stored_password = stored_data[1+stored_salt_length:]
            return stored_salt_length, stored_salt, stored_password
    except IOError:
        print("Error: Could not read from password file.")
        exit(1)

# Main script logic
try:
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Get the paths of the key and password files
    key_file = os.path.join(script_dir, 'key.key')
    password_file = os.path.join(script_dir, 'password.txt')

    # Ask the user to enter a password
    password_input = input('Set a password: ')

    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    salt_length = len(salt)
    hashed_password = bcrypt.hashpw(password_input.encode(), salt)

    # Write the hashed password and salt to a file
    write_password_file(salt, salt_length, hashed_password, password_file)

    # Read the stored salt and password from the file
    stored_salt_length, stored_salt, stored_password = read_password_file(password_file)

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
            with open(key_file, 'wb') as file:
                file.write(stored_key)
                print('Key is stored in key.key file.')
        except IOError:
            print("Error: Could not write to key file.")
            exit(1)
    else:
        print('Password did not match stored password. Password is not set.')

except Exception as e:
    print(f"An error occurred: {str(e)}")
