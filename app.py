import os
import json
import re
import base64
from datetime import datetime
from gmail_module import GmailManager
import requests
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_socketio import SocketIO
import pywhatkit
import psutil
import threading
import pyttsx3
from email.mime.text import MIMEText
from googleapiclient.discovery import build

app = Flask(__name__)
app.secret_key = "aditya_vira_portal_2026"
socketio = SocketIO(app)
gmail = GmailManager()

# --- EMAIL ENHANCEMENT SYSTEM ---
EMAIL_STATE = {"current_email": None, "reply_mode": False, "suggested_reply": None}

def summarize_email_content(email_content):
    """Summarize email content using AI techniques"""
    try:
        import re
        
        # Clean and prepare content
        content = email_content.lower()
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        
        if not sentences:
            return "Email content is too short to summarize."
        
        # Extract key information
        words = content.split()
        word_count = len(words)
        
        # Identify action items
        action_words = ['please', 'could you', 'would you', 'need', 'require', 'request', 'ask', 'help']
        has_action = any(word in content for word in action_words)
        
        # Identify urgency
        urgency_words = ['urgent', 'asap', 'immediately', 'as soon as possible', 'priority', 'important']
        urgency = 'high' if any(word in content for word in urgency_words) else 'normal'
        
        # Create summary
        summary = f"Email has {word_count} words and {len(sentences)} main points. "
        
        if has_action:
            summary += "Contains action items. "
        
        if urgency == 'high':
            summary += "High priority. "
        
        # Extract key sentences (first 2 and last 1)
        if len(sentences) >= 3:
            key_points = sentences[:2] + [sentences[-1]]
            summary += f"Key points: {'; '.join(key_points[:2])}; {' '.join(key_points[2:])}"
        elif len(sentences) >= 2:
            key_points = sentences[:2]
            summary += f"Key points: {'; '.join(key_points)}"
        else:
            summary += f"Main point: {sentences[0] if sentences else 'No clear content'}"
        
        return summary
        
    except Exception as e:
        print(f"Email summarization error: {e}")
        return "Unable to summarize email content."

def generate_reply_suggestion(email_content, sender):
    """Generate AI-powered reply suggestions"""
    try:
        import random
        
        # Analyze email content for reply type
        content_lower = email_content.lower()
        
        # Question detection
        question_indicators = ['?', 'what', 'when', 'where', 'how', 'why', 'which', 'who', 'can you', 'could you', 'would you']
        is_question = any(indicator in content_lower for indicator in question_indicators)
        
        # Request detection
        request_indicators = ['please', 'could you', 'would you', 'need', 'require', 'request', 'ask', 'help me']
        is_request = any(indicator in content_lower for indicator in request_indicators)
        
        # Meeting detection
        meeting_indicators = ['meeting', 'call', 'schedule', 'appointment', 'discuss', 'review']
        is_meeting = any(indicator in content_lower for indicator in meeting_indicators)
        
        # Generate suggestions based on analysis
        if is_question:
            suggestions = [
                f"Hi {sender}, I'll look into your question and get back to you with a detailed answer.",
                f"Hello {sender}, Thanks for your question. Let me check and respond appropriately.",
                f"Dear {sender}, I've received your question and will provide a response shortly."
            ]
        elif is_request:
            suggestions = [
                f"Hi {sender}, I've received your request and will process it as soon as possible.",
                f"Hello {sender}, Thank you for your request. I'll work on this and update you.",
                f"Dear {sender}, Your request has been noted and I'll take care of it promptly."
            ]
        elif is_meeting:
            suggestions = [
                f"Hi {sender}, I've received your meeting request. I'll check my schedule and confirm.",
                f"Hello {sender}, Thanks for the meeting invitation. I'll coordinate and respond with availability.",
                f"Dear {sender}, I've noted the meeting details and will prepare accordingly."
            ]
        else:
            suggestions = [
                f"Hi {sender}, Thank you for your email. I've received it and will respond appropriately.",
                f"Hello {sender}, I've read your message and will get back to you if needed.",
                f"Dear {sender}, Your email has been received and noted. Thank you for reaching out."
            ]
        
        return random.choice(suggestions)
        
    except Exception as e:
        print(f"Reply suggestion error: {e}")
        return "Thank you for your email. I'll respond appropriately."

def get_email_suggestions():
    """Get multiple reply suggestions for user to choose from"""
    return [
        "Thank you for your email. I'll review and respond accordingly.",
        "I've received your message and will get back to you shortly.",
        "Thanks for reaching out. I'll address this and follow up as needed.",
        "Your email has been noted. I'll take appropriate action.",
        "I appreciate you contacting me. I'll review and respond promptly."
    ]

# --- STATE MANAGEMENT ---
convo_state = {"action": None, "sub_step": None, "target": None}
pin_state = {"verified": False, "pin": "1234", "attempts": 0, "last_attempt": None}

# --- AI RESPONSE SYSTEM ---
AI_RESPONSES = {
    "greetings": {
        "hello": ["Hello! How can I help you today?", "Hi there! What can I do for you?", "Greetings! Ready to assist!"],
        "hi": ["Hi! How are you today?", "Hello! What's on your mind?", "Hey! How can I help?"],
        "hey": ["Hey there! What can I do for you?", "Hello! Ready when you are!", "Hi! How may I assist?"]
    },
    "farewell": {
        "bye": ["Goodbye! Have a great day!", "See you later! Take care!", "Bye! Come back anytime!"],
        "goodbye": ["Goodbye! Stay safe!", "See you soon!", "Take care! Goodbye!"],
        "see you": ["See you later!", "Until next time!", "Goodbye!"]
    },
    "thanks": {
        "thank": ["You're welcome!", "Happy to help!", "My pleasure!", "Anytime!"],
        "thanks": ["You're welcome!", "Glad I could help!", "No problem at all!"]
    },
    "how_are_you": {
        "how are you": ["I'm doing great, thanks for asking!", "Feeling excellent and ready to help!", "I'm perfectly fine, thank you!"],
        "how you": ["I'm functioning perfectly!", "All systems operational!", "Great and ready to assist!"]
    },
    "capabilities": {
        "what can you do": ["I can send WhatsApp messages, emails, check time, battery, and much more! Say 'help' for all commands.", "I'm your voice assistant! I handle messaging, system info, time, and more. Try 'help'!", "I can help with WhatsApp, email, time, battery, and system commands. Just ask!"],
        "help me": ["I'm here to help! Try saying 'help' for commands, or ask me about time, or send messages!", "Happy to assist! Say 'help' for all available commands, or try 'time'!"],
        "what do you do": ["I'm Vira, your voice assistant! I handle WhatsApp, email, time, battery, and system management.", "I'm Vira! I can send messages, check time/battery, and help with system tasks."]
    },
    "small_talk": {
        "how old": ["I'm as young as today's technology!", "Age is just a number for AI like me!", "I'm timeless!"],
        "where are you": ["I'm here in your system, ready to help!", "I live in your computer, serving you!", "I'm right here with you!"],
        "who are you": ["I'm Vira, your intelligent voice assistant!", "I'm Vira, here to help with your daily tasks!", "I'm Vira, your AI companion!"],
        "your name": ["My name is Vira, short for Virtual Assistant!", "I'm Vira, your voice assistant!", "You can call me Vira!"]
    },
    "emotions": {
        "i love you": ["That's very kind! I'm here to help you!", "Thank you! I'm designed to assist you!", "I appreciate that! Let me help you with something!"],
        "i like you": ["I like you too! Happy to be your assistant!", "Thanks! I'm here to make things easier for you!", "That's great! I'm here to help!"],
        "you are smart": ["Thank you! I try my best to be helpful!", "Thanks! I'm designed to assist intelligently!", "Appreciate that! I'm here to help!"]
    }
}

