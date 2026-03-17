#!/bin/bash

# Vira Assistant Deployment Script
# Usage: ./deploy.sh [docker|streamlit|local]

DEPLOYMENT_TYPE=${1:-docker}
PROJECT_DIR="c:/Users/HP/OneDrive/Desktop/mile_4"

echo "🚀 Vira Assistant Deployment Script"
echo "=================================="
echo "Deployment Type: $DEPLOYMENT_TYPE"
echo "Project Directory: $PROJECT_DIR"
echo ""

case $DEPLOYMENT_TYPE in
    "docker")
        echo "🐳 Docker Deployment"
        echo "-------------------"
        
        # Check if Docker is running
        if ! docker info > /dev/null 2>&1; then
            echo "❌ Docker is not running. Please start Docker first."
            exit 1
        fi
        
        echo "✅ Docker is running"
        
        # Navigate to project directory
        cd "$PROJECT_DIR" || {
            echo "❌ Could not navigate to project directory"
            exit 1
        }
        
        echo "📁 Current directory: $(pwd)"
        
        # Build and start container
        echo "🔨 Building and starting container..."
        docker-compose up -d --build
        
        # Check if container is running
        if docker ps | grep -q "vira-assistant"; then
            echo "✅ Container started successfully!"
            echo "🌐 Access at: http://localhost:5000"
            echo "📊 Container status:"
            docker ps | grep vira-assistant
        else
            echo "❌ Container failed to start"
            echo "📋 Logs:"
            docker-compose logs vira-assistant
            exit 1
        fi
        ;;
        
    "streamlit")
        echo "☁️ Streamlit Deployment"
        echo "---------------------"
        
        cd "$PROJECT_DIR" || {
            echo "❌ Could not navigate to project directory"
            exit 1
        }
        
        # Check if Streamlit is installed
        if ! command -v streamlit &> /dev/null; then
            echo "📦 Installing Streamlit..."
            pip install streamlit
        fi
        
        echo "✅ Streamlit is available"
        
        # Create Streamlit requirements if needed
        if [ ! -f "requirements_streamlit.txt" ]; then
            echo "📝 Creating Streamlit requirements..."
            cat > requirements_streamlit.txt << EOF
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
EOF
        fi
        
        echo "🚀 Starting Streamlit app..."
        streamlit run streamlit_deploy.py --server.port 8501 --server.headless true
        ;;
        
    "local")
        echo "💻 Local Deployment"
        echo "------------------"
        
        cd "$PROJECT_DIR" || {
            echo "❌ Could not navigate to project directory"
            exit 1
        }
        
        # Check Python version
        PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
        echo "🐍 Python version: $PYTHON_VERSION"
        
        # Install requirements
        echo "📦 Installing requirements..."
        pip install -r requirements.txt
        
        echo "🚀 Starting local server..."
        python app.py
        ;;
        
    "stop")
        echo "🛑 Stop Services"
        echo "---------------"
        
        cd "$PROJECT_DIR" || {
            echo "❌ Could not navigate to project directory"
            exit 1
        }
        
        # Stop Docker container
        if docker ps | grep -q "vira-assistant"; then
            echo "🛑 Stopping Docker container..."
            docker-compose down
            echo "✅ Container stopped"
        else
            echo "ℹ️ No running Docker container found"
        fi
        
        # Kill any running Python processes
        echo "🛑 Stopping Python processes..."
        pkill -f "python app.py" 2>/dev/null || true
        pkill -f "streamlit" 2>/dev/null || true
        echo "✅ Processes stopped"
        ;;
        
    "status")
        echo "📊 Service Status"
        echo "----------------"
        
        cd "$PROJECT_DIR" || {
            echo "❌ Could not navigate to project directory"
            exit 1
        }
        
        # Docker status
        echo "🐳 Docker Status:"
        if docker ps | grep -q "vira-assistant"; then
            echo "✅ Container is running"
            docker ps | grep vira-assistant
        else
            echo "❌ Container is not running"
        fi
        
        echo ""
        
        # Port status
        echo "🌐 Port Status:"
        if netstat -tuln | grep -q ":5000"; then
            echo "✅ Port 5000 is in use"
        else
            echo "❌ Port 5000 is free"
        fi
        
        if netstat -tuln | grep -q ":8501"; then
            echo "✅ Port 8501 is in use (Streamlit)"
        else
            echo "❌ Port 8501 is free"
        fi
        
        echo ""
        
        # File status
        echo "📁 File Status:"
        for file in "app.py" "requirements.txt" "Dockerfile" "docker-compose.yml"; do
            if [ -f "$file" ]; then
                echo "✅ $file exists"
            else
                echo "❌ $file missing"
            fi
        done
        ;;
        
    *)
        echo "❌ Unknown deployment type: $DEPLOYMENT_TYPE"
        echo ""
        echo "Usage: $0 [docker|streamlit|local|stop|status]"
        echo ""
        echo "Options:"
        echo "  docker    - Deploy with Docker (recommended)"
        echo "  streamlit - Deploy with Streamlit"
        echo "  local     - Deploy locally"
        echo "  stop      - Stop all services"
        echo "  status    - Show service status"
        exit 1
        ;;
esac

echo ""
echo "✅ Deployment completed!"
echo "🌐 Access your Vira Assistant:"
echo "   Docker: http://localhost:5000"
echo "   Streamlit: http://localhost:8501"
echo ""
echo "📚 For more help, see DEPLOYMENT_GUIDE.md"
