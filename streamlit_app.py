import streamlit as st
import json
import os
import threading
import time
from datetime import datetime
import psutil
import requests
import random

# Page configuration
st.set_page_config(
    page_title="Vira Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for glass morphism effect
st.markdown("""
<style>
    .glass {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0,0,0,0.1);
        border-radius: 16px;
        padding: 20px;
        margin: 10px 0;
    }
    .dark-mode {
        background: rgba(0, 0, 0, 0.8);
        color: white;
    }
    .admin-badge {
        background: linear-gradient(135deg, #ff6b6b, #ff8e53);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
    }
    .user-badge {
        background: linear-gradient(135deg, #4facfe, #00f2fe);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
    }
    .command-button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 25px;
        cursor: pointer;
        margin: 5px;
        transition: all 0.3s ease;
    }
    .command-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None
if 'role' not in st.session_state:
    st.session_state.role = None
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# User roles
ADMIN_USERS = ["admin", "administrator", "root"]
USER_ROLES = {
    "admin": "admin",
    "administrator": "admin", 
    "root": "admin",
    "aditya": "user"
}

def get_user_role(username):
    return USER_ROLES.get(username.lower(), "user")

def is_admin(username):
    return get_user_role(username) == "admin"

def get_weather_data(location="Delhi", days=0):
    try:
        current_hour = datetime.now().hour
        
        if 6 <= current_hour < 12:
            conditions = [
                {"temp": 22, "desc": "Clear sky", "icon": "☀️"},
                {"temp": 20, "desc": "Partly cloudy", "icon": "⛅"},
                {"temp": 18, "desc": "Mist", "icon": "🌫️"}
            ]
        elif 12 <= current_hour < 17:
            conditions = [
                {"temp": 28, "desc": "Sunny", "icon": "☀️"},
                {"temp": 26, "desc": "Partly cloudy", "icon": "⛅"},
                {"temp": 24, "desc": "Cloudy", "icon": "☁️"}
            ]
        elif 17 <= current_hour < 20:
            conditions = [
                {"temp": 25, "desc": "Clear sky", "icon": "🌤️"},
                {"temp": 23, "desc": "Partly cloudy", "icon": "⛅"},
                {"temp": 21, "desc": "Cloudy", "icon": "☁️"}
            ]
        else:
            conditions = [
                {"temp": 19, "desc": "Clear sky", "icon": "🌙"},
                {"temp": 17, "desc": "Partly cloudy", "icon": "☁️"},
                {"temp": 16, "desc": "Cloudy", "icon": "☁️"}
            ]
        
        weather = random.choice(conditions)
        temp = weather["temp"] + random.randint(-2, 2)
        
        if days == 1:
            temp = temp + random.randint(-3, 3)
            tomorrow_conditions = [
                {"temp": temp, "desc": "Sunny", "icon": "☀️"},
                {"temp": temp, "desc": "Partly cloudy", "icon": "⛅"},
                {"temp": temp, "desc": "Cloudy", "icon": "☁️"},
                {"temp": temp - 2, "desc": "Light rain", "icon": "🌧️"}
            ]
            weather = random.choice(tomorrow_conditions)
        
        return {
            "temp": temp,
            "description": weather["desc"],
            "icon": weather["icon"],
            "location": location,
            "day": "Tomorrow" if days == 1 else "Today"
        }
    except Exception as e:
        print(f"Weather data error: {e}")
        return None

def process_command(command, user_name):
    """Process voice/text commands"""
    command = command.lower().strip()
    
    # Admin commands
    if is_admin(user_name):
        if "system info" in command:
            try:
                cpu_usage = psutil.cpu_percent()
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                
                info = f"💻 **System Info:**\n"
                info += f"🖥️ CPU: {cpu_usage}%\n"
                info += f"💾 Memory: {memory.percent}% used\n"
                info += f"💿 Disk: {disk.percent}% used"
                return info
            except Exception as e:
                return f"❌ Error getting system info: {e}"
        
        elif "user list" in command:
            try:
                if os.path.exists("user_database.json"):
                    with open("user_database.json", "r") as f:
                        users = json.load(f)
                    return f"👥 **Registered Users:** {len(users)}"
                else:
                    return "📝 No users registered"
            except Exception as e:
                return f"❌ Error getting user list: {e}"
    
    # Basic commands
    if "battery" in command:
        try:
            battery = psutil.sensors_battery()
            if battery:
                return f"🔋 **Battery:** {battery.percent}%"
            else:
                return "🔋 Battery info not available"
        except Exception as e:
            return f"❌ Error checking battery: {e}"
    
    elif "time" in command:
        current_time = datetime.now().strftime("%I:%M %p")
        return f"⏰ **Current Time:** {current_time}"
    
    elif "weather" in command and "tomorrow" in command:
        weather = get_weather_data(days=1)
        if weather:
            return f"🌤️ **Tomorrow's Weather:** {weather['description']}, {weather['temp']}°C"
        else:
            return "❌ Weather data unavailable"
    
    elif "weather" in command:
        weather = get_weather_data(days=0)
        if weather:
            return f"🌤️ **Current Weather:** {weather['description']}, {weather['temp']}°C"
        else:
            return "❌ Weather data unavailable"
    
    elif "help" in command:
        help_text = """
        🤖 **Vira Assistant Commands:**
        
        **Basic Commands:**
        🔋 Battery - Check battery status
        ⏰ Time - Get current time
        🌤️ Weather - Get current weather
        🌤️ Weather tomorrow - Get tomorrow's forecast
        
        **Admin Commands:**
        💻 System info - Get system statistics
        👥 User list - See registered users
        """
        if is_admin(user_name):
            help_text += "\n🛑 Shutdown system - Shutdown the application"
        return help_text
    
    else:
        return f"❓ Unknown command: '{command}'. Try 'help' for available commands."

def load_users():
    """Load users from database"""
    if os.path.exists("user_database.json"):
        with open("user_database.json", "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    """Save users to database"""
    with open("user_database.json", "w") as f:
        json.dump(users, f, indent=4)

# Login page
if st.session_state.user is None:
    st.title("🤖 Vira Assistant Login")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.container():
            st.markdown('<div class="glass">', unsafe_allow_html=True)
            
            tab1, tab2 = st.tabs(["Login", "Register"])
            
            with tab1:
                username = st.text_input("Username", key="login_username")
                password = st.text_input("Password", type="password", key="login_password")
                
                if st.button("Login", key="login_btn"):
                    users = load_users()
                    if username in users and users[username]['password'] == password:
                        st.session_state.user = username
                        st.session_state.role = get_user_role(username)
                        st.success(f"Welcome back, {username}!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
            
            with tab2:
                new_username = st.text_input("Username", key="reg_username")
                new_password = st.text_input("Password", type="password", key="reg_password")
                confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
                
                if st.button("Register", key="reg_btn"):
                    users = load_users()
                    if new_username in users:
                        st.error("Username already exists")
                    elif new_password != confirm_password:
                        st.error("Passwords do not match")
                    elif len(new_password) < 4:
                        st.error("Password must be at least 4 characters")
                    else:
                        users[new_username] = {'password': new_password}
                        save_users(users)
                        st.success("Registration successful! Please login.")
            
            st.markdown('</div>', unsafe_allow_html=True)

# Main application
else:
    # Header
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 20px;">
        <div>
            <h1 style="margin: 0;">🤖 Vira Assistant</h1>
            <p style="margin: 0; color: gray;">Welcome back, {st.session_state.user}!</p>
        </div>
        <div>
            <span class="{'admin-badge' if is_admin(st.session_state.user) else 'user-badge'}">
                {st.session_state.role.upper()}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.header("🎛️ Controls")
        
        # Quick commands
        st.subheader("⚡ Quick Commands")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔋 Battery", key="sidebar_battery"):
                response = process_command("battery", st.session_state.user)
                st.session_state.messages.append(("user", "battery"))
                st.session_state.messages.append(("assistant", response))
        
        with col2:
            if st.button("⏰ Time", key="sidebar_time"):
                response = process_command("time", st.session_state.user)
                st.session_state.messages.append(("user", "time"))
                st.session_state.messages.append(("assistant", response))
        
        col3, col4 = st.columns(2)
        with col3:
            if st.button("🌤️ Weather", key="sidebar_weather"):
                response = process_command("weather", st.session_state.user)
                st.session_state.messages.append(("user", "weather"))
                st.session_state.messages.append(("assistant", response))
        
        with col4:
            if st.button("🌤️ Tomorrow", key="sidebar_tomorrow"):
                response = process_command("weather tomorrow", st.session_state.user)
                st.session_state.messages.append(("user", "weather tomorrow"))
                st.session_state.messages.append(("assistant", response))
        
        # Admin controls
        if is_admin(st.session_state.user):
            st.subheader("🔧 Admin Controls")
            
            if st.button("💻 System Info", key="sidebar_system"):
                response = process_command("system info", st.session_state.user)
                st.session_state.messages.append(("user", "system info"))
                st.session_state.messages.append(("assistant", response))
            
            if st.button("👥 User List", key="sidebar_users"):
                response = process_command("user list", st.session_state.user)
                st.session_state.messages.append(("user", "user list"))
                st.session_state.messages.append(("assistant", response))
        
        # Logout
        if st.button("🚪 Logout", key="sidebar_logout"):
            st.session_state.user = None
            st.session_state.role = None
            st.session_state.messages = []
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main chat interface
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    
    # Chat messages
    chat_container = st.container()
    with chat_container:
        for sender, message in st.session_state.messages:
            if sender == "user":
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-end; margin: 10px 0;">
                    <div style="background: linear-gradient(135deg, #667eea, #764ba2); 
                                color: white; padding: 10px 20px; border-radius: 20px; 
                                max-width: 70%; text-align: right;">
                        <strong>You:</strong> {message}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-start; margin: 10px 0;">
                    <div style="background: #f0f0f0; color: black; padding: 10px 20px; 
                                border-radius: 20px; max-width: 70%;">
                        <strong>🤖 Vira:</strong><br>{message}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Command input
    st.markdown("---")
    col1, col2 = st.columns([4, 1])
    
    with col1:
        command = st.text_input("Enter command:", key="command_input", placeholder="Type your command here...")
    
    with col2:
        if st.button("📤 Send", key="send_btn"):
            if command:
                response = process_command(command, st.session_state.user)
                st.session_state.messages.append(("user", command))
                st.session_state.messages.append(("assistant", response))
                st.rerun()
    
    # Help section
    with st.expander("💡 Need help?"):
        st.markdown("""
        **Available Commands:**
        - `battery` - Check battery status
        - `time` - Get current time  
        - `weather` - Get current weather
        - `weather tomorrow` - Get tomorrow's forecast
        - `help` - Show this help message
        
        **Admin Commands:**
        - `system info` - Get system statistics
        - `user list` - See registered users
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)
