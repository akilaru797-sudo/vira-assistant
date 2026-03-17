# 🚀 Vira Assistant Deployment Guide

## 📋 Deployment Options

### Option 1: Docker Deployment (Recommended)

#### 🐳 Prerequisites:
- Docker Desktop installed
- Docker Compose installed
- 4GB+ RAM available

#### 🚀 Quick Start:
```bash
# 1. Clone or navigate to project directory
cd c:/Users/HP/OneDrive/Desktop/mile_4

# 2. Build and start container
docker-compose up -d

# 3. Check status
docker ps

# 4. Access application
# Open browser: http://localhost:5000
```

#### 📝 Docker Commands:
```bash
# Start container
docker-compose up -d

# Stop container
docker-compose down

# View logs
docker logs vira-assistant

# Rebuild container
docker-compose up --build

# Access container shell
docker exec -it vira-assistant bash
```

#### 🔧 Docker Configuration:
- **Port:** 5000 (host) → 5000 (container)
- **Volumes:** Persistent data storage
- **Health Check:** Every 30 seconds
- **Restart:** Automatic unless stopped

---

### Option 2: Streamlit Cloud Deployment

#### ☁️ Prerequisites:
- GitHub account
- Streamlit account (free)
- All code pushed to GitHub

#### 🚀 Deployment Steps:

**1. Prepare GitHub Repository:**
```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Ready for Streamlit deployment"
git branch -M main

# Create GitHub repository and push
git remote add origin https://github.com/YOUR_USERNAME/vira-assistant.git
git push -u origin main
```

**2. Streamlit Cloud Setup:**
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Connect your GitHub account
4. Select repository: `vira-assistant`
5. Main file path: `streamlit_deploy.py`
6. Python version: 3.9+
7. Click "Deploy"

**3. Configuration:**
```toml
# .streamlit/config.toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"

[server]
port = 8501
headless = true
```

---

### Option 3: Local Development

#### 💻 Prerequisites:
- Python 3.9+
- pip package manager
- 2GB+ RAM

#### 🚀 Quick Start:
```bash
# 1. Navigate to project
cd c:/Users/HP/OneDrive/Desktop/mile_4

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start application
python app.py

# 4. Access in browser
# Open: http://localhost:5000
```

#### 📝 Local Commands:
```bash
# Install requirements
pip install -r requirements.txt

# Start Flask app
python app.py

# Start with debug mode
FLASK_ENV=development python app.py

# Check dependencies
pip list
```

---

### Option 4: Streamlit Local Deployment

#### 🎯 Prerequisites:
- Python 3.9+
- Streamlit installed

#### 🚀 Quick Start:
```bash
# 1. Install Streamlit
pip install streamlit

# 2. Run Streamlit app
streamlit run streamlit_deploy.py

# 3. Access in browser
# Open: http://localhost:8501
```

---

## 🔧 Configuration Files

### Docker Configuration:
```yaml
# docker-compose.yml
version: '3.8'
services:
  vira-assistant:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./user_database.json:/app/user_database.json
      - ./contacts.json:/app/contacts.json
      - ./command_history.json:/app/command_history.json
    environment:
      - FLASK_ENV=production
    restart: unless-stopped
```

### Dockerfile:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

### Requirements:
```txt
# requirements.txt
flask==2.3.3
flask-socketio==5.3.6
pyttsx3==2.90
psutil==5.9.5
pywhatkit==5.4
google-api-python-client==2.100.0
google-auth-httplib2==0.1.1
google-auth-oauthlib==1.0.0
requests==2.31.0
```

---

## 🌐 Cloud Deployment Options

### Render.com (Recommended for Production):
1. Push code to GitHub
2. Create Render account
3. New Web Service
4. Connect GitHub repo
5. Auto-detect from `render.yaml`

### Heroku:
1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create vira-assistant`
4. Deploy: `git push heroku main`

### AWS EC2:
1. Launch EC2 instance (t2.micro)
2. Install Docker
3. Clone repository
4. Run: `docker-compose up -d`

### DigitalOcean:
1. Create Droplet
2. Install Docker
3. Deploy with Docker Compose

---

## 📱 Mobile Deployment

### Progressive Web App (PWA):
- Works on mobile browsers
- Voice commands supported
- Responsive design
- No app store required

### Mobile Testing:
```bash
# Test on mobile
1. Start server: python app.py
2. Find local IP: ipconfig (Windows) / ifconfig (Mac/Linux)
3. Access on mobile: http://YOUR_IP:5000
```

---

## 🔍 Troubleshooting

### Docker Issues:
```bash
# Container won't start
docker logs vira-assistant

# Port conflict
docker-compose down
docker-compose up -d --force-recreate

# Permission issues
docker-compose down
docker-compose up -d --user root
```

### Streamlit Issues:
```bash
# Port already in use
lsof -ti:8501 | xargs kill -9

# Dependencies missing
pip install -r requirements_streamlit.txt
```

### Local Issues:
```bash
# Python version mismatch
python --version  # Should be 3.9+

# Permission denied
chmod +x app.py

# Module not found
pip install MODULE_NAME
```

---

## 📊 Monitoring

### Docker Monitoring:
```bash
# Container status
docker ps

# Resource usage
docker stats

# Logs
docker logs -f vira-assistant
```

### Application Monitoring:
- **Health Check:** http://localhost:5000/test
- **Admin Panel:** http://localhost:5000/admin
- **API Usage:** Available in admin panel

---

## 🚀 Production Checklist

### Before Deployment:
- [ ] Test all features locally
- [ ] Update environment variables
- [ ] Configure SSL certificates
- [ ] Set up monitoring
- [ ] Backup data files

### After Deployment:
- [ ] Test mobile compatibility
- [ ] Verify voice commands
- [ ] Check API integrations
- [ ] Monitor performance
- [ ] Set up alerts

---

## 🎯 Quick Deployment Commands

### Docker (Fastest):
```bash
cd c:/Users/HP/OneDrive/Desktop/mile_4
docker-compose up -d
```

### Streamlit Cloud:
```bash
git add .
git commit -m "Deploy"
git push origin main
# Then deploy on Streamlit Cloud
```

### Local:
```bash
pip install -r requirements.txt
python app.py
```

---

## 💡 Tips

1. **Use Docker** for consistent environments
2. **Streamlit Cloud** for easy sharing
3. **Monitor logs** for debugging
4. **Test mobile** compatibility
5. **Backup data** regularly

---

**Choose the deployment method that best fits your needs. Docker is recommended for production, Streamlit Cloud for easy sharing, and local for development!**
