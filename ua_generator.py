#!/usr/bin/env python3
import sqlite3
import click
import random
import json
import re
from faker import Faker
from tqdm import tqdm
from datetime import datetime
import os

class UserAgentGenerator:
    def __init__(self, db_path='useragents.db'):
        self.db_path = db_path
        self.fake = Faker('en_US')
        self.setup_database()
        
    def setup_database(self):
        """Initialize SQLite database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables for devices and user agents
        cursor.executescript('''
            CREATE TABLE IF NOT EXISTS android_devices (
                id INTEGER PRIMARY KEY,
                manufacturer TEXT,
                model TEXT,
                android_version TEXT
            );
            
            CREATE TABLE IF NOT EXISTS ios_devices (
                id INTEGER PRIMARY KEY,
                model TEXT,
                ios_version TEXT
            );
            
            CREATE TABLE IF NOT EXISTS chrome_versions (
                id INTEGER PRIMARY KEY,
                version TEXT,
                build TEXT
            );
            
            CREATE TABLE IF NOT EXISTS safari_versions (
                id INTEGER PRIMARY KEY,
                version TEXT,
                build TEXT
            );
            
            CREATE TABLE IF NOT EXISTS generated_agents (
                id INTEGER PRIMARY KEY,
                user_agent TEXT UNIQUE,
                device_type TEXT,
                created_at TIMESTAMP
            );
        ''')
        
        # Populate initial data if tables are empty
        if not cursor.execute("SELECT 1 FROM android_devices LIMIT 1").fetchone():
            self._populate_android_data(cursor)
        
        if not cursor.execute("SELECT 1 FROM ios_devices LIMIT 1").fetchone():
            self._populate_ios_data(cursor)
            
        if not cursor.execute("SELECT 1 FROM chrome_versions LIMIT 1").fetchone():
            self._populate_chrome_versions(cursor)
            
        if not cursor.execute("SELECT 1 FROM safari_versions LIMIT 1").fetchone():
            self._populate_safari_versions(cursor)
        
        conn.commit()
        conn.close()

    def _populate_android_data(self, cursor):
        """Populate Android device data"""
        android_devices = [
            # Samsung Latest Devices
            ('Samsung', 'Galaxy S24 Ultra', '14.0'),
            ('Samsung', 'Galaxy S24+ 5G', '14.0'),
            ('Samsung', 'Galaxy S24 5G', '14.0'),
            ('Samsung', 'Galaxy S23 Ultra', '14.0'),
            ('Samsung', 'Galaxy S23+ 5G', '14.0'),
            ('Samsung', 'Galaxy S23 5G', '14.0'),
            ('Samsung', 'Galaxy Z Fold5 5G', '14.0'),
            ('Samsung', 'Galaxy Z Flip5 5G', '14.0'),
            ('Samsung', 'Galaxy S23 FE 5G', '14.0'),
            
            # Samsung A Series
            ('Samsung', 'Galaxy A54 5G', '14.0'),
            ('Samsung', 'Galaxy A53 5G', '13.0'),
            ('Samsung', 'Galaxy A34 5G', '14.0'),
            ('Samsung', 'Galaxy A25 5G', '14.0'),
            ('Samsung', 'Galaxy A15 5G', '14.0'),
            
            # Samsung Tablets
            ('Samsung', 'Galaxy Tab S9 Ultra', '14.0'),
            ('Samsung', 'Galaxy Tab S9+', '14.0'),
            ('Samsung', 'Galaxy Tab S9', '14.0'),
            ('Samsung', 'Galaxy Tab S9 FE+', '14.0'),
            ('Samsung', 'Galaxy Tab S9 FE', '14.0'),
            
            # Google Devices
            ('Google', 'Pixel 8 Pro', '14.0'),
            ('Google', 'Pixel 8', '14.0'),
            ('Google', 'Pixel 7a', '14.0'),
            ('Google', 'Pixel 7 Pro', '14.0'),
            ('Google', 'Pixel 7', '14.0'),
            ('Google', 'Pixel Fold', '14.0'),
            ('Google', 'Pixel Tablet', '14.0'),
            ('Google', 'Pixel 6a', '14.0'),
            
            # OnePlus Devices
            ('OnePlus', '12', '14.0'),
            ('OnePlus', '12R', '14.0'),
            ('OnePlus', '11 5G', '14.0'),
            ('OnePlus', '10T 5G', '14.0'),
            ('OnePlus', '10 Pro', '14.0'),
            ('OnePlus', 'Nord N30 5G', '13.0'),
            ('OnePlus', 'Nord N20 5G', '13.0'),
            
            # Motorola Latest
            ('Motorola', 'Edge+ 2023', '14.0'),
            ('Motorola', 'Edge 2023', '14.0'),
            ('Motorola', 'Razr+ 2023', '14.0'),
            ('Motorola', 'Razr 2023', '14.0'),
            ('Motorola', 'Edge 40 Pro', '14.0'),
            ('Motorola', 'Edge 40 Neo', '14.0'),
            
            # Motorola G Series
            ('Motorola', 'Moto G Stylus 5G 2024', '14.0'),
            ('Motorola', 'Moto G Power 5G 2024', '14.0'),
            ('Motorola', 'Moto G 5G 2024', '14.0'),
            
            # Nothing Devices
            ('Nothing', 'Phone (2a)', '14.0'),
            ('Nothing', 'Phone (2)', '14.0'),
            ('Nothing', 'Phone (1)', '14.0'),
            
            # ASUS Gaming/Premium
            ('ASUS', 'ROG Phone 8 Pro', '14.0'),
            ('ASUS', 'ROG Phone 8', '14.0'),
            ('ASUS', 'Zenfone 10', '14.0'),
            ('ASUS', 'ROG Phone 7 Ultimate', '14.0'),
            
            # Sony Premium
            ('Sony', 'Xperia 1 V', '14.0'),
            ('Sony', 'Xperia 5 V', '14.0'),
            ('Sony', 'Xperia 10 V', '14.0'),
            
            # OPPO Premium (US Models)
            ('OPPO', 'Find X7 Ultra', '14.0'),
            ('OPPO', 'Find X7 Pro', '14.0'),
            ('OPPO', 'Find X7', '14.0'),
            
            # Xiaomi Premium (US Models)
            ('Xiaomi', '14 Ultra', '14.0'),
            ('Xiaomi', '14 Pro', '14.0'),
            ('Xiaomi', '14', '14.0'),
            
            # Other Major USA Carriers' Devices
            ('TCL', '50 XE 5G', '14.0'),
            ('TCL', '50 XL 5G', '14.0'),
            ('TCL', '50 LE 5G', '14.0')
        ]
        cursor.executemany(
            "INSERT INTO android_devices (manufacturer, model, android_version) VALUES (?, ?, ?)",
            android_devices
        )

    def _populate_ios_data(self, cursor):
        """Populate iOS device data"""
        ios_devices = [
            # iPhone 15 Series
            ('iPhone 15 Pro Max', '17.3.1'),
            ('iPhone 15 Pro Max', '17.3'),
            ('iPhone 15 Pro Max', '17.2.1'),
            ('iPhone 15 Pro', '17.3.1'),
            ('iPhone 15 Pro', '17.3'),
            ('iPhone 15 Pro', '17.2.1'),
            ('iPhone 15 Plus', '17.3.1'),
            ('iPhone 15 Plus', '17.3'),
            ('iPhone 15 Plus', '17.2.1'),
            ('iPhone 15', '17.3.1'),
            ('iPhone 15', '17.3'),
            ('iPhone 15', '17.2.1'),
            
            # iPhone 14 Series
            ('iPhone 14 Pro Max', '17.3.1'),
            ('iPhone 14 Pro Max', '17.2.1'),
            ('iPhone 14 Pro Max', '16.7.2'),
            ('iPhone 14 Pro', '17.3.1'),
            ('iPhone 14 Pro', '17.2.1'),
            ('iPhone 14 Pro', '16.7.2'),
            ('iPhone 14 Plus', '17.3.1'),
            ('iPhone 14 Plus', '17.2.1'),
            ('iPhone 14 Plus', '16.7.2'),
            ('iPhone 14', '17.3.1'),
            ('iPhone 14', '17.2.1'),
            ('iPhone 14', '16.7.2'),
            
            # iPhone 13 Series
            ('iPhone 13 Pro Max', '17.3.1'),
            ('iPhone 13 Pro Max', '17.2.1'),
            ('iPhone 13 Pro Max', '16.7.2'),
            ('iPhone 13 Pro', '17.3.1'),
            ('iPhone 13 Pro', '17.2.1'),
            ('iPhone 13 Pro', '16.7.2'),
            ('iPhone 13', '17.3.1'),
            ('iPhone 13', '17.2.1'),
            ('iPhone 13', '16.7.2'),
            ('iPhone 13 mini', '17.3.1'),
            ('iPhone 13 mini', '17.2.1'),
            ('iPhone 13 mini', '16.7.2'),
            
            # iPhone 12 Series
            ('iPhone 12 Pro Max', '17.3.1'),
            ('iPhone 12 Pro Max', '16.7.2'),
            ('iPhone 12 Pro', '17.3.1'),
            ('iPhone 12 Pro', '16.7.2'),
            ('iPhone 12', '17.3.1'),
            ('iPhone 12', '16.7.2'),
            ('iPhone 12 mini', '17.3.1'),
            ('iPhone 12 mini', '16.7.2'),
            
            # iPad Pro Models
            ('iPad Pro (12.9-inch) (6th generation)', '17.3.1'),
            ('iPad Pro (12.9-inch) (6th generation)', '17.2.1'),
            ('iPad Pro (11-inch) (4th generation)', '17.3.1'),
            ('iPad Pro (11-inch) (4th generation)', '17.2.1'),
            
            # iPad Air Models
            ('iPad Air (5th generation)', '17.3.1'),
            ('iPad Air (5th generation)', '17.2.1'),
            
            # iPad Mini Models
            ('iPad mini (6th generation)', '17.3.1'),
            ('iPad mini (6th generation)', '17.2.1')
        ]
        cursor.executemany(
            "INSERT INTO ios_devices (model, ios_version) VALUES (?, ?)",
            ios_devices
        )

    def _populate_chrome_versions(self, cursor):
        """Populate Chrome browser versions"""
        chrome_versions = [
            # Latest Chrome versions
            ('121.0.6167.85', '6167.85'),
            ('121.0.6167.78', '6167.78'),
            ('121.0.6167.71', '6167.71'),
            ('121.0.6167.65', '6167.65'),
            ('121.0.6167.59', '6167.59'),
            
            # Chrome 120 versions
            ('120.0.6099.230', '6099.230'),
            ('120.0.6099.224', '6099.224'),
            ('120.0.6099.216', '6099.216'),
            ('120.0.6099.210', '6099.210'),
            ('120.0.6099.200', '6099.200'),
            ('120.0.6099.195', '6099.195'),
            ('120.0.6099.180', '6099.180'),
            ('120.0.6099.175', '6099.175'),
            ('120.0.6099.155', '6099.155'),
            
            # Chrome 119 versions
            ('119.0.6045.200', '6045.200'),
            ('119.0.6045.195', '6045.195'),
            ('119.0.6045.190', '6045.190'),
            ('119.0.6045.185', '6045.185'),
            ('119.0.6045.180', '6045.180'),
            
            # Chrome 118 versions (for older Android devices)
            ('118.0.5993.175', '5993.175'),
            ('118.0.5993.170', '5993.170'),
            ('118.0.5993.165', '5993.165')
        ]
        cursor.executemany(
            "INSERT INTO chrome_versions (version, build) VALUES (?, ?)",
            chrome_versions
        )

    def _populate_safari_versions(self, cursor):
        """Populate Safari browser versions"""
        safari_versions = [
            # Latest Safari versions
            ('17.3.1', '17617.3.1.11.12'),
            ('17.3', '17617.3.0.11.12'),
            ('17.2.1', '17617.2.4.11.12'),
            ('17.2', '17617.2.3.11.12'),
            ('17.1.2', '17617.1.17.11.13'),
            ('17.1.1', '17617.1.17.11.12'),
            ('17.1', '17617.1.17.11.11'),
            ('17.0.1', '17617.1.17.11.10'),
            ('17.0', '17617.1.17.11.9'),
            
            # Safari 16 versions (for older devices)
            ('16.6.1', '16616.4.9.1.13'),
            ('16.6', '16616.4.9.1.12'),
            ('16.5.2', '16615.3.12.11.2'),
            ('16.5.1', '16615.3.12.11.1'),
            ('16.5', '16615.3.12.11.0'),
            ('16.4.1', '16614.3.7.11.3'),
            ('16.4', '16614.3.7.11.2'),
            
            # iPad-specific versions
            ('17.3.1', '17617.3.1.11.12.1'),
            ('17.3', '17617.3.0.11.12.1'),
            ('17.2.1', '17617.2.4.11.12.1'),
            ('17.2', '17617.2.3.11.12.1'),
            ('17.1', '17617.1.17.11.12.1')
        ]
        cursor.executemany(
            "INSERT INTO safari_versions (version, build) VALUES (?, ?)",
            safari_versions
        )

    def calculate_entropy_score(self, ua):
        """Calculate entropy score for a user agent string"""
        score = 0
        total_checks = 0
        
        # Check device and version entropy
        if 'Android' in ua:
            # Check Android version format
            if re.search(r'Android \d+\.\d+', ua):
                score += 1
            total_checks += 1
            
            # Check device manufacturer presence
            manufacturers = ['Samsung', 'Google', 'OnePlus', 'Motorola', 'Nothing', 'ASUS', 'Sony', 'TCL']
            if any(mfr in ua for mfr in manufacturers):
                score += 1
            total_checks += 1
            
            # Check Chrome version format
            if re.search(r'Chrome/\d+\.\d+\.\d+\.\d+', ua):
                score += 1
            total_checks += 1
            
            # Check build tag entropy
            if re.search(r'Build/[A-Z]{2}[A-Z0-9]\d{6}', ua):
                score += 1
            total_checks += 1
            
            # Check WebKit version variation
            if re.search(r'WebKit/537\.(34|35|36)', ua):
                score += 1
            total_checks += 1
            
            # Check for additional tags
            if any(tag in ua for tag in ['wv', 'EdgA', 'GoogleApp', 'Mobile Safari']):
                score += 1
            total_checks += 1
            
        else:  # iOS
            # Check iOS version format
            if re.search(r'OS \d+_\d+(_\d+)? like Mac OS X', ua):
                score += 1
            total_checks += 1
            
            # Check device type
            if any(device in ua for device in ['iPhone', 'iPad']):
                score += 1
            total_checks += 1
            
            # Check Safari/WebKit version
            if re.search(r'Version/\d+\.\d+(\.\d+)?', ua):
                score += 1
            total_checks += 1
            
            # Check Mobile version code
            if re.search(r'Mobile/[0-9A-Z]+', ua):
                score += 1
            total_checks += 1
            
            # Check for variations
            if any(var in ua for var in ['CriOS', 'FxiOS', 'EdgiOS', 'GSA']):
                score += 1
            total_checks += 1
            
            # Check WebKit version
            if re.search(r'WebKit/60[0-9]\.\d+\.\d+', ua):
                score += 1
            total_checks += 1
        
        # Calculate percentage
        entropy_score = (score / total_checks) * 100
        
        # Add randomization factor (±2%) to prevent pattern detection
        entropy_score += random.uniform(-2, 2)
        
        # Ensure score stays within 0-100 range
        entropy_score = max(0, min(100, entropy_score))
        
        return round(entropy_score, 1)

    def save_generated_ua(self, ua, device_type):
        """Save generated user agent to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO generated_agents (user_agent, device_type, created_at) VALUES (?, ?, ?)",
                (ua, device_type, datetime.now().isoformat())
            )
            conn.commit()
        except sqlite3.IntegrityError:
            # Skip if duplicate
            pass
        finally:
            conn.close()

    def generate_batch(self, count, device_type='both'):
        """Generate a batch of user agents"""
        user_agents = []
        
        with tqdm(total=count, desc="Generating User Agents") as pbar:
            while len(user_agents) < count:
                if device_type == 'android':
                    ua = self.generate_android_ua()
                elif device_type == 'ios':
                    ua = self.generate_ios_ua()
                else:
                    ua = self.generate_android_ua() if random.random() < 0.5 else self.generate_ios_ua()
                
                # Add entropy by slightly modifying the user agent
                if random.random() < 0.1:  # 10% chance to add minor variations
                    ua = ua.replace("Mobile", "Mobile Safari")
                
                if ua not in user_agents:
                    user_agents.append(ua)
                    self.save_generated_ua(ua, 'android' if 'Android' in ua else 'ios')
                    pbar.update(1)
        
        return user_agents

    def generate_android_ua(self):
        """Generate Android user agent with entropy"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get device with weighted probability (newer devices more likely)
        device = cursor.execute("""
            WITH RECURSIVE
            cnt(x) AS (
                SELECT 1
                UNION ALL
                SELECT x+1 FROM cnt LIMIT 100
            ),
            weighted_devices AS (
                SELECT d.*, 
                    CASE 
                        WHEN android_version = '14.0' THEN x % 3 + 3
                        WHEN android_version = '13.0' THEN x % 2 + 1
                        ELSE 1
                    END as weight
                FROM android_devices d
                CROSS JOIN cnt
            )
            SELECT manufacturer, model, android_version
            FROM weighted_devices
            ORDER BY RANDOM()
            LIMIT 1
        """).fetchone()
        
        # Get Chrome version with weighted probability (newer versions more likely)
        chrome_version = cursor.execute("""
            WITH RECURSIVE
            cnt(x) AS (
                SELECT 1
                UNION ALL
                SELECT x+1 FROM cnt LIMIT 100
            ),
            weighted_versions AS (
                SELECT v.*, 
                    CASE 
                        WHEN version LIKE '121%' THEN x % 4 + 4
                        WHEN version LIKE '120%' THEN x % 3 + 2
                        WHEN version LIKE '119%' THEN x % 2 + 1
                        ELSE 1
                    END as weight
                FROM chrome_versions v
                CROSS JOIN cnt
            )
            SELECT version, build
            FROM weighted_versions
            ORDER BY RANDOM()
            LIMIT 1
        """).fetchone()
        
        conn.close()
        
        # Generate realistic build ID
        build_prefixes = ['QP', 'RP', 'SP', 'TP']
        build_id = f"{random.choice(build_prefixes)}{self.fake.random_letter()}{self.fake.random_number(6)}"
        
        # Add entropy to the WebKit version
        webkit_version = f"537.{random.randint(34,36)}"
        
        # Randomly add build tags
        build_tags = [
            f"wv",  # WebView
            f"Build/{build_id}",
            f"{build_id}",
            ""  # No build tag
        ]
        build_tag = random.choice(build_tags)
        
        # Base UA string
        ua = (
            f"Mozilla/5.0 (Linux; Android {device[2]}; "
            f"{device[0]} {device[1]}"
        )
        
        # Add build tag if selected
        if build_tag:
            ua += f"; {build_tag}"
        
        # Complete UA string
        ua += (
            f") AppleWebKit/{webkit_version} (KHTML, like Gecko) "
            f"Chrome/{chrome_version[0]} Mobile Safari/{webkit_version}"
        )
        
        # Sometimes add additional tags
        if random.random() < 0.1:  # 10% chance
            additional_tags = [
                " EdgA/1.0",
                " GoogleApp/13.47.8.23",
                " Chrome/96.0.4664.104 Mobile Safari/537.36",
                " Mobile"
            ]
            ua += random.choice(additional_tags)
        
        return ua

    def generate_ios_ua(self):
        """Generate iOS user agent with entropy"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get device with weighted probability (newer devices more likely)
        device = cursor.execute("""
            WITH RECURSIVE
            cnt(x) AS (
                SELECT 1
                UNION ALL
                SELECT x+1 FROM cnt LIMIT 100
            ),
            weighted_devices AS (
                SELECT d.*, 
                    CASE 
                        WHEN ios_version LIKE '17.3%' THEN x % 4 + 4
                        WHEN ios_version LIKE '17.2%' THEN x % 3 + 3
                        WHEN ios_version LIKE '17.1%' THEN x % 2 + 2
                        WHEN ios_version LIKE '17.0%' THEN x % 2 + 1
                        ELSE 1
                    END as weight
                FROM ios_devices d
                CROSS JOIN cnt
            )
            SELECT model, ios_version
            FROM weighted_devices
            ORDER BY RANDOM()
            LIMIT 1
        """).fetchone()
        
        # Get Safari version with weighted probability (newer versions more likely)
        safari_version = cursor.execute("""
            WITH RECURSIVE
            cnt(x) AS (
                SELECT 1
                UNION ALL
                SELECT x+1 FROM cnt LIMIT 100
            ),
            weighted_versions AS (
                SELECT v.*, 
                    CASE 
                        WHEN version LIKE '17.3%' THEN x % 4 + 4
                        WHEN version LIKE '17.2%' THEN x % 3 + 3
                        WHEN version LIKE '17.1%' THEN x % 2 + 2
                        ELSE 1
                    END as weight
                FROM safari_versions v
                CROSS JOIN cnt
            )
            SELECT version, build
            FROM weighted_versions
            ORDER BY RANDOM()
            LIMIT 1
        """).fetchone()
        
        conn.close()
        
        # Generate realistic mobile version
        mobile_versions = ['15E148', '15E148a', '15F79', '15G77', '17A844', '17B111', '17C54', '17D50']
        mobile_version = random.choice(mobile_versions)
        
        # Add entropy to the WebKit version
        webkit_versions = ['605.1.15', '605.2.15', '605.3.8', '605.4.6', '605.5.4']
        webkit_version = random.choice(webkit_versions)
        
        # Base UA components
        device_type = 'iPhone' if 'iPhone' in device[0] else 'iPad'
        cpu_type = 'iPhone' if device_type == 'iPhone' else 'iPad'
        os_version = device[1].replace('.', '_')
        
        # Construct UA with variations
        ua_base = f"Mozilla/5.0 ({device_type}; CPU {cpu_type} OS {os_version} like Mac OS X)"
        
        # Add WebKit with entropy
        ua = f"{ua_base} AppleWebKit/{webkit_version} (KHTML, like Gecko)"
        
        # Different UA patterns
        ua_patterns = [
            # Standard Safari
            f"{ua} Version/{safari_version[0]} Mobile/{mobile_version} Safari/{safari_version[0]}",
            
            # Safari with additional info
            f"{ua} Version/{safari_version[0]} Mobile/{mobile_version} Safari/{safari_version[0]} {device_type}/20C65",
            
            # App-specific (low probability)
            f"{ua} {self.fake.random_element(elements=('GSA','FxiOS','EdgiOS'))}/{random.randint(100, 371)}.0.{random.randint(1, 99)} Mobile/{mobile_version} Safari/{safari_version[0]}",
            
            # Chrome iOS (low probability)
            f"{ua} CriOS/{random.randint(90, 120)}.0.{random.randint(4000, 6000)}.{random.randint(80, 200)} Mobile/{mobile_version} Safari/{safari_version[0]}"
        ]
        
        # Weight the patterns (standard Safari should be most common)
        weights = [0.7, 0.2, 0.05, 0.05]
        ua = random.choices(ua_patterns, weights=weights)[0]
        
        return ua

