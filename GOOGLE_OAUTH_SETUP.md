# Google OAuth Setup for Vira Assistant

## 📱 Mobile-Friendly Google Sign-In

### 🚀 What This Does:
- **Mobile Compatible**: Opens Google account selection on device
- **Secure Authentication**: OAuth 2.0 with Google
- **Gmail Integration**: Access to Gmail API for email features
- **One-Click Login**: No password required for Google users

### 🔧 Setup Instructions:

#### 1. Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project: "Vira Assistant"
3. Enable APIs:
   - Gmail API
   - Google+ API
   - OAuth 2.0 API

#### 2. Create OAuth Credentials
1. Go to **Credentials** → **Create Credentials** → **OAuth 2.0 Client ID**
2. Application type: **Web application**
3. Name: **Vira Assistant Web**
4. Authorized redirect URIs:
   - `http://localhost:5000/oauth/callback`
   - `https://vira-assistant.onrender.com/oauth/callback`
5. Copy **Client ID** and **Client Secret**

#### 3. Update Configuration
In `app.py`, replace these lines:
```python
GOOGLE_CLIENT_ID = "your-google-client-id.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "your-google-client-secret"
```

With your actual credentials:
```python
GOOGLE_CLIENT_ID = "123456789-abc.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "GOCSPX-abc123def456"
```

#### 4. Install Dependencies
```bash
pip install google-auth google-auth-oauthlib google-api-python-client
```

### 📱 Mobile Features:

#### **Device Account Selection:**
- ✅ **Opens Google account picker** on device
- ✅ **Shows all Google accounts** on phone/tablet
- ✅ **Biometric authentication** if enabled
- ✅ **One-tap sign-in** for returning users

#### **Cross-Platform Support:**
- ✅ **Android**: Opens Google account selection
- ✅ **iOS**: Opens Google account selection  
- ✅ **Desktop**: Opens Google account selection
- ✅ **Tablet**: Works on all tablets

### 🔒 Security Features:

#### **OAuth 2.0 Security:**
- ✅ **Secure token exchange**
- ✅ **Limited scope permissions**
- ✅ **Session-based authentication**
- ✅ **Automatic token refresh**

#### **User Permissions:**
- ✅ **Email access**: Read/send emails
- ✅ **Profile info**: Name and email
- ✅ **Gmail API**: Send emails through Vira
- ✅ **Revocable**: Users can disconnect anytime

### 🎯 User Experience:

#### **Login Flow:**
1. **Click "Sign in with Google"**
2. **Opens Google account picker** on device
3. **Select Google account**
4. **Grant permissions** (first time only)
5. **Redirect to dashboard**

#### **Mobile Benefits:**
- 📱 **Native experience** - uses device Google accounts
- 🔐 **Biometric support** - fingerprint/face ID
- ⚡ **Fast login** - no typing required
- 🔄 **Auto-sync** - stays logged in

### 🌐 Cloud Deployment:

#### **Render.com Configuration:**
```yaml
envVars:
  - key: GOOGLE_CLIENT_ID
    value: "your-client-id.apps.googleusercontent.com"
  - key: GOOGLE_CLIENT_SECRET  
    value: "your-client-secret"
```

#### **Testing:**
- **Local:** `http://localhost:5000/google/auth`
- **Cloud:** `https://vira-assistant.onrender.com/google/auth`

### 🛠️ Troubleshooting:

#### **Common Issues:**
1. **"redirect_uri_mismatch"**: Check redirect URIs in Google Console
2. **"invalid_client"**: Verify Client ID and Secret
3. **"access_denied"**: User denied permissions
4. **"mobile_not_working"**: Ensure mobile browser supports OAuth

#### **Debug Mode:**
```python
# Add to app.py for debugging
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 📋 Checklist:

#### **Before Deployment:**
- [ ] Create Google Cloud project
- [ ] Enable Gmail API
- [ ] Create OAuth credentials
- [ ] Update Client ID and Secret
- [ ] Test locally
- [ ] Deploy to cloud
- [ ] Test mobile login

#### **After Deployment:**
- [ ] Test mobile login
- [ ] Verify Gmail integration
- [ ] Check token refresh
- [ ] Test logout functionality

### 🎉 Ready to Use:

Once configured, users can:
- **Click "Sign in with Google"**
- **Select their Google account** on any device
- **Access Vira Assistant** instantly
- **Use Gmail features** seamlessly

**The Google OAuth system is now mobile-ready and will open Google account selection on any device!**
