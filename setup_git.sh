#!/bin/bash

# Vira Assistant - Git Setup Script with MIT License
echo "🤖 Vira Assistant - Git Setup with MIT License"
echo "=================================================="

# Navigate to project directory
cd "$(dirname "$0")"

# Step 1: Initialize Git repository
echo "📋 Step 1: Initializing Git repository..."
git init
if [ $? -eq 0 ]; then
    echo "✅ Git repository initialized successfully"
else
    echo "❌ Failed to initialize Git repository"
    exit 1
fi

# Step 2: Configure Git (if not configured)
echo "📋 Step 2: Checking Git configuration..."
if ! git config user.name > /dev/null 2>&1; then
    echo "⚠️ Git user not configured. Please set your name:"
    read -p "Enter your name: " GIT_NAME
    git config --global user.name "$GIT_NAME"
fi

if ! git config user.email > /dev/null 2>&1; then
    echo "⚠️ Git email not configured. Please set your email:"
    read -p "Enter your email: " GIT_EMAIL
    git config --global user.email "$GIT_EMAIL"
fi

echo "✅ Git configuration complete"
echo "   Name: $(git config user.name)"
echo "   Email: $(git config user.email)"

# Step 3: Add all files
echo "📋 Step 3: Adding files to Git..."
git add .
if [ $? -eq 0 ]; then
    echo "✅ Files added to staging area"
else
    echo "❌ Failed to add files to Git"
    exit 1
fi

# Step 4: Commit files
echo "📋 Step 4: Creating initial commit..."
git commit -m "Initial commit - Vira Assistant with MIT License

Features:
- Voice commands with location-based processing
- WhatsApp and email integration with PIN security
- Weather information for Vijayawada, India
- Admin panel with API usage tracking
- Google OAuth authentication
- Mobile-responsive interface
- MIT License compliance

Technology Stack:
- Flask with SocketIO
- HTML5, TailwindCSS, JavaScript
- pyttsx3 for text-to-speech
- Gmail API and Weather API integration"
if [ $? -eq 0 ]; then
    echo "✅ Initial commit created successfully"
else
    echo "❌ Failed to create initial commit"
    exit 1
fi

# Step 5: Create GitHub repository instructions
echo "📋 Step 5: GitHub Repository Setup"
echo "=================================="
echo ""
echo "To complete the setup, follow these steps:"
echo ""
echo "1. 🌐 Go to GitHub: https://github.com"
echo "2. ➕ Click 'New repository'"
echo "3. 📝 Repository name: vira-assistant"
echo "4. 📄 Description: Vira Voice Assistant - Location-based AI with WhatsApp, Email, Weather"
echo "5. 🔓 Visibility: Public (or Private)"
echo "6. ✅ Click 'Create repository'"
echo ""
echo "7. 📋 Copy the repository URL (HTTPS)"
echo "8. 🔄 Run these commands:"
echo ""
echo "   git remote add origin https://github.com/YOUR_USERNAME/vira-assistant.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "9. 🎉 Your repository is now on GitHub!"
echo ""

# Step 6: Show repository status
echo "📊 Repository Status:"
echo "===================="
echo "📁 Files committed:"
git log --oneline -1
echo ""
echo "📋 Files in repository:"
git ls-files | head -20
echo "..."
echo ""
echo "📄 License: MIT License"
echo "📍 Location: Vijayawada, India"
echo "🔐 Security: PIN protection enabled"
echo "🌐 Mobile: Responsive design"
echo ""

echo "✅ Git setup completed successfully!"
echo "🚀 Ready to push to GitHub!"
echo ""
echo "📝 Don't forget to:"
echo "   1. Create GitHub repository"
echo "   2. Add remote origin"
echo "   3. Push to main branch"
echo ""
echo "🎯 Your Vira Assistant is now MIT licensed and ready for sharing!"
