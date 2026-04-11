# 🤖 Vira Assistant - Voice AI System

**Location-based Voice Assistant with WhatsApp, Email, and Weather Integration**

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🚀 Features

### 🎤 Voice Commands
- **Natural Language Processing** - Understands English and Telugu
- **Location-Aware** - Works in Vijayawada, India
- **Real-time Processing** - Fast command recognition

### 📱 Communication

## 🚀 Quick Start

### Option 1: Railway Cloud (Recommended)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway up
```

### Option 2: Docker
```bash
# Deploy with Docker
docker-compose up -d
```

### Option 3: Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python railway_app.py
```

## 📋 Requirements

- Python 3.9+
- Flask 2.3.3
- Flask-SocketIO 5.3.6
- Node.js (for Railway CLI)

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/vira-assistant.git
   cd vira-assistant
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python railway_app.py
   ```

4. **Access the application**
   - Open http://localhost:5000
   - Login with: `admin` / `admin123`

## 🌐 Deployment Options

### � Railway Cloud
- **Best for:** Production deployment
- **Features:** Auto-scaling, persistent storage, HTTPS
- **Cost:** Free tier available, $5/month for production
- **Guide:** See [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md)

### 🌊 Streamlit Cloud
- **Best for:** Quick demos and prototypes
- **Features:** Easy deployment, free tier
- **Cost:** Free tier available
- **File:** Use `streamlit_app.py`

### 🐳 Docker
- **Best for:** Local development and custom hosting
- **Features:** Containerized, portable
- **Cost:** Free (hosting costs vary)
- **Files:** `Dockerfile`, `docker-compose.yml`

### 🎨 Render
- **Best for:** Flask applications
- **Features:** Easy deployment, good free tier
- **Cost:** Free tier available

## 📁 Project Structure

```
vira-assistant/
├── railway_app.py          # Main Flask application (Railway optimized)
├── app.py                  # Original Flask application
├── streamlit_app.py        # Streamlit version
├── requirements.txt        # Python dependencies
├── Procfile               # Process configuration (Railway)
├── runtime.txt            # Python version
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose setup
├── templates/             # HTML templates
│   ├── login.html
│   ├── dashboard.html
│   ├── admin.html
│   ├── contacts.html
│   └── register.html
├── static/                # Static files
│   ├── voice.js
│   ├── auth_voice.js
│   └── styles.css
├── gmail_module.py        # Gmail integration
└── JSON Data Files        # Application data
    ├── user_database.json
    ├── contacts.json
    ├── reminders.json
    ├── api_usage.json
    ├── command_history.json
    ├── credentials.json
    └── token.json
```

## � Default Credentials

- **Username:** `admin`
- **Password:** `admin123`

⚠️ **Important:** Change the default password before deploying to production!

## 📱 Mobile Usage

The application is fully responsive and works on:
- 📱 **Mobile phones** - iOS and Android
- 💻 **Tablets** - iPad and Android tablets
- 🖥️ **Desktop** - Windows, Mac, Linux

## 🎤 Voice Commands

Available voice commands:
- `hello` - Greeting
- `time` - Get current time
- `battery` - Check battery status
- `add contact` - Add new contact
- `as admin` - Admin login
- `help` - Show available commands

## � Features Overview

### 🏠 **Dashboard**
- Real-time statistics
- Quick action buttons
- Recent activity feed
- System status

### 📱 **Contact Management**
- Add, edit, delete contacts
- Search and filter contacts
- Import/export contacts
- Contact groups

### 📧 **Email Integration**
- Gmail OAuth integration
- Send emails
- Read emails
- Email summaries

### 📊 **Analytics**
- Usage statistics
- Command history
- User activity
- System performance

### � **Admin Panel**
- User management
- System settings
- API usage tracking
- Security settings

## 🔧 Configuration

### Environment Variables
```bash
FLASK_ENV=production          # Production mode
SECRET_KEY=your-secret-key    # Flask secret key
PORT=5000                     # Application port
```

### Gmail Integration
1. Create Google Cloud project
2. Enable Gmail API
3. Create OAuth credentials
4. Update `credentials.json`
5. Update `token.json`

## 🛠️ Development

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
python railway_app.py

# Or use original app
python app.py
```

### Docker Development
```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down
```

## 📈 API Endpoints

### Authentication
- `POST /login` - User login
- `GET /logout` - User logout

### Contacts
- `GET /api/contacts` - Get all contacts
- `POST /api/contacts` - Add new contact
- `DELETE /api/contacts/<id>` - Delete contact

### Utilities
- `GET /api/time` - Get current time
- `GET /api/battery` - Get battery info
- `GET /api/admin/api_usage` - Get usage stats (admin only)

### Health
- `GET /health` - Health check
- `GET /test` - Test endpoint

## 🔍 Troubleshooting

### Common Issues

**Build Failed:**
- Check `requirements.txt` format
- Verify Python version compatibility
- Ensure all JSON files are valid

**Application Not Starting:**
- Check environment variables
- Verify port availability
- Check application logs

**Voice Commands Not Working:**
- Check microphone permissions
- Verify browser compatibility
- Check network connection

**Email Integration Issues:**
- Verify OAuth credentials
- Check Gmail API settings
- Ensure proper token refresh

### Debug Commands
```bash
# Check application health
curl http://localhost:5000/health

# View logs (Railway)
railway logs

# View logs (Docker)
docker-compose logs -f
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Flask team for the excellent web framework
- Socket.IO for real-time communication
- Railway for excellent hosting platform
- Google for Gmail API

## 📞 Support

If you encounter any issues:
1. Check the troubleshooting section
2. Search existing GitHub issues
3. Create a new issue with details
4. Join our community discussions

## 🚀 Roadmap

- [ ] Mobile app (React Native)
- [ ] More voice commands
- [ ] AI-powered responses
- [ ] Multi-language support
- [ ] Advanced analytics
- [ ] Team collaboration features
- [ ] Mobile app development
- [ ] API rate limiting
- [ ] Enhanced security features

---

**Built with ❤️ in Vijayawada, India**

*Licensed under MIT License - See [LICENSE](LICENSE) for details*
