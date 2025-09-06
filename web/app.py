from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from database import get_db, init_db, AndroidDevice, IOSDevice, ChromeVersion, SafariVersion, GeneratedAgent
import os
import sys
from datetime import datetime
import random
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
CORS(app)

# Initialize rate limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# Initialize database
init_db()

def get_random_device(db, device_type):
    """Get a random device from the database"""
    if device_type == 'android':
        devices = db.query(AndroidDevice).all()
        device = random.choice(devices)
        return {
            'manufacturer': device.manufacturer,
            'model': device.model,
            'android_version': device.android_version
        }
    else:
        devices = db.query(IOSDevice).all()
        device = random.choice(devices)
        return {
            'model': device.model,
            'ios_version': device.ios_version
        }

def get_browser_version(db, browser_type):
    """Get a random browser version"""
    if browser_type == 'chrome':
        versions = db.query(ChromeVersion).all()
        version = random.choice(versions)
        return {
            'version': version.version,
            'build': version.build
        }
    else:
        versions = db.query(SafariVersion).all()
        version = random.choice(versions)
        return {
            'version': version.version,
            'build': version.build
        }

def calculate_entropy_score(ua):
    """Calculate entropy score for a user agent string"""
    score = 0
    total_checks = 0
    
    # Check device and version entropy
    if 'Android' in ua:
        # Various checks for Android UA...
        score += sum([
            'Android' in ua,
            any(mfr in ua for mfr in ['Samsung', 'Google', 'OnePlus', 'Motorola']),
            'Chrome' in ua,
            'Mobile' in ua,
            'Build/' in ua or 'wv' in ua,
            'WebKit' in ua
        ])
        total_checks = 6
    else:
        # Various checks for iOS UA...
        score += sum([
            'iPhone' in ua or 'iPad' in ua,
            'OS' in ua and '_' in ua,
            'Safari' in ua,
            'Mobile' in ua,
            'WebKit' in ua
        ])
        total_checks = 5
    
    # Calculate percentage and add small random variation
    entropy_score = (score / total_checks) * 100
    entropy_score += random.uniform(-2, 2)
    
    # Ensure score stays within bounds
    return max(0, min(100, entropy_score))

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
@limiter.limit("10 per minute")
def generate_ua():
    """Generate a user agent"""
    try:
        data = request.get_json()
        device_type = data.get('device_type', 'both')
        
        if device_type == 'both':
            device_type = 'android' if random.random() < 0.5 else 'ios'
        
        db = next(get_db())
        
        # Generate user agent
        max_attempts = 5
        attempts = 0
        while attempts < max_attempts:
            if device_type == 'android':
                device = get_random_device(db, 'android')
                browser = get_browser_version(db, 'chrome')
                webkit_version = f"537.{random.randint(34,36)}"
                build_id = f"QP{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(100000, 999999)}"
                
                ua = (
                    f"Mozilla/5.0 (Linux; Android {device['android_version']}; "
                    f"{device['manufacturer']} {device['model']}) "
                    f"AppleWebKit/{webkit_version} (KHTML, like Gecko) "
                    f"Chrome/{browser['version']} Mobile Safari/{webkit_version}"
                )
            else:
                device = get_random_device(db, 'ios')
                browser = get_browser_version(db, 'safari')
                webkit_version = "605.1.15"
                
                ua = (
                    f"Mozilla/5.0 (iPhone; CPU iPhone OS {device['ios_version'].replace('.', '_')} like Mac OS X) "
                    f"AppleWebKit/{webkit_version} (KHTML, like Gecko) "
                    f"Version/{browser['version']} Mobile/15E148 Safari/{browser['version']}"
                )
            
            entropy_score = calculate_entropy_score(ua)
            if entropy_score >= 90:
                break
            attempts += 1
        
        # Save the generated UA
        generated = GeneratedAgent(
            user_agent=ua,
            device_type=device_type,
            created_at=datetime.utcnow()
        )
        db.add(generated)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
        
        return jsonify({
            'user_agent': ua,
            'entropy_score': round(entropy_score, 1),
            'device_type': device_type
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats')
def get_stats():
    """Get generation statistics"""
    try:
        db = next(get_db())
        android_count = db.query(GeneratedAgent).filter_by(device_type='android').count()
        ios_count = db.query(GeneratedAgent).filter_by(device_type='ios').count()
        
        return jsonify({
            'android': android_count,
            'ios': ios_count
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)