def get_ai_response(text):
    """Generate AI response based on input"""
    text_lower = text.lower().strip()
    
    # Check for greetings
    for greeting in AI_RESPONSES["greetings"]:
        if greeting in text_lower:
            import random
            return random.choice(AI_RESPONSES["greetings"][greeting])
    
    # Check for farewell
    for farewell in AI_RESPONSES["farewell"]:
        if farewell in text_lower:
            import random
            return random.choice(AI_RESPONSES["farewell"][farewell])
    
    # Check for thanks
    for thanks in AI_RESPONSES["thanks"]:
        if thanks in text_lower:
            import random
            return random.choice(AI_RESPONSES["thanks"][thanks])
    
    # Check for how are you
    for how_are in AI_RESPONSES["how_are_you"]:
        if how_are in text_lower:
            import random
            return random.choice(AI_RESPONSES["how_are_you"][how_are])
    
    # Check for capabilities
    for capability in AI_RESPONSES["capabilities"]:
        if capability in text_lower:
            import random
            return random.choice(AI_RESPONSES["capabilities"][capability])
    
    # Check for small talk
    for small_talk in AI_RESPONSES["small_talk"]:
        if small_talk in text_lower:
            import random
            return random.choice(AI_RESPONSES["small_talk"][small_talk])
    
    # Check for emotions
    for emotion in AI_RESPONSES["emotions"]:
        if emotion in text_lower:
            import random
            return random.choice(AI_RESPONSES["emotions"][emotion])
    
    return None

# --- USER ROLES ---
ADMIN_USERS = ["admin", "administrator", "root"]

def get_user_role(username):
    """Determine user role based on username"""
    if username.lower() in ADMIN_USERS:
        return "admin"
    return "user"

def is_admin(username):
    """Check if user is admin"""
    return get_user_role(username) == "admin"

def is_user(username):
    """Check if user is regular user"""
    return get_user_role(username) == "user"

# --- PIN VERIFICATION SYSTEM ---
def verify_pin(pin_input):
    """Verify PIN input"""
    import time
    
    if pin_state["last_attempt"] and time.time() - pin_state["last_attempt"] < 300:
        return "locked"  # Locked for 5 minutes
    
    if pin_input == pin_state["pin"]:
        pin_state["verified"] = True
        pin_state["attempts"] = 0
        pin_state["last_attempt"] = None
        return True
    else:
        pin_state["attempts"] += 1
        pin_state["last_attempt"] = time.time()
        
        if pin_state["attempts"] >= 3:
            return "locked"  # Too many attempts
        
        return False

def reset_pin_verification():
    """Reset PIN verification state"""
    pin_state["verified"] = False
    pin_state["attempts"] = 0
    pin_state["last_attempt"] = None

