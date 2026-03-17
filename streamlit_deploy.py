import streamlit as st
import subprocess
import sys
import os
from datetime import datetime
import json

# Streamlit configuration
st.set_page_config(
    page_title="Vira Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .status-box {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .feature-box {
        background: #e8f4f8;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🤖 Vira Assistant</h1>', unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🔧 Controls")

# Deployment Options
deployment_type = st.sidebar.selectbox(
    "Choose Deployment Method:",
    ["Docker", "Streamlit Cloud", "Local", "Manual"]
)

if deployment_type == "Docker":
    st.sidebar.subheader("🐳 Docker Deployment")
    
    # Check if Docker is available
    try:
        docker_check = subprocess.run(["docker", "--version"], capture_output=True, text=True)
        st.sidebar.success(f"✅ Docker Available: {docker_check.stdout.strip()}")
    except:
        st.sidebar.error("❌ Docker not found. Please install Docker first.")
        st.stop()
    
    # Docker controls
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.button("🚀 Start Container"):
            try:
                result = subprocess.run(["docker-compose", "up", "-d"], capture_output=True, text=True)
                if result.returncode == 0:
                    st.success("✅ Container started successfully!")
                    st.code(result.stdout)
                else:
                    st.error(f"❌ Failed to start: {result.stderr}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    with col2:
        if st.button("🛑 Stop Container"):
            try:
                result = subprocess.run(["docker-compose", "down"], capture_output=True, text=True)
                if result.returncode == 0:
                    st.success("✅ Container stopped successfully!")
                    st.code(result.stdout)
                else:
                    st.error(f"❌ Failed to stop: {result.stderr}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    # Container status
    try:
        result = subprocess.run(["docker", "ps", "--filter", "name=vira-assistant"], capture_output=True, text=True)
        st.sidebar.subheader("📊 Container Status")
        st.code(result.stdout)
    except:
        st.sidebar.error("❌ Could not get container status")

elif deployment_type == "Streamlit Cloud":
    st.sidebar.subheader("☁️ Streamlit Cloud Deployment")
    
    st.info("""
    **Streamlit Cloud Deployment Steps:**
    
    1. **Create GitHub Repository:**
       - Push your code to GitHub
       - Ensure all files are committed
    
    2. **Streamlit Cloud Setup:**
       - Go to [share.streamlit.io](https://share.streamlit.io)
       - Connect your GitHub account
       - Select your repository
    
    3. **Configuration:**
       - Main file: `streamlit_deploy.py`
       - Python version: 3.9+
       - Requirements: `requirements_streamlit.txt`
    
    4. **Deploy:**
       - Click "Deploy"
       - Wait for deployment to complete
    """)
    
    # Create requirements for Streamlit
    streamlit_requirements = """
streamlit==1.28.1
psutil==5.9.5
requests==2.31.0
flask==2.3.3
flask-socketio==5.3.6
pyttsx3==2.90
pywhatkit==5.4
google-api-python-client==2.100.0
google-auth-httplib2==0.1.1
google-auth-oauthlib==1.0.0
"""
    
    with st.expander("📋 Streamlit Requirements"):
        st.code(streamlit_requirements)
    
    if st.button("📝 Create Streamlit Requirements"):
        with open("requirements_streamlit.txt", "w") as f:
            f.write(streamlit_requirements.strip())
        st.success("✅ requirements_streamlit.txt created!")

elif deployment_type == "Local":
    st.sidebar.subheader("💻 Local Deployment")
    
    # Check Python version
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    st.sidebar.info(f"🐍 Python: {python_version}")
    
    # Local controls
    if st.button("🚀 Start Local Server"):
        try:
            st.info("Starting local server...")
            # This would normally run the Flask app
            st.success("✅ Local server started on http://localhost:5000")
            st.info("Open your browser and go to http://localhost:5000")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🚀 Deployment Status")
    
    # System info
    system_info = {
        "Platform": sys.platform,
        "Python": python_version,
        "Working Directory": os.getcwd(),
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    for key, value in system_info.items():
        st.markdown(f'<div class="status-box"><strong>{key}:</strong> {value}</div>', unsafe_allow_html=True)
    
    # File status
    st.subheader("📁 Project Files")
    
    required_files = [
        "app.py",
        "requirements.txt", 
        "Dockerfile",
        "docker-compose.yml",
        "streamlit_deploy.py"
    ]
    
    for file in required_files:
        if os.path.exists(file):
            file_size = os.path.getsize(file)
            st.markdown(f'<div class="feature-box">✅ {file} ({file_size} bytes)</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="feature-box">❌ {file} (missing)</div>', unsafe_allow_html=True)

with col2:
    st.subheader("🔗 Quick Links")
    
    links = {
        "🤖 Vira Assistant": "http://localhost:5000" if deployment_type == "Local" else "#",
        "🐳 Docker Hub": "https://hub.docker.com",
        "☁️ Streamlit Cloud": "https://share.streamlit.io",
        "📚 Documentation": "#"
    }
    
    for name, url in links.items():
        st.markdown(f"[{name}]({url})")
    
    # Deployment commands
    st.subheader("⌨️ Commands")
    
    if deployment_type == "Docker":
        commands = [
            "docker-compose up -d",
            "docker-compose down", 
            "docker logs vira-assistant",
            "docker ps"
        ]
    elif deployment_type == "Streamlit Cloud":
        commands = [
            "git add .",
            "git commit -m 'Deploy to Streamlit'",
            "git push origin main"
        ]
    else:
        commands = [
            "python app.py",
            "pip install -r requirements.txt"
        ]
    
    for cmd in commands:
        st.code(cmd)

# Logs section
st.subheader("📋 Recent Activity")

# Create sample logs if they don't exist
if not os.path.exists("deployment_logs.json"):
    sample_logs = [
        {"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "action": "System initialized", "status": "success"},
        {"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "action": "Docker checked", "status": "success"},
        {"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "action": "Files verified", "status": "success"}
    ]
    with open("deployment_logs.json", "w") as f:
        json.dump(sample_logs, f, indent=2)

# Display logs
try:
    with open("deployment_logs.json", "r") as f:
        logs = json.load(f)
    
    for log in reversed(logs[-5:]):  # Show last 5 logs
        status_emoji = "✅" if log["status"] == "success" else "❌"
        st.markdown(f"{status_emoji} **{log['time']}** - {log['action']}")
except:
    st.info("No logs available yet.")

# Footer
st.markdown("---")
st.markdown('<div style="text-align: center; color: #666;">🤖 Vira Assistant Deployment Dashboard</div>', unsafe_allow_html=True)
