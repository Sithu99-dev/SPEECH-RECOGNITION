# 🎤 Speech Number Recognition System

A Python application that listens to your voice and extracts numbers using OpenAI's GPT-4o-mini model.

## 🎯 What This App Does

- **Listens to your speech** through your microphone
- **Converts speech to text** using Google Speech Recognition
- **Extracts numbers** using OpenAI GPT-4o-mini AI model
- **Supports multiple formats**: "twenty-three" → 23, "forty-seven fifty" → 47, 50
- **Works on Mac and Windows**

## 📋 Prerequisites

- **Computer**: Mac (Intel/M1/M2/M3) or Windows 10/11
- **Python 3.7+**
- **Working microphone** and internet connection
- **OpenAI API key** (free tier available)

## 🚀 Installation Guide

### 📱 **For Mac Users**

#### 1. Install System Dependencies

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install PortAudio (required for microphone)
brew install portaudio

# Install Python (if needed)
brew install python@3.11
```

#### 2. Set Up Project

```bash
# Navigate to your project folder
cd /path/to/your/project

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) in your prompt
```

#### 3. Install Python Packages

```bash
# Update pip
pip install --upgrade pip

# For M1/M2/M3 Macs - install PyAudio with specific flags
CPPFLAGS=-I/opt/homebrew/include LDFLAGS=-L/opt/homebrew/lib pip install pyaudio

# Install other packages
pip install SpeechRecognition openai python-dotenv

# OR install all at once from requirements.txt
pip install -r requirements.txt
```

#### 4. Set Microphone Permissions

1. Go to **System Settings** → **Privacy & Security** → **Microphone**
2. Enable **Terminal** (or your terminal app)

### 🖥️ **For Windows Users**

#### 1. Install Python

1. Go to [python.org](https://www.python.org/downloads/)
2. Download Python 3.11+
3. **IMPORTANT**: Check "Add Python to PATH" during installation
4. Verify: Open Command Prompt and type `python --version`

#### 2. Set Up Project

```cmd
# Open Command Prompt (Win + R, type cmd)
# Navigate to your project folder
cd C:\Users\YourName\Documents\your-project

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# You should see (venv) in your prompt
```

#### 3. Install Python Packages

```cmd
# Update pip
python -m pip install --upgrade pip

# Install packages
pip install pyaudio SpeechRecognition openai python-dotenv

# OR install from requirements.txt
pip install -r requirements.txt
```

**If PyAudio fails on Windows:**

```cmd
# Method 1: Use pipwin
pip install pipwin
pipwin install pyaudio

# Method 2: Use conda
# Install Anaconda/Miniconda first, then:
conda install pyaudio
```

#### 4. Set Microphone Permissions

1. Go to **Settings** → **Privacy & security** → **Microphone**
2. Turn **ON** "Microphone access"
3. Turn **ON** "Let desktop apps access your microphone"

## 🔑 API Key Setup

### 1. Get OpenAI API Key

1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)

### 2. Configure API Key

**Create .env file in your project folder:**

**Mac:**

```bash
nano .env
```

**Windows:**

```cmd
notepad .env
```

**Add this line (replace with your actual key):**

```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

Save and close the file.

## 📁 Project Files

Create these files in your project folder:

### requirements.txt

```
openai>=1.0.0
SpeechRecognition>=3.10.0
pyaudio>=0.2.11
python-dotenv>=1.0.0
typing-extensions>=4.0.0
```

### speech_numbers.py

_(The main Python script - copy the full code provided)_

### .env

```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

## 🎮 Usage

### Starting the Application

**Mac:**

```bash
cd /path/to/your/project
source venv/bin/activate
python3 speech_numbers.py
```

**Windows:**

```cmd
cd C:\path\to\your\project
venv\Scripts\activate
python speech_numbers.py
```

### What You'll See

```
==================================================
Speech Number Recognition System
Powered by OpenAI GPT-4o-mini
==================================================

🎤 Available microphones:
  0: External Microphone
  1: MacBook Air Microphone
✅ Using MacBook Air Microphone

Ready to listen...
🎤 Listening for speech... Speak NOW!
```

### Example Usage

```
✅ Heard: 'I have twenty-three apples and forty-seven oranges'

📝 Original speech: 'I have twenty-three apples and forty-seven oranges'
🔢 Numbers found: 23, 47
📊 Total numbers detected: 2
------------------------------
```

### Test Phrases

Try saying these:

- **"One two three four five"**
- **"I have twenty-five dollars"**
- **"The price is forty-seven fifty"**
- **"Call me at five five five one two three four"**
- **"I need ninety-nine apples and seven oranges"**

### Exiting

- Say **"quit"** or **"exit"**
- Press **Ctrl+C**

## 💡 Speaking Tips

### For Best Results

- **Speak clearly** and at normal pace
- **Get close to microphone** (6-12 inches)
- **Reduce background noise** (close windows, turn off fans)
- **Speak louder** than normal conversation
- **Use natural sentences**: "I have twenty-three apples"

### Number Formats Supported

- **Written numbers**: "twenty-three", "forty-seven", "ninety-nine"
- **Digits**: "23", "47", "99"
- **Decimals**: "seven point five", "99.99"
- **Phone numbers**: "five five five one two three four"
- **Mixed**: "I need 25 apples and forty-seven oranges"

## 🔧 Troubleshooting

### Common Issues

#### "No module named 'speech_recognition'"

```bash
# Make sure virtual environment is activated
# Mac:
source venv/bin/activate

# Windows:
venv\Scripts\activate

# Reinstall packages
pip install -r requirements.txt
```

#### "Could not understand the audio"

1. **Check microphone permissions**
2. **Test with this command:**
   ```bash
   python test_mic.py  # (if you have the test file)
   ```
3. **Speak closer and louder**
4. **Reduce background noise**

#### "OPENAI_API_KEY not set"

```bash
# Check if .env file exists
# Mac:
ls -la .env
cat .env

# Windows:
dir .env
type .env

# Should show: OPENAI_API_KEY=sk-your-key-here
```

#### PyAudio Installation Issues

**Mac (M1/M2/M3):**

```bash
brew install portaudio
CPPFLAGS=-I/opt/homebrew/include LDFLAGS=-L/opt/homebrew/lib pip install pyaudio
```

**Windows:**

```cmd
pip install pipwin
pipwin install pyaudio
```

#### Python Not Found (Windows)

1. Reinstall Python with "Add to PATH" checked
2. Or manually add Python to PATH in Environment Variables

### Platform-Specific Issues

#### Mac Issues

- **Microphone permission denied**: Check System Settings → Privacy → Microphone
- **"xcrun: error"**: Install Xcode command line tools: `xcode-select --install`
- **Homebrew issues**: Reinstall Homebrew

#### Windows Issues

- **Antivirus blocking**: Add Python folder to antivirus exclusions
- **Windows Defender**: Allow Python through Windows Defender Firewall
- **Corporate networks**: May block OpenAI API calls

## 🧪 Testing

### Quick Microphone Test

Create `test_mic.py`:

```python
import speech_recognition as sr

r = sr.Recognizer()
mic = sr.Microphone()

print("Say 'hello'...")
with mic as source:
    audio = r.listen(source, timeout=5)

try:
    text = r.recognize_google(audio)
    print(f"You said: {text}")
except:
    print("Could not understand")
```

Run: `python test_mic.py`

### Package Test

```bash
python -c "import speech_recognition, openai; print('✅ All packages working!')"
```

## 🚀 Advanced Usage

### Custom Microphone Selection

The app automatically selects the best microphone, but you can create a chooser script:

```python
import speech_recognition as sr

# List all microphones
for i, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"{i}: {name}")

# Use specific microphone
mic = sr.Microphone(device_index=1)  # Use microphone #1
```

### Batch Processing (Windows)

Create `run_app.bat`:

```batch
@echo off
cd /d "%~dp0"
call venv\Scripts\activate
python speech_numbers.py
pause
```

## 📊 Performance Tips

### Optimize Recognition

- **Close audio apps** (Zoom, Discord, Spotify)
- **Use wired headset** if built-in mic isn't working well
- **Stable internet** for OpenAI API calls
- **Quiet environment** for better speech recognition

### Cost Management

- OpenAI GPT-4o-mini is very affordable
- Each recognition costs approximately $0.001-0.002
- Monitor usage at [OpenAI Usage Dashboard](https://platform.openai.com/usage)

## 🔍 File Structure

```
your-project/
├── speech_numbers.py      # Main application
├── requirements.txt       # Python dependencies
├── .env                  # API key (keep private!)
├── README.md             # This file
├── test_mic.py           # Microphone test (optional)
├── venv/                 # Virtual environment folder
└── run_app.bat           # Windows launcher (optional)
```

## 🆘 Getting Help

### Useful Commands

```bash
# Check Python version
python --version

# Check installed packages
pip list

# Check virtual environment
which python  # Mac
where python  # Windows

# Test microphone
python test_mic.py
```

### Support Resources

- [OpenAI Documentation](https://platform.openai.com/docs)
- [SpeechRecognition Library](https://pypi.org/project/SpeechRecognition/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)

## 📄 License

This project is provided as-is for educational and personal use.

## 🎉 Success!

Once everything is working, you should be able to:

1. **Start the application**
2. **Speak numbers naturally**
3. **See them extracted and displayed**
4. **Use in real applications** like voice-controlled calculators, data entry, etc.

---

**Enjoy your speech number recognition system! 🎤🔢**
