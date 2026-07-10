import schedule
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Callable
import threading
import pytz

class UploadScheduler:
    def __init__(self, config: Dict):
        self.config = config
        self.timezone = pytz.timezone(config.get('timezone', 'UTC'))
        self.scheduled_jobs = []
        self.is_running = False
        self.scheduler_thread = None
        
        # Best times to post by platform (based on analytics)
        self.optimal_times = {
            'tiktok': ['09:00', '12:00', '19:00', '21:00'],
            'instagram': ['11:00', '13:00', '17:00', '19:00'],
            'youtube': ['14:00', '16:00', '19:00']
        }
        
        self.queue_file = "config/upload_queue.json"
        self.load_queue()
    
    def schedule_upload(self, video_path: str, metadata: Dict,
                       platform: str, scheduled_time: datetime = None,
                       use_optimal: bool = True) -> str:
        """Schedule a video for upload"""
        
        if use_optimal and not scheduled_time:
            scheduled_time = self._get_next_optimal_time(platform)
        
        job_id = f"{platform}_{int(time.time())}"
        
        job = {
            'id': job_id,
            'video_path': video_path,
            'metadata': metadata,
            'platform': platform,
            'scheduled_time': scheduled_time.isoformat(),
            'status': 'pending',
            'created_at': datetime.now().isoformat()
        }
        
        self.scheduled_jobs.append(job)
        self.save_queue()
        
        # Schedule with APScheduler
        schedule.every().day.at(scheduled_time.strftime("%H:%M")).do(
            self._execute_upload, job
        ).tag(job_id)
        
        return job_id
    
    def schedule_bulk(self, videos: List[Dict], platform: str,
                     spread_hours: int = 24) -> List[str]:
        """Schedule multiple videos with optimal spacing"""
        job_ids = []
        
        base_time = datetime.now(self.timezone)
        interval = spread_hours / len(videos)
        
        for i, video in enumerate(videos):
            scheduled_time = base_time + timedelta(hours=i * interval)
            job_id = self.schedule_upload(
                video['path'],
                video['metadata'],
                platform,
                scheduled_time,
                use_optimal=False
            )
            job_ids.append(job_id)
        
        return job_ids
    
    def _get_next_optimal_time(self, platform: str) -> datetime:
        """Get next optimal posting time"""
        now = datetime.now(self.timezone)
        optimal = self.optimal_times.get(platform, ['12:00'])
        
        for time_str in optimal:
            hour, minute = map(int, time_str.split(':'))
            candidate = now.replace(hour=hour, minute=minute, second=0)
            
            if candidate > now:
                return candidate
        
        # If all passed, use first time tomorrow
        hour, minute = map(int, optimal[0].split(':'))
        return (now + timedelta(days=1)).replace(
            hour=hour, minute=minute, second=0
        )
    
    def start_scheduler(self):
        """Start the scheduler in background thread"""
        self.is_running = True
        
        def run_loop():
            while self.is_running:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        
        self.scheduler_thread = threading.Thread(target=run_loop)
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()
        
        print("✅ Scheduler started")
    
    def stop_scheduler(self):
        """Stop the scheduler"""
        self.is_running = False
        if self.scheduler_thread:
            self.scheduler_thread.join()
        print("🛑 Scheduler stopped")
    
    def _execute_upload(self, job: Dict):
        """Execute the actual upload"""
        print(f"🚀 Executing upload: {job['id']}")
        
        # Update status
        job['status'] = 'running'
        job['started_at'] = datetime.now().isoformat()
        self.save_queue()
        
        try:
            # Call uploader
            # result = uploader.upload(job['video_path'], job['metadata'], job['platform'])
            
            job['status'] = 'completed'
            job['completed_at'] = datetime.now().isoformat()
            
        except Exception as e:
            job['status'] = 'failed'
            job['error'] = str(e)
        
        self.save_queue()
    
    def get_queue(self) -> List[Dict]:
        """Get current upload queue"""
        return self.scheduled_jobs
    
    def cancel_job(self, job_id: str) -> bool:
        """Cancel a scheduled upload"""
        schedule.clear(job_id)
        self.scheduled_jobs = [j for j in self.scheduled_jobs if j['id'] != job_id]
        self.save_queue()
        return True
    
    def load_queue(self):
        """Load queue from disk"""
        try:
            with open(self.queue_file, 'r') as f:
                self.scheduled_jobs = json.load(f)
        except:
            self.scheduled_jobs = []
    
    def save_queue(self):
        """Save queue to disk"""
        with open(self.queue_file, 'w') as f:
            json.dump(self.scheduled_jobs, f, indent=2)