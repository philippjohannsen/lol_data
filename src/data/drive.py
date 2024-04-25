# import the required libraries 
from pathlib import Path
import pickle
import json
from datetime import datetime, timedelta
from .config import DATA_DIR, RAW_DIR
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# Define paths

rel_path = Path(__file__).resolve().parent # Path of current file
print(rel_path)

DRIVE_FILES = rel_path / 'drive_files'

TOKEN = 'token.pickle'

METADATA = 'metadata.json'

CREDENTIALS = 'credentials.json'

# Define the scopes
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def authenticate_google_drive():
    creds = None
    if Path(DRIVE_FILES / TOKEN).exists():
        with open(TOKEN, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(DRIVE_FILES / CREDENTIALS, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN, 'wb') as token:
            pickle.dump(creds, token)

    return creds

# Function for loading metadata
def load_metadata(path):
    if path.exists():
        with open(path, 'r') as f:
            return json.load(f)
    else:
        return {}

# Function for saving metadata
def save_metadata(path, data):
    with open(path, 'w') as f:
        json.dump(data, f)

# # function for downloading files from google drive
# def drive_downloader(google_drive_service, files_to_download, path):
#     for file_name, details in files_to_download.items():
#         file_id = details['id']
#         print(f"Downloading {file_name}...")
#         # from https://googleapis.github.io/google-api-python-client/docs/epy/googleapiclient.http.MediaIoBaseDownload-class.html
#         request = google_drive_service.files().get_media(fileId=file_id)
#         with open(path, 'wb') as f:
#             downloader = MediaIoBaseDownload(f, request)
#             done = False
#             while not done:
#                 status, done = downloader.next_chunk()
#                 print(f"Downloaded {file_name} {int(status.progress() * 100)}% complete.")
#     print("All files downloaded successfully.")

# # function to manage the data from google drive in local data storage. this function is called in data.py 
# def drive_manager(folder_id, path=None):
#     creds = authenticate_google_drive()
#     google_drive_service = build('drive', 'v3', credentials=creds)
#     query = f"'{folder_id}' in parents and trashed = false"
#     results = google_drive_service.files().list(q=query, fields="files(id, name, modifiedTime)").execute()
#     drive_files = results.get('files', [])

#     if not drive_files:
#         print("No files found in the Google Drive folder.")
#         return
#     else:
#         print(drive_files)


# # def manage_folder_files(folder_id, local_folder):
# #     creds = authenticate_google_drive()
# #     service = build('drive', 'v3', credentials=creds)
# #     query = f"'{folder_id}' in parents and trashed = false"
# #     results = service.files().list(q=query, fields="files(id, name, modifiedTime)").execute()
# #     drive_files = results.get('files', [])

# #     if not drive_files:
# #         print("No files found in the Google Drive folder.")
# #         return

# #     if not os.path.exists(local_folder):
# #         os.makedirs(local_folder)
# #         print(f"Created folder '{local_folder}'.")

# #     metadata = load_metadata(local_folder)
# #     local_files = {file for file in os.listdir(local_folder) if file != 'metadata.json'}
# #     drive_files_dict = {file['name']: {'id': file['id'], 'modifiedTime': file['modifiedTime']} for file in drive_files}

# #     files_to_download = {}
# #     for file_name, file_info in drive_files_dict.items():
# #         file_modified_time = file_info['modifiedTime']
# #         if file_name not in local_files or metadata.get(file_name, '1970-01-01T00:00:00.000Z') < file_modified_time:
# #             files_to_download[file_name] = {'id': file_info['id'], 'name': file_name}

# #     if files_to_download:
# #         print("The following files are missing or outdated:")
# #         for file_name in files_to_download:
# #             print(f"{file_name} (Last modified: {drive_files_dict[file_name]['modifiedTime']})")
# #         print("Downloading updated or missing files...")
# #         download_files(service, files_to_download, local_folder)
# #         # Update metadata after downloading
# #         for file_name in files_to_download:
# #             metadata[file_name] = drive_files_dict[file_name]['modifiedTime']
# #         save_metadata(local_folder, metadata)
# #     else:
# #         print("No updates found. All files are up-to-date.")

# # Example usage
# # parent_dir = os.path.dirname(os.getcwd())  # Move up to the parent directory
# # local_folder = os.path.join(parent_dir, 'data')  # Path to the data folder in the parent directory
# # folder_id = '1gLSw0RLjBbtaNy0dgnGQDAZOHIgCe-HH'  # Replace with your Google Drive folder ID
# # manage_folder_files(folder_id, local_folder)

# drive_manager('1gLSw0RLjBbtaNy0dgnGQDAZOHIgCe-HH')
#  #