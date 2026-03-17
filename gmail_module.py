import os.path
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

class GmailManager:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
        self.creds = None
        self.service = None
        self.authenticated = False

    def authenticate(self):
        """Standard Desktop Auth Flow for Vira with fallback"""
        try:
            if os.path.exists('token.json'):
                self.creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
            
            # If there are no (valid) credentials available, let the user log in.
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    if os.path.exists('credentials.json'):
                        flow = InstalledAppFlow.from_client_secrets_file(
                            'credentials.json', self.SCOPES)
                        # This opens your browser locally
                        self.creds = flow.run_local_server(port=0)
                    else:
                        print("Gmail credentials.json not found. Using demo mode.")
                        return False
            
            # Save the credentials for the next run
            if self.creds:
                with open('token.json', 'w') as token:
                    token.write(self.creds.to_json())
                self.service = build('gmail', 'v1', credentials=self.creds)
                self.authenticated = True
                return True
            else:
                return False
                
        except Exception as e:
            print(f"Gmail authentication failed: {e}")
            return False

    def ensure_authenticated(self):
        """Ensure Gmail is authenticated, fallback to demo mode if not"""
        if not self.authenticated:
            return self.authenticate()
        return True

    def get_latest_unread(self):
        """Get latest unread email with demo fallback"""
        if not self.ensure_authenticated():
            return self._get_demo_email()
        
        try:
            results = self.service.users().messages().list(userId='me', q="is:unread", maxResults=1).execute()
            messages = results.get('messages', [])
            if not messages: 
                return self._get_demo_email()
            
            msg = self.service.users().messages().get(userId='me', id=messages[0]['id']).execute()
            
            # Extract sender
            sender = next(h['value'] for h in msg['payload']['headers'] if h['name'] == 'From')
            sender = sender.split('<')[0].strip() if '<' in sender else sender
            
            # Extract subject
            subject = next(h['value'] for h in msg['payload']['headers'] if h['name'] == 'Subject')
            
            # Use snippet as body
            body = msg.get('snippet', '')
            
            return {'sender': sender, 'subject': subject, 'body': body}
        except Exception as e:
            print(f"Error accessing Gmail: {e}")
            return self._get_demo_email()

    def _get_demo_email(self):
        """Return demo email data when Gmail is not available"""
        return {
            'sender': 'demo@example.com',
            'subject': 'Demo Email - Vira Assistant',
            'body': 'This is a demo email for testing Vira Assistant. The Gmail service is not configured, so this is sample data. You can set up Gmail authentication by adding credentials.json file.'
        }

    def send_mail(self, to, subject, body):
        """Send an email using Gmail API with demo fallback"""
        if not self.ensure_authenticated():
            print(f"Demo mode: Would send email to {to} with subject '{subject}'")
            return True
        
        try:
            message = f"From: me\r\nTo: {to}\r\nSubject: {subject}\r\n\r\n{body}"
            raw_message = base64.urlsafe_b64encode(message.encode()).decode()
            
            self.service.users().messages().send(
                userId='me', 
                body={'raw': raw_message}
            ).execute()
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False

    def get_summary(self):
        # Placeholder for your summarization logic
        content = self.get_latest_unread()
        if content:
            return f"Summary: From {content['sender']}: {content['body'][:100]}..."
        return "Summary: No unread emails"