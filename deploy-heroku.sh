#!/bin/bash
# Deploy to Heroku - Production Deployment Script

echo "🚀 Deploying Vira Assistant to Heroku..."

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found. Installing..."
    npm install -g heroku
fi

# Login to Heroku
echo "📝 Please login to Heroku..."
heroku login

# Create Heroku app
APP_NAME="vira-assistant-$(date +%s)"
echo "🏗️  Creating Heroku app: $APP_NAME"
heroku create $APP_NAME

# Set environment variables
echo "⚙️  Setting environment variables..."
heroku config:set FLASK_ENV=production --app $APP_NAME
heroku config:set SECRET_KEY=$(openssl rand -hex 32) --app $APP_NAME

# Add buildpacks
echo "📦 Adding buildpacks..."
heroku buildpacks:set heroku/python --app $APP_NAME

# Deploy to Heroku
echo "🚀 Deploying to Heroku..."
git init
git add .
git commit -m "Deploy to Heroku production"
heroku git:remote -a $APP_NAME heroku
git push heroku main

# Open the app
echo "🌐 Opening your Vira Assistant..."
heroku open --app $APP_NAME

echo "✅ Deployment complete!"
echo "📱 Your app is available at: https://$APP_NAME.herokuapp.com"
