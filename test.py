from google.oauth2 import service_account
from googleapiclient.discovery import build

# 서비스 계정 키 파일 경로
SERVICE_ACCOUNT_FILE = '/Users/ykpark/Downloads/gs-python-425314-cbc3bd9b486a.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# Google Sheet ID
SAMPLE_SPREADSHEET_ID = '14xN1CNfh8FtqGBZSuOaBPZuxwm5JmD7KxypK1ArO3Ns'
SHEET_NAME = 'datasheet'
SAMPLE_RANGE_NAME = f'{SHEET_NAME}!A1:A3'

# 인증 및 Google Sheets API 초기화
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# API 요청 보내기
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range=SAMPLE_RANGE_NAME).execute()

values = result.get('values', [])
if not values:
    print('No data found.')
else:
    for row in values:
        print(row)
