# Vira Assistant - Cloud Deployment Guide

## 🚀 Cloud Deployment Options

### ☁️ AWS Deployment

#### **1. AWS Elastic Beanstalk**
```bash
# Install EB CLI
pip install awsebcli

# Initialize EB app
eb init vira-assistant

# Create environment
eb create production

# Deploy
eb deploy
```

#### **2. AWS ECS with Fargate**
```dockerfile
# Dockerfile already optimized for cloud
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

#### **3. AWS Lambda (Serverless)**
```python
# lambda_handler.py
import json
from app import app

def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
```

---

### 🐳 Docker Cloud Platforms

#### **1. Google Cloud Run**
```bash
# Build and push to GCR
gcloud builds submit --tag gcr.io/PROJECT-ID/vira-assistant

# Deploy to Cloud Run
gcloud run deploy --image gcr.io/PROJECT-ID/vira-assistant --platform managed
```

#### **2. Azure Container Instances**
```bash
# Build and push to ACR
az acr build --registry myregistry --image vira-assistant .

# Deploy to Container Instances
az container create --resource-group myResourceGroup --name vira-assistant --image myregistry.azurecr.io/vira-assistant
```

#### **3. DigitalOcean App Platform**
```yaml
# .do/app.yaml
name: vira-assistant
services:
- name: web
  source_dir: /
  github:
    repo: your-username/vira-assistant
    branch: main
  run_command: gunicorn --bind 0.0.0.0:5000 app:app
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  http_port: 5000
```

---

### 🌐 PaaS Platforms

#### **1. Heroku**
```dockerfile
# Heroku Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "app:app"]
```

```bash
# Deploy to Heroku
heroku create vira-assistant
heroku container:push web --app vira-assistant
heroku open --app vira-assistant
```

#### **2. Render.com**
```yaml
# render.yaml
services:
  type: web
  name: vira-assistant
  env: python
  buildCommand: pip install -r requirements.txt
  startCommand: gunicorn app:app
  envVars:
    - key: PORT
      value: 5000
```

#### **3. Railway.app**
```bash
# Deploy to Railway
railway login
railway init
railway up
```

---

### ⚡ Serverless Platforms

#### **1. Vercel**
```javascript
// vercel.json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

#### **2. Netlify Functions**
```python
# netlify/functions/api.py
import json
from app import app

def handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Hello from Netlify!'})
    }
```

---

### 🔧 Production Configuration

#### **Environment Variables**
```bash
# Required for production
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Optional
REDIS_URL=redis://user:pass@host:port
DATABASE_URL=postgresql://user:pass@host:db
```

#### **Production Server**
```python
# wsgi.py for production
from app import app

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
```

#### **Gunicorn Config**
```bash
# gunicorn.conf.py
bind = "0.0.0.0:5000"
workers = 4
worker_class = "gevent"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
preload_app = True
```

---

### 📊 Monitoring & Scaling

#### **1. Health Checks**
```python
@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })
```

#### **2. Metrics**
```python
@app.route('/metrics')
def metrics():
    return jsonify({
        'active_users': len(active_sessions),
        'commands_processed': command_count,
        'uptime': uptime_seconds
    })
```

#### **3. Logging**
```python
import logging
from logging.handlers import RotatingFileHandler

# Production logging
if app.config['ENV'] == 'production':
    handler = RotatingFileHandler('vira.log', maxBytes=10000000, backupCount=5)
    handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s'
    ))
    app.logger.addHandler(handler)
```

---

### 🔒 Security for Production

#### **1. HTTPS Only**
```python
from flask_talisman import Talisman

# Force HTTPS
Talisman(app, force_https=True)
```

#### **2. Rate Limiting**
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/command')
@limiter.limit("10 per minute")
def process_api_command():
    pass
```

#### **3. CORS**
```python
from flask_cors import CORS

# Configure CORS for production
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://yourdomain.com"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

---

### 🚀 Quick Deploy Scripts

#### **AWS Deployment Script**
```bash
#!/bin/bash
# deploy-aws.sh
echo "Building Docker image..."
docker build -t vira-assistant .

echo "Pushing to ECR..."
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-west-2.amazonaws.com
docker tag vira-assistant:latest 123456789012.dkr.ecr.us-west-2.amazonaws.com/vira-assistant:latest
docker push 123456789012.dkr.ecr.us-west-2.amazonaws.com/vira-assistant:latest

echo "Deploying to ECS..."
aws ecs update-service --cluster vira-cluster --service vira-service --force-new-deployment
```

#### **Heroku Deployment Script**
```bash
#!/bin/bash
# deploy-heroku.sh
echo "Deploying to Heroku..."
git add .
git commit -m "Deploy to production"
git push heroku main
heroku open
```

---

### 💰 Cost Optimization

#### **1. Serverless Benefits**
- **Pay per use** - No idle costs
- **Auto-scaling** - Handle traffic spikes
- **No maintenance** - Managed infrastructure

#### **2. Container Benefits**
- **Consistent environment** - Docker ensures consistency
- **Easy scaling** - Horizontal scaling
- **Resource control** - CPU/memory limits

#### **3. CDN Integration**
```python
# Serve static files from CDN
app.config['STATIC_URL'] = 'https://cdn.yourdomain.com/static'
```

---

### 📱 Mobile Optimization

#### **1. Progressive Web App**
```json
// manifest.json
{
  "name": "Vira Assistant",
  "short_name": "Vira",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#4facfe"
}
```

#### **2. Service Worker**
```javascript
// sw.js
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open('vira-v1').then(cache => {
            return cache.addAll([
                '/',
                '/static/css/style.css',
                '/static/js/app.js'
            ]);
        })
    );
});
```

Choose your preferred cloud platform and follow the specific deployment instructions!
