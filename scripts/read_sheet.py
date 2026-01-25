from googleapiclient.discovery import build
import google.auth

SPREADSHEET_ID = "1jKdw4CsEbBOarEfYaDODsI88OsNkJBHARB3sV9XaQYQ"
RANGE = "Sheet1!A2:C"

def main():
    creds, _ = google.auth.default(scopes=[
        "https://www.googleapis.com/auth/spreadsheets.readonly"
    ])

    service = build("sheets", "v4", credentials=creds)

    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE
    ).execute()

    rows = result.get("values", [])

    print(f"Read {len(rows)} rows")
    for row in rows:
        print(row)

if __name__ == "__main__":
    main()
