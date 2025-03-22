import os
import whisper
import pandas as pd

def transcribe_folder(folder_path, output_excel_file):
    """
    Transcribes all audio files in a folder using Whisper Turbo and saves the results to an Excel file.

    Args:
        folder_path (str): The path to the folder containing the audio files.
        output_excel_file (str): The name of the Excel file to save the results to.
    """
    audio_files = [f for f in os.listdir(folder_path) if f.endswith(('.mp3', '.wav', '.m4a', '.aac', '.flac'))]
    if not audio_files:
        print(f"No audio files found in the folder: {folder_path}")
        return

    model = whisper.load_model("whisper-turbo")
    results =

    for filename in audio_files:
        file_path = os.path.join(folder_path, filename)
        print(f"Transcribing: {filename}")
        try:
            transcript = model.transcribe(file_path)
            results.append({'Filename': filename, 'Transcription': transcript['text']})
            print(f"Transcription of {filename} complete.")
        except Exception as e:
            print(f"Error transcribing {filename}: {e}")
            results.append({'Filename': filename, 'Transcription': f"Error: {e}"})

    df = pd.DataFrame(results)
    try:
        df.to_excel(output_excel_file, index=False)
        print(f"Transcription results saved to: {output_excel_file}")
    except Exception as e:
        print(f"Error saving to Excel file: {e}")

if __name__ == "__main__":
    folder_path = input("Enter the path to the folder containing the audio files: ")
    output_excel_file = input("Enter the name for the output Excel file (e.g., transcriptions.xlsx): ")
    transcribe_folder(folder_path, output_excel_file)
