#!/usr/bin/env python3
"""
Very simple microphone test
"""

import speech_recognition as sr
import sys

def simple_test():
    print("🔍 Simple Microphone Test")
    print("=" * 30)
    
    r = sr.Recognizer()
    
    # Try to list microphones
    try:
        mics = sr.Microphone.list_microphone_names()
        print(f"📱 Found {len(mics)} microphones:")
        for i, name in enumerate(mics):
            print(f"  {i}: {name}")
    except Exception as e:
        print(f"❌ Error listing microphones: {e}")
        return
    
    # Test default microphone
    try:
        mic = sr.Microphone()
        print(f"\n🎤 Using default microphone")
    except Exception as e:
        print(f"❌ Error accessing microphone: {e}")
        print("💡 Try: brew install portaudio")
        return
    
    # Calibrate
    print("\n📊 Calibrating... (be quiet for 2 seconds)")
    try:
        with mic as source:
            r.adjust_for_ambient_noise(source, duration=2)
        print(f"✅ Energy threshold: {r.energy_threshold}")
    except Exception as e:
        print(f"❌ Calibration error: {e}")
        return
    
    # Simple test
    print("\n🗣️  Say 'HELLO' loudly and clearly")
    input("Press Enter when ready...")
    
    try:
        with mic as source:
            print("🎤 Listening for 5 seconds...")
            audio = r.listen(source, timeout=5, phrase_time_limit=3)
            print("📡 Audio captured!")
        
        print("🔄 Converting to text...")
        
        # Try multiple recognition services
        results = {}
        
        try:
            text = r.recognize_google(audio)
            results["Google"] = text
        except Exception as e:
            results["Google"] = f"Error: {e}"
        
        try:
            text = r.recognize_sphinx(audio)
            results["Sphinx"] = text
        except Exception as e:
            results["Sphinx"] = f"Error: {e}"
        
        print("\n📝 Results:")
        for service, result in results.items():
            print(f"  {service}: {result}")
        
    except sr.WaitTimeoutError:
        print("⏰ No speech detected")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    simple_test()