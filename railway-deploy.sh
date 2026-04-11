#!/bin/bash

# Vira Assistant - Railway Deployment Script
# Quick deployment to Railway cloud platform

set -e

echo "🚂 Vira Assistant - Railway Deployment"
echo "======================================="

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Installing..."
    npm install -g @railway/cli
fi

echo "✅ Railway CLI is installed"

# Check if user is logged in
if ! railway whoami &> /dev/null; then
    echo "🔐 Please login to Railway..."
    railway login
fi

echo "✅ Logged in to Railway"

# Deploy to Railway
echo "🚀 Deploying to Railway..."
railway up

echo "⏳ Waiting for deployment..."
sleep 10

# Get the application URL
echo "🌐 Getting application URL..."
APP_URL=$(railway domain)
echo "✅ Your app is deployed at: $APP_URL"

echo ""
echo "🎉 Deployment completed successfully!"
echo "======================================="
echo "🌐 App URL: $APP_URL"
echo "👤 Login: admin / admin123"
echo "📊 Admin Panel: $APP_URL/admin"
echo "📱 Mobile: Works on all devices"
echo ""
echo "💡 Next steps:"
echo "1. Visit your app at the URL above"
echo "2. Login with admin / admin123"
echo "3. Change the default password"
echo "4. Test all features"
echo ""
echo "🔧 To view logs: railway logs"
echo "🔧 To open app: railway open"
