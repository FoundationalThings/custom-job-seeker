from googleapiclient.discovery import build
import google.auth

SPREADSHEET_ID = "1jKdw4CsEbBOarEfYaDODsI88OsNkJBHARB3sV9XaQYQ"
RANGE = "A2:C"  # start from row 2 to skip headers

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
    enabled_companies = []

    for row in rows:
        enabled = row[0].strip().upper() if len(row) > 0 else ""
        company = row[1] if len(row) > 1 else "Unnamed Company"
        url = row[2] if len(row) > 2 else "No URL"

        if enabled == "TRUE":
            enabled_companies.append((company, url))

    print("Enabled companies:")
    for company, url in enabled_companies:
        print(f"- {company} → {url}")

if __name__ == "__main__":
    main()
