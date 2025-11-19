# gsc-index-alert
This Python script monitors whether specific URLs from your website are indexed by Google using the Google Search Console API.  
If any monitored URL is not indexed, you’ll receive an email.

This is my frist ever Python script. In this blogpost I explain why I built it. [corinaburri.com/gsc-index-alert/](https://corinaburri.com/gsc-index-alert/)

## Features

- Uses the URL Inspection API from Google Search Console  
- Sends email alerts for de-indexed URLs  
- Supports `.env` for secure credentials  
- Cron-job ready for automated weekly checks  

---

## Setup

1. **Clone the repository**

Run in Terminal:

```bash
git clone https://github.com/yourusername/gsc-index-alert.git
cd gsc-index-alert
```

2. **Create your .env file based on .env.example:**
```bash

SMTP_SERVER=
SMTP_PORT=
SENDER_EMAIL=
SENDER_PASSWORD=
RECIPIENT_EMAIL=
SITE_URL=
```
3. **Add your Google OAuth credentials**

Place your own credentials file named `credentials.json` in the project folder.
Do not share this file publicly.
Optionally, keep a placeholder `credentials.json.example` for reference

4. **Add URLs to monitor**

Edit `urls.txt` and enter one URL per line.
I added a non-exist URL to test the script.

5. **Install dependencies**

```bash
pip3 install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client python-dotenv
```

5. **Run the script**
```
python3 gsc_alert.py
```

6. **Automate with cron (macOS )**
Example: run every Tuesday at 10:35 am
```
35 10 * * 2 /usr/bin/python3 /path/to/gsc_alert.py >> /path/to/gsc_alert.log 2>&1
```

   
---

## **Notes**

The script generates ```token.json``` after OAuth login. Do not commit this file.
Keep ```.env``` and ```credentials.json``` private to protect your credentials.


Contributions are welcome, you can also [buy me a coffee](https://buymeacoffee.com/corinaburri).
