from googleapiclient.discovery import build
import google.auth
import requests

SPREADSHEET_ID = "1jKdw4CsEbBOarEfYaDODsI88OsNkJBHARB3sV9XaQYQ"
RANGE = "A2:C"  # our columns: enabled, company, URL

def main():
    creds, _ = google.auth.default(scopes=[
        "https://www.googleapis.com/auth/spreadsheets.readonly"
    ])
    service = build("sheets", "v4", credentials=creds)

    # Read the sheet
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE
    ).execute()

    rows = result.get("values", [])
    enabled_companies = []

    for row in rows:
        enabled = row[0].strip().upper() if len(row) > 0 else ""
        company = row[1] if len(row) > 1 else "Unnamed Company"
        url = row[2] if len(row) > 2 else None

        if enabled == "TRUE" and url:
            enabled_companies.append((company, url))

    print("Checking URLs...")
    for company, url in enabled_companies:
        try:
            resp = requests.head(url, allow_redirects=True, timeout=10)
            status = resp.status_code
            if status == 404:
                print(f"- {company} → {url} [404 ❌]")
            else:
                print(f"- {company} → {url} [{status} ✅]")
        except requests.RequestException as e:
            print(f"- {company} → {url} [ERROR ⚠️: {e}]")

if __name__ == "__main__":
    main()
