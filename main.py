#!/usr/bin/env python3
"""
CLIPSTER GOD MODE - Complete Automation System
Usage: python main.py [command] [options]
"""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Dict

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.config_manager import ConfigManager
from ai.ai_editor import AIVideoEditor
from ai.content_generator import AIContentGenerator
from upload.uploader import SocialUploader
from upload.scheduler import UploadScheduler
from analytics.performance_tracker import PerformanceTracker
from core.logger import setup_logger

# Setup logging
logger = setup_logger("clipster_god_mode")

def banner():
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║   ██████╗██╗     ██╗██████╗ ███████╗████████╗███████╗██████╗    ║
    ║  ██╔════╝██║     ██║██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗   ║
    ║  ██║     ██║     ██║██████╔╝███████╗   ██║   █████╗  ██████╔╝   ║
    ║  ██║     ██║     ██║██╔═══╝ ╚════██║   ██║   ██╔══╝  ██╔══██╗   ║
    ║  ╚██████╗███████╗██║██║     ███████║   ██║   ███████╗██║  ██║   ║
    ║   ╚═════╝╚══════╝╚═╝╚═╝     ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝   ║
    ║                                                                  ║
    ║              🤖 GOD MODE ACTIVATED v2.0 🤖                       ║
    ║         Auto-Edit → Auto-Upload → Auto-Profit                    ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)

async def process_campaign(campaign_file: str, auto_upload: bool = True):
    """Process a campaign with full AI automation"""
    
    logger.info(f"Processing campaign: {campaign_file}")
    
    # Load configs
    cm = ConfigManager()
    config = cm.load_all()
    
    # Initialize components
    ai_editor = AIVideoEditor(config)
    content_gen = AIContentGenerator(config)
    uploader = SocialUploader(config)
    tracker = PerformanceTracker()
    
    # Load campaign
    with open(campaign_file, 'r') as f:
        campaign = json.load(f)
    
    print(f"\n🎯 Campaign: {campaign['name']}")
    print(f"   Brand: {campaign['brand']}")
    print(f"   AI Editing: ENABLED")
    print(f"   Auto-Upload: {'YES' if auto_upload else 'NO'}")
    
    # Generate content if needed
    if campaign.get('generate_content', False):
        print("\n🧠 Generating AI content...")
        idea = content_gen.generate_video_concept(
            campaign['niche'],
            campaign['platforms'][0]
        )
        print(f"   Generated: {idea.title}")
        campaign['generated_content'] = idea.__dict__
    
    # AI Video Editing
    print("\n✂️  Starting AI video editing...")
    print("   • Analyzing content...")
    print("   • Detecting highlights...")
    print("   • Generating captions...")
    print("   • Applying effects...")
    
    source_video = campaign['source_video']
    edited_video = ai_editor.smart_edit(source_video, campaign)
    
    print(f"\n✅ Video edited: {edited_video}")
    
    # Generate thumbnail
    print("\n🎨 Generating AI thumbnail...")
    thumbnail = await generate_thumbnail(edited_video, campaign)
    print(f"   Thumbnail: {thumbnail}")
    
    # Track upload
    upload_id = f"upload_{int(time.time())}"
    tracker.log_upload(upload_id, edited_video, 
                      campaign['platforms'][0], 
                      campaign['campaign_id'])
    
    # Auto-upload
    if auto_upload:
        print("\n📤 Starting auto-upload sequence...")
        
        metadata = {
            'title': campaign.get('video_title', campaign['name']),
            'caption': campaign.get('caption', ''),
            'description': campaign.get('description', ''),
            'hashtags': campaign.get('hashtags', []),
            'thumbnail': thumbnail
        }
        
        for platform in campaign['platforms']:
            print(f"\n   Uploading to {platform.upper()}...")
            
            result = await uploader.upload_to_platform(
                edited_video, 
                metadata, 
                platform
            )
            
            if result['status'] == 'success':
                print(f"   ✅ Uploaded: {result['url']}")
                
                # Submit to Clipster
                if campaign.get('auto_submit_clipster'):
                    clipster_result = await uploader.submit_to_clipster(
                        result['url'],
                        campaign['campaign_id'],
                        platform
                    )
                    print(f"   📋 Clipster: {clipster_result['status']}")
            else:
                print(f"   ❌ Failed: {result.get('error')}")
    
    # Summary
    print("\n" + "="*60)
    print("📊 CAMPAIGN COMPLETE")
    print("="*60)
    print(f"Video: {edited_video}")
    print(f"Thumbnail: {thumbnail}")
    print(f"Upload ID: {upload_id}")
    print("\n💰 Ready to earn!")
    
    return {
        'video': edited_video,
        'thumbnail': thumbnail,
        'upload_id': upload_id
    }

