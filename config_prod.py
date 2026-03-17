# Production Configuration for Vira Assistant
import os
from app import app

# Production settings
app.config['ENV'] = 'production'
app.config['DEBUG'] = False
app.config['TESTING'] = False

# Security settings
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'production-secret-key-change-me')
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# CORS settings for production
if os.environ.get('ALLOWED_ORIGINS'):
    from flask_cors import CORS
    CORS(app, origins=os.environ.get('ALLOWED_ORIGINS').split(','))

# Rate limiting
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Production logging
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    # File logging
    file_handler = RotatingFileHandler('logs/vira.log', maxBytes=10000000, backupCount=5)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    # Console logging
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    app.logger.addHandler(stream_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Vira Assistant startup')

# Health check endpoint
@app.route('/health')
def health_check():
    from datetime import datetime
    return {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'environment': app.config['ENV']
    }

# Metrics endpoint for monitoring
@app.route('/metrics')
def metrics():
    import json
    try:
        # Get basic metrics
        with open('command_history.json', 'r') as f:
            history = json.load(f)
        
        with open('user_database.json', 'r') as f:
            users = json.load(f)
        
        return {
            'active_users': len(users),
            'commands_today': len([cmd for cmd in history if cmd.get('date') == datetime.now().strftime('%Y-%m-%d')]),
            'total_commands': len(history),
            'uptime': 'uptime_command_here'
        }
    except:
        return {'status': 'metrics_unavailable'}

if __name__ == '__main__':
    # Production server
    import gunicorn
    gunicorn.run(
        app,
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        workers=4,
        worker_class='gevent',
        worker_connections=1000,
        timeout=30,
        keepalive=2,
        max_requests=1000,
        max_requests_jitter=100,
        preload_app=True
    )
