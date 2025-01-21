from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os
from dotenv import load_dotenv
import json
import tempfile
import time

load_dotenv()

def get_credentials():
    """Get Google Drive credentials from environment JSON string"""
    service_account_json = os.getenv('GOOGLE_SERVICE_JSON')
    if not service_account_json:
        raise ValueError("GOOGLE_SERVICE_JSON not found in environment variables")
    
    # Parse the JSON string
    service_account_info = json.loads(service_account_json)
    
    # Create credentials from the parsed JSON
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info,
        scopes=['https://www.googleapis.com/auth/drive.file']
    )
    
    return credentials

def upload_file_to_drive(file_path: str, folder_id: str = "1l-wV54W5S6b8cTMD-qbGp4hlkNN7txvh", mime_type: str = None) -> dict:
    """
    Upload a file to a specific Google Drive folder using service account credentials.
    
    Args:
        file_path (str): Path to the file to upload
        folder_id (str): ID of the Google Drive folder to upload to
        mime_type (str, optional): MIME type of the file. If None, will be guessed
        
    Returns:
        dict: Response from Google Drive API containing file details
    """
    try:
        # Get credentials using the JSON string from environment
        credentials = get_credentials()
        
        # Build the Drive API service
        service = build('drive', 'v3', credentials=credentials)
        
        # Prepare the file metadata
        file_metadata = {
            'name': os.path.basename(file_path),
            'parents': [folder_id]
        }
        
        # Create the media file upload object
        media = MediaFileUpload(
            file_path,
            mimetype=mime_type,
            resumable=True
        )
        
        # Execute the upload
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, name, webViewLink'
        ).execute()
        
        return {
            'success': True,
            'file_id': file.get('id'),
            'name': file.get('name'),
            'web_link': file.get('webViewLink')
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def list_files_in_folder(folder_id: str) -> dict:
    """
    List all files in a specific Google Drive folder.
    
    Args:
        folder_id (str): ID of the Google Drive folder
        
    Returns:
        dict: List of files with their details
    """
    try:
        # Get credentials using the JSON string from environment
        credentials = get_credentials()
        
        service = build('drive', 'v3', credentials=credentials)
        
        # Query files in the specified folder
        results = service.files().list(
            q=f"'{folder_id}' in parents",
            pageSize=100,
            fields="files(id, name, mimeType, webViewLink, createdTime)"
        ).execute()
        
        return {
            'success': True,
            'files': results.get('files', [])
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def upload_json_to_drive(json_data: dict, folder_id: str="1l-wV54W5S6b8cTMD-qbGp4hlkNN7txvh", filename: str = None) -> dict:
    """
    Upload JSON data directly to a specific Google Drive folder.
    
    Args:
        json_data (dict): The JSON data to upload
        folder_id (str): ID of the Google Drive folder to upload to
        filename (str, optional): Name for the file. If None, uses timestamp
        
    Returns:
        dict: Response from Google Drive API containing file details
    """
    try:
        # Get credentials using the JSON string from environment
        credentials = get_credentials()
        
        # Build the Drive API service
        service = build('drive', 'v3', credentials=credentials)
        
        # Create a temporary file with the JSON data
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            json.dump(json_data, temp_file, indent=2)
            temp_file_path = temp_file.name
        
        try:
            # If no filename provided, use timestamp
            if not filename:
                timestamp = int(time.time())
                filename = f"data_{timestamp}.json"
            elif not filename.endswith('.json'):
                filename += '.json'
            
            # Prepare the file metadata
            file_metadata = {
                'name': filename,
                'parents': [folder_id],
                'mimeType': 'application/json'
            }
            
            # Create the media file upload object
            media = MediaFileUpload(
                temp_file_path,
                mimetype='application/json',
                resumable=True
            )
            
            # Execute the upload
            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name, webViewLink'
            ).execute()
            
            return {
                'success': True,
                'file_id': file.get('id'),
                'name': file.get('name'),
                'web_link': file.get('webViewLink')
            }
            
        finally:
            # Clean up the temporary file
            os.unlink(temp_file_path)
            
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
