import os
import smtplib
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from dotenv import load_dotenv
load_dotenv()



# -----------------------
# CONFIGURATION
# -----------------------
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")
SITE_URL = os.getenv("SITE_URL")

SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]

# -----------------------
# LOAD URLS FROM FILE
# -----------------------
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(script_dir, "urls.txt"), "r") as f:
    URLS = [line.strip() for line in f if line.strip()]

# -----------------------
# AUTHENTICATION
# -----------------------

def get_gsc_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("searchconsole", "v1", credentials=creds)

# -----------------------
# CHECK INDEXATION
# -----------------------
def check_urls(service, urls):
    problem_states = [
        "URL_NOT_INDEXED",
        "BLOCKED_BY_ROBOTS",
        "INDEXING_BLOCKED",
        "INDEXING_STATE_UNSPECIFIED"
    ]
    
    not_indexed = []
    for url in urls:
        try:
            request = {
                "inspectionUrl": url,
                "siteUrl": SITE_URL
            }
            result = service.urlInspection().index().inspect(body=request).execute()
            index_result = result["inspectionResult"]["indexStatusResult"]
            status = index_result.get("indexingState", "UNKNOWN")  # e.g., INDEXED, INDEXING_ALLOWED
            reason = index_result.get("reason", "")  # optional extra info

            # Only show URLs with a problem
            if status in problem_states:
                print(f"{url} → {status} {f'({reason})' if reason else ''}")
                not_indexed.append((url, f"{status} {f'({reason})' if reason else ''}"))
                
        except Exception as e:
            print(f"Error with {url}: {e}")
            not_indexed.append((url, "Error"))
    
    return not_indexed

# -----------------------
# SEND EMAIL
# -----------------------
def send_email(urls):
    if not urls:
        print("All URLs are indexed ✅ No email sent.")
        return


         # Count the number of not-indexed URLs
    not_indexed_count = len(urls)
    
    body_lines = [f"⚠️ The following {not_indexed_count} URLs are not indexed:\n"]
    for url, status in urls:
        body_lines.append(f"{url} → {status}")

    body = "\n".join(body_lines)

    msg = MIMEText(body)
    msg["Subject"] = f"Indexation Alert: {not_indexed_count} URLs are not indexed - Google Search Console"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        print("Email sent successfully ✅")
    except Exception as e:
        print("Error sending email:", e)


# -----------------------
# MAIN
# -----------------------
if __name__ == "__main__":
    service = get_gsc_service()
    not_indexed = check_urls(service, URLS)
    send_email(not_indexed)
