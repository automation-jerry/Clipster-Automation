import sqlite3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pandas as pd
import plotly.express as px

class PerformanceTracker:
    def __init__(self, db_path: str = "logs/analytics.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize analytics database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS uploads (
                id TEXT PRIMARY KEY,
                video_path TEXT,
                platform TEXT,
                campaign_id TEXT,
                uploaded_at TIMESTAMP,
                status TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                upload_id TEXT,
                timestamp TIMESTAMP,
                views INTEGER,
                likes INTEGER,
                comments INTEGER,
                shares INTEGER,
                FOREIGN KEY (upload_id) REFERENCES uploads(id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS earnings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                upload_id TEXT,
                platform TEXT,
                amount DECIMAL(10,2),
                currency TEXT,
                recorded_at TIMESTAMP,
                FOREIGN KEY (upload_id) REFERENCES uploads(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def log_upload(self, upload_id: str, video_path: str,
                   platform: str, campaign_id: str):
        """Log new upload"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO uploads (id, video_path, platform, campaign_id, uploaded_at, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (upload_id, video_path, platform, campaign_id, 
              datetime.now(), 'active'))
        
        conn.commit()
        conn.close()
    
    def update_metrics(self, upload_id: str, metrics: Dict):
        """Update performance metrics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO metrics (upload_id, timestamp, views, likes, comments, shares)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (upload_id, datetime.now(), metrics.get('views', 0),
              metrics.get('likes', 0), metrics.get('comments', 0),
              metrics.get('shares', 0)))
        
        conn.commit()
        conn.close()
    
    def log_earnings(self, upload_id: str, platform: str, 
                     amount: float, currency: str = "USD"):
        """Log earnings"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO earnings (upload_id, platform, amount, currency, recorded_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (upload_id, platform, amount, currency, datetime.now()))
        
        conn.commit()
        conn.close()
    
    def get_performance_report(self, days: int = 30) -> Dict:
        """Generate performance report"""
        conn = sqlite3.connect(self.db_path)
        
        # Get uploads in period
        query = '''
            SELECT u.*, 
                   SUM(m.views) as total_views,
                   SUM(m.likes) as total_likes,
                   SUM(e.amount) as total_earnings
            FROM uploads u
            LEFT JOIN metrics m ON u.id = m.upload_id
            LEFT JOIN earnings e ON u.id = e.upload_id
            WHERE u.uploaded_at >= ?
            GROUP BY u.id
        '''
        
        since = datetime.now() - timedelta(days=days)
        df = pd.read_sql_query(query, conn, params=(since,))
        
        report = {
            'period_days': days,
            'total_uploads': len(df),
            'total_views': df['total_views'].sum() if 'total_views' in df else 0,
            'total_likes': df['total_likes'].sum() if 'total_likes' in df else 0,
            'total_earnings': df['total_earnings'].sum() if 'total_earnings' in df else 0,
            'by_platform': df.groupby('platform').agg({
                'total_views': 'sum',
                'total_earnings': 'sum'
            }).to_dict() if len(df) > 0 else {},
            'best_performing': df.nlargest(5, 'total_views')[['video_path', 'total_views', 'total_earnings']].to_dict('records') if len(df) > 0 else []
        }
        
        conn.close()
        return report
    
    def create_dashboard_charts(self) -> Dict:
        """Create Plotly charts for dashboard"""
        conn = sqlite3.connect(self.db_path)
        
        # Views over time
        df = pd.read_sql_query('''
            SELECT date(timestamp) as date, SUM(views) as views
            FROM metrics
            GROUP BY date(timestamp)
            ORDER BY date
        ''', conn)
        
        views_chart = px.line(df, x='date', y='views', 
                             title='Views Over Time') if len(df) > 0 else None
        
        # Earnings by platform
        earnings_df = pd.read_sql_query('''
            SELECT platform, SUM(amount) as earnings
            FROM earnings
            GROUP BY platform
        ''', conn)
        
        earnings_chart = px.pie(earnings_df, values='earnings', 
                               names='platform',
                               title='Earnings by Platform') if len(earnings_df) > 0 else None
        
        conn.close()
        
        return {
            'views_chart': views_chart,
            'earnings_chart': earnings_chart
        }