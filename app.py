from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import random
from datetime import datetime
from ua_generator import UserAgentGenerator

app = Flask(__name__)
CORS(app)

# Initialize rate limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# Initialize the UA generator
generator = UserAgentGenerator()

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
        
        # Generate user agent until we get one with high entropy
        max_attempts = 5
        attempts = 0
        while attempts < max_attempts:
            if device_type == 'android':
                ua = generator.generate_android_ua()
            elif device_type == 'ios':
                ua = generator.generate_ios_ua()
            else:
                ua = generator.generate_android_ua() if random.random() < 0.5 else generator.generate_ios_ua()
            
            entropy_score = generator.calculate_entropy_score(ua)
            if entropy_score >= 90:
                break
            attempts += 1
        
        # Save the generated UA
        generator.save_generated_ua(ua, 'android' if 'Android' in ua else 'ios')
        
        return jsonify({
            'user_agent': ua,
            'entropy_score': entropy_score,
            'device_type': 'android' if 'Android' in ua else 'ios'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats')
def get_stats():
    """Get generation statistics"""
    try:
        import sqlite3
        conn = sqlite3.connect(generator.db_path)
        cursor = conn.cursor()
        
        stats = cursor.execute("""
            SELECT device_type, COUNT(*) as count
            FROM generated_agents
            GROUP BY device_type
        """).fetchall()
        
        conn.close()
        
        return jsonify({
            'android': next((count for type_, count in stats if type_ == 'android'), 0),
            'ios': next((count for type_, count in stats if type_ == 'ios'), 0)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)