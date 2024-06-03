from googleapiclient.discovery import build
from google.oauth2 import service_account
import pandas as pd

# 서비스 계정 키 파일 경로
SERVICE_ACCOUNT_FILE = '/Users/ykpark/Downloads/gs-python-425314-cbc3bd9b486a.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# Google Sheet ID
SAMPLE_SPREADSHEET_ID = '14xN1CNfh8FtqGBZSuOaBPZuxwm5JmD7KxypK1ArO3Ns'

# 시트 이름을 정확하게 지정합니다.
SHEET_NAME = 'datasheet'

# Google Sheet에서 데이터 가져올 범위
SAMPLE_RANGE_NAME = f'{SHEET_NAME}!A1:C'

# 인증 및 Google Sheets API 초기화
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

def fetch_data():
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    
    if not values:
        print('No data found.')
        return None
    else:
        df = pd.DataFrame(values[1:], columns=values[0])
        return df

def update_html(df):
    with open('template.html', 'r') as file:
        html_template = file.read()

    table_rows = ""
    for index, row in df.iterrows():
        table_rows += f"<tr><td>{row['date']}</td><td>{row['title']}</td><td><a href='{row['datalink']}'>Download</a></td></tr>\n"

    updated_html = html_template.replace("{{TABLE_ROWS}}", table_rows)

    with open('index.html', 'w') as file:
        file.write(updated_html)

if __name__ == "__main__":
    df = fetch_data()
    if df is not None:
        update_html(df)
    print("HTML file updated successfully.")
