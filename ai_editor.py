import torch
import cv2
import numpy as np
from moviepy.editor import *
import whisper
from transformers import pipeline
import openai
from typing import List, Dict, Tuple, Optional
import json
from dataclasses import dataclass
from pathlib import Path

@dataclass
class EditDecision:
    timestamp: float
    action: str
    confidence: float
    reason: str

class AIVideoEditor:
    def __init__(self, config: Dict):
        self.config = config
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        print(f"🚀 Loading AI models on {self.device}...")
        
        # Load Whisper for transcription
        self.whisper_model = whisper.load_model("large-v3").to(self.device)
        
        # Load emotion detection
        self.emotion_classifier = pipeline(
            "image-classification",
            model="dima806/facial_emotions_image_detection",
            device=0 if torch.cuda.is_available() else -1
        )
        
        # Load highlight detection
        self.highlight_detector = self._load_highlight_model()
        
        # Load scene detection
        self.scene_detector = cv2.createBackgroundSubtractorMOG2()
        
        # OpenAI for content analysis
        openai.api_key = config.get('openai_api_key')
        
        self.frame_cache = {}
        
    def _load_highlight_model(self):
        """Load custom highlight detection model"""
        # Using a simple approach with optical flow and audio peaks
        return None
    
    def analyze_content(self, video_path: str) -> Dict:
        """Deep AI analysis of video content"""
        print(f"🔍 Analyzing: {video_path}")
        
        clip = VideoFileClip(video_path)
        
        analysis = {
            'duration': clip.duration,
            'fps': clip.fps,
            'resolution': clip.size,
            'scenes': self._detect_scenes(clip),
            'audio_peaks': self._detect_audio_peaks(clip),
            'transcription': self._transcribe_audio(clip),
            'emotions': self._analyze_emotions(clip),
            'highlights': [],
            'viral_moments': []
        }
        
        # Find viral moments combining multiple signals
        analysis['highlights'] = self._find_highlights(analysis)
        analysis['viral_moments'] = self._predict_viral_potential(analysis)
        
        clip.close()
        return analysis
    
    def _detect_scenes(self, clip: VideoFileClip) -> List[Dict]:
        """Detect scene changes using computer vision"""
        scenes = []
        prev_frame = None
        threshold = 30.0
        
        for t in np.arange(0, clip.duration, 0.5):
            frame = clip.get_frame(t)
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            
            if prev_frame is not None:
                diff = cv2.absdiff(gray, prev_frame)
                mean_diff = np.mean(diff)
                
                if mean_diff > threshold:
                    scenes.append({
                        'timestamp': t,
                        'intensity': mean_diff,
                        'type': 'cut'
                    })
            
            prev_frame = gray
        
        return scenes
    
    def _detect_audio_peaks(self, clip: VideoFileClip) -> List[Dict]:
        """Detect audio peaks and exciting moments"""
        audio = clip.audio
        if audio is None:
            return []
        
        # Extract audio array
        fps = 44100
        audio_array = audio.to_soundarray(fps=fps)
        volume = np.sqrt(np.mean(audio_array**2, axis=1))
        
        # Find peaks
        from scipy.signal import find_peaks
        peaks, properties = find_peaks(volume, height=np.percentile(volume, 90), 
                                       distance=fps)
        
        return [{
            'timestamp': p / fps,
            'intensity': float(volume[p]),
            'type': 'audio_peak'
        } for p in peaks]
    
    def _transcribe_audio(self, clip: VideoFileClip) -> Dict:
        """Transcribe audio with Whisper"""
        # Extract audio to temp file
        temp_audio = "temp_audio.wav"
        clip.audio.write_audiofile(temp_audio, fps=16000, nbytes=2, 
                                   codec='pcm_s16le', verbose=False)
        
        result = self.whisper_model.transcribe(
            temp_audio,
            language="en",
            task="transcribe",
            word_timestamps=True
        )
        
        # Clean up
        Path(temp_audio).unlink(missing_ok=True)
        
        return {
            'text': result['text'],
            'segments': result['segments'],
            'words': [word for seg in result['segments'] 
                     for word in seg.get('words', [])]
        }
    
    def _analyze_emotions(self, clip: VideoFileClip) -> List[Dict]:
        """Analyze facial emotions throughout video"""
        emotions = []
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        sample_times = np.linspace(0, clip.duration, min(60, int(clip.duration)))
        
        for t in sample_times:
            frame = clip.get_frame(t)
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            if len(faces) > 0:
                # Get dominant face
                x, y, w, h = max(faces, key=lambda f: f[2]*f[3])
                face_img = frame[y:y+h, x:x+w]
                
                # Classify emotion
                try:
                    results = self.emotion_classifier(face_img)
                    emotions.append({
                        'timestamp': t,
                        'emotions': results,
                        'face_count': len(faces)
                    })
                except:
                    pass
        
        return emotions
    
    def _find_highlights(self, analysis: Dict) -> List[Dict]:
        """Combine signals to find highlight moments"""
        highlights = []
        
        # Combine audio peaks with scene changes
        audio_times = [p['timestamp'] for p in analysis['audio_peaks']]
        scene_times = [s['timestamp'] for s in analysis['scenes']]
        
        for audio_peak in analysis['audio_peaks']:
            t = audio_peak['timestamp']
            
            # Check if near scene change
            near_scene = any(abs(t - s) < 2.0 for s in scene_times)
            
            # Check transcription for exciting words
            words_at_time = self._get_words_at_time(
                analysis['transcription'], t
            )
            excitement_score = self._calculate_excitement(words_at_time)
            
            if near_scene or excitement_score > 0.7:
                highlights.append({
                    'start': max(0, t - 3),
                    'end': min(analysis['duration'], t + 3),
                    'score': audio_peak['intensity'] * (1.5 if near_scene else 1),
                    'reason': 'audio_peak' + ('+scene_change' if near_scene else '')
                })
        
        # Sort by score and remove overlaps
        highlights.sort(key=lambda x: x['score'], reverse=True)
        filtered = self._remove_overlapping_segments(highlights)
        
        return filtered[:10]  # Top 10 highlights
    
    def _predict_viral_potential(self, analysis: Dict) -> List[Dict]:
        """Use AI to predict which moments might go viral"""
        viral_moments = []
        
        # Analyze transcription with GPT
        segments = analysis['transcription']['segments']
        
        for i, segment in enumerate(segments):
            # Get context window
            context = self._get_segment_context(segments, i)
            
            # Score viral potential
            viral_score = self._score_viral_potential(context)
            
            if viral_score > 0.8:
                viral_moments.append({
                    'start': segment['start'],
                    'end': segment['end'],
                    'text': segment['text'],
                    'viral_score': viral_score,
                    'hook_type': self._classify_hook(context)
                })
        
        return sorted(viral_moments, key=lambda x: x['viral_score'], reverse=True)[:5]
    
    def _score_viral_potential(self, text: str) -> float:
        """Score text for viral potential"""
        # Use OpenAI or keyword heuristics
        viral_keywords = [
            'shocking', 'unbelievable', 'wait for it', 'watch till end',
            'secret', 'hack', 'insane', 'crazy', 'must see', 'you won\'t believe'
        ]
        
        text_lower = text.lower()
        score = sum(1 for kw in viral_keywords if kw in text_lower) / len(viral_keywords)
        
        # Boost for questions and controversy
        if '?' in text:
            score += 0.2
        if any(w in text_lower for w in ['vs', 'better', 'worse', 'never', 'always']):
            score += 0.15
        
        return min(score, 1.0)
    
    def _classify_hook(self, text: str) -> str:
        """Classify the type of viral hook"""
        text_lower = text.lower()
        
        if any(w in text_lower for w in ['secret', 'hack', 'trick', 'method']):
            return 'educational'
        elif any(w in text_lower for w in ['shocking', 'unbelievable', 'crazy']):
            return 'shock'
        elif any(w in text_lower for w in ['story', 'when i', 'my', 'i was']):
            return 'story'
        elif '?' in text:
            return 'question'
        else:
            return 'entertainment'
    
    def smart_edit(self, video_path: str, campaign: Dict) -> str:
        """AI-powered smart editing based on campaign requirements"""
        print("🎬 Starting smart edit...")
        
        # Analyze content
        analysis = self.analyze_content(video_path)
        
        # Determine edit strategy
        strategy = self._determine_edit_strategy(campaign, analysis)
        
        # Execute edits
        clip = VideoFileClip(video_path)
        edited_clips = []
        
        if strategy['use_highlights']:
            # Create highlight reel
            for highlight in analysis['highlights'][:strategy['num_clips']]:
                subclip = clip.subclip(highlight['start'], highlight['end'])
                
                # Apply AI enhancements
                subclip = self._apply_enhancements(subclip, highlight)
                edited_clips.append(subclip)
        else:
            # Full video with smart cuts
            edited_clips = self._smart_cut_full_video(clip, analysis)
        
        # Concatenate
        final = concatenate_videoclips(edited_clips)
        
        # Add AI-generated elements
        final = self._add_ai_elements(final, campaign, analysis)
        
        # Export
        output_path = f"output/videos/edited_{int(time.time())}.mp4"
        final.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            fps=30,
            threads=4,
            preset='medium'
        )
        
        clip.close()
        final.close()
        
        return output_path
    
    def _apply_enhancements(self, clip: VideoFileClip, 
                           highlight: Dict) -> VideoFileClip:
        """Apply AI enhancements to clip"""
        # Speed ramping for impact
        if highlight['score'] > 0.8:
            # Slow motion at peak moment
            center = (highlight['start'] + highlight['end']) / 2
            # Implementation would adjust speed curve
        
        # Auto color grading
        clip = self._auto_color_grade(clip)
        
        # Add subtle zoom
        clip = clip.fx(vfx.resize, lambda t: 1 + 0.1 * np.sin(t * 2))
        
        return clip
    
    def _auto_color_grade(self, clip: VideoFileClip) -> VideoFileClip:
        """Apply AI color grading"""
        # Simple LUT application
        def apply_lut(frame):
            # Enhance contrast and saturation
            lab = cv2.cvtColor(frame, cv2.COLOR_RGB2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            l = clahe.apply(l)
            enhanced = cv2.merge([l, a, b])
            return cv2.cvtColor(enhanced, cv2.COLOR_LAB2RGB)
        
        return clip.fl_image(apply_lut)
    
    def _add_ai_elements(self, clip: VideoFileClip, campaign: Dict,
                         analysis: Dict) -> VideoFileClip:
        """Add AI-generated captions, effects, and branding"""
        
        # Generate captions
        if campaign.get('auto_captions', True):
            clip = self._add_auto_captions(clip, analysis['transcription'])
        
        # Add hook animation
        if analysis['viral_moments']:
            hook = analysis['viral_moments'][0]
            clip = self._add_hook_animation(clip, hook['start'])
        
        # Add background music
        if campaign.get('background_music'):
            clip = self._mix_background_music(clip, campaign['background_music'])
        
        # Add end screen
        clip = self._add_end_screen(clip, campaign.get('cta', 'Follow for more!'))
        
        return clip
    
    def _add_auto_captions(self, clip: VideoFileClip, 
                          transcription: Dict) -> VideoFileClip:
        """Add animated captions with word-level highlighting"""
        from moviepy.video.fx.all import margin
        
        words = transcription.get('words', [])
        if not words:
            return clip
        
        # Create caption clips
        caption_clips = []
        
        for word_info in words:
            text = word_info['word'].upper()
            start = word_info['start']
            end = word_info['end']
            
            # Style: TikTok-style captions
            txt_clip = (TextClip(
                text,
                fontsize=70,
                color='white',
                stroke_color='black',
                stroke_width=3,
                font='Arial-Bold',
                method='caption',
                size=(clip.w * 0.9, None),
                align='center'
            )
            .set_start(start)
            .set_duration(end - start)
            .set_position(('center', 'bottom'))
            .margin(bottom=100, opacity=0))
            
            caption_clips.append(txt_clip)
        
        # Composite
        return CompositeVideoClip([clip] + caption_clips)
    
    def _add_hook_animation(self, clip: VideoFileClip, 
                            hook_time: float) -> VideoFileClip:
        """Add attention-grabbing hook animation"""
        # Flash effect at hook moment
        def flash(get_frame, t):
            frame = get_frame(t)
            if abs(t - hook_time) < 0.1:
                return np.clip(frame * 1.5, 0, 255).astype(np.uint8)
            return frame
        
        return clip.fl(flash)
    
    def _mix_background_music(self, clip: VideoFileClip, 
                               music_path: str) -> VideoFileClip:
        """Mix background music with ducking"""
        music = AudioFileClip(music_path).subclip(0, clip.duration)
        music = music.volumex(0.3)  # Lower volume
        
        # Duck music when speech detected
        # Implementation would analyze audio and duck accordingly
        
        final_audio = CompositeAudioClip([clip.audio, music])
        return clip.set_audio(final_audio)
    
    def _add_end_screen(self, clip: VideoFileClip, 
                        cta_text: str) -> VideoFileClip:
        """Add branded end screen with CTA"""
        # Create end screen
        end_duration = 3
        
        # Background
        bg = ColorClip(size=clip.size, color=(0, 0, 0))
        bg = bg.set_duration(end_duration).set_opacity(0.8)
        
        # CTA Text
        cta = (TextClip(
            cta_text,
            fontsize=60,
            color='white',
            font='Arial-Bold'
        )
        .set_duration(end_duration)
        .set_position('center'))
        
        # Subscribe button animation
        subscribe = (TextClip(
            "🔔 SUBSCRIBE",
            fontsize=50,
            color='red',
            font='Arial-Bold'
        )
        .set_duration(end_duration)
        .set_position(('center', clip.h * 0.7)))
        
        end_screen = CompositeVideoClip([bg, cta, subscribe])
        
        # Fade transition
        end_screen = end_screen.fadein(0.5).fadeout(0.5)
        
        return concatenate_videoclips([clip, end_screen])
    
    # Helper methods
    def _get_words_at_time(self, transcription: Dict, timestamp: float) -> List[Dict]:
        """Get words spoken around a timestamp"""
        words = transcription.get('words', [])
        return [w for w in words if abs(w['start'] - timestamp) < 2.0]
    
    def _calculate_excitement(self, words: List[Dict]) -> float:
        """Calculate excitement score from words"""
        excitement_words = ['wow', 'amazing', 'insane', 'crazy', 'omg', 'no way']
        if not words:
            return 0.0
        count = sum(1 for w in words if w['word'].lower() in excitement_words)
        return min(count / 3, 1.0)
    
    def _remove_overlapping_segments(self, segments: List[Dict]) -> List[Dict]:
        """Remove overlapping time segments"""
        if not segments:
            return []
        
        sorted_segs = sorted(segments, key=lambda x: x['start'])
        filtered = [sorted_segs[0]]
        
        for seg in sorted_segs[1:]:
            if seg['start'] >= filtered[-1]['end']:
                filtered.append(seg)
        
        return filtered
    
    def _determine_edit_strategy(self, campaign: Dict, 
                                  analysis: Dict) -> Dict:
        """Determine optimal editing strategy"""
        return {
            'use_highlights': campaign.get('format') == 'highlights',
            'num_clips': campaign.get('num_clips', 3),
            'target_duration': campaign.get('duration', 30),
            'style': campaign.get('style', 'fast_paced')
        }
    
    def _get_segment_context(self, segments: List[Dict], 
                              idx: int, window: int = 3) -> str:
        """Get context window around a segment"""
        start = max(0, idx - window)
        end = min(len(segments), idx + window + 1)
        return ' '.join(s['text'] for s in segments[start:end])
    
    def _smart_cut_full_video(self, clip: VideoFileClip, 
                               analysis: Dict) -> List[VideoFileClip]:
        """Smart cutting for full video retention"""
        # Remove dead air and boring moments
        clips = []
        current_start = 0
        
        for scene in analysis['scenes']:
            # Keep segment if it has audio peaks or emotional moments
            segment = clip.subclip(current_start, scene['timestamp'])
            
            if self._is_segment_interesting(segment, analysis):
                clips.append(segment)
            
            current_start = scene['timestamp']
        
        # Add final segment
        final = clip.subclip(current_start, clip.duration)
        if self._is_segment_interesting(final, analysis):
            clips.append(final)
        
        return clips
    
    def _is_segment_interesting(self, segment: VideoFileClip, 
                                  analysis: Dict) -> bool:
        """Determine if a segment is worth keeping"""
        duration = segment.duration
        
        # Skip if too short
        if duration < 1.0:
            return False
        
        # Skip if silence (simple check)
        if segment.audio is None:
            return False
        
        return True