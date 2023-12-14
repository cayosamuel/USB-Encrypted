import os
import subprocess
import stat

def set_password():
    subprocess.run(['python3', 'password.py'])

def get_usb_drive_path():
    # Get the list of all USB drives connected to the computer
    available_drives = []
    for drive in os.listdir('/Volumes/'):
        drive_path = os.path.join('/Volumes/', drive)
        if os.path.isdir(drive_path):
            available_drives.append(drive_path)

    if len(available_drives) == 0:
        print('No USB drives found')
        return None

    # Ask the user to choose a USB drive
    print('Available USB drives:')
    for i, drive_path in enumerate(available_drives):
        print(f'{i+1}. {drive_path}')

    choice = input('Enter the number of the USB drive you want to use: ')

    try:
        choice = int(choice)
        if 1 <= choice <= len(available_drives):
            return available_drives[choice-1]
        else:
            print('Invalid choice')
    except ValueError:
        if os.path.isdir(choice):
            print 
            return choice
        else:
            print('Invalid choice')

    return None

def encrypt_files(): # To test localy use this : '/Users/sammycayo/Desktop/USBsimulation'
    # Get the path of the USB drive
    usb_drive_path = get_usb_drive_path()
    if usb_drive_path is None:
        return
    # Iterate through all the files in the USB drive
    for root, dirs, files in os.walk(usb_drive_path):
        for file in files:
            file_path = os.path.join(root, file)

            # Encrypt each file individually
            subprocess.run(['python3', 'encrypt.py', file_path])

    print("Encryption of files complete")

def set_permission():
  #  owner_permissions = stat.S_IRUSR | stat.S_IWUSR  # Read and write permissions for the owner
    all_permissions = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH  # Read permissions for all users
    # Set owner permissions for key.key
    file_path = 'key.key'
    os.chmod(file_path, all_permissions)

    # Set owner permissions for password.txt
    password_file_path = 'password.txt' 
    os.chmod(password_file_path, all_permissions)  

def warning():
    print('WARNING: This will encrypt all the files in the USB drive')
    print('Make sure you have a backup of the files before proceeding or you will lose them forever')
    choice = input('Do you want to continue? (y/n): ')
    if choice == 'n':
        print('Aborting...')
    if choice == 'y':
        encrypt_files()
        set_permission()
    else: print('Invalid choice')

def main():
    # Welcome to USB Encryption
    print("Welcome ! This is the first step to protect yourself from whoever")

    # Ask the user to choose an option

    action = input("Enter 1 to set a password: ")

    if action == '1':
        set_password()
        warning()
    elif action == '2':
        encrypt_files()
    else:
        print('Invalid choice')
        main()

if __name__ == '__main__':
    main()