async def generate_thumbnail(video_path: str, campaign: Dict) -> str:
    """Generate AI thumbnail from video"""
    # Extract best frame
    from moviepy.editor import VideoFileClip
    import numpy as np
    
    clip = VideoFileClip(video_path)
    best_frame_time = clip.duration / 2  # Middle frame
    
    frame = clip.get_frame(best_frame_time)
    
    # Save frame
    from PIL import Image
    img = Image.fromarray(frame)
    
    # Add text overlay
    # Implementation would add campaign title, branding
    
    thumbnail_path = f"output/thumbnails/thumb_{int(time.time())}.jpg"
    os.makedirs("output/thumbnails", exist_ok=True)
    img.save(thumbnail_path)
    
    clip.close()
    return thumbnail_path

async def run_dashboard():
    """Launch web dashboard"""
    import subprocess
    subprocess.run(["streamlit", "run", "dashboard/app.py"])

async def main():
    banner()
    
    parser = argparse.ArgumentParser(description='Clipster God Mode')
    
    # Commands
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Setup
    setup_parser = subparsers.add_parser('setup', help='Initial setup')
    
    # Process
    process_parser = subparsers.add_parser('process', help='Process campaign')
    process_parser.add_argument('campaign', help='Campaign JSON file')
    process_parser.add_argument('--no-upload', action='store_true',
                               help='Edit only, no upload')
    
    # Generate
    gen_parser = subparsers.add_parser('generate', help='Generate content ideas')
    gen_parser.add_argument('niche', help='Content niche')
    gen_parser.add_argument('--count', type=int, default=10,
                          help='Number of ideas')
    
    # Schedule
    schedule_parser = subparsers.add_parser('schedule', help='Schedule uploads')
    
    # Analytics
    analytics_parser = subparsers.add_parser('analytics', help='View analytics')
    analytics_parser.add_argument('--days', type=int, default=30,
                                 help='Days to report')
    
    # Dashboard
    dashboard_parser = subparsers.add_parser('dashboard', help='Launch dashboard')
    
    # God Mode (everything)
    god_parser = subparsers.add_parser('god', help='Full automation mode')
    god_parser.add_argument('--campaigns-dir', default='config/campaigns',
                           help='Campaigns directory')
    
    args = parser.parse_args()
    
    if args.command == 'setup':
        cm = ConfigManager()
        cm.setup_wizard()
        
    elif args.command == 'process':
        await process_campaign(args.campaign, auto_upload=not args.no_upload)
        
    elif args.command == 'generate':
        cm = ConfigManager()
        config = cm.load_all()
        gen = AIContentGenerator(config)
        
        ideas = gen.generate_batch(args.niche, args.count)
        
        print(f"\n🧠 Generated {len(ideas)} ideas for '{args.niche}':\n")
        for i, idea in enumerate(ideas, 1):
            print(f"{i}. {idea.title}")
            print(f"   Hook: {idea.hook}")
            print(f"   Viral Score: {idea.estimated_viral_score:.2f}")
            print(f"   Hashtags: {', '.join(idea.hashtags[:5])}")
            print()
        
    elif args.command == 'schedule':
        print("📅 Upload Scheduler")
        # Implementation would show TUI for scheduling
        
    elif args.command == 'analytics':
        tracker = PerformanceTracker()
        report = tracker.get_performance_report(args.days)
        
        print(f"\n📊 Performance Report (Last {args.days} days)")
        print("="*50)
        print(f"Total Uploads: {report['total_uploads']}")
        print(f"Total Views: {report['total_views']:,}")
        print(f"Total Likes: {report['total_likes']:,}")
        print(f"Total Earnings: ${report['total_earnings']:.2f}")
        
        if report['by_platform']:
            print("\nBy Platform:")
            for platform, data in report['by_platform'].items():
                print(f"  {platform}: {data.get('total_views', 0):,} views")
        
    elif args.command == 'dashboard':
        await run_dashboard()
        
    elif args.command == 'god':
        print("🔥 GOD MODE: Full Automation")
        print("Scanning for campaigns...")
        
        campaigns_dir = Path(args.campaigns_dir)
        if not campaigns_dir.exists():
            print(f"❌ Directory not found: {campaigns_dir}")
            return
        
        campaigns = list(campaigns_dir.glob("*.json"))
        print(f"Found {len(campaigns)} campaigns")
        
        for campaign_file in campaigns:
            print(f"\n{'='*60}")
            await process_campaign(str(campaign_file), auto_upload=True)
            await asyncio.sleep(5)  # Rate limiting
        
        print("\n✅ All campaigns processed!")
        
    else:
        parser.print_help()

if __name__ == "__main__":
    import time
    asyncio.run(main())