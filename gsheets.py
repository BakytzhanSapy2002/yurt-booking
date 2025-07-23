# gsheets.py

import os
import json
from google.oauth2.service_account import Credentials
import gspread
from dotenv import load_dotenv

load_dotenv()  # .env файлын оқимыз

def get_gsheets_client():
    credentials_dict = {
        "type": "service_account",
        "project_id": os.environ["GOOGLE_PROJECT_ID"],
        "private_key_id": os.environ["GOOGLE_PRIVATE_KEY_ID"],
        "private_key": os.environ["GOOGLE_PRIVATE_KEY"].replace("\\n", "\n"),
        "client_email": os.environ["GOOGLE_CLIENT_EMAIL"],
        "client_id": os.environ["GOOGLE_CLIENT_ID"],
        "auth_uri": os.environ["GOOGLE_AUTH_URI"],
        "token_uri": os.environ["GOOGLE_TOKEN_URI"],
        "auth_provider_x509_cert_url": os.environ["GOOGLE_AUTH_PROVIDER_X509_CERT_URL"],
        "client_x509_cert_url": os.environ["GOOGLE_CLIENT_X509_CERT_URL"]
    }

    credentials = Credentials.from_service_account_info(credentials_dict)
    return gspread.authorize(credentials)