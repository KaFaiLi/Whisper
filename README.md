# Whisper Turbo Transcription & Translation

This project transcribes audio files in a folder using Whisper Turbo, then translates the Japanese transcription to English using LangChain's ChatOpenAI. Results are saved incrementally to an Excel file.

## Features
- Batch transcribe audio files (mp3, wav, m4a, aac, flac)
- Translate Japanese transcriptions to English using OpenAI's GPT models
- Results are written to Excel after each file is processed (safe for long jobs)
- Parallel processing for efficient throughput

## Workspace Structure
```
Whisper/
├── main.py
├── config.py
├── requirements.txt
├── README.md
└── audio/           # (Place your audio files here)
```

## Setup
1. **Clone the repository**
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set your OpenAI API key**
   - Edit `config.py` and replace `your-openai-api-key-here` with your actual OpenAI API key.

## Usage
1. Place your audio files in a folder (e.g., `audio/`).
2. Run the script:
   ```bash
   python main.py
   ```
3. Enter the path to your audio folder and the desired output Excel filename when prompted.

## Output
- The Excel file will contain three columns: `Filename`, `Transcription` (Japanese), and `Translation` (English).
- Results are appended after each file is processed, so you can safely interrupt and resume.

## Notes
- Make sure your OpenAI API key has access to the GPT model specified in `main.py`.
- For best performance, use a machine with a GPU for Whisper Turbo. 