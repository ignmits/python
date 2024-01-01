import PyPDF2
import os
import shutil
import getpass
import sys

BACKUP_FOLDER_NAME = 'backup'

pdf_source_loc = r'../'
save_pdf_loc = os.path.join(pdf_source_loc, 'decrpyted')
backup_folder = os.path.join(pdf_source_loc, BACKUP_FOLDER_NAME)

def get_user_password_secure(password_location, password='13-06-1986'):
    try:
        # Use getpass to hide the password input
        if(len(password) == 0 or password is None):
            password = getpass.getpass("Enter pdfs password : ")
        pass_file = os.path.join(password_location, 'password.txt')
        with open(pass_file, "w") as file:
            file.write(password)

        print("Password saved to password.txt.")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    return password

def delete_folder(folder_path):
    try:
        # Delete the folder and all its contents
        shutil.rmtree(folder_path)
        print(f"Folder '{folder_path}' and its contents deleted.")
    except FileNotFoundError:
        print(f"Error: Folder not found - '{folder_path}'.")
    except PermissionError:
        print(f"Error: Permission denied while deleting '{folder_path}'.")
    except Exception as e:
        print(f"Error: {e}")


def copy_files(source_path, destination_path, files):
    for file in files:
        try:
            # Copy the file from source to destination
            source_file = os.path.join(source_path, file)
            shutil.copy2(source_file, destination_path)
            print(f"File {file} copied to {destination_path}.")
        except FileNotFoundError:
            print(f"Error: File not found - '{source_path}'.")
        except PermissionError:
            print(f"Error: Permission denied while copying '{source_path}' to '{destination_path}'.")
        except Exception as e:
            print(f"Error: {e}")

def create_path_if_not_exists(path_to_check):
    # Check if the directory exists
    if not os.path.exists(path_to_check):
        try:
            # Create the directory and its parents if they don't exist
            os.makedirs(path_to_check)
            print(f"Directory '{path_to_check}' created.")
        except OSError as e:
            print(f"Error creating directory '{path_to_check}': {e}")
    else:
        if BACKUP_FOLDER_NAME in path_to_check:
            print('Files must have been decrypted. Remove backup folder to rerun the program.\nThe program will end here.')
            sys.exit()
        print(f"Directory '{path_to_check}' already exists.")


def read_file_with_extension(directory, extension='.pdf'):
    file_list = []

    # Check if the directory exists
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return file_list

    # Get all files in the directory
    files = os.listdir(directory)

    # Filter files based on the extension
    file_list = [file for file in files if file.endswith(extension)]

    return file_list


create_path_if_not_exists(backup_folder)

pdf_files = read_file_with_extension(pdf_source_loc)
create_path_if_not_exists(save_pdf_loc)


copy_files(pdf_source_loc, backup_folder, pdf_files)

# Example usage:
passwd = get_user_password_secure(backup_folder)

for _ in range(len(pdf_files)):
    print(f'Reading file - {pdf_files[_]}')
    decrypted_pdf = PyPDF2.PdfFileWriter()
    file = os.path.join(pdf_source_loc, pdf_files[_])
    encrypted_pdf = open(file, 'rb')
    pdf = PyPDF2.PdfFileReader(encrypted_pdf,strict=False)

    # decrypt with password if set
    if (passwd):
        print('****Decrypting')
        pdf.decrypt(passwd)

    for page in pdf.pages:
        decrypted_pdf.addPage(page)

    # Saving location
    decrypt_pdf_filename = os.path.join(save_pdf_loc, pdf_files[_])
    decrypted_pdf_descriptor = open(decrypt_pdf_filename, 'wb')
    decrypted_pdf.write(decrypted_pdf_descriptor)
    encrypted_pdf.close()
    decrypted_pdf_descriptor.close()

print('\nMoving decrypted pdf`s to the main folder.')
copy_files(save_pdf_loc, pdf_source_loc, pdf_files)

print('\nRemoving temporary folder.')
delete_folder(save_pdf_loc)