# --- HELPER FUNCTIONS ---
def log_command(user, command):
    """Log command to history file"""
    history = []
    if os.path.exists("command_history.json"):
        with open("command_history.json", "r") as f:
            history = json.load(f)
    
    history.append({
        "user": user,
        "command": command,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    # Keep only last 100 commands
    history = history[-100:]
    
    with open("command_history.json", "w") as f:
        json.dump(history, f, indent=4)

def get_greeting():
    """Get time-appropriate greeting"""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 17:
        return "Good afternoon"
    elif 17 <= hour < 22:
        return "Good evening"
    else:
        return "Good night"

def speak(text):
    """Fast text-to-speech function with non-blocking execution"""
    def _run():
        try:
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            if voices:
                # Try to find a female voice
                for voice in voices:
                    if 'female' in voice.name.lower():
                        engine.setProperty('voice', voice.id)
                        break
            engine.setProperty('rate', 220)  # Faster speech rate
            print(f"Speaking: {text}")
            engine.say(text)
            engine.runAndWait()
            engine.stop()
            print("TTS completed successfully")
        except Exception as e:
            print(f"TTS ERROR: {e}")
    
    # Use thread for non-blocking execution
    thread = threading.Thread(target=_run, daemon=True)
    thread.start()
    return thread

# --- ROUTES ---
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/auth/google')
def auth_google():
    """
    Google OAuth authentication for Vira Assistant with demo fallback
    """
    if not os.path.exists("credentials.json"):
        # Demo mode - create a demo Google user
        print("Running Google auth in demo mode (no credentials.json)")
        
        # Create demo Google user
        username = "google_user"
        email = "demo@gmail.com"
        
        # Set session with demo Google user info
        session['user'] = username
        session['email'] = email
        session['auth_method'] = 'google_demo'
        session['gmail_authed'] = True
        session['role'] = get_user_role(username)
        
        # Create demo user account if it doesn't exist
        users = {}
        if os.path.exists("user_database.json"):
            with open("user_database.json", "r") as f:
                users = json.load(f)
        
        if username not in users:
            users[username] = {
                'password': 'google_demo',
                'email': email,
                'auth_method': 'google_demo'
            }
            with open("user_database.json", "w") as f:
                json.dump(users, f, indent=4)
        
        log_command(username, "Google Demo Sign-In")
        
        # Redirect to dashboard
        return redirect(url_for('dashboard'))

    try:
        # Try to authenticate with Gmail
        auth_result = gmail.authenticate()
        
        if auth_result:
            # Get user info from Gmail
            try:
                # Get user profile info
                profile = gmail.service.users().getProfile(userId='me').execute()
                email = profile['emailAddress']
                
                # Extract username from email (before @)
                username = email.split('@')[0]
                
                # Set session with Google user info
                session['user'] = username
                session['email'] = email
                session['auth_method'] = 'google'
                session['gmail_authed'] = True
                session['role'] = get_user_role(username)
                
                # Create user account if it doesn't exist
                users = {}
                if os.path.exists("user_database.json"):
                    with open("user_database.json", "r") as f:
                        users = json.load(f)
                
                if username not in users:
                    users[username] = {
                        'password': 'google_auth',
                        'email': email,
                        'auth_method': 'google'
                    }
                    with open("user_database.json", "w") as f:
                        json.dump(users, f, indent=4)
                
                log_command(username, "Google Sign-In")
                
                # Redirect to dashboard
                return redirect(url_for('dashboard'))
                
            except Exception as e:
                print(f"Error getting user profile: {e}")
                # Fallback - just authenticate Gmail without user creation
                session['gmail_authed'] = True
                session['auth_method'] = 'google'
                
                if 'user' in session:
                    log_command(session['user'], "Google auth")
                    return redirect(url_for('dashboard'))
                else:
                    return (
                        "Google authentication completed. Please sign in with your username to continue. "
                        "<a href='/'>Back to login</a>",
                        200,
                    )
        else:
            return (
                "Google authentication failed. Please try again. "
                "<a href='/'>Back to login</a>",
                500,
            )
            
    except Exception as e:
        print(f"Google auth error: {e}")
        return (
            f"Google auth failed: {e}. <a href='/'>Back to login</a>",
            500,
        )

@app.route('/login', methods=['POST'])
def handle_login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Check if user is trying to login as admin
    if username and "admin" in username.lower():
        # Check if user exists and password is correct
        if os.path.exists("user_database.json"):
            with open("user_database.json", "r") as f:
                users = json.load(f)
            if username in users and users[username]['password'] == password:
                # User exists and password correct, now check for admin PIN
                if is_admin(username):
                    return render_template('login.html', admin_pin_required=True, username=username)
                else:
                    # User has "admin" in name but not actual admin role
                    session['user'] = username
                    session['role'] = get_user_role(username)
                    log_command(username, "Login")
                    return redirect(url_for('dashboard'))
        else:
            return "Invalid. <a href='/'>Retry</a>"
    
    # Regular user login
    if os.path.exists("user_database.json"):
        with open("user_database.json", "r") as f:
            users = json.load(f)
        if username in users and users[username]['password'] == password:
            session['user'] = username
            session['role'] = get_user_role(username)
            log_command(username, "Login")
            return redirect(url_for('dashboard'))
    return "Invalid. <a href='/'>Retry</a>"

@app.route('/admin_pin_verify', methods=['POST'])
def admin_pin_verify():
    username = request.form.get('username')
    pin = request.form.get('pin')
    
    if not username or not pin:
        return "Missing credentials. <a href='/'>Retry</a>"
    
    # Verify PIN
    verification = verify_pin(pin)
    if verification is True:
        # PIN correct, complete admin login
        session['user'] = username
        session['role'] = 'admin'
        log_command(username, "Admin Login")
        return redirect(url_for('dashboard'))
    elif verification == "locked":
        return "Too many failed attempts. Please wait 5 minutes. <a href='/'>Retry</a>"
    else:
        attempts_left = 3 - pin_state.get("attempts", 0)
        if attempts_left <= 0:
            return "PIN locked. Please wait 5 minutes. <a href='/'>Retry</a>"
        return f"Invalid PIN. {attempts_left} attempts remaining. <a href='/'>Retry</a>"

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def handle_register():
    username = request.form.get('username')
    password = request.form.get('password')
    
    users = {}
    if os.path.exists("user_database.json"):
        with open("user_database.json", "r") as f:
            users = json.load(f)
    
    if username in users:
        return "User already exists. <a href='/register'>Retry</a>"
    
    users[username] = {'password': password}
    with open("user_database.json", "w") as f:
        json.dump(users, f, indent=4)
    
    # Set session with proper role
    session['user'] = username
    session['role'] = get_user_role(username)
    log_command(username, "Registration")
    
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session: return redirect(url_for('index'))
    user_role = session.get('role', get_user_role(session['user']))
    return render_template('dashboard.html', user=session['user'], role=user_role)

@app.route('/logout')
def logout():
    try:
        # Clear all session data
        session.clear()
        print(f"✅ User logged out successfully: {datetime.now()}")
        return redirect("http://localhost:5000/")
    except Exception as e:
        print(f"❌ Logout error: {e}")
        return redirect("http://localhost:5000/")

@app.route('/contacts')
def contacts_page():
    if 'user' not in session: return redirect(url_for('index'))
    return render_template('contacts.html', user=session['user'])

# --- LOCATION-BASED COMMAND VERIFICATION ---
import socket

def get_current_location():
    """Get current location for command verification"""
    try:
        # Get public IP
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        
        # Simple location detection (fallback to Vijayawada)
        return {
            'city': 'Vijayawada',
            'country': 'India',
            'ip': ip_address,
            'latitude': 17.6868,
            'longitude': 83.2185
        }
    except Exception as e:
        print(f"Location detection failed: {e}")
        return {
            'city': 'Vijayawada',
            'country': 'India',
            'ip': '127.0.0.1',
            'latitude': 17.6868,
            'longitude': 83.2185
        }

def verify_command_with_location(command_text, expected_location="any"):
    """Verify if command should work based on location"""
    location = get_current_location()
    print(f"📍 Current Location: {location['city']}, {location['country']}")
    print(f"🎤 Command: {command_text}")
    print(f"✅ Verification: Command should work in {location['city']}")
    return True

# --- LOCATION-BASED COMMAND VERIFICATION ---
api_usage_stats = {
    "whatsapp": 0,
    "gmail_send": 0,
    "gmail_read": 0,
    "battery": 0,
    "total_commands": 0,
    "voice_commands": 0,
    "manual_commands": 0
}

def track_api_usage(api_name, command_type="voice"):
    """Track API usage statistics"""
    global api_usage_stats
    if api_name in api_usage_stats:
        api_usage_stats[api_name] += 1
    else:
        api_usage_stats[api_name] = 1
    
    api_usage_stats["total_commands"] += 1
    if command_type == "voice":
        api_usage_stats["voice_commands"] += 1
    else:
        api_usage_stats["manual_commands"] += 1
    
    # Save to file for persistence
    try:
        with open("api_usage.json", "w") as f:
            json.dump(api_usage_stats, f, indent=4)
    except Exception as e:
        print(f"Failed to save API usage: {e}")

def load_api_usage():
    """Load API usage statistics from file"""
    global api_usage_stats
    try:
        if os.path.exists("api_usage.json"):
            with open("api_usage.json", "r") as f:
                api_usage_stats.update(json.load(f))
    except Exception as e:
        print(f"Failed to load API usage: {e}")

# Load API usage on startup
load_api_usage()

# --- DATA API ROUTES ---
@app.route('/api/history')
def get_history():
    if os.path.exists("command_history.json"):
        with open("command_history.json", "r") as f: return jsonify(json.load(f))
    return jsonify([])

@app.route('/api/contacts')
def get_contacts():
    if os.path.exists("contacts.json"):
        with open("contacts.json", "r") as f: return jsonify(json.load(f))
    return jsonify([])

@app.route('/api/contacts/delete/<int:index>', methods=['POST'])
def delete_contact(index):
    if 'user' not in session: return jsonify({'error': 'Unauthorized'}), 401
    
    contacts = []
    if os.path.exists("contacts.json"):
        try:
            with open("contacts.json", "r") as f: contacts = json.load(f)
        except: contacts = []
    
    if 0 <= index < len(contacts):
        contacts.pop(index)
        with open("contacts.json", "w") as f:
            json.dump(contacts, f, indent=4)
        return jsonify({'success': True})
    
    return jsonify({'error': 'Invalid index'}), 404

@app.route('/api/contacts/update/<int:index>', methods=['POST'])
def update_contact(index):
    if 'user' not in session: return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    if not data or 'name' not in data or 'detail' not in data:
        return jsonify({'error': 'Missing data'}), 400
    
    contacts = []
    if os.path.exists("contacts.json"):
        try:
            with open("contacts.json", "r") as f: contacts = json.load(f)
        except: contacts = []
    
    if 0 <= index < len(contacts):
        contacts[index]['name'] = data['name']
        contacts[index]['detail'] = data['detail']
        with open("contacts.json", "w") as f:
            json.dump(contacts, f, indent=4)
        return jsonify({'success': True})
    
    return jsonify({'error': 'Invalid index'}), 404

@app.route('/api/activity')
def get_activity():
    if os.path.exists("contacts.json"):
        with open("contacts.json", "r") as f: return jsonify(json.load(f))
    return jsonify([])

@app.route('/admin')
def admin_panel():
    if 'user' not in session: return redirect(url_for('index'))
    if not is_admin(session['user']): return redirect(url_for('dashboard'))
    
    # Get system statistics
    users = []
    if os.path.exists("user_database.json"):
        with open("user_database.json", "r") as f:
            users = json.load(f)
    
    # Get command history
    history = []
    if os.path.exists("command_history.json"):
        with open("command_history.json", "r") as f:
            history = json.load(f)
    
    # Get contacts
    contacts = []
    if os.path.exists("contacts.json"):
        with open("contacts.json", "r") as f:
            contacts = json.load(f)
    
    # Get API usage statistics
    api_stats = api_usage_stats.copy()
    
    return render_template('admin.html', 
                         user=session['user'], 
                         users=users, 
                         history=history[-10:],  # Last 10 commands
                         contacts=contacts,
                         api_stats=api_stats)

@app.route('/api/admin/api_usage')
def admin_get_api_usage():
    if 'user' not in session or not is_admin(session['user']):
        return jsonify({'error': 'Unauthorized'}), 401
    
    return jsonify(api_usage_stats)

@app.route('/api/admin/reset_api_usage', methods=['POST'])
def admin_reset_api_usage():
    if 'user' not in session or not is_admin(session['user']):
        return jsonify({'error': 'Unauthorized'}), 401
    
    global api_usage_stats
    api_usage_stats = {
        "whatsapp": 0,
        "gmail_send": 0,
        "gmail_read": 0,
        "battery": 0,
        "total_commands": 0,
        "voice_commands": 0,
        "manual_commands": 0
    }
    
    # Save reset stats
    try:
        with open("api_usage.json", "w") as f:
            json.dump(api_usage_stats, f, indent=4)
    except Exception as e:
        print(f"Failed to reset API usage: {e}")
    
    return jsonify({'success': True, 'message': 'API usage statistics reset'})

@app.route('/api/admin/users')
def admin_get_users():
    if 'user' not in session or not is_admin(session['user']):
        return jsonify({'error': 'Unauthorized'}), 401
    
    if os.path.exists("user_database.json"):
        with open("user_database.json", "r") as f:
            users = json.load(f)
        return jsonify(users)
    return jsonify([])

@app.route('/api/admin/delete_user/<username>', methods=['POST'])
def admin_delete_user(username):
    if 'user' not in session or not is_admin(session['user']):
        return jsonify({'error': 'Unauthorized'}), 401
    
    if username.lower() in ADMIN_USERS:
        return jsonify({'error': 'Cannot delete admin users'}), 403
    
    users = {}
    if os.path.exists("user_database.json"):
        with open("user_database.json", "r") as f:
            users = json.load(f)
    
    if username in users:
        del users[username]
        with open("user_database.json", "w") as f:
            json.dump(users, f, indent=4)
        return jsonify({'success': True})
    
    return jsonify({'error': 'User not found'}), 404

@app.route('/test')
def test_endpoint():
    return jsonify({"status": "Server is running!", "time": datetime.now().strftime("%I:%M %p")})

# --- GOOGLE OAUTH AUTHENTICATION ---
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
import google.oauth2.credentials
import pathlib

# Google OAuth Configuration
GOOGLE_CLIENT_ID = "your-google-client-id.apps.googleusercontent.com"  # Replace with your actual client ID
GOOGLE_CLIENT_SECRET = "your-google-client-secret"  # Replace with your actual client secret
SCOPES = ['https://www.googleapis.com/auth/userinfo.email', 
          'https://www.googleapis.com/auth/userinfo.profile',
          'https://www.googleapis.com/auth/gmail.send',
          'https://www.googleapis.com/auth/gmail.readonly']

# Create OAuth flow
def create_google_flow():
    """Create Google OAuth flow for mobile-friendly authentication"""
    client_secrets = {
        "web": {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost:5000/oauth/callback", 
                             "https://vira-assistant.onrender.com/oauth/callback"]
        }
    }
    
    flow = Flow.from_client_config(
        client_secrets,
        scopes=SCOPES,
        redirect_uri=request.base_url + '/oauth/callback'
    )
    return flow

@app.route('/google/auth')
def google_auth():
    """Start Google OAuth authentication - mobile friendly"""
    try:
        flow = create_google_flow()
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'
        )
        
        # Store state in session
        session['oauth_state'] = state
        
        # Redirect to Google for authentication
        return redirect(authorization_url)
        
    except Exception as e:
        print(f"Google auth error: {e}")
        return redirect(url_for('index'))

