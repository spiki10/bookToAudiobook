import fitz  # PyMuPDF
from gtts import gTTS
import os
import time
from tqdm import tqdm
from pydub import AudioSegment
import winsound  # For sound notification
from plyer import notification  # For desktop alerts

# Step 1: Extract text from the PDF
def extract_text_from_pdf(pdf_path):
    try:
        pdf_document = fitz.open(pdf_path)
        full_text = ""
        print("Extracting text from PDF...")
        for page_number in tqdm(range(len(pdf_document)), desc="Pages processed"):
            page = pdf_document[page_number]
            full_text += page.get_text() + "\n"  # Add newline for readability
        pdf_document.close()
        return full_text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

# Step 2: Split text into manageable chunks
def split_text_into_chunks(text, max_chars=4000):
    chunks = []
    while len(text) > max_chars:
        split_index = text[:max_chars].rfind(" ")  # Split at the last space
        chunks.append(text[:split_index])
        text = text[split_index:]
    chunks.append(text)
    return chunks

# Step 3: Convert text to audio
def text_to_audio(text, output_audio_path):
    try:
        chunks = split_text_into_chunks(text)
        print("Converting text to audio...")
        for i, chunk in enumerate(tqdm(chunks, desc="Audio chunks processed")):
            tts = gTTS(text=chunk, lang='en')
            chunk_file = f"{output_audio_path}_part{i+1}.mp3"
            tts.save(chunk_file)
            print(f"Chunk {i+1} saved as: {chunk_file}")
            time.sleep(2)  # Pauza od 2 sekunde između zahteva
        return len(chunks)
    except Exception as e:
        print(f"Error during text-to-speech conversion: {e}"

# Step 4: Merge audio files
def merge_audio_chunks(output_audio_path, total_chunks):
    try:
        merged_audio = AudioSegment.empty()
        print("Merging audio chunks...")
        for i in range(total_chunks):
            chunk_file = f"{output_audio_path}_part{i+1}.mp3"
            merged_audio += AudioSegment.from_file(chunk_file)
            os.remove(chunk_file)  # Clean up individual chunk files
        merged_audio.export(output_audio_path, format="mp3")
        print(f"Final audiobook saved as: {output_audio_path}")
    except Exception as e:
        print(f"Error during audio merging: {e}")

# Completion notifications
def notify_completion(output_audio_path):
    # Print completion message
    print(f"\n🎉 Audiobook creation complete! File saved as: {output_audio_path}")
    
    # Play a sound notification (Windows beep)
    winsound.MessageBeep(winsound.MB_ICONASTERISK)
    
    # Show desktop notification
    notification.notify(
        title="Audiobook Ready",
        message=f"Your audiobook has been created: {output_audio_path}",
        app_name="Audiobook Creator",
        timeout=10  # Notification duration in seconds
    )

# Main script
def pdf_to_audiobook(pdf_path, output_audio_path):
    text = extract_text_from_pdf(pdf_path)
    if text.strip():
        print("Text extracted successfully.")
        total_chunks = text_to_audio(text, output_audio_path)
        merge_audio_chunks(output_audio_path, total_chunks)
        notify_completion(output_audio_path)
    else:
        print("No text found in the PDF.")

# Example usage
if __name__ == "__main__":
    # Provide the file path to your PDF
    pdf_path = r"C:\Users\dzafi\Downloads\Jonathan Mind_ Alejandro Mendoza_ Melanie Blackwood_ Shannon Mac - Dark Psychology_ 9 IN 1_ The Complete Body Language Guide to Take Full Control Of Your Life And Make Your Mind Inaccessible From.pdf"
    
    # Specify the desired output audio file name
    output_audio_path = r"C:\Users\dzafi\OneDrive\Desktop\AudioBook\audiobook.mp3"
    
    # Convert the PDF to an audiobook
    pdf_to_audiobook(pdf_path, output_audio_path)
