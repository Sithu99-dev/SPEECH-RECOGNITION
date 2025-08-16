#!/usr/bin/env python3
"""
Speech Number Recognition Project
Uses OpenAI GPT-4o-mini to recognize and extract numbers from speech
"""

import speech_recognition as sr
import openai
import os
import sys
import json
from typing import Optional, List
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class SpeechNumberRecognizer:
    def __init__(self, openai_api_key: str):
        """
        Initialize the speech number recognizer
        
        Args:
            openai_api_key: Your OpenAI API key
        """
        self.openai_client = openai.OpenAI(api_key=openai_api_key)
        self.recognizer = sr.Recognizer()
        
        # List available microphones and use MacBook's built-in mic
        print("🎤 Available microphones:")
        mic_list = sr.Microphone.list_microphone_names()
        for index, name in enumerate(mic_list):
            print(f"  {index}: {name}")
        
        # Try to use MacBook Air Microphone (index 1) or fallback to default
        try:
            if len(mic_list) > 1 and "MacBook" in mic_list[1]:
                self.microphone = sr.Microphone(device_index=1)
                print("✅ Using MacBook Air Microphone")
            else:
                self.microphone = sr.Microphone()
                print("✅ Using default microphone")
        except:
            self.microphone = sr.Microphone()
            print("✅ Using default microphone")
        
        # Adjust for ambient noise
        print("📊 Calibrating microphone for ambient noise...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        print(f"✅ Microphone calibrated! Energy threshold: {self.recognizer.energy_threshold}")
    
    def capture_speech(self, timeout: int = 10, phrase_time_limit: int = 8) -> Optional[str]:
        """
        Capture speech from microphone
        
        Args:
            timeout: Maximum time to wait for speech to start
            phrase_time_limit: Maximum time for a single phrase
            
        Returns:
            Transcribed text or None if failed
        """
        try:
            print(f"🎤 Listening for speech... Speak NOW! (timeout: {timeout}s)")
            print("💡 Tip: Speak clearly and close to the microphone")
            
            with self.microphone as source:
                # Adjust recognizer settings for better performance
                self.recognizer.energy_threshold = 4000  # Adjust for ambient noise
                self.recognizer.dynamic_energy_threshold = True
                self.recognizer.pause_threshold = 0.8  # Seconds of silence to register as end of phrase
                
                # Listen for audio with timeout
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            
            print("🔄 Processing speech...")
            
            # Use Google Speech Recognition for initial transcription
            text = self.recognizer.recognize_google(audio, language='en-US')
            print(f"✅ Heard: '{text}'")
            return text
            
        except sr.WaitTimeoutError:
            print("⏰ No speech detected - try speaking louder or closer to mic")
            return None
        except sr.UnknownValueError:
            print("❓ Could not understand - try speaking more clearly")
            return None
        except sr.RequestError as e:
            print(f"🌐 Network/API error: {e}")
            return None
    
    def extract_numbers_with_openai(self, text: str) -> List[str]:
        """
        Use OpenAI GPT-4o-mini to extract and interpret numbers from text
        
        Args:
            text: The transcribed speech text
            
        Returns:
            List of recognized numbers
        """
        try:
            prompt = f"""
            Extract all numbers from the following text and convert them to their numeric form.
            Include both written numbers (like "twenty-three") and digit numbers (like "23").
            
            Text: "{text}"
            
            Please respond with a JSON object containing:
            1. "numbers": a list of all numbers found (as strings)
            2. "original_text": the original text
            3. "interpretation": a brief explanation of what numbers were found
            
            Example response format:
            {{
                "numbers": ["23", "456", "7.5"],
                "original_text": "I have twenty-three apples and 456 oranges, plus 7.5 pounds of grapes",
                "interpretation": "Found three numbers: 23 (written as twenty-three), 456 (digits), and 7.5 (decimal)"
            }}
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts numbers from text accurately."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=500
            )
            
            # Parse the JSON response
            response_text = response.choices[0].message.content.strip()
            
            # Try to extract JSON from the response
            try:
                # Look for JSON in the response
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    json_str = json_match.group()
                    result = json.loads(json_str)
                    return result.get("numbers", [])
                else:
                    print("No JSON found in OpenAI response")
                    return []
            except json.JSONDecodeError:
                print(f"Could not parse JSON from OpenAI response: {response_text}")
                return []
                
        except Exception as e:
            print(f"Error with OpenAI API: {e}")
            return []
    
    def run_recognition_session(self):
        """
        Run a continuous speech recognition session
        """
        print("\n" + "="*50)
        print("Speech Number Recognition System")
        print("Powered by OpenAI GPT-4o-mini")
        print("="*50)
        print("\nCommands:")
        print("- Speak numbers and they will be recognized")
        print("- Say 'quit' or 'exit' to stop")
        print("- Press Ctrl+C to force quit")
        print("-"*50)
        
        try:
            while True:
                print("\nReady to listen...")
                
                # Capture speech
                speech_text = self.capture_speech()
                
                if speech_text is None:
                    continue
                
                # Check for quit commands
                if any(word in speech_text.lower() for word in ['quit', 'exit', 'stop']):
                    print("Goodbye!")
                    break
                
                # Extract numbers using OpenAI
                numbers = self.extract_numbers_with_openai(speech_text)
                
                # Display results
                print(f"\n📝 Original speech: '{speech_text}'")
                if numbers:
                    print(f"🔢 Numbers found: {', '.join(numbers)}")
                    print(f"📊 Total numbers detected: {len(numbers)}")
                else:
                    print("❌ No numbers detected in the speech")
                
                print("-" * 30)
                
        except KeyboardInterrupt:
            print("\n\nSession ended by user. Goodbye!")
        except Exception as e:
            print(f"\nUnexpected error: {e}")

def main():
    """Main function to run the application"""
    
    # Check for OpenAI API key
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        print("\nTo set up your API key:")
        print("1. Get your API key from https://platform.openai.com/api-keys")
        print("2. Set it as an environment variable:")
        print("   export OPENAI_API_KEY='your-api-key-here'")
        print("3. Or create a .env file with: OPENAI_API_KEY=your-api-key-here")
        sys.exit(1)
    
    try:
        # Initialize the speech recognizer
        recognizer = SpeechNumberRecognizer(api_key)
        
        # Run the recognition session
        recognizer.run_recognition_session()
        
    except Exception as e:
        print(f"Failed to initialize speech recognizer: {e}")
        print("\nMake sure you have:")
        print("1. A working microphone")
        print("2. Internet connection")
        print("3. Valid OpenAI API key")
        sys.exit(1)

if __name__ == "__main__":
    main()