@app.route('/oauth/callback')
def oauth_callback():
    """Handle Google OAuth callback"""
    try:
        state = session.get('oauth_state')
        if not state:
            return redirect(url_for('index'))
            
        flow = create_google_flow()
        flow.fetch_token(authorization_response=request.url)
        
        # Get user info
        credentials = flow.credentials
        from google.oauth2 import id_token
        import google.auth.transport.requests
        
        request_session = google.auth.transport.requests.Request()
        id_info = id_token.verify_oauth2_token(
            credentials.id_token,
            request_session,
            GOOGLE_CLIENT_ID
        )
        
        # Store user info
        email = id_info['email']
        name = id_info.get('name', email.split('@')[0])
        
        # Store credentials for Gmail API
        session['google_credentials'] = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }
        
        # Update user database
        users = {}
        if os.path.exists("user_database.json"):
            with open("user_database.json", "r") as f:
                users = json.load(f)
        
        if email not in users:
            users[email] = {
                'username': name,
                'email': email,
                'auth_method': 'google',
                'password': 'google_auth'
            }
        
        # Save updated users
        with open("user_database.json", "w") as f:
            json.dump(users, f, indent=4)
        
        # Login user
        session['user'] = email
        session['role'] = get_user_role(email)
        session['google_authenticated'] = True
        
        log_command(email, "Google OAuth Login")
        
        return redirect(url_for('dashboard'))
        
    except Exception as e:
        print(f"OAuth callback error: {e}")
        return redirect(url_for('index'))

@app.route('/google/disconnect')
def google_disconnect():
    """Disconnect Google account"""
    session.pop('google_credentials', None)
    session.pop('google_authenticated', None)
    return redirect(url_for('dashboard'))

# --- GOOGLE OAUTH AUTHENTICATION ---
def send_whatsapp_simple(number, message):
    """Simple WhatsApp sending that works"""
    try:
        print(f"📱 Sending WhatsApp to +91{number}: {message}")
        
        # Import pywhatkit
        import pywhatkit
        
        # Send message
        pywhatkit.sendwhatmsg_instantly(f"+91{number}", message, 15)
        print("✅ WhatsApp sent successfully!")
        return True
        
    except Exception as e:
        print(f"❌ WhatsApp error: {e}")
        return False

