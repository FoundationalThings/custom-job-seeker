from googleapiclient.discovery import build

def main():
    service = build("sheets", "v4")

    sheet_id = "1jKdw4CsEbBOarEfYaDODsI88OsNkJBHARB3sV9XaQYQ"
    result = service.spreadsheets().get(
        spreadsheetId=sheet_id
    ).execute()

    print("Sheet title:", result["properties"]["title"])

if __name__ == "__main__":
    main()
