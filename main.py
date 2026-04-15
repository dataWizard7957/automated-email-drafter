import os
import base64
import json
import time
from dotenv import load_dotenv
from groq import Groq
from email.message import EmailMessage

# Google
import gspread
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# ---------------- INIT ----------------
load_dotenv()
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/gmail.compose',
    'https://www.googleapis.com/auth/drive.readonly'
]

# ---------------- GOOGLE AUTH ----------------
def get_google_auth():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

# ---------------- CLEAN RATE ----------------
def clean_rate(rate):
    try:
        if isinstance(rate, str):
            rate = rate.replace('%', '').strip()
        return float(rate)
    except:
        return 0.0

# ---------------- FETCH DATA ----------------
def fetch_sheet_data(sheet_name):
    creds = get_google_auth()
    gc = gspread.authorize(creds)

    sh = gc.open(sheet_name)
    worksheet = sh.get_worksheet(0)
    records = worksheet.get_all_records()

    return records, creds

# ---------------- AI EMAIL ----------------
def generate_ai_content(name, contact, rate, status, notes, audit_date):
    prompt = f"""
  Instructions:
- If compliance ≥ 90: use an appreciative and congratulatory tone. Recognize specific strengths.
- If 80–89: use an encouraging tone. Acknowledge progress and suggest one improvement.
- If <80: use a concerned but supportive tone. Clearly explain issues and include 1 actionable suggestion.
- Do NOT praise performance if compliance is below 80%.

- Mention the specific issues from "Notes" clearly and contextually.
- Convert the audit date into a natural format (e.g., April 8, 2026).

- Keep the email concise (120–180 words), clear, and natural (avoid robotic phrasing).
- Avoid generic phrases like "we appreciate your efforts" unless justified by performance.
- Make the email feel personalized and specific to the partner.

- Structure:
  1. Greeting using the contact name
  2. Reference audit and compliance
  3. Key feedback (based on performance)
  4. Actionable suggestion (if needed)
  5. Closing

- End with:
  Best regards,  
  [Your Name]  
  Fortify Health

Output JSON:
{{
  "subject": "...",
  "body": "..."
}}
    """

    try:
        completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Return ONLY valid JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.6,
        )

        res = json.loads(completion.choices[0].message.content)
        return res.get("subject"), res.get("body")

    except Exception as e:
        print(f"Groq Error: {e}")
        return (
            "Fortify Health: Compliance Update",
            f"Hi {contact},\n\nFollowing up on your recent audit.\n\nRegards,\nFortify Health"
        )

# ---------------- CREATE GMAIL DRAFT ----------------
def create_gmail_draft(creds, to, subject, body):
    service = build('gmail', 'v1', credentials=creds)

    message = EmailMessage()
    message.set_content(body)
    message['To'] = to
    message['Subject'] = subject

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    service.users().drafts().create(
        userId="me",
        body={'message': {'raw': encoded_message}}
    ).execute()

# ---------------- PROCESS PARTNERS ----------------
def process_partners(sheet_name):
    records, creds = fetch_sheet_data(sheet_name)

    results = []

    for partner in records:
        name = partner.get('partner_name', 'Partner')
        contact = partner.get('contact_person', 'Team')
        email = partner.get('email')
        raw_rate = partner.get('compliance_rate', 0)
        rate = clean_rate(raw_rate)  
        audit_date = partner.get('last_audit_date', 'Recently')
        status = partner.get('status', 'Active')
        notes = partner.get('key_issues/notes', 'No major issues noted.')

        if not email:
            continue

        subject, body = generate_ai_content(
            name, contact, rate, status, notes, audit_date
        )

        results.append({
            "name": name,
            "email": email,
            "subject": subject,
            "body": body,
            "rate": rate  
        })

        time.sleep(1)  # prevent rate limits

    return results, creds

# ---------------- TEST RUN ----------------
if __name__ == "__main__":
    fetch_sheet_data("Mill Partner Compliance")
    print("✅ Auth successful. Now run Streamlit.")
