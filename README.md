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
- **WhatsApp Integration** - Send messages with PIN security
- **Email System** - Gmail integration for sending/receiving
- **PIN Protection** - 4-digit PIN for sensitive operations

### 🌐 Location Services
- **Weather Information** - Current and forecast data
- **Location-based Commands** - Works in your current location
- **Geographic Verification** - Confirms command compatibility

### 🔧 System Features
- **Admin Panel** - User management and API tracking
- **Session Management** - Secure user sessions
- **Logout Functionality** - Proper session cleanup
- **API Usage Statistics** - Track all API calls

## 🛠️ Technology Stack

- **Backend:** Flask with SocketIO
- **Frontend:** HTML5, TailwindCSS, JavaScript
- **Voice:** pyttsx3 (Text-to-Speech)
- **APIs:** Gmail API, Weather API
- **Authentication:** Google OAuth 2.0

## 📦 Installation

### Prerequisites
- Python 3.9+
- Git
- Modern web browser

### Setup
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/vira-assistant.git
cd vira-assistant

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

## 🚀 Quick Start

### Using Launcher
```bash
# Windows
vira.bat

# Linux/Mac
./vira.sh
```

### Manual Start
```bash
python app.py
```

Then open http://localhost:5000 in your browser.

## 📱 Mobile Support

- **Responsive Design** - Works on all devices
- **Voice Commands** - Mobile microphone support
- **Touch Interface** - Mobile-optimized controls
- **PWA Features** - App-like experience

## 🔐 Security

- **PIN Protection** - 4-digit PIN for sensitive operations
- **Session Management** - Secure user sessions
- **OAuth Integration** - Google authentication
- **Data Encryption** - Secure data transmission

## 📊 Admin Features

### User Management
- Add/remove users
- Manage user roles
- View user activity

### API Tracking
- Monitor API usage
- Track command frequency
- View system statistics

### System Monitoring
- Real-time status
- Performance metrics
- Error logging

## 🌐 Deployment Options

### Docker
```bash
docker-compose up -d
```

### Streamlit Cloud
1. Push to GitHub
2. Deploy on share.streamlit.io

### Traditional Hosting
- Render.com
- Heroku
- AWS EC2
- DigitalOcean

## 📝 Commands

### Basic Commands
- `hello` - Greeting
- `time` - Current time
- `weather` - Weather information
- `battery` - Battery status

### Communication Commands
- `whatsapp` - Send WhatsApp messages
- `send email` - Send emails
- `read mail` - Read emails

### System Commands
- `logout` - Logout and redirect to login
- `reset` - Reset conversation state
- `stop` - Stop application

### Help Commands
- `help` - Show all commands
- `commands` - Display command list

## 🌍 Location Support

Currently configured for:
- **City:** Vijayawada
- **Country:** India
- **Coordinates:** 17.6868°N, 83.2185°E

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 MIT License

This project is licensed under the MIT License. You are free to:
- Use the software for any purpose
- Modify the software
- Distribute the software
- Sublicense the software

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Check the documentation
- Review the troubleshooting guide

## 🎯 Roadmap

- [ ] Multi-language support expansion
- [ ] Advanced AI integration
- [ ] Cloud deployment automation
- [ ] Mobile app development
- [ ] API rate limiting
- [ ] Enhanced security features

---

**Built with ❤️ in Vijayawada, India**

*Licensed under MIT License - See [LICENSE](LICENSE) for details*
