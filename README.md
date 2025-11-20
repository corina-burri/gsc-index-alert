# gsc-index-alert
This Python script monitors whether specific URLs from your website are indexed by Google using the Google Search Console API.  
If any monitored URL is deindexed, you’ll receive an email.

Full walkthrough is here: [corinaburri.com/gsc-index-alert/](https://corinaburri.com/gsc-index-alert/) (And also, this is my very first Python project. Any feedback is welcome).

## Features

- Uses the URL Inspection API from Google Search Console  
- Sends email alerts for de-indexed URLs  
- Supports `.env` for secure credentials  
- Cron-job ready for automated weekly checks  

## Requirements
 - Google account with your website [verified](https://support.google.com/webmasters/answer/9008080) in Google Search Console.

---

## Setup

1. **Clone the repository**

Run in Terminal:

```bash
git clone https://github.com/Corina-Bu/gsc-index-alert.git
cd gsc-index-alert
```

2. **Add URLs to monitor**

Edit `urls.txt` and enter one URL per line.
I added a non-existent URL to confirm that the script is working in case all URLs are indexed.


3. **Add your Google OAuth credentials**
4. 
This script uses Google's OAuth. For full instructions on enabling the Google Search Console API and creating `credentials.json`, see the walkthrough on the [blogpost](https://www.corinaburri.com/gsc-index-alert/) in the section [_Enable Google Search Console API on Google Cloud_](https://www.corinaburri.com/gsc-index-alert/#4-enable-google-search-console-api-on-google-cloud).

Place your own credentials file named `credentials.json` in the project folder.
Do not share this file publicly.
Optionally, keep a placeholder `credentials.json.example` for reference.

4. **Create your .env file based on .env.example:**
   
```bash

SMTP_SERVER=
SMTP_PORT=
SENDER_EMAIL=
SENDER_PASSWORD=
RECIPIENT_EMAIL=
SITE_URL=
```


5. **Install dependencies**

```bash
pip3 install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client python-dotenv
```

6. **Run the script**

```bash
pip3 install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client python-dotenv
```
Or with an absolute path:
```bash
python3 /path/to/your/folder/gsc_alert.py
```

7. **Automate with cron (macOS )**
Example: run every Tuesday at 10:35 am
```
35 10 * * 2 /usr/bin/python3 /path/to/gsc_alert.py >> /path/to/gsc_alert.log 2>&1
```



   
---

## **Notes**

The script generates ```token.json``` after OAuth login. Do not commit this file.
Keep ```.env``` and ```credentials.json``` private to protect your credentials.


Contributions are welcome, you can also [buy me a coffee](https://buymeacoffee.com/corinaburri).
