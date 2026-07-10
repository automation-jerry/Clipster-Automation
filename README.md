
# 📘 README.md

```markdown
# 🤖 CLIPSTER GOD MODE - Complete Automation System

> **Auto-Edit → Auto-Upload → Auto-Profit**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)]()

A fully automated content creation and monetization system for Clipster and social media platforms.

---

## ✨ Features

- 🎬 **AI Video Editing** - Smart cuts, auto-captions, viral moment detection
- 🎙️ **AI Voiceover** - Generate realistic voiceovers
- 🎨 **Auto Thumbnails** - AI-generated thumbnails
- 📤 **Auto Upload** - TikTok, Instagram, YouTube, Clipster
- ⏰ **Smart Scheduling** - Post at optimal times
- 📊 **Analytics** - Track views, earnings, performance
- 🧠 **Content AI** - Generate viral video ideas
- 🏷️ **Auto Hashtags** - AI-generated trending hashtags
- 🔄 **A/B Testing** - Test multiple variants
- 📱 **Multi-Account** - Rotate between accounts

---

## 📁 Project Structure

```
clipster_god_mode/
├── 📂 config/                      # Configuration files
│   ├── accounts.json               # Social media credentials (ENCRYPTED)
│   ├── schedules.json              # Upload schedules
│   ├── campaigns/                  # Campaign configurations
│   │   ├── example_campaign.json
│   │   └── your_campaigns_here.json
│   └── templates/                  # Video templates
│       ├── gaming_template.json
│       └── fitness_template.json
│
├── 📂 src/                         # Source code
│   ├── core/                       # Core utilities
│   │   ├── config_manager.py      # Config encryption/management
│   │   ├── database.py            # SQLite analytics database
│   │   └── logger.py              # Advanced logging
│   │
│   ├── ai/                         # AI modules
│   │   ├── ai_editor.py           # AI video editing engine
│   │   ├── content_generator.py   # Viral content ideas
│   │   ├── voice_generator.py     # AI voice synthesis
│   │   └── hashtag_generator.py   # Trending hashtag AI
│   │
│   ├── editing/                    # Video editing
│   │   ├── video_editor.py        # Core editing
│   │   ├── effects_engine.py      # Visual effects
│   │   └── caption_generator.py   # Auto-captions
│   │
│   ├── upload/                     # Upload automation
│   │   ├── uploader.py            # Multi-platform uploader
│   │   ├── scheduler.py           # Upload scheduling
│   │   └── session_manager.py     # Cookie/session handling
│   │
│   ├── analytics/                  # Performance tracking
│   │   ├── performance_tracker.py # View/engagement tracking
│   │   ├── trend_detector.py      # Trending content finder
│   │   └── optimizer.py           # Content optimization AI
│   │
│   └── api/                        # API integrations
│       ├── clipster_api.py        # Clipster API client
│       └── webhook_server.py      # Webhook receiver
│
├── 📂 assets/                      # Media assets
│   ├── fonts/                      # Typography files
│   ├── music/                      # Royalty-free audio
│   ├── overlays/                   # Visual overlays
│   ├── stickers/                   # Animated stickers
│   └── templates/                  # Premiere/FCP templates
│
├── 📂 output/                      # Generated content
│   ├── videos/                     # Rendered videos
│   ├── thumbnails/                 # Generated thumbnails
│   └── temp/                       # Processing temp files
│
├── 📂 logs/                        # Logs & analytics
│   ├── uploads/                    # Upload logs
│   ├── analytics/                  # Performance data
│   └── errors/                     # Error logs
│
├── 📂 dashboard/                   # Web UI
│   └── app.py                      # Streamlit dashboard
│
├── 📂 docker/                      # Docker deployment
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── 📂 tests/                       # Unit tests
│
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
├── main.py                         # CLI entry point
├── setup.py                        # Package setup
├── LICENSE                         # MIT License
└── README.md                       # This file
```

---

## 🚀 Installation

### Prerequisites

- Python 3.10+
- FFmpeg
- Chrome/Chromium (for browser automation)
- CUDA (optional, for GPU acceleration)

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/clipster-god-mode.git
cd clipster-god-mode
```

### Step 2: Install System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y \
    ffmpeg \
    libavcodec-extra \
    libsm6 \
    libxext6 \
    libgl1-mesa-glx \
    tesseract-ocr \
    tesseract-ocr-eng \
    chromium-browser
```

**macOS:**
```bash
brew install ffmpeg tesseract chromium
```

**Windows:**
1. Download FFmpeg from https://ffmpeg.org/download.html
2. Download Tesseract from https://github.com/UB-Mannheim/tesseract/wiki
3. Add both to your PATH

### Step 3: Create Virtual Environment

```bash
python -m venv venv

# Activate
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows
```

### Step 4: Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 5: Run Setup Wizard

```bash
python main.py setup
```

This will:
- Create encrypted config files
- Prompt for your social media credentials
- Set up your Clipster API key
- Configure upload preferences

---

## ⚙️ Configuration

### File: `config/accounts.json`

This file stores your credentials (automatically encrypted):

```json
{
  "tiktok": {
    "username": "your_tiktok_username",
    "password": "your_password",
    "session_id": null,
    "cookies_file": "config/tiktok_cookies.json",
    "upload_defaults": {
      "privacy": "public",
      "allow_comments": true,
      "allow_duet": true,
      "allow_stitch": true
    }
  },
  
  "instagram": {
    "username": "your_ig_username",
    "password": "your_password",
    "2fa_enabled": false,
    "session_file": "config/ig_session.json",
    "upload_defaults": {
      "is_reel": true,
      "share_to_feed": true
    }
  },
  
  "youtube": {
    "client_secrets": "config/youtube_client_secrets.json",
    "credentials": "config/youtube_credentials.json",
    "channel_id": "your_channel_id",
    "upload_defaults": {
      "privacy": "public",
      "category": "22",
      "tags": ["shorts", "viral"]
    }
  },
  
  "clipster": {
    "api_key": "your_clipster_api_key",
    "auto_submit": true,
    "default_campaigns": ["camp_123", "camp_456"]
  },
  
  "openai": {
    "api_key": "sk-your-openai-key",
    "model": "gpt-4"
  },
  
  "settings": {
    "timezone": "America/New_York",
    "default_output_quality": "1080p",
    "auto_thumbnail": true,
    "auto_captions": true,
    "watermark_enabled": true,
    "watermark_text": "YourBrand"
  }
}
```

### File: `config/campaigns/example_campaign.json`

```json
{
  "name": "Gaming_App_Promo",
  "brand": "GameStudio Inc",
  "campaign_id": "camp_12345",
  "active": true,
  
  "platforms": ["tiktok", "instagram", "youtube"],
  
  "source_video": "assets/raw/gameplay_footage.mp4",
  
  "requirements": {
    "duration": {
      "min": 15,
      "max": 60,
      "target": 30
    },
    "format": "vertical_9_16",
    "resolution": "1080x1920",
    "fps": 30,
    
    "style": "fast_paced_gaming",
    "mood": "exciting",
    " pacing": "quick_cuts",
    
    "hook": {
      "type": "shock",
      "duration": 3,
      "text": "You won't believe this!"
    },
    
    "cta": {
      "text": "Download link in bio!",
      "position": "end",
      "duration": 3
    }
  },
  
  "ai_settings": {
    "auto_captions": true,
    "caption_style": "tiktok_bold",
    "highlight_detection": true,
    "emotion_enhancement": true,
    "color_grading": "gaming_vibrant",
    "background_music": "assets/music/upbeat_electronic.mp3",
    "music_ducking": true,
    "voiceover": {
      "enabled": false,
      "voice": "en-US-Neural2-F",
      "script": ""
    }
  },
  
  "content": {
    "title": "INSANE Gaming Moment! 🔥",
    "caption": "This had me SHOOK 😱",
    "description": "Watch till the end for the surprise!",
    "hashtags": ["gaming", "mobilegame", "gamer", "indiegame", "gameplay"],
    "mentions": ["@gamestudio"],
    "tags": ["gaming", "mobile", "viral"]
  },
  
  "schedule": {
    "enabled": true,
    "optimal_time": true,
    "specific_time": null,
    "spread_uploads": true,
    "hours_between": 2
  },
  
  "thumbnail": {
    "enabled": true,
    "style": "clickbait",
    "text": "WAIT FOR IT...",
    "emoji": "😱",
    "arrow": true
  },
  
  "clipster": {
    "auto_submit": true,
    "track_performance": true,
    "expected_cpm": 5.0
  }
}
```

---

## 🎮 Usage

### 1. Setup (First Time Only)

```bash
python main.py setup
```

### 2. Process Single Campaign

```bash
python main.py process config/campaigns/my_campaign.json
```

### 3. Process All Campaigns (God Mode)

```bash
python main.py god
```

### 4. Generate Content Ideas

```bash
python main.py generate "gaming" --count 20
```

### 5. View Analytics

```bash
python main.py analytics --days 7
```

### 6. Launch Dashboard

```bash
python main.py dashboard
# Opens at http://localhost:8501
```

---

## 🐳 Docker Deployment

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## 🔒 Security

- All credentials are **encrypted** using Fernet (AES-128)
- Session cookies stored separately
- API keys in environment variables
- No credentials in git history

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `FFmpeg not found` | Install FFmpeg and add to PATH |
| `Chrome driver error` | Run `webdriver-manager update` |
| `Upload failed` | Check credentials in `accounts.json` |
| `CUDA out of memory` | Reduce batch size or use CPU |

---

## 📈 Performance Tips

1. **Use GPU**: Install CUDA for 10x faster processing
2. **Batch Processing**: Process multiple videos overnight
3. **Optimal Times**: Let scheduler post at peak hours
4. **A/B Testing**: Create multiple variants of same video

---

## 📝 License

MIT License - See [LICENSE](LICENSE)

---

## 🙏 Credits

- Built with [MoviePy](https://zulko.github.io/moviepy/)
- AI powered by [OpenAI](https://openai.com)
- Voice by [ElevenLabs](https://elevenlabs.io)

---

**Made with ❤️ by creators, for creators**
```

