from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload

# Define the scopes required for accessing Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate():
    """Authenticate user and obtain credentials."""
    creds = None
    # Load previously stored credentials if available
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    # If no valid credentials, prompt user to authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for future use
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def upload_file(file_path):
    """Upload a file to Google Drive."""
    # Authenticate user
    creds = authenticate()
    # Build Drive API service
    service = build('drive', 'v3', credentials=creds)
    # Define file metadata
    file_metadata = {'name': os.path.basename(file_path)}
    # Upload file
    media = MediaFileUpload(file_path)
    file = service.files().create(body=file_metadata,
                                  media_body=media,
                                  fields='id').execute()
    return file.get('id')

def share_file(file_id, email, role='reader'):
    """Share a file with a specific user."""
    # Authenticate user
    creds = authenticate()
    # Build Drive API service
    service = build('drive', 'v3', credentials=creds)
    # Define permission details
    permission = {
        'type': 'user',
        'role': role,
        'emailAddress': email
    }
    # Add permission to the file
    service.permissions().create(fileId=file_id, body=permission).execute()

# Example usage:
if __name__ == "__main__":
    file_id = upload_file('sample.txt')  #Path to the file you want to upload
    print('File uploaded. File ID:', file_id)
    share_file(file_id, 'example@gmail.com', role='writer') 
    print('File shared with example@gmail.com.')
