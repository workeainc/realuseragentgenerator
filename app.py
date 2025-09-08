from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import random
import sqlite3
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

def init_analytics_db():
    """Initialize analytics database"""
    conn = sqlite3.connect('analytics.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS page_views (
            id INTEGER PRIMARY KEY,
            ip_address TEXT,
            user_agent TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            referer TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS generations (
            id INTEGER PRIMARY KEY,
            device_type TEXT,
            ip_address TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS copy_actions (
            id INTEGER PRIMARY KEY,
            ip_address TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize analytics database
init_analytics_db()

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

@app.route('/api/track-visit', methods=['POST'])
def track_visit():
    """Track page visits"""
    try:
        conn = sqlite3.connect('analytics.db')
        cursor = conn.cursor()
        
        ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR', 'unknown'))
        user_agent = request.headers.get('User-Agent', 'unknown')
        referer = request.headers.get('Referer', 'direct')
        
        cursor.execute(
            "INSERT INTO page_views (ip_address, user_agent, referer) VALUES (?, ?, ?)",
            (ip_address, user_agent, referer)
        )
        
        conn.commit()
        conn.close()
        
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/track-generation', methods=['POST'])
def track_generation():
    """Track user agent generations"""
    try:
        data = request.get_json()
        device_type = data.get('device_type', 'unknown')
        
        conn = sqlite3.connect('analytics.db')
        cursor = conn.cursor()
        
        ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR', 'unknown'))
        
        cursor.execute(
            "INSERT INTO generations (device_type, ip_address) VALUES (?, ?)",
            (device_type, ip_address)
        )
        
        conn.commit()
        conn.close()
        
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/track-copy', methods=['POST'])
def track_copy():
    """Track copy actions"""
    try:
        conn = sqlite3.connect('analytics.db')
        cursor = conn.cursor()
        
        ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR', 'unknown'))
        
        cursor.execute(
            "INSERT INTO copy_actions (ip_address) VALUES (?)",
            (ip_address,)
        )
        
        conn.commit()
        conn.close()
        
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics')
def get_analytics():
    """Get analytics data"""
    try:
        conn = sqlite3.connect('analytics.db')
        cursor = conn.cursor()
        
        # Get total page views
        total_views = cursor.execute("SELECT COUNT(*) FROM page_views").fetchone()[0]
        
        # Get unique visitors (unique IPs)
        unique_visitors = cursor.execute("SELECT COUNT(DISTINCT ip_address) FROM page_views").fetchone()[0]
        
        # Get total generations
        total_generations = cursor.execute("SELECT COUNT(*) FROM generations").fetchone()[0]
        
        # Get total copy actions
        total_copies = cursor.execute("SELECT COUNT(*) FROM copy_actions").fetchone()[0]
        
        # Get device type breakdown
        device_stats = cursor.execute("""
            SELECT device_type, COUNT(*) as count 
            FROM generations 
            GROUP BY device_type
        """).fetchall()
        
        # Get recent activity (last 24 hours)
        recent_views = cursor.execute("""
            SELECT COUNT(*) FROM page_views 
            WHERE timestamp > datetime('now', '-1 day')
        """).fetchone()[0]
        
        conn.close()
        
        return jsonify({
            'total_views': total_views,
            'unique_visitors': unique_visitors,
            'total_generations': total_generations,
            'total_copies': total_copies,
            'recent_views_24h': recent_views,
            'device_breakdown': dict(device_stats)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)