---

## 📋 CONFIG FILES (Complete)

### 1. `config/accounts.json`

```json
{
  "tiktok": {
    "username": "",
    "password": "",
    "session_id": null,
    "cookies_file": "config/tiktok_cookies.json",
    "upload_defaults": {
      "privacy": "public",
      "allow_comments": true,
      "allow_duet": true,
      "allow_stitch": true
    }
  },
  "instagram": {
    "username": "",
    "password": "",
    "2fa_enabled": false,
    "session_file": "config/ig_session.json",
    "upload_defaults": {
      "is_reel": true,
      "share_to_feed": true
    }
  },
  "youtube": {
    "client_secrets": "config/youtube_client_secrets.json",
    "credentials": "config/youtube_credentials.json",
    "channel_id": "",
    "upload_defaults": {
      "privacy": "public",
      "category": "22",
      "tags": ["shorts", "viral"]
    }
  },
  "clipster": {
    "api_key": "",
    "auto_submit": true,
    "default_campaigns": []
  },
  "openai": {
    "api_key": "",
    "model": "gpt-4"
  },
  "anthropic": {
    "api_key": ""
  },
  "elevenlabs": {
    "api_key": ""
  },
  "settings": {
    "timezone": "America/New_York",
    "default_output_quality": "1080p",
    "auto_thumbnail": true,
    "auto_captions": true,
    "watermark_enabled": false,
    "watermark_text": "",
    "max_concurrent_uploads": 3,
    "retry_failed_uploads": true,
    "retry_attempts": 3
  }
}
```

### 2. `config/campaigns/template.json`

```json
{
  "name": "Your_Campaign_Name",
  "brand": "Brand Name",
  "campaign_id": "",
  "active": true,
  
  "platforms": ["tiktok", "instagram", "youtube"],
  
  "source_video": "assets/raw/your_video.mp4",
  
  "requirements": {
    "duration": {
      "min": 15,
      "max": 60,
      "target": 30
    },
    "format": "vertical_9_16",
    "resolution": "1080x1920",
    "fps": 30,
    "style": "fast_paced",
    "mood": "exciting"
  },
  
  "ai_settings": {
    "auto_captions": true,
    "caption_style": "tiktok_bold",
    "highlight_detection": true,
    "emotion_enhancement": true,
    "color_grading": "vibrant",
    "background_music": "",
    "music_ducking": true,
    "voiceover": {
      "enabled": false,
      "voice": "en-US-Neural2-F",
      "script": ""
    }
  },
  
  "content": {
    "title": "Your Video Title",
    "caption": "Your caption here",
    "description": "Longer description for YouTube",
    "hashtags": ["hashtag1", "hashtag2", "hashtag3"],
    "mentions": [],
    "tags": []
  },
  
  "schedule": {
    "enabled": true,
    "optimal_time": true,
    "spread_uploads": true,
    "hours_between": 2
  },
  
  "thumbnail": {
    "enabled": true,
    "style": "clickbait",
    "text": "HOOK TEXT",
    "emoji": "🔥"
  },
  
  "clipster": {
    "auto_submit": true,
    "track_performance": true
  }
}
```

### 3. `config/schedules.json`

```json
{
  "upload_queue": [],
  "recurring_schedules": [],
  "optimal_times": {
    "tiktok": ["09:00", "12:00", "19:00", "21:00"],
    "instagram": ["11:00", "13:00", "17:00", "19:00"],
    "youtube": ["14:00", "16:00", "19:00"]
  },
  "timezone": "America/New_York",
  "last_updated": ""
}
```

### 4. `.env.example`

```bash
# API Keys
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key
ELEVENLABS_API_KEY=your-key

# Database
DATABASE_URL=sqlite:///logs/analytics.db
REDIS_URL=redis://localhost:6379

# Paths
FFMPEG_PATH=/usr/bin/ffmpeg
CHROME_PATH=/usr/bin/chromium

# Features
ENABLE_GPU=true
CUDA_VISIBLE_DEVICES=0

# Monitoring
SENTRY_DSN=
ENABLE_ANALYTICS=true
```

---

## 🚀 QUICK START

```bash
# 1. Install
git clone <repo>
cd clipster_god_mode
pip install -r requirements.txt

# 2. Setup
python main.py setup

# 3. Create campaign
cp config/campaigns/template.json config/campaigns/my_first.json
# Edit my_first.json with your details

# 4. RUN
python main.py god
```

**Done!** The system will auto-edit, auto-upload, and start making you money! 💰