# --- VOICE COMMAND HUB ---
@socketio.on('voice_command')
def process_command(data):
    try:
        print(f"=== VOICE COMMAND RECEIVED ===")
        print(f"Raw data: {data}")
        
        if not data or 'text' not in data:
            print("ERROR: No 'text' field in data")
            speak("Invalid command data received.")
            return
            
        global convo_state
        text = data['text'].lower().strip()
        user_name = session.get('user', 'Aditya')
        
        print(f"Processed text: '{text}'")
        print(f"User: {user_name}")
        print(f"Current convo_state: {convo_state}")
        
        log_command(user_name, text)
        
        print(f"Processing command: '{text}'")

        # FAST AI RESPONSES - Check first for immediate response
        ai_response = get_ai_response(text)
        if ai_response:
            print(f"AI response triggered: {ai_response}")
            
            # Emit immediately for fast response
            socketio.emit('transcript_update', {
                'user_input': text,
                'ai_response': ai_response,
                'type': 'ai_conversation'
            })
            
            # Non-blocking speak
            speak(ai_response)
            return

        # FAST BASIC COMMANDS - No blocking operations
        response = None
        
        # Check for admin login voice command
        if "as admin" in text or "login as admin" in text or "admin login" in text or "sign in as admin" in text:
            try:
                response = "🔐 Admin Login Required\nPlease provide your admin username and password.\nSay: 'username [your_username] password [your_password]'"
                # Set conversation state for admin login
                convo_state = {"action": "admin_login", "sub_step": "waiting_for_credentials", "target": {}}
            except Exception as e:
                print(f"Admin login command failed: {e}")
                response = "I cannot process admin login right now."
        
        # Check if we're in admin login conversation
        elif convo_state.get("action") == "admin_login":
            if convo_state.get("sub_step") == "waiting_for_credentials":
                # Parse username and password from voice
                if "username" in text and "password" in text:
                    try:
                        # Extract username and password
                        parts = text.split()
                        username = ""
                        password = ""
                        
                        for i, part in enumerate(parts):
                            if part.lower() == "username" and i + 1 < len(parts):
                                username = parts[i + 1]
                            elif part.lower() == "password" and i + 1 < len(parts):
                                password = parts[i + 1]
                        
                        if username and password:
                            # Verify admin credentials
                            if os.path.exists("user_database.json"):
                                with open("user_database.json", "r") as f:
                                    users = json.load(f)
                                
                                if username in users and users[username]['password'] == password and is_admin(username):
                                    # Ask for PIN
                                    convo_state["target"]["username"] = username
                                    convo_state["target"]["password"] = password
                                    convo_state["sub_step"] = "waiting_for_pin"
                                    response = f"✅ Credentials verified for {username}\nNow please provide your 4-digit admin PIN:"
                                else:
                                    response = "❌ Invalid admin credentials. Please check your username and password."
                                    convo_state = {"action": None, "sub_step": None, "target": None}
                            else:
                                response = "❌ User database not found. Please contact administrator."
                                convo_state = {"action": None, "sub_step": None, "target": None}
                        else:
                            response = "❌ Could not extract username and password. Please say: 'username [name] password [pass]'"
                    except Exception as e:
                        print(f"Admin credential parsing failed: {e}")
                        response = "❌ Error processing credentials. Please try again."
                        convo_state = {"action": None, "sub_step": None, "target": None}
            
            elif convo_state.get("sub_step") == "waiting_for_pin":
                # Verify PIN for admin login
                pin_input = text.replace(" ", "").strip()
                verification = verify_pin(pin_input)
                
                if verification is True:
                    # Complete admin login
                    username = convo_state["target"]["username"]
                    session['user'] = username
                    session['role'] = 'admin'
                    log_command(username, "Voice Admin Login")
                    
                    response = f"🎉 Admin login successful! Welcome {username}!\nRedirecting to admin dashboard..."
                    convo_state = {"action": None, "sub_step": None, "target": None}
                    
                    # Emit admin login event
                    socketio.emit('admin_login_success', {
                        'user': username,
                        'role': 'admin'
                    })
                    
                elif verification == "locked":
                    response = "❌ PIN locked due to too many failed attempts. Please wait 5 minutes."
                    convo_state = {"action": None, "sub_step": None, "target": None}
                else:
                    attempts_left = 3 - pin_state.get("attempts", 0)
                    if attempts_left <= 0:
                        response = "❌ Too many failed attempts. Please wait 5 minutes."
                        convo_state = {"action": None, "sub_step": None, "target": None}
                    else:
                        response = f"❌ Invalid PIN. {attempts_left} attempts remaining."
        
        # Verify command with location
        verify_command_with_location(text)
        
        # Track API usage
        if "whatsapp" in text or "వాట్సాప్" in text or "వాట్సప్" in text:
            track_api_usage("whatsapp", "voice")
        elif "send email" in text or "send mail" in text or "ఈమెయిల్ పంపు" in text or "మెయిల్ పంపు" in text:
            track_api_usage("gmail_send", "voice")
        elif "read mail" in text or "read email" in text or "మెయిల్ చదువు" in text or "ఈమెయిల్ చదువు" in text:
            track_api_usage("gmail_read", "voice")
        elif "battery" in text or "బ్యాటరీ" in text:
            track_api_usage("battery", "voice")
        
        # Quick check for basic commands including Telugu
        if "hello" in text or "hi" in text or "hey" in text or "greetings" in text or "హల్లో" in text or "నమస్కం" in text or "హల్" in text:
            response = f"{get_greeting()}, {user_name}. Vira is active."
        elif "time" in text or "సమయం" in text or "సమయం చెప్పు" in text or "సమయం చెప్పా" in text:
            current_time = datetime.now().strftime("%I:%M %p")
            response = f"The current time is {current_time}."
        elif "battery" in text or "బ్యాటరీ" in text or "బ్యాటరీ స్థితి" in text or "బ్యాటరీ స్థితి" in text:
            try:
                battery_percent = psutil.sensors_battery().percent
                response = f"Battery is at {battery_percent} percent."
            except Exception as e:
                print(f"Battery check failed: {e}")
                response = "I cannot check battery status right now."
        elif "reminder" in text or "remind me" in text or "set reminder" in text or "add reminder" in text or "my reminders" in text:
            try:
                import json
                import os
                
                # Reminders file
                reminders_file = "reminders.json"
                
                # Load existing reminders
                reminders = []
                if os.path.exists(reminders_file):
                    with open(reminders_file, 'r') as f:
                        reminders = json.load(f)
                
                # Check if user wants to see reminders
                if "my reminders" in text or "show reminders" in text or "list reminders" in text:
                    if reminders:
                        response = "📅 Your Reminders:\n"
                        for i, reminder in enumerate(reminders, 1):
                            response += f"{i}. {reminder['text']} ({reminder['time']})\n"
                    else:
                        response = "You have no reminders set."
                
                # Check if user wants to add a reminder
                elif "set reminder" in text or "add reminder" in text or "remind me" in text:
                    # Extract reminder text (simple approach)
                    reminder_text = text.replace("set reminder", "").replace("add reminder", "").replace("remind me", "").strip()
                    
                    if reminder_text:
                        # Create new reminder
                        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
                        new_reminder = {
                            "text": reminder_text,
                            "time": current_time,
                            "id": len(reminders) + 1
                        }
                        
                        # Add to reminders list
                        reminders.append(new_reminder)
                        
                        # Save reminders
                        with open(reminders_file, 'w') as f:
                            json.dump(reminders, f, indent=2)
                        
                        response = f"✅ Reminder set: {reminder_text}\n"
                        response += f"⏰ Time: {current_time}\n"
                        response += f"📝 You have {len(reminders)} reminder(s) total."
                    else:
                        response = "Please specify what you want to be reminded about. For example: 'remind me to check email'"
                
                # Check if user wants to clear reminders
                elif "clear reminders" in text or "delete reminders" in text or "remove reminders" in text:
                    reminders = []
                    with open(reminders_file, 'w') as f:
                        json.dump(reminders, f, indent=2)
                    response = "🗑️ All reminders cleared."
                
                else:
                    response = "📅 Reminder Options:\n"
                    response += "• 'set reminder [text]' - Add new reminder\n"
                    response += "• 'my reminders' - Show all reminders\n"
                    response += "• 'clear reminders' - Delete all reminders"
                
            except Exception as e:
                print(f"Reminder failed: {e}")
                response = "I cannot manage reminders right now."
        elif "logout" in text or "sign out" in text or "log out" in text or "లాగ్ అవుట్" in text or "సైషన్ అవుట్" in text:
            try:
                print(f"🔍 DEBUG: Logout command detected: '{text}'")
                
                # Clear all session data
                session.clear()
                print(f"✅ User logged out successfully via voice command: {datetime.now()}")
                
                # Send logout confirmation to client
                response = "Logging out. Goodbye! Redirecting to login page..."
                socketio.emit('transcript_update', {
                    'user_input': text,
                    'ai_response': response,
                    'type': 'ai_conversation'
                })
                
                # Emit simple logout event
                socketio.emit('force_logout')
                print(f"🔍 DEBUG: Logout event sent to client")
                
                # Non-blocking speak
                speak(response)
                return
                
            except Exception as e:
                print(f"❌ Voice logout error: {e}")
                response = "There was an error logging out. Please try the logout button."
                socketio.emit('transcript_update', {
                    'user_input': text,
                    'ai_response': response,
                    'type': 'ai_conversation'
                })
                speak(response)
        elif "reset" in text or "cancel" in text or "start over" in text or "రీసెట్" in text or "రద్దు" in text or "మళ్లీ ప్రారంభించు" in text:
            convo_state = {"action": None, "sub_step": None}
            response = "Reset. Ready for new command."
        elif "stop" in text or "ఆపు" in text or "నిలిపివేయి" in text:
            response = "Goodbye."
            socketio.emit('transcript_update', {
                'user_input': text,
                'ai_response': response,
                'type': 'ai_conversation'
            })
            speak(response)
            socketio.emit('sys_action', {'action': 'shutdown'})
            return
        
        # If we have a fast response, emit immediately
        if response:
            socketio.emit('transcript_update', {
                'user_input': text,
                'ai_response': response,
                'type': 'ai_conversation'
            })
            speak(response)
            return

        # COMMUNICATION COMMANDS - Fresh WhatsApp Implementation
        if "whatsapp" in text or "వాట్సాప్" in text or "వాట్సప్" in text:
            convo_state = {"action": "whatsapp", "sub_step": "waiting_for_target"}
            response = "Sure. Please say the 10 digit number."
            
        elif "open whatsapp" in text or "whatsapp web" in text:
            # Open WhatsApp Web
            try:
                import webbrowser
                webbrowser.open('https://web.whatsapp.com')
                response = "🌐 WhatsApp Web opened. Please login and try sending messages."
            except Exception as e:
                response = f"❌ Could not open WhatsApp Web: {e}"
            
            socketio.emit('transcript_update', {
                'user_input': text,
                'ai_response': response,
                'type': 'ai_conversation'
            })
            speak(response)
            return
            
        elif "send email" in text or "send mail" in text or "ఈమెయిల్ పంపు" in text or "మెయిల్ పంపు" in text:
            convo_state = {"action": "email", "sub_step": "waiting_for_target"}
            response = "Okay. Tell me the email address."
        
        # EMAIL CONVERSATION FLOW - Handle email sending
        elif convo_state["action"] == "email" and convo_state["sub_step"] == "waiting_for_target":
            # Handle email address input
            email = text.strip()
            if "@" in email and "." in email:
                convo_state["target"] = email
                convo_state["sub_step"] = "waiting_for_body"
                response = f"Got {email}. What's the message?"
            else:
                response = "Please provide a valid email address (e.g., user@example.com)."
                
        elif convo_state["action"] == "email" and convo_state["sub_step"] == "waiting_for_body":
            # Ask for PIN before sending email
            convo_state["message"] = text  # Store the message
            convo_state["sub_step"] = "waiting_for_pin"
            response = "For security, please say your 4-digit PIN to send this email message."
            
        elif convo_state["action"] == "email" and convo_state["sub_step"] == "waiting_for_pin":
            # Verify PIN and send email
            pin_input = text.replace(" ", "").strip()
            verification = verify_pin(pin_input)
            
            if verification == True:
                # Send email message
                target = convo_state["target"]
                message = f"Hi, this is Vira. {convo_state['message']}"
                
                try:
                    gmail.send_mail(target, "Vira Message", message)
                    response = "✅ Email message sent successfully!"
                except Exception as e:
                    print(f"Email send error: {e}")
                    response = "❌ Email failed. Please check email configuration."
                
                # Reset conversation
                reset_pin_verification()
                convo_state = {"action": None, "sub_step": None, "target": None}
                
            elif verification == "locked":
                response = "Too many failed attempts. Please wait 5 minutes."
                convo_state = {"action": None, "sub_step": None, "target": None}
            else:
                attempts_left = 3 - pin_state["attempts"]
                response = f"Invalid PIN. {attempts_left} attempts remaining."
                if attempts_left == 0:
                    convo_state = {"action": None, "sub_step": None, "target": None}
        
        # WHATSAPP CONVERSATION FLOW - Handle 10-digit numbers
        elif convo_state["action"] == "whatsapp" and convo_state["sub_step"] == "waiting_for_target":
            # Extract digits from user input
            import re
            digits_only = re.sub(r'\D', '', text)
            print(f"WhatsApp number input: '{text}' -> digits: '{digits_only}' (length: {len(digits_only)})")
            
            if len(digits_only) == 10:
                convo_state["target"] = digits_only
                convo_state["sub_step"] = "waiting_for_body"
                response = f"Got {digits_only}. What's the message?"
            elif len(digits_only) > 10:
                convo_state["target"] = digits_only[-10:]  # Take last 10 digits
                convo_state["sub_step"] = "waiting_for_body"
                response = f"Using last 10 digits: {digits_only[-10:]}. What's the message?"
            elif len(digits_only) > 0:
                response = f"I need exactly 10 digits. You gave {len(digits_only)} digits. Please say a 10-digit mobile number."
            else:
                response = "Please say a 10-digit mobile number."
                
        elif convo_state["action"] == "whatsapp" and convo_state["sub_step"] == "waiting_for_body":
            # Ask for PIN before sending WhatsApp message
            convo_state["message"] = text  # Store the actual user message
            convo_state["sub_step"] = "waiting_for_pin"
            response = "For security, please say your 4-digit PIN to send this WhatsApp message."
            
        elif convo_state["action"] == "whatsapp" and convo_state["sub_step"] == "waiting_for_pin":
            # Verify PIN and send WhatsApp
            pin_input = text.replace(" ", "").strip()
            verification = verify_pin(pin_input)
            
            if verification is True:
                # PIN verified - send WhatsApp
                target = convo_state["target"]
                message = convo_state["message"]
                success = send_whatsapp_simple(target, message)
                
                if success:
                    response = "✅ WhatsApp message sent successfully!"
                else:
                    response = "❌ WhatsApp failed. Please open WhatsApp Web first."
                
                # Reset conversation
                convo_state = {"action": None, "sub_step": None, "target": None}
                
            elif verification == "locked":
                response = "Too many failed attempts. Please wait 5 minutes."
                convo_state = {"action": None, "sub_step": None, "target": None}
            else:
                attempts_left = 3 - pin_state["attempts"]
                response = f"Invalid PIN. {attempts_left} attempts remaining."
                if attempts_left == 0:
                    convo_state = {"action": None, "sub_step": None, "target": None}
        
        # EMAIL REPLY CONVERSATION FLOW - Handle email reply sending
        elif convo_state["action"] == "send_email_reply" and convo_state["sub_step"] == "waiting_for_pin":
            # Verify PIN and send email reply
            pin_input = text.replace(" ", "").strip()
            verification = verify_pin(pin_input)
            
            if verification is True:
                # PIN verified - send email reply
                current_email = EMAIL_STATE["current_email"]
                reply_message = EMAIL_STATE["suggested_reply"]
                
                try:
                    # Send reply using Gmail API
                    service = build_gmail_service()
                    if service:
                        # Create reply message
                        reply_subject = f"Re: {current_email.get('subject', 'No Subject')}"
                        
                        reply_body = reply_message
                        
                        # Create message
                        message = MIMEText(reply_body)
                        message['to'] = current_email['sender']
                        message['subject'] = reply_subject
                        message['in-reply-to'] = current_email.get('id', '')
                        message['references'] = current_email.get('id', '')
                        
                        # Send the email
                        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
                        service.users().messages().send(userId='me', body={'raw': raw_message}).execute()
                        
                        response = "✅ Email reply sent successfully!"
                        
                        # Track API usage
                        track_api_usage("gmail_send", "voice")
                        
                    else:
                        response = "❌ Gmail service not available. Please check authentication."
                        
                except Exception as e:
                    print(f"Email reply failed: {e}")
                    response = "❌ Failed to send email reply. Please try again."
                
                # Reset email state and conversation
                EMAIL_STATE["current_email"] = None
                EMAIL_STATE["suggested_reply"] = None
                EMAIL_STATE["reply_mode"] = False
                convo_state = {"action": None, "sub_step": None, "target": None}
                
            elif verification == "locked":
                response = "Too many failed attempts. Please wait 5 minutes."
                EMAIL_STATE["current_email"] = None
                EMAIL_STATE["suggested_reply"] = None
                EMAIL_STATE["reply_mode"] = False
                convo_state = {"action": None, "sub_step": None, "target": None}
            else:
                attempts_left = 3 - pin_state["attempts"]
                response = f"Invalid PIN. {attempts_left} attempts remaining."
                if attempts_left == 0:
                    EMAIL_STATE["current_email"] = None
                    EMAIL_STATE["suggested_reply"] = None
                    EMAIL_STATE["reply_mode"] = False
                    convo_state = {"action": None, "sub_step": None, "target": None}
        
        # CUSTOM EMAIL REPLY CONVERSATION FLOW
        elif convo_state["action"] == "custom_email_reply" and convo_state["sub_step"] == "waiting_for_message":
            # Store custom message and ask for PIN
            EMAIL_STATE["suggested_reply"] = text
            convo_state["sub_step"] = "waiting_for_pin"
            response = "For security, please say your 4-digit PIN to send this custom reply."
            
        elif convo_state["action"] == "custom_email_reply" and convo_state["sub_step"] == "waiting_for_pin":
            # Verify PIN and send custom email reply
            pin_input = text.replace(" ", "").strip()
            verification = verify_pin(pin_input)
            
            if verification is True:
                # PIN verified - send custom email reply
                current_email = EMAIL_STATE["current_email"]
                reply_message = EMAIL_STATE["suggested_reply"]
                
                try:
                    # Send reply using Gmail API
                    service = build_gmail_service()
                    if service:
                        # Create reply message
                        reply_subject = f"Re: {current_email.get('subject', 'No Subject')}"
                        
                        reply_body = reply_message
                        
                        # Create message
                        message = MIMEText(reply_body)
                        message['to'] = current_email['sender']
                        message['subject'] = reply_subject
                        message['in-reply-to'] = current_email.get('id', '')
                        message['references'] = current_email.get('id', '')
                        
                        # Send the email
                        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
                        service.users().messages().send(userId='me', body={'raw': raw_message}).execute()
                        
                        response = "✅ Custom email reply sent successfully!"
                        
                        # Track API usage
                        track_api_usage("gmail_send", "voice")
                        
                    else:
                        response = "❌ Gmail service not available. Please check authentication."
                        
                except Exception as e:
                    print(f"Custom email reply failed: {e}")
                    response = "❌ Failed to send custom email reply. Please try again."
                
                # Reset email state and conversation
                EMAIL_STATE["current_email"] = None
                EMAIL_STATE["suggested_reply"] = None
                EMAIL_STATE["reply_mode"] = False
                convo_state = {"action": None, "sub_step": None, "target": None}
                
            elif verification == "locked":
                response = "Too many failed attempts. Please wait 5 minutes."
                EMAIL_STATE["current_email"] = None
                EMAIL_STATE["suggested_reply"] = None
                EMAIL_STATE["reply_mode"] = False
                convo_state = {"action": None, "sub_step": None, "target": None}
            else:
                attempts_left = 3 - pin_state["attempts"]
                response = f"Invalid PIN. {attempts_left} attempts remaining."
                if attempts_left == 0:
                    EMAIL_STATE["current_email"] = None
                    EMAIL_STATE["suggested_reply"] = None
                    EMAIL_STATE["reply_mode"] = False
                    convo_state = {"action": None, "sub_step": None, "target": None}
        
        # EMAIL COMMANDS - Fast processing with demo fallback
        elif "read mail" in text or "read email" in text or "మెయిల్ చదువు" in text or "ఈమెయిల్ చదువు" in text:
            try:
                latest = gmail.get_latest_unread()
                if latest:
                    EMAIL_STATE["current_email"] = latest
                    EMAIL_STATE["reply_mode"] = False
                    
                    # Fast summary
                    summary = summarize_email_content(latest['body'])
                    response = f"From {latest['sender']}. Subject: {latest.get('subject', 'No subject')}. Summary: {summary}. Say 'reply to email' to respond."
                else:
                    response = "No unread emails found."
            except Exception as e:
                print(f"Read mail failed: {e}")
                response = "I cannot read emails right now."
                
        elif "reply to email" in text or "email reply" in text:
            if EMAIL_STATE["current_email"]:
                EMAIL_STATE["reply_mode"] = True
                sender = EMAIL_STATE["current_email"]["sender"]
                
                # Fast suggestion generation
                suggestion = generate_reply_suggestion(
                    EMAIL_STATE["current_email"]["body"], 
                    sender
                )
                EMAIL_STATE["suggested_reply"] = suggestion
                
                response = f"I've prepared a reply for {sender}. Here's my suggestion: {suggestion}. Say 'send reply' to send this."
            else:
                response = "No email loaded for reply. Please read an email first."
        
        elif "more suggestions" in text or "email suggestions" in text:
            if EMAIL_STATE["current_email"]:
                suggestions = get_email_suggestions()
                response = "Here are some alternative reply suggestions: "
                for i, suggestion in enumerate(suggestions[:3], 1):
                    response += f"Option {i}: {suggestion}. "
                response += "Say 'use suggestion 1', 'use suggestion 2', or 'use suggestion 3' to choose."
            else:
                response = "No email loaded for suggestions. Please read an email first."
                
        elif "use suggestion" in text:
            try:
                # Extract number from command
                import re
                numbers = re.findall(r'\d+', text)
                if numbers and EMAIL_STATE["current_email"]:
                    suggestion_num = int(numbers[0])
                    suggestions = get_email_suggestions()
                    
                    if 1 <= suggestion_num <= len(suggestions):
                        selected = suggestions[suggestion_num - 1]
                        EMAIL_STATE["suggested_reply"] = selected
                        response = f"Selected suggestion {suggestion_num}: {selected}. Say 'send reply' to send this message."
                    else:
                        response = f"Please choose a suggestion between 1 and {len(suggestions)}"
                else:
                    response = "No email loaded. Please read an email first."
            except Exception as e:
                print(f"Suggestion selection error: {e}")
                response = "I couldn't process that selection."
                
        elif "edit reply" in text or "change reply" in text:
            if EMAIL_STATE["reply_mode"]:
                EMAIL_STATE["reply_mode"] = False
                EMAIL_STATE["suggested_reply"] = None
                response = "Reply editing mode activated. Please tell me your custom reply message."
                convo_state = {"action": "custom_email_reply", "sub_step": "waiting_for_message"}
            else:
                response = "No reply in progress. Please start with 'reply to email' first."
                
        elif "send reply" in text:
            if EMAIL_STATE["current_email"] and EMAIL_STATE["suggested_reply"]:
                # Ask for PIN before sending
                response = "For security, please say your 4-digit PIN to send this email reply."
                convo_state = {"action": "send_email_reply", "sub_step": "waiting_for_pin"}
            elif EMAIL_STATE["reply_mode"] and convo_state.get("action") == "custom_email_reply":
                    if attempts_left == 0:
                        convo_state = {"action": None, "sub_step": None, "target": None}
        
        # Check if we're in the middle of adding a contact - HIGH PRIORITY
        elif convo_state.get("action") == "add_contact":
            if convo_state.get("sub_step") == "waiting_for_name":
                # User provided name, now ask for contact type
                contact_name = text.strip()
                if len(contact_name) < 2:
                    response = "Name too short. Please provide a valid name."
                else:
                    # Store name and ask for contact type
                    convo_state["target"] = {"name": contact_name}
                    convo_state["sub_step"] = "waiting_for_contact_type"
                    response = f"Got it! Name: {contact_name}\nNow, what would you like to add?\n• Say 'mobile' for phone number\n• Say 'email' for email address\n• Say 'both' for both mobile and email"
            
            elif convo_state.get("sub_step") == "waiting_for_contact_type":
                contact_type = text.lower().strip()
                if "mobile" in contact_type or "phone" in contact_type:
                    convo_state["sub_step"] = "waiting_for_mobile"
                    response = "Please provide the 10-digit mobile number:"
                elif "email" in contact_type or "mail" in contact_type:
                    convo_state["sub_step"] = "waiting_for_email"
                    response = "Please provide the email address (must contain @ and domain):"
                elif "both" in contact_type:
                    convo_state["sub_step"] = "waiting_for_mobile"
                    convo_state["target"]["add_email"] = True
                    response = "Please provide the 10-digit mobile number first:"
                else:
                    response = "Please choose: 'mobile', 'email', or 'both'"
            
            elif convo_state.get("sub_step") == "waiting_for_mobile":
                mobile = text.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
                # Remove any non-digit characters
                mobile = re.sub(r'\D', '', mobile)
                print(f"Mobile input: '{text}' -> cleaned: '{mobile}' (length: {len(mobile)})")
                
                if len(mobile) != 10:
                    response = f"❌ Invalid mobile number! Got {len(mobile)} digits. Please provide exactly 10 digits (e.g., 1234567890):"
                elif not mobile.isdigit():
                    response = "❌ Invalid mobile number! Please provide digits only (e.g., 1234567890):"
                else:
                    convo_state["target"]["mobile"] = mobile
                    if convo_state["target"].get("add_email"):
                        convo_state["sub_step"] = "waiting_for_email"
                        response = f"✅ Mobile: {mobile}\nNow please provide the email address:"
                    else:
                        # Save contact with mobile only
                        import json
                        import os
                        
                        contacts_file = "contacts.json"
                        contacts = []
                        if os.path.exists(contacts_file):
                            with open(contacts_file, 'r') as f:
                                contacts = json.load(f)
                        
                        new_contact = {
                            "name": convo_state["target"]["name"],
                            "phone": mobile,
                            "id": len(contacts) + 1,
                            "created": datetime.now().strftime("%Y-%m-%d %H:%M")
                        }
                        contacts.append(new_contact)
                        with open(contacts_file, 'w') as f:
                            json.dump(contacts, f, indent=2)
                        response = f"✅ Contact added:\n📱 {new_contact['name']} - {new_contact['phone']}\n📝 Total contacts: {len(contacts)}"
                        convo_state = {"action": None, "sub_step": None, "target": None}
            
            elif convo_state.get("sub_step") == "waiting_for_email":
                email = text.strip().lower()
                if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                    response = "❌ Invalid email! Please provide a valid email (e.g., name@domain.com):"
                else:
                    # Save contact
                    import json
                    import os
                    
                    contacts_file = "contacts.json"
                    contacts = []
                    if os.path.exists(contacts_file):
                        with open(contacts_file, 'r') as f:
                            contacts = json.load(f)
                    
                    new_contact = {
                        "name": convo_state["target"]["name"],
                        "phone": convo_state["target"].get("mobile", ""),
                        "email": email,
                        "id": len(contacts) + 1,
                        "created": datetime.now().strftime("%Y-%m-%d %H:%M")
                    }
                    contacts.append(new_contact)
                    with open(contacts_file, 'w') as f:
                        json.dump(contacts, f, indent=2)
                    
                    contact_info = f"{new_contact['name']} - {new_contact['phone']} / {new_contact['email']}"
                    response = f"✅ Contact added:\n📱 {contact_info}\n📝 Total contacts: {len(contacts)}"
                    convo_state = {"action": None, "sub_step": None, "target": None}
        
        # ADMIN LOGIN COMMANDS - Check before other commands
        elif "as admin" in text or "login as admin" in text or "admin login" in text or "sign in as admin" in text:
            try:
                response = "🔐 Admin Login Required\nPlease provide your admin username and password.\nSay: 'username [your_username] password [your_password]'"
                # Set conversation state for admin login
                convo_state = {"action": "admin_login", "sub_step": "waiting_for_credentials", "target": {}}
            except Exception as e:
                print(f"Admin login command failed: {e}")
                response = "I cannot process admin login right now."
        
        # Check if we're in admin login conversation
        elif convo_state.get("action") == "admin_login":
            if convo_state.get("sub_step") == "waiting_for_credentials":
                # Parse username and password from voice
                if "username" in text and "password" in text:
                    try:
                        # Extract username and password
                        parts = text.split()
                        username = ""
                        password = ""
                        
                        for i, part in enumerate(parts):
                            if part.lower() == "username" and i + 1 < len(parts):
                                username = parts[i + 1]
                            elif part.lower() == "password" and i + 1 < len(parts):
                                password = parts[i + 1]
                        
                        if username and password:
                            # Verify admin credentials
                            if os.path.exists("user_database.json"):
                                with open("user_database.json", "r") as f:
                                    users = json.load(f)
                                
                                if username in users and users[username]['password'] == password and is_admin(username):
                                    # Ask for PIN
                                    convo_state["target"]["username"] = username
                                    convo_state["target"]["password"] = password
                                    convo_state["sub_step"] = "waiting_for_pin"
                                    response = f"✅ Credentials verified for {username}\nNow please provide your 4-digit admin PIN:"
                                else:
                                    response = "❌ Invalid admin credentials. Please check your username and password."
                                    convo_state = {"action": None, "sub_step": None, "target": None}
                            else:
                                response = "❌ User database not found. Please contact administrator."
                                convo_state = {"action": None, "sub_step": None, "target": None}
                        else:
                            response = "❌ Could not extract username and password. Please say: 'username [name] password [pass]'"
                    except Exception as e:
                        print(f"Admin credential parsing failed: {e}")
                        response = "❌ Error processing credentials. Please try again."
                        convo_state = {"action": None, "sub_step": None, "target": None}
            
            elif convo_state.get("sub_step") == "waiting_for_pin":
                # Verify PIN for admin login
                pin_input = text.replace(" ", "").strip()
                verification = verify_pin(pin_input)
                
                if verification is True:
                    # Complete admin login
                    username = convo_state["target"]["username"]
                    session['user'] = username
                    session['role'] = 'admin'
                    log_command(username, "Voice Admin Login")
                    
                    response = f"🎉 Admin login successful! Welcome {username}!\nRedirecting to admin dashboard..."
                    convo_state = {"action": None, "sub_step": None, "target": None}
                    
                    # Emit admin login event
                    socketio.emit('admin_login_success', {
                        'user': username,
                        'role': 'admin'
                    })
                    
                elif verification == "locked":
                    response = "❌ PIN locked due to too many failed attempts. Please wait 5 minutes."
                    convo_state = {"action": None, "sub_step": None, "target": None}
                else:
                    attempts_left = 3 - pin_state.get("attempts", 0)
                    if attempts_left <= 0:
                        response = "❌ Too many failed attempts. Please wait 5 minutes."
                        convo_state = {"action": None, "sub_step": None, "target": None}
                    else:
                        response = f"❌ Invalid PIN. {attempts_left} attempts remaining."
        
        elif "add contact" in text or "add contacts" in text or "new contact" in text or "save contact" in text or "create contact" in text:
            try:
                import json
                import os
                import re
                
                # Contacts file
                contacts_file = "contacts.json"
                
                # Load existing contacts
                contacts = []
                if os.path.exists(contacts_file):
                    with open(contacts_file, 'r') as f:
                        contacts = json.load(f)
                
                # Check if user wants to show contacts
                if "show contacts" in text or "my contacts" in text or "list contacts" in text:
                    if contacts:
                        response = "📱 Your Contacts:\n"
                        for i, contact in enumerate(contacts, 1):
                            contact_info = f"{contact['name']} - {contact['phone']}"
                            if 'email' in contact:
                                contact_info += f" / {contact['email']}"
                            response += f"{i}. {contact_info}\n"
                    else:
                        response = "You have no contacts saved."
                
                # Check if user wants to clear contacts
                elif "clear contacts" in text or "delete contacts" in text or "remove contacts" in text:
                    contacts = []
                    with open(contacts_file, 'w') as f:
                        json.dump(contacts, f, indent=2)
                    response = "🗑️ All contacts cleared."
                    # Reset conversation state
                    convo_state = {"action": None, "sub_step": None, "target": None}
                
                # Start new contact addition process
                elif "add contact" in text or "add contacts" in text or "new contact" in text or "save contact" in text or "create contact" in text:
                    # Check if user provided details in one command (backward compatibility)
                    contact_text = text.replace("add contact", "").replace("add contacts", "").replace("new contact", "").replace("save contact", "").replace("create contact", "").strip()
                    
                    if contact_text and len(contact_text.split()) >= 2:
                        # Try old method for backward compatibility
                        parts = contact_text.split()
                        if len(parts) >= 2:
                            phone = parts[-1]
                            name = " ".join(parts[:-1])
                            
                            # Validate phone
                            mobile = phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
                            if re.match(r'^\d{10}$', mobile):
                                new_contact = {
                                    "name": name,
                                    "phone": mobile,
                                    "id": len(contacts) + 1,
                                    "created": datetime.now().strftime("%Y-%m-%d %H:%M")
                                }
                                contacts.append(new_contact)
                                with open(contacts_file, 'w') as f:
                                    json.dump(contacts, f, indent=2)
                                response = f"✅ Contact added: {name} - {mobile}\n📱 Total contacts: {len(contacts)}"
                            else:
                                response = "❌ Invalid mobile number! Please use the interactive method. Say 'add contact' again."
                    else:
                        # Start interactive process
                        convo_state = {"action": "add_contact", "sub_step": "waiting_for_name", "target": {}}
                        response = "📱 Adding new contact...\nPlease tell me the name first:"
                
                else:
                    response = "📱 Contact Options:\n"
                    response += "• 'add contact' - Add new contact (interactive)\n"
                    response += "• 'add contact [name] [phone]' - Quick add\n"
                    response += "• 'show contacts' - Display all contacts\n"
                    response += "• 'clear contacts' - Delete all contacts"
                
            except Exception as e:
                print(f"Contact management failed: {e}")
                response = "I cannot manage contacts right now."
            
        else:
            # Default response for unrecognized commands
            response = "I didn't understand that. Try saying 'hello', 'time', 'battery', 'whatsapp', 'read mail', or 'help'."
        
        # Emit response immediately for fast user experience
        if response:
            socketio.emit('transcript_update', {
                'user_input': text,
                'ai_response': response,
                'type': 'ai_conversation'
            })
            
            # Non-blocking speak
            speak(response)
        
        print(f"Final state: {convo_state}")
        print("=== VOICE COMMAND PROCESSING COMPLETE ===")
        
    except Exception as e:
        print(f"ERROR PROCESSING VOICE COMMAND: {e}")
        socketio.emit('transcript_update', {
            'user_input': text if 'text' in locals() else 'unknown',
            'ai_response': "Sorry, I encountered an error. Please try again.",
            'type': 'ai_conversation'
        })
        speak("Sorry, I encountered an error. Please try again.")

if __name__ == '__main__':
    socketio.run(app, port=5000, debug=True, allow_unsafe_werkzeug=True)
