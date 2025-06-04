import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/drive"]
# Path to service account JSON. Replace with your file path.
SERVICE_ACCOUNT_FILE = "service_account.json"
# ID of the parent folder in Google Drive where new folders will be created.
PARENT_FOLDER_ID = "YOUR_PARENT_FOLDER_ID"

df = pd.read_excel("Telegram_Chat_IDs.xlsx")

def clean(name):
    return ''.join(c for c in str(name) if c.isalnum() or c in ' _-').strip().replace(" ", "_")[:100]

# Authorize and build Drive service using a service account.
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
service = build("drive", "v3", credentials=creds)

for name in df["Название"]:
    folder_name = clean(name)
    if not folder_name:
        continue
    file_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [PARENT_FOLDER_ID],
    }
    try:
        service.files().create(body=file_metadata, fields="id").execute()
        print(f"Created folder: {folder_name}")
    except Exception as e:
        print(f"Failed to create folder {folder_name}: {e}")
