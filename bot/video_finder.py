"""
Video clip finder module using Pexels API
"""

import asyncio
import logging
import re
from typing import List, Dict, Optional, Any
import aiohttp

logger = logging.getLogger(__name__)


class VideoFinder:
    """Find stock video clips and images using Pexels API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.pexels.com/v1"
        self.video_url = "https://api.pexels.com/videos"
    
    async def extract_keywords(self, script: str) -> List[str]:
        """Extract keywords from script and translate to English for better video search"""
        # Hindi to English keyword mapping for better Pexels results
        hindi_to_english = {
            'पानी': 'water', 'आग': 'fire', 'हवा': 'air', 'पेड़': 'tree', 'पौधे': 'plants',
            'जानवर': 'animals', 'पशु': 'animals', 'मछली': 'fish', 'पक्षी': 'birds',
            'सूरज': 'sun', 'चांद': 'moon', 'तारे': 'stars', 'आकाश': 'sky', 'समुद्र': 'ocean',
            'पहाड़': 'mountain', 'नदी': 'river', 'जंगल': 'forest', 'रेगिस्तान': 'desert',
            'बर्फ': 'snow', 'बारिश': 'rain', 'बादल': 'clouds', 'धरती': 'earth',
            'स्पेस': 'space', 'अंतरिक्ष': 'space', 'ग्रह': 'planet', 'दिमाग': 'brain',
            'हृदय': 'heart', 'आंखें': 'eyes', 'हाथ': 'hands', 'शरीर': 'body',
            'भोजन': 'food', 'खाना': 'food', 'फल': 'fruits', 'सब्जी': 'vegetables',
            'तकनीक': 'technology', 'कंप्यूटर': 'computer', 'मोबाइल': 'mobile',
            'इंटरनेट': 'internet', 'कार': 'car', 'ट्रेन': 'train', 'हवाई': 'airplane',
            'डॉक्टर': 'doctor', 'अस्पताल': 'hospital', 'दवा': 'medicine',
            'स्कूल': 'school', 'किताब': 'book', 'पढ़ाई': 'study', 'बच्चे': 'children',
            'माता': 'mother', 'पिता': 'father', 'परिवार': 'family', 'घर': 'house',
            'शहर': 'city', 'गांव': 'village', 'भारत': 'india', 'दुनिया': 'world',
            'विज्ञान': 'science', 'गणित': 'math', 'रसायन': 'chemistry', 'भौतिक': 'physics',
            'प्रकृति': 'nature', 'वातावरण': 'environment', 'जलवायु': 'climate',
            'व्यायाम': 'exercise', 'योग': 'yoga', 'खेल': 'sports', 'क्रिकेट': 'cricket',
            'संगीत': 'music', 'नृत्य': 'dance', 'कला': 'art', 'फिल्म': 'movie',
            'रोबोट': 'robot', 'एआई': 'ai', 'मशीन': 'machine', 'इंजीनियर': 'engineer',
            'समुंदर': 'ocean', 'पृथ्वी': 'earth', 'सूर्य': 'sun', 'चांद': 'moon'
        }
        
        # Extract words from script
        keywords = []
        script_lower = script.lower()
        
        # Find Hindi words and translate them
        for hindi_word, english_word in hindi_to_english.items():
            if hindi_word in script_lower:
                keywords.append(english_word)
        
        # Extract English words that might be good search terms
        english_words = re.findall(r'\b[a-zA-Z]{4,}\b', script)
        keywords.extend(english_words[:3])  # Add first 3 English words
        
        # Add generic science keywords if nothing specific found
        if not keywords:
            keywords = ["science", "technology", "laboratory", "experiment", "discovery"]
        
        # Remove duplicates and limit
        keywords = list(set(keywords))[:5]  # Return top 5 unique keywords
        
        return keywords
    
    async def search_videos(self, keywords: List[str], limit: int = 5) -> List[Dict[str, Any]]:
        """Search for videos using Pexels API"""
        try:
            async with aiohttp.ClientSession() as session:
                all_videos = []
                
                for keyword in keywords:
                    # Search for videos
                    url = f"{self.video_url}/search"
                    params = {
                        "query": keyword,
                        "per_page": limit,
                        "orientation": "portrait"  # For shorts format
                    }
                    headers = {"Authorization": self.api_key}
                    
                    async with session.get(url, params=params, headers=headers) as response:
                        if response.status == 200:
                            data = await response.json()
                            videos = data.get("videos", [])
                            
                            for video in videos:
                                video_info = {
                                    "id": video.get("id"),
                                    "title": f"Video for '{keyword}'",
                                    "url": video.get("url"),
                                    "duration": video.get("duration"),
                                    "thumbnail": video.get("image"),
                                    "user": video.get("user", {}).get("name"),
                                    "keyword": keyword,
                                    "type": "video"
                                }
                                
                                # Get video files
                                video_files = video.get("video_files", [])
                                if video_files:
                                    # Prefer HD quality
                                    hd_file = next(
                                        (f for f in video_files if f.get("quality") == "hd"),
                                        video_files[0]
                                    )
                                    video_info["download_url"] = hd_file.get("link")
                                    video_info["file_type"] = hd_file.get("file_type")
                                
                                all_videos.append(video_info)
                        
                        # Small delay to avoid rate limiting
                        await asyncio.sleep(0.5)
                
                return all_videos[:limit]
        
        except Exception as e:
            logger.error(f"Error searching videos: {e}")
            return []
    
    async def search_images(self, keywords: List[str], limit: int = 5) -> List[Dict[str, Any]]:
        """Search for images using Pexels API"""
        try:
            async with aiohttp.ClientSession() as session:
                all_images = []
                
                for keyword in keywords:
                    # Search for images
                    url = f"{self.base_url}/search"
                    params = {
                        "query": keyword,
                        "per_page": limit,
                        "orientation": "portrait"
                    }
                    headers = {"Authorization": self.api_key}
                    
                    async with session.get(url, params=params, headers=headers) as response:
                        if response.status == 200:
                            data = await response.json()
                            photos = data.get("photos", [])
                            
                            for photo in photos:
                                image_info = {
                                    "id": photo.get("id"),
                                    "title": f"Image for '{keyword}'",
                                    "url": photo.get("url"),
                                    "photographer": photo.get("photographer"),
                                    "keyword": keyword,
                                    "type": "image",
                                    "thumbnail": photo.get("src", {}).get("medium"),
                                    "download_url": photo.get("src", {}).get("large")
                                }
                                all_images.append(image_info)
                        
                        # Small delay to avoid rate limiting
                        await asyncio.sleep(0.5)
                
                return all_images[:limit]
        
        except Exception as e:
            logger.error(f"Error searching images: {e}")
            return []
    
    async def find_media_for_script(self, script: str) -> Dict[str, Any]:
        """Find both videos and images for a script"""
        try:
            # Extract keywords
            keywords = await self.extract_keywords(script)
            
            # Search for media
            videos_task = self.search_videos(keywords, limit=3)
            images_task = self.search_images(keywords, limit=3)
            
            videos, images = await asyncio.gather(videos_task, images_task)
            
            return {
                "success": True,
                "keywords": keywords,
                "videos": videos,
                "images": images,
                "total_media": len(videos) + len(images)
            }
            
        except Exception as e:
            logger.error(f"Error finding media for script: {e}")
            return {
                "success": False,
                "error": str(e),
                "keywords": [],
                "videos": [],
                "images": []
            }
