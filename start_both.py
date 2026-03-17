#!/usr/bin/env python3
"""
Vira Assistant - Unified Launcher
Starts both Flask web app and Streamlit dashboard
"""

import subprocess
import sys
import time
import webbrowser
import threading
from datetime import datetime

def start_flask_app():
    """Start the Flask web application"""
    print("🚀 Starting Flask Web App...")
    try:
        # Start Flask app in background
        process = subprocess.Popen([
            sys.executable, "app.py"
        ], cwd=".")
        
        print("✅ Flask Web App started on http://localhost:5000")
        return process
    except Exception as e:
        print(f"❌ Failed to start Flask app: {e}")
        return None

def start_streamlit_dashboard():
    """Start Streamlit dashboard"""
    print("🚀 Starting Streamlit Dashboard...")
    try:
        # Start Streamlit in background
        process = subprocess.Popen([
            "streamlit", "run", "streamlit_deploy.py", 
            "--server.port", "8501",
            "--server.headless", "true"
        ], cwd=".")
        
        print("✅ Streamlit Dashboard started on http://localhost:8501")
        return process
    except Exception as e:
        print(f"❌ Failed to start Streamlit: {e}")
        return None

def open_browsers():
    """Open browsers for both applications"""
    time.sleep(3)  # Wait for servers to start
    
    print("🌐 Opening browsers...")
    
    # Open Flask web app
    try:
        webbrowser.open("http://localhost:5000")
        print("✅ Flask Web App opened in browser")
    except:
        print("❌ Could not open Flask app in browser")
    
    # Open Streamlit dashboard
    try:
        webbrowser.open("http://localhost:8501")
        print("✅ Streamlit Dashboard opened in browser")
    except:
        print("❌ Could not open Streamlit in browser")

def check_dependencies():
    """Check if all dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    # Check Python packages
    required_packages = ["flask", "streamlit", "psutil"]
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"📦 Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install"
            ] + missing_packages, check=True)
            print("✅ All packages installed successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to install packages")
            return False
    
    return True

def main():
    """Main launcher function"""
    print("=" * 60)
    print("🤖 Vira Assistant - Unified Launcher")
    print("=" * 60)
    print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Please install missing dependencies and try again")
        return
    
    print()
    print("🚀 Starting both applications...")
    print()
    
    # Start Flask app
    flask_process = start_flask_app()
    
    # Wait a moment before starting Streamlit
    time.sleep(2)
    
    # Start Streamlit dashboard
    streamlit_process = start_streamlit_dashboard()
    
    # Open browsers after a short delay
    browser_thread = threading.Thread(target=open_browsers)
    browser_thread.daemon = True
    browser_thread.start()
    
    print()
    print("=" * 60)
    print("🌐 Both applications are running!")
    print("=" * 60)
    print("📱 Flask Web App:   http://localhost:5000")
    print("📊 Streamlit Dashboard: http://localhost:8501")
    print()
    print("🔧 Features:")
    print("   • Flask Web App - Full Vira Assistant with voice commands")
    print("   • Streamlit Dashboard - Deployment controls and monitoring")
    print("   • Mobile Compatible - Both work on phones/tablets")
    print()
    print("⚡ Quick Access:")
    print("   • Main Assistant: http://localhost:5000")
    print("   • Admin Panel: http://localhost:5000/admin")
    print("   • Deployment: http://localhost:8501")
    print()
    print("🛑 To stop: Press Ctrl+C in this window")
    print("=" * 60)
    
    try:
        # Keep the launcher running
        while True:
            time.sleep(1)
            
            # Check if processes are still running
            if flask_process and flask_process.poll() is not None:
                print("❌ Flask Web App stopped unexpectedly")
                break
                
            if streamlit_process and streamlit_process.poll() is not None:
                print("❌ Streamlit Dashboard stopped unexpectedly")
                break
                
    except KeyboardInterrupt:
        print("\n🛑 Stopping applications...")
        
        # Stop Flask process
        if flask_process:
            flask_process.terminate()
            print("✅ Flask Web App stopped")
        
        # Stop Streamlit process
        if streamlit_process:
            streamlit_process.terminate()
            print("✅ Streamlit Dashboard stopped")
        
        print("👋 Goodbye!")
    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
