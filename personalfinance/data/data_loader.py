import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID of your existing spreadsheet
SPREADSHEET_ID = '1qncxXfqgbsFmCqRuBF7eiqKFQrY3573dyUKTRYy2sU0'
RANGE_NAME = 'data!A:Z'  # Adjust this to match your sheet's structure

def get_google_sheets_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('sheets', 'v4', credentials=creds)

def load_transactions():
    service = get_google_sheets_service()
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=RANGE_NAME).execute()
    values = result.get('values', [])
    if not values:
        return []
    # Assuming the first row is headers
    headers = values[0]
    return [dict(zip(headers, row)) for row in values[1:]]

def save_transactions(transactions):
    service = get_google_sheets_service()
    sheet = service.spreadsheets()
    
    # Assuming the first row is headers
    headers = list(transactions[0].keys())
    values = [headers] + [list(t.values()) for t in transactions]
    
    body = {'values': values}
    result = sheet.values().update(
        spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
        valueInputOption='USER_ENTERED', body=body).execute()
    print(f"{result.get('updatedCells')} cells updated.")
