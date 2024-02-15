import os
from pydub import AudioSegment
from pydub.generators import Sine
import pygame
from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav

'''
TODO: 
* Update voice generation to this: https://github.com/coqui-ai/TTS
* Fetch an image
* Fetch amount of meanings (how? Cambridge dictionary?)
* Fetch voices
* Settings
'''

preload_models()

pygame.mixer.init()

def synthesize_and_play_sound(word):

    audio_array = generate_audio(word)

    # save audio to disk
    write_wav(f"{word}.wav", SAMPLE_RATE, audio_array)
    # synthesized_audio = gTTS(text=word, lang='en', tld="us", slow=0.8)

    # # Save the audio to a file (optional)
    # synthesized_audio.save(f"{word}.mp3")

    # Load the MP3 file
    pygame.mixer.music.load(f"{word}.wav")

    # Play the MP3 file
    pygame.mixer.music.play()

    # Optional: Wait for the song to finish
    while pygame.mixer.music.get_busy():
        pygame.time.wait(100)

# Function to load the history of shown words
def load_history(filename):
    history = set()
    if os.path.exists(filename):
        with open(filename, "r") as f:
            for line in f:
                history.add(line.strip())
    return history

# Function to save the history of shown words
def save_history(history, filename):
    with open(filename, "w") as f:
        for word in history:
            f.write(word + "\n")

# Function to prompt user if they know a word and handle their response
def prompt_user(word):
    while True:
        response = input(f"\n'{word}'").lower()
        if response in ["y", "n", ""]:
            return response == "n"
        else:
            print("Please respond with 'y' or 'n'. Hit enter in case of yes")

# Function to filter out known words and update the file
def filter_file(file_path, history):
    new_lines = []
    with open(file_path, "r") as f:
        for line in f:
            if line not in history:
                new_lines.append(line)
    with open(file_path, "w") as f:
        f.write("".join(new_lines))

def main():
    known_history = load_history("known.txt")
    unknown_history = load_history("unknown.txt")
    file_path = "30k.txt"  # Path to your file with 30k most frequent words
    if not os.path.exists(file_path):
        print("Error: File not found.")
        return

    print("Please, tell yes if you know a word that will appear next. Answer no otherwise.")
    with open(file_path, "r") as f:
        for line in f:
            word = line.strip()
            if word in known_history or word in unknown_history:
                continue
            synthesize_and_play_sound(word)
            if prompt_user(word):
                unknown_history.add(word)
                save_history(unknown_history, "unknown.txt")
            else:
                known_history.add(word)
                filter_file(file_path, known_history)
                save_history(known_history, "known.txt")

    print("Done.")

if __name__ == "__main__":
    main()