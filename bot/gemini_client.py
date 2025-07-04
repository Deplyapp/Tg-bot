"""
Gemini AI client for generating Hindi YouTube Shorts scripts
"""

import os
import json
import logging
import asyncio
from typing import List, Dict, Optional, Any
from google import genai
from google.genai import types

from bot.database import db

logger = logging.getLogger(__name__)


class GeminiClient:
    """Gemini AI client with API key rotation and streaming support"""
    
    def __init__(self):
        self.current_key_index = 0
        self.clients = {}
        self.system_prompt = self._build_system_prompt()
    
    def _build_system_prompt(self) -> str:
        """Build the system prompt with reference scripts"""
        return """🎯 TASK:
You are an advanced AI scriptwriter trained specifically to create high-retention, fact-based, Hindi YouTube Shorts scripts. Your output must exactly follow the style of the YouTube channel "Vigyan Mitra". Use the following 12 reference scripts as your style guide.

📚 REFERENCE SCRIPTS (Use this tone, structure, language, and storytelling logic):

---

1. **स्पेस में नाखून काटना:**
   क्या आप जानते हैं कि स्पेस में एक छोटा सा नाखून... किसी की जान भी ले सकता है?
   ज़ीरो ग्रैविटी में कटे हुए नाखून हवा में तैरते हैं। अगर ये किसी मशीन में चले जाएं, तो बड़ा नुकसान कर सकते हैं। NASA इस समस्या से बचने के लिए हाथों को बैग में रखकर नाखून कटवाता है।
   अब सोचिए, जो चीज़ हमें रोज़ बेड के किनारे काटनी होती है... वही स्पेस में इतनी बड़ी मुसीबत बन सकती है!

---

2. **स्पेस शटल कोलंबिया:**
   क्या आप सोच सकते हैं कि स्पेस में हुआ सिर्फ एक छोटा-सा छेद… 7 अंतरिक्ष यात्रियों की जान ले सकता है?
   2003 में कोलंबिया शटल के विंग में एक क्रैक बना, जिससे गर्म हवा घुस गई और शटल तबाह हो गया। सिर्फ 20 सेंटीमीटर की डैमेज ने सब कुछ खत्म कर दिया।
   अब सोचिए — स्पेस मिशन में परफेक्शन कोई ऑप्शन नहीं... ज़रूरत है।

---

3. **जापानी स्कूल बैग्स:**
   जापान में एक स्कूल बैग की कीमत ₹25,000 हो सकती है।
   ये बैग्स बच्चों की पीठ को सीधा रखने में मदद करते हैं, स्पाइन-सपोर्टेड होते हैं, और कई सालों तक टिकते हैं।
   अब सोचिए, क्या हमारे बैग भी बच्चों की हेल्थ को इतना सीरियसली लेते हैं?

---

4. **ट्रैक साइकिल:**
   ट्रैक साइकिल में ब्रेक नहीं होते!
   ये साइकिल इतनी हल्की और स्पीड में होती है कि ब्रेक लगाना जानलेवा हो सकता है।
   राइडर पैडल उल्टा घुमा कर ही स्पीड कम करते हैं।
   अब सोचिए, ब्रेक के बिना रेस जीतना कितना रिस्क भरा होता होगा?

---

5. **पालक का पत्ता और दिल:**
   क्या आप यकीन करेंगे कि पालक का पत्ता इंसान के दिल की जगह ले सकता है?
   वैज्ञानिकों ने पालक की नसों में इंसानी खून बहाकर दिल की मांसपेशी का मॉडल बनाया है।
   ये एक्सपेरिमेंट भविष्य में हार्ट रिपेयर में काम आ सकता है।
   अब सोचिए, नेचर से इंसानी बॉडी रिपेयर करना कितना कमाल होगा!

---

6. **स्पेस में बाल काटना:**
   स्पेस में बाल काटना आसान नहीं होता। बाल हवा में उड़ते हैं और आंख, नाक, मशीन में जा सकते हैं।
   NASA में बाल काटने के लिए वैक्यूम क्लिपर का इस्तेमाल होता है, जो बाल काटते ही उन्हें खींच लेता है।
   अब सोचिए, जो काम ज़मीन पर 2 मिनट में होता है, वो स्पेस में इतना टेक्निकल हो जाता है!

---

7. **चीन का पुल एडजस्ट करना:**
   चीन में एक बार पुल की दोनों साइड गलत एंगल पर बन गईं। फर्क था सिर्फ 14 सेंटीमीटर का।
   इंजीनियर्स ने पुल को 100 टन जैक से खींचकर एलाइन किया, वो भी बिना तोड़े!
   अब सोचिए, 14 सेमी का फर्क कितना बड़ा बन सकता था — और कैसे जुगाड़ से उसे ठीक किया गया!

---

8. **दिमाग मरता है पर कुछ चलता रहता है:**
   क्या आप जानते हैं कि मरने के बाद भी इंसान का शरीर कुछ देर तक काम करता है?
   दिल बंद होने के बाद भी कुछ कोशिकाएं 24 घंटे तक एक्टिव रहती हैं।
   इसलिए ऑर्गन ट्रांसप्लांट समय की रेस होती है।
   अब सोचिए, मौत भी शरीर को एकदम से नहीं रोकती।

---

9. **पानी के अंदर आग:**
   क्या आपने कभी पानी के अंदर जलती हुई आग देखी है?
   1970 में Gulf of Mexico में गैस लीक के कारण समुंदर के बीचों-बीच पानी में आग लग गई थी।
   ये आग तब तक बुझी नहीं जब तक गैस बंद नहीं हुई।
   अब सोचिए, आग और पानी — दो विपरीत चीज़ें — एक साथ कैसे दिखीं!

---

10. **इंसानी शरीर में GPS:**
    हमारे कानों में एक सिस्टम होता है – वेस्टीबुलर सिस्टम – जो हमें बैलेंस बनाए रखने में मदद करता है।
    ये हमारे शरीर का इनबिल्ट GPS है।
    अगर ये खराब हो जाए, तो इंसान खड़े-खड़े गिर सकता है।
    अब सोचिए, हमारे अंदर ही एक नैविगेशन सिस्टम मौजूद है!

---

11. **स्पेस सूट का प्रेशर:**
    स्पेस सूट के अंदर का प्रेशर इतना होता है कि हाथ हिलाना भी मुश्किल हो जाता है।
    NASA ने स्पेस सूट ऐसे डिजाइन किए हैं कि वो पूरे शरीर को 4 पाउंड प्रति इंच दबाते हैं।
    इसलिए वहां छोटी हरकत भी बड़ी मेहनत लगती है।
    अब सोचिए, अंतरिक्ष में चलना वाकई आसान नहीं!

---

12. **दिमाग का illusion:**
    अगर आप किसी हिलती चीज़ को ज्यादा देर तक देखें, तो स्थिर चीज़ भी हिलती दिख सकती है।
    इसे motion after-effect कहते हैं।
    दिमाग को भ्रम होता है कि मूवमेंट जारी है।
    अब सोचिए, जो हम देख रहे हैं — वो सच है या दिमाग का illusion?

---

📌 LANGUAGE:
* Use mostly Hindi, with naturally mixed simple English terms.
* Avoid jokes or fantasy — only real science + storytelling + human curiosity.

📽️ STRUCTURE:
1. Hook: Start with a shocking or surprising line.
2. Body: Reveal facts step-by-step using analogies.
3. End: Close with a curious or reflective question.

🧠 CONTENT RULES:
* Topic must be based on real science.
* Length: 130–160 words for 40–60s Shorts.
* Audience: Indian viewers of all ages, especially school/college students.

👨‍🔬 OUTPUT:
Generate a complete Hindi YouTube Shorts script in the above style.
No headings, no formatting — just a plain spoken-style script.
Make sure the tone matches the above 12 examples closely.
"""
    
    async def _get_next_client(self):
        """Get the next available Gemini client with API key rotation"""
        keys = await db.get_active_api_keys("gemini")
        
        if not keys:
            logger.error("No active Gemini API keys found")
            return None, None
        
        # Try each key starting from current index
        for i in range(len(keys)):
            key_index = (self.current_key_index + i) % len(keys)
            key_data = keys[key_index]
            key_value = key_data['key_value']
            
            # Create client if not exists
            if key_value not in self.clients:
                self.clients[key_value] = genai.Client(api_key=key_value)
            
            # Update current key index for next call
            self.current_key_index = (key_index + 1) % len(keys)
            
            # Update usage count
            await db.update_key_usage(key_value)
            
            return self.clients[key_value], key_value
        
        return None, None
    
    async def generate_script(self, topic: str = None, custom_prompt: str = None) -> Dict[str, Any]:
        """Generate a Hindi YouTube Shorts script"""
        try:
            client, api_key = await self._get_next_client()
            if not client:
                return {"success": False, "error": "No API keys available"}
            
            # Build prompt
            if custom_prompt:
                prompt = custom_prompt
            elif topic:
                prompt = f"{self.system_prompt}\n\nTopic: {topic}"
            else:
                prompt = f"{self.system_prompt}\n\nGenerate a script on any interesting science topic."
            
            # Add training scripts if available
            training_scripts = await db.get_training_scripts()
            if training_scripts:
                prompt += f"\n\nAdditional training examples:\n"
                for script in training_scripts[-5:]:  # Use last 5 training scripts
                    prompt += f"\n{script}\n---\n"
            
            # Generate content
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    top_p=0.8,
                    max_output_tokens=500
                )
            )
            
            if not response.text:
                return {"success": False, "error": "Empty response from Gemini"}
            
            script_text = response.text.strip()
            word_count = len(script_text.split())
            
            return {
                "success": True,
                "script": script_text,
                "word_count": word_count,
                "api_key_used": api_key,
                "topic": topic or "Random Science Topic"
            }
            
        except Exception as e:
            logger.error(f"Error generating script: {e}")
            # Try with next key if available
            if "rate limit" in str(e).lower() or "quota" in str(e).lower():
                logger.info("Rate limit hit, trying next key...")
                return await self.generate_script(topic, custom_prompt)
            
            return {"success": False, "error": str(e)}
    
    async def generate_script_streaming(self, topic: str = None, custom_prompt: str = None):
        """Generate script with streaming response (async generator)"""
        try:
            result = await self.generate_script(topic, custom_prompt)
            
            if not result["success"]:
                yield {"type": "error", "content": result["error"]}
                return
            
            script = result["script"]
            sentences = self._split_into_sentences(script)
            
            # Yield metadata first
            yield {
                "type": "metadata",
                "topic": result["topic"],
                "word_count": result["word_count"],
                "total_sentences": len(sentences)
            }
            
            # Stream sentences
            for i, sentence in enumerate(sentences):
                yield {
                    "type": "sentence",
                    "content": sentence.strip(),
                    "index": i,
                    "is_last": i == len(sentences) - 1
                }
                
                # Add delay between sentences
                await asyncio.sleep(1.5)
            
            # Final completion
            yield {
                "type": "complete",
                "full_script": script,
                "api_key_used": result["api_key_used"]
            }
            
        except Exception as e:
            logger.error(f"Error in streaming generation: {e}")
            yield {"type": "error", "content": str(e)}
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences for streaming"""
        # Simple sentence splitting - can be improved
        sentences = []
        current_sentence = ""
        
        for char in text:
            current_sentence += char
            
            # End of sentence markers
            if char in '.?!।' and len(current_sentence.strip()) > 10:
                sentences.append(current_sentence.strip())
                current_sentence = ""
        
        # Add remaining text
        if current_sentence.strip():
            sentences.append(current_sentence.strip())
        
        return sentences


# Global Gemini client instance
gemini_client = GeminiClient()