@click.group()
def cli():
    """User Agent Generator CLI"""
    pass

@cli.command()
@click.option('--count', '-c', default=100, help='Number of user agents to generate')
@click.option('--device', '-d', type=click.Choice(['android', 'ios', 'both']), default='both',
              help='Device type to generate user agents for')
@click.option('--output', '-o', type=click.Path(), help='Output file path (JSON format)')
def generate(count, device, output):
    """Generate user agents"""
    generator = UserAgentGenerator()
    user_agents = generator.generate_batch(count, device)
    
    if output:
        with open(output, 'w') as f:
            json.dump(user_agents, f, indent=2)
        click.echo(f"Generated {len(user_agents)} user agents and saved to {output}")
    else:
        click.echo("\nGenerated User Agents:")
        for ua in user_agents:
            click.echo(ua)
            click.echo("-" * 80)

@cli.command()
@click.option('--device', '-d', type=click.Choice(['android', 'ios', 'both']), default='both',
              help='Device type to show statistics for')
def stats(device):
    """Show statistics about generated user agents"""
    generator = UserAgentGenerator()
    conn = sqlite3.connect(generator.db_path)
    cursor = conn.cursor()
    
    if device == 'both':
        result = cursor.execute("""
            SELECT device_type, COUNT(*) as count,
                   MIN(created_at) as first_generated,
                   MAX(created_at) as last_generated
            FROM generated_agents
            GROUP BY device_type
        """).fetchall()
    else:
        result = cursor.execute("""
            SELECT device_type, COUNT(*) as count,
                   MIN(created_at) as first_generated,
                   MAX(created_at) as last_generated
            FROM generated_agents
            WHERE device_type = ?
            GROUP BY device_type
        """, (device,)).fetchall()
    
    conn.close()
    
    click.echo("\nUser Agent Statistics:")
    for row in result:
        click.echo(f"\nDevice Type: {row[0]}")
        click.echo(f"Total Generated: {row[1]}")
        click.echo(f"First Generated: {row[2]}")
        click.echo(f"Last Generated: {row[3]}")

if __name__ == '__main__':
    cli()