#!/usr/bin/env python3
"""
Simple Voice Math Tutor (TTS-Free Version)
Focus on excellent speech recognition and math learning
Alternative: Uses system 'say' command for macOS or text-only mode
"""

import speech_recognition as sr
import openai
import os
import sys
import json
import random
import re
import time
import subprocess
from typing import Optional, Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SimpleVoiceMathTutor:
    def __init__(self, openai_api_key: str):
        """Initialize the Simple Voice Math Tutor"""
        self.openai_client = openai.OpenAI(api_key=openai_api_key)
        self.recognizer = sr.Recognizer()
        
        # Check for system TTS alternatives
        self.setup_voice_system()
        
        # Setup microphone
        self.setup_microphone()
        
        # Statistics
        self.stats = {
            'total_questions': 0,
            'correct_answers': 0,
            'wrong_answers': 0,
            'questions_history': []
        }
        
        # Simple difficulty
        self.difficulty_levels = {
            'easy': {'range': (0, 5), 'operations': ['+', '-']},
            'medium': {'range': (0, 10), 'operations': ['+', '-']},
            'hard': {'range': (0, 15), 'operations': ['+', '-', '*']}
        }
        self.current_difficulty = 'easy'
        self.current_question = None
    
    def setup_voice_system(self):
        """Setup voice system using macOS 'say' command or text-only"""
        print("🔊 Setting up voice system...")
        
        # Try macOS 'say' command (much more reliable)
        try:
            # Test if 'say' command works
            result = subprocess.run(['say', 'test'], 
                                  capture_output=True, 
                                  timeout=3, 
                                  check=True)
            self.voice_method = 'macos_say'
            print("✅ Using macOS 'say' command for voice")
            
            # Get available voices
            try:
                result = subprocess.run(['say', '-v', '?'], 
                                      capture_output=True, 
                                      text=True, 
                                      timeout=5)
                voices = result.stdout.strip().split('\n')
                print(f"🔊 Found {len(voices)} macOS voices")
                
                # Look for female voices
                self.selected_voice = None
                for voice_line in voices:
                    voice_name = voice_line.split()[0] if voice_line else ""
                    if any(name in voice_name.lower() for name in ['samantha', 'alex', 'allison', 'ava', 'karen', 'susan', 'victoria']):
                        self.selected_voice = voice_name
                        print(f"✅ Selected female voice: {voice_name}")
                        break
                
                if not self.selected_voice:
                    # Default to Samantha if available, otherwise use system default
                    if any('samantha' in voice.lower() for voice in voices):
                        self.selected_voice = 'Samantha'
                    print(f"✅ Using voice: {self.selected_voice or 'system default'}")
                        
            except Exception as e:
                print(f"⚠️ Could not get voice list: {e}")
                self.selected_voice = 'Samantha'  # Default
                
        except Exception as e:
            print(f"⚠️ macOS 'say' command not available: {e}")
            self.voice_method = 'text_only'
            print("📖 Using text-only mode")
    
    def speak(self, text: str):
        """Speak text using the best available method"""
        print(f"🔊 AI: {text}")
        
        if self.voice_method == 'macos_say':
            try:
                # Use macOS 'say' command with slower speech
                cmd = ['say']
                if self.selected_voice:
                    cmd.extend(['-v', self.selected_voice])
                cmd.extend(['-r', '120'])  # Slow speech rate
                cmd.append(text)
                
                # Run the say command
                subprocess.run(cmd, timeout=10, check=True)
                print("✅ Speech completed")
                
            except subprocess.TimeoutExpired:
                print("⚠️ Speech timeout")
            except Exception as e:
                print(f"⚠️ Speech error: {e}")
        
        elif self.voice_method == 'text_only':
            # Text-only mode with emphasis
            print(f"📖 PLEASE READ: {text.upper()}")
            time.sleep(2)  # Give time to read
    
    def setup_microphone(self):
        """Setup microphone with optimal settings"""
        print("🎤 Setting up microphone...")
        
        try:
            # List microphones
            mic_list = sr.Microphone.list_microphone_names()
            print("Available microphones:")
            for index, name in enumerate(mic_list):
                print(f"  {index}: {name}")
            
            # Smart selection: prefer MacBook Air Microphone
            best_mic = None
            for i, name in enumerate(mic_list):
                if "MacBook Air Microphone" in name:
                    best_mic = i
                    break
                elif "MacBook" in name and "Microphone" in name:
                    best_mic = i
            
            if best_mic is not None:
                self.microphone = sr.Microphone(device_index=best_mic)
                print(f"✅ Using: {mic_list[best_mic]}")
            else:
                self.microphone = sr.Microphone()
                print("✅ Using default microphone")
            
            # Optimal settings
            self.recognizer.energy_threshold = 300
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 1.0
            self.recognizer.phrase_threshold = 0.3
            
            # Calibrate
            print("📊 Calibrating microphone (stay quiet for 3 seconds)...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=3)
            
            print(f"✅ Calibrated! Energy: {self.recognizer.energy_threshold:.1f}")
            
        except Exception as e:
            print(f"⚠️ Microphone setup error: {e}")
            self.microphone = sr.Microphone()
    
    def listen_for_answer(self, timeout: int = 15) -> Optional[str]:
        """Listen for user's answer"""
        try:
            print("🎤 Listening for your answer... (speak clearly)")
            print("💡 Say just the number (like 'two' or 'five')")
            
            with self.microphone as source:
                # Quick ambient adjustment
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Listen
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=8)
            
            print("🔄 Processing your speech...")
            
            # Try recognition with multiple attempts
            try:
                # Primary attempt
                text = self.recognizer.recognize_google(audio, language='en-US')
                print(f"✅ You said: '{text}'")
                return text.strip()
                
            except sr.UnknownValueError:
                # Try with different settings
                try:
                    text = self.recognizer.recognize_google(audio, language='en-US', show_all=True)
                    if text and 'alternative' in text:
                        best = text['alternative'][0]['transcript']
                        print(f"✅ You said (alt): '{best}'")
                        return best.strip()
                except:
                    pass
                    
                print("❓ Could not understand - please try again")
                return None
                
        except sr.WaitTimeoutError:
            print("⏰ No speech detected - please speak louder")
            return None
        except Exception as e:
            print(f"❌ Listening error: {e}")
            return None
    
    def extract_number(self, speech: str) -> Optional[int]:
        """Extract number from speech with comprehensive matching"""
        if not speech:
            return None
            
        speech_lower = speech.lower().strip()
        print(f"🔍 Analyzing: '{speech_lower}'")
        
        # Comprehensive number mapping including common mishearings
        number_words = {
            # Standard numbers
            'zero': 0, 'oh': 0,
            'one': 1, 'won': 1, 'wan': 1,
            'two': 2, 'to': 2, 'too': 2, 'tu': 2,
            'three': 3, 'tree': 3, 'free': 3,
            'four': 4, 'for': 4, 'fore': 4, 'floor': 4,
            'five': 5, 'hive': 5, 'dive': 5,
            'six': 6, 'sex': 6, 'sicks': 6, 'sick': 6,
            'seven': 7, 'heaven': 7, 'eleven': 7,  # sometimes misheard
            'eight': 8, 'ate': 8, 'weight': 8, 'gate': 8,
            'nine': 9, 'wine': 9, 'nein': 9, 'mine': 9,
            'ten': 10, 'pen': 10, 'hen': 10,
            'eleven': 11, 'twelve': 12, 'thirteen': 13,
            'fourteen': 14, 'fifteen': 15, 'sixteen': 16,
            'seventeen': 17, 'eighteen': 18, 'nineteen': 19,
            'twenty': 20, 'thirty': 30, 'forty': 40, 'fifty': 50
        }
        
        # Direct word match
        for word, value in number_words.items():
            if word in speech_lower:
                print(f"✅ Found '{word}' = {value}")
                return value
        
        # Digit search
        digit_match = re.search(r'\b(\d+)\b', speech)
        if digit_match:
            number = int(digit_match.group(1))
            print(f"✅ Found digit: {number}")
            return number
        
        # Phonetic variations
        phonetic_map = {
            'to': 2, 'too': 2, 'tue': 2,
            'for': 4, 'fore': 4, 'four': 4,
            'ate': 8, 'weight': 8,
            'won': 1, 'one': 1,
            'tree': 3, 'free': 3,
            'hive': 5, 'five': 5,
            'sex': 6, 'six': 6, 'sicks': 6,
            'heaven': 7, 'seven': 7,
            'wine': 9, 'nine': 9, 'mine': 9,
            'pen': 10, 'ten': 10
        }
        
        for word, value in phonetic_map.items():
            if word in speech_lower:
                print(f"✅ Phonetic match '{word}' = {value}")
                return value
        
        print(f"❌ No number found in '{speech_lower}'")
        return None
    
    def generate_question(self) -> Dict:
        """Generate a simple math question"""
        config = self.difficulty_levels[self.current_difficulty]
        min_val, max_val = config['range']
        operations = config['operations']
        
        operation = random.choice(operations)
        
        if operation == '+':
            a = random.randint(min_val, max_val)
            b = random.randint(min_val, max_val)
            # Keep answers reasonable
            if a + b > 12:
                a, b = random.randint(0, 3), random.randint(0, 3)
            answer = a + b
            question = f"{a} plus {b}"
            expression = f"{a} + {b}"
            
        elif operation == '-':
            b = random.randint(min_val, max_val)
            a = random.randint(b, max_val + 3)
            answer = a - b
            question = f"{a} minus {b}"
            expression = f"{a} - {b}"
            
        elif operation == '*':
            a = random.randint(1, 5)
            b = random.randint(1, 5)
            answer = a * b
            question = f"{a} times {b}"
            expression = f"{a} × {b}"
        
        return {
            'question': question,
            'expression': expression,
            'answer': answer,
            'operation': operation
        }
    
    def ask_question(self, question_data: Dict) -> bool:
        """Ask a question and get the answer"""
        self.current_question = question_data
        max_attempts = 3
        
        for attempt in range(max_attempts):
            # Ask the question
            if attempt == 0:
                question_text = f"What is {question_data['question']}?"
                print(f"\n❓ Question #{self.stats['total_questions']}: {question_text}")
                print(f"   📝 {question_data['expression']} = ?")
                self.speak(question_text)
            else:
                retry_text = f"Try again. What is {question_data['question']}?"
                print(f"\n🔄 Attempt {attempt + 1}: {retry_text}")
                self.speak(retry_text)
            
            # Listen for answer
            user_speech = self.listen_for_answer()
            
            if user_speech is None:
                if attempt < max_attempts - 1:
                    self.speak("I didn't hear you. Let me ask again.")
                    continue
                else:
                    # Give the answer
                    correct_msg = f"The answer is {question_data['answer']}."
                    self.speak(correct_msg)
                    return False
            
            # Check for quit
            if any(word in user_speech.lower() for word in ['quit', 'exit', 'stop']):
                return "quit"
            
            # Extract the number
            user_answer = self.extract_number(user_speech)
            correct_answer = question_data['answer']
            
            if user_answer is None:
                if attempt < max_attempts - 1:
                    self.speak("Please say just the number. For example, say 'five' or 'three'.")
                    continue
                else:
                    self.speak(f"The answer is {correct_answer}. Let's try another question.")
                    return False
            
            # Check if correct
            if user_answer == correct_answer:
                # Correct!
                responses = [
                    f"Excellent! {correct_answer} is correct!",
                    f"Perfect! The answer is {correct_answer}!",
                    f"Great job! {correct_answer} is right!",
                    f"Well done! {correct_answer} is the answer!"
                ]
                self.speak(random.choice(responses))
                return True
            else:
                # Wrong answer
                if attempt < max_attempts - 1:
                    self.speak(f"Not quite. You said {user_answer}. Try again.")
                else:
                    self.speak(f"The correct answer is {correct_answer}. You said {user_answer}.")
                    return False
        
        return False
    
    def show_stats(self):
        """Show statistics"""
        total = self.stats['total_questions']
        correct = self.stats['correct_answers']
        wrong = self.stats['wrong_answers']
        
        if total > 0:
            accuracy = (correct / total) * 100
            print(f"\n📊 Your Progress:")
            print(f"   Questions: {total}")
            print(f"   Correct: {correct}")
            print(f"   Wrong: {wrong}")
            print(f"   Accuracy: {accuracy:.1f}%")
            
            stats_msg = f"You got {correct} out of {total} questions correct. That's {accuracy:.0f} percent!"
            self.speak(stats_msg)
    
    def run_session(self):
        """Main tutoring session"""
        print("\n" + "="*60)
        print("🎓 SIMPLE VOICE MATH TUTOR")
        print("   Reliable Speech Recognition • Simple Questions")
        print("="*60)
        
        # Welcome
        welcome = "Hello! I'm your math tutor."
        self.speak(welcome)
        
        instructions = "I'll ask simple math questions. Say just the number answer."
        self.speak(instructions)
        
        print("\n📋 Instructions:")
        print("   ✅ Listen to the question")
        print("   ✅ Say just the number (like 'three' or 'seven')")
        print("   ✅ Speak clearly and close to microphone")
        print("   ✅ Say 'quit' to exit anytime")
        print("-" * 60)
        
        # Brief pause
        time.sleep(2)
        
        try:
            while True:
                # Generate question
                question_data = self.generate_question()
                self.stats['total_questions'] += 1
                
                # Ask the question
                result = self.ask_question(question_data)
                
                if result == "quit":
                    self.speak("Goodbye! Great job practicing math!")
                    break
                elif result:
                    self.stats['correct_answers'] += 1
                else:
                    self.stats['wrong_answers'] += 1
                
                # Show progress every 5 questions
                if self.stats['total_questions'] % 5 == 0:
                    self.show_stats()
                
                # Pause between questions
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n👋 Session ended by user")
            self.speak("Goodbye!")
        
        finally:
            if self.stats['total_questions'] > 0:
                print("\n" + "="*50)
                print("📊 FINAL RESULTS")
                print("="*50)
                self.show_stats()

def main():
    """Main function"""
    # Check API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY not found!")
        print("Create .env file with: OPENAI_API_KEY=your-key")
        sys.exit(1)
    
    print("🚀 Starting Simple Voice Math Tutor...")
    
    try:
        tutor = SimpleVoiceMathTutor(api_key)
        tutor.run_session()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Install: pip install openai speechrecognition python-dotenv pyaudio")

if __name__ == "__main__":
    main()