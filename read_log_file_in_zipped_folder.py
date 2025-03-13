import zipfile
import os

# Specify the folder path where zip files are located
folder_path = '/path/to/your/folder'

# Iterate through each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.zip'):
        file_path = os.path.join(folder_path, filename)
        
        # Open the zip file
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            # Iterate through each file in the zip archive
            for file_name_in_zip in zip_ref.namelist():
                if file_name_in_zip.endswith('.log'):
                    # Open the log file directly from the zip archive
                    with zip_ref.open(file_name_in_zip) as log_file:
                        log_contents = log_file.read().decode('utf-8')
                        
                    # Process log contents as needed
                    print(f"Contents of {file_name_in_zip} from {filename}:")
                    print(log_contents)
