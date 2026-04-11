"""
Vira Assistant - Streamlit Cloud Version
Modified for deployment on Streamlit Cloud and other cloud platforms
"""

import streamlit as st
import os
import json
import requests
import time
from datetime import datetime
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Vira AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'page' not in st.session_state:
    st.session_state.page = 'login'

# Load user database
def load_users():
    try:
        if os.path.exists('user_database.json'):
            with open('user_database.json', 'r') as f:
                return json.load(f)
        return {"admin": {"password": "admin123", "role": "admin"}}
    except:
        return {"admin": {"password": "admin123", "role": "admin"}}

# Load contacts
def load_contacts():
    try:
        if os.path.exists('contacts.json'):
            with open('contacts.json', 'r') as f:
                return json.load(f)
        return []
    except:
        return []

# Save contacts
def save_contacts(contacts):
    try:
        with open('contacts.json', 'w') as f:
            json.dump(contacts, f, indent=2)
        return True
    except:
        return False

# Login page
def login_page():
    st.markdown('<h1 class="main-header">🤖 Vira AI Assistant</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🔐 Login to Access Vira</h3>
            <p>Your AI-powered voice assistant is ready to help!</p>
        </div>
        """, unsafe_allow_html=True)
        
        username = st.text_input("👤 Username", placeholder="Enter your username")
        password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")
        
        if st.button("🚀 Login", use_container_width=True):
            users = load_users()
            
            if username in users and users[username]['password'] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.page = 'dashboard'
                st.rerun()
            else:
                st.error("❌ Invalid username or password")
        
        st.markdown("---")
        st.info("💡 **Default Login:** admin / admin123")

# Dashboard page
def dashboard_page():
    st.markdown('<h1 class="main-header">🤖 Vira AI Dashboard</h1>', unsafe_allow_html=True)
    
    # User info
    st.sidebar.markdown(f"### 👋 Welcome, {st.session_state.username}!")
    
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.page = 'login'
        st.rerun()
    
    # Main dashboard content
    tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home", "📱 Contacts", "📊 Analytics", "⚙️ Settings"])
    
    with tab1:
        st.markdown("""
        <div class="feature-card">
            <h3>🎤 Voice Commands</h3>
            <p>Vira can help you with various tasks using voice commands:</p>
            <ul>
                <li>👋 Say "hello" for greetings</li>
                <li>⏰ Say "time" to check current time</li>
                <li>📱 Say "add contact" to add new contacts</li>
                <li>📧 Say "send email" to compose emails</li>
                <li>🔐 Say "as admin" for admin access</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>🚀 Quick Actions</h3>
            <p>Access your favorite features instantly:</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📱 Add Contact", use_container_width=True):
                st.session_state.page = 'contacts'
                st.rerun()
        
        with col2:
            if st.button("📊 View Analytics", use_container_width=True):
                st.session_state.page = 'analytics'
                st.rerun()
        
        with col3:
            if st.button("⚙️ Settings", use_container_width=True):
                st.session_state.page = 'settings'
                st.rerun()
    
    with tab2:
        contacts_page()
    
    with tab3:
        analytics_page()
    
    with tab4:
        settings_page()

# Contacts page
def contacts_page():
    st.markdown("### 📱 Contact Management")
    
    contacts = load_contacts()
    
    # Add contact form
    with st.expander("➕ Add New Contact", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("👤 Name", placeholder="Enter contact name")
            mobile = st.text_input("📱 Mobile", placeholder="Enter 10-digit number")
        
        with col2:
            email = st.text_input("📧 Email", placeholder="Enter email address")
            notes = st.text_area("📝 Notes", placeholder="Additional notes")
        
        if st.button("💾 Save Contact", use_container_width=True):
            if name and (mobile or email):
                new_contact = {
                    "name": name,
                    "phone": mobile,
                    "email": email,
                    "notes": notes,
                    "id": len(contacts) + 1,
                    "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                contacts.append(new_contact)
                
                if save_contacts(contacts):
                    st.success("✅ Contact added successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to save contact")
            else:
                st.error("❌ Please provide at least name and mobile or email")
    
    # Display contacts
    if contacts:
        st.markdown("#### 📋 Your Contacts")
        
        for contact in contacts:
            with st.expander(f"👤 {contact['name']}", expanded=False):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    if contact.get('phone'):
                        st.write(f"📱 **Mobile:** {contact['phone']}")
                    if contact.get('email'):
                        st.write(f"📧 **Email:** {contact['email']}")
                    if contact.get('notes'):
                        st.write(f"📝 **Notes:** {contact['notes']}")
                    st.write(f"📅 **Added:** {contact.get('created', 'Unknown')}")
                
                with col2:
                    if st.button(f"🗑️ Delete", key=f"del_{contact['id']}"):
                        contacts.remove(contact)
                        save_contacts(contacts)
                        st.rerun()
    else:
        st.info("📭 No contacts yet. Add your first contact above!")

# Analytics page
def analytics_page():
    st.markdown("### 📊 Usage Analytics")
    
    # Load analytics data
    try:
        with open('api_usage.json', 'r') as f:
            api_stats = json.load(f)
        
        # Display statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📧 WhatsApp", api_stats.get('whatsapp', 0))
        
        with col2:
            st.metric("📤 Gmail Sent", api_stats.get('gmail_send', 0))
        
        with col3:
            st.metric("📥 Gmail Read", api_stats.get('gmail_read', 0))
        
        with col4:
            st.metric("🔋 Battery", api_stats.get('battery', 0))
        
        # Command statistics
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("🎤 Voice Commands", api_stats.get('voice_commands', 0))
        
        with col2:
            st.metric("💻 Manual Commands", api_stats.get('manual_commands', 0))
        
        # Total commands chart
        total_commands = api_stats.get('total_commands', 0)
        if total_commands > 0:
            st.markdown("#### 📈 Command Usage Overview")
            
            # Create a simple bar chart
            command_data = {
                'WhatsApp': api_stats.get('whatsapp', 0),
                'Gmail Send': api_stats.get('gmail_send', 0),
                'Gmail Read': api_stats.get('gmail_read', 0),
                'Battery': api_stats.get('battery', 0)
            }
            
            df = pd.DataFrame(list(command_data.items()), columns=['Command', 'Count'])
            st.bar_chart(df.set_index('Command'))
        
    except Exception as e:
        st.error(f"❌ Could not load analytics data: {e}")

# Settings page
def settings_page():
    st.markdown("### ⚙️ Application Settings")
    
    st.markdown("""
    <div class="feature-card">
        <h3>🔧 Application Configuration</h3>
        <p>Configure your Vira Assistant settings below.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # User settings
    st.markdown("#### 👤 User Settings")
    st.write(f"**Current User:** {st.session_state.username}")
    st.write(f"**Login Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Application info
    st.markdown("#### ℹ️ Application Information")
    st.write("**Version:** 1.0.0")
    st.write("**Platform:** Streamlit Cloud")
    st.write("**Deployment:** Cloud-based")
    
    # Features status
    st.markdown("#### 🚀 Features Status")
    
    features = {
        "🎤 Voice Commands": "🟢 Available (Limited in Cloud)",
        "📱 Contact Management": "🟢 Fully Available",
        "📧 Email Integration": "🟡 Requires OAuth Setup",
        "📊 Analytics": "🟢 Fully Available",
        "🔐 Admin Access": "🟢 Available"
    }
    
    for feature, status in features.items():
        st.write(f"**{feature}:** {status}")

# Main app logic
def main():
    if st.session_state.page == 'login' or not st.session_state.logged_in:
        login_page()
    else:
        dashboard_page()

if __name__ == "__main__":
    main()
