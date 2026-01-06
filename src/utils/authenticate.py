import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# The required scopes for accessing Google Cloud APIs
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

def authenticate():
    creds = None
    # Check if the token.pickle file already exists (this file stores the user's access and refresh tokens)
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If there are no credentials or they are invalid, request new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())  # Refresh the credentials if expired
        else:
            # If no valid credentials, prompt user to log in
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)  # Load the credentials from the JSON file
            creds = flow.run_local_server(port=0)  # Start the OAuth flow
        # Save the credentials for future use
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return creds
