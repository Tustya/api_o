from a1range import A1Range
import os.path
from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'credentials.json')

credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1WmjZY6ClPzGHoky4_fj4E3mSnLMvo7KUbmMQQMWusGw'
SAMPLE_RANGE_NAME = 'Лист1'


service = build('sheets', 'v4', credentials=credentials).spreadsheets().values()

# Call the Sheets API
result = service.get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                     range=SAMPLE_RANGE_NAME).execute()
print(result)

# data_from_sheet = result.get('values', [])

# array = {'values': [[5, 6, None, 100], ['=SUM(A1:A4)', '=SUM(B1:B4)']]}
# range_ = A1Range.create_a1range_from_list('Sheet1', 4, 1, array['values']).format()
# response = service.update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
#                           range=range_,
#                           valueInputOption='USER_ENTERED',
#                           body=array).execute()