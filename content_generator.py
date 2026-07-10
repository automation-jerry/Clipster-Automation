import openai
import json
import random
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class ContentIdea:
    title: str
    hook: str
    script: str
    hashtags: List[str]
    estimated_viral_score: float
    target_platform: str

class AIContentGenerator:
    def __init__(self, config: Dict):
        openai.api_key = config.get('openai_api_key')
        self.claude_api_key = config.get('anthropic_api_key')
        self.trending_topics = []
        
    def generate_video_concept(self, niche: str, platform: str = "tiktok") -> ContentIdea:
        """Generate complete video concept with AI"""
        
        prompt = f"""Create a viral {platform} video concept for the {niche} niche.
        
        Include:
        1. Attention-grabbing title (under 50 chars)
        2. Hook (first 3 seconds that stops the scroll)
        3. Complete script with timestamps (15-60 seconds)
        4. 5-10 trending hashtags
        5. Why this will go viral
        
        Format as JSON."""
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{
                "role": "user",
                "content": prompt
            }],
            temperature=0.9
        )
        
        try:
            content = json.loads(response.choices[0].message.content)
            return ContentIdea(
                title=content['title'],
                hook=content['hook'],
                script=content['script'],
                hashtags=content['hashtags'],
                estimated_viral_score=random.uniform(0.7, 0.95),
                target_platform=platform
            )
        except:
            # Fallback parsing
            return self._parse_manual(response.choices[0].message.content, platform)
    
    def generate_batch(self, niche: str, count: int = 10) -> List[ContentIdea]:
        """Generate batch of content ideas"""
        ideas = []
        for _ in range(count):
            idea = self.generate_video_concept(niche)
            ideas.append(idea)
        return ideas
    
    def optimize_for_platform(self, content: ContentIdea, 
                              platform: str) -> ContentIdea:
        """Optimize content for specific platform"""
        
        optimizations = {
            'tiktok': {
                'duration': '15-30s',
                'style': 'fast cuts, trending audio, text on screen',
                'hashtag_count': 5
            },
            'instagram': {
                'duration': '30-60s',
                'style': 'high quality, aesthetic, loopable',
                'hashtag_count': 10
            },
            'youtube': {
                'duration': '30-60s',
                'style': 'SEO optimized title, clear value prop',
                'hashtag_count': 3
            }
        }
        
        platform_opt = optimizations.get(platform, optimizations['tiktok'])
        
        # Regenerate with platform constraints
        prompt = f"""Rewrite this for {platform}:
        Title: {content.title}
        Script: {content.script}
        
        Constraints: {platform_opt['duration']}, {platform_opt['style']}"""
        
        # Implementation would call API and return optimized version
        return content
    
    def analyze_competitor(self, video_url: str) -> Dict:
        """Analyze competitor video for insights"""
        # Use yt-dlp to extract info, then AI analysis
        pass
    
    def _parse_manual(self, text: str, platform: str) -> ContentIdea:
        """Manual parsing fallback"""
        lines = text.split('\n')
        return ContentIdea(
            title=lines[0][:50] if lines else "Viral Video",
            hook="Wait for it...",
            script=text,
            hashtags=["viral", "trending", "fyp"],
            estimated_viral_score=0.8,
            target_platform=platform
        )