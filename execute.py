import os
import pygame
from gtts import gTTS
from pathlib import Path

'''
TODO: 
* Fetch an image
* Fetch amount of meanings (how? Cambridge dictionary?)
* Fetch voices
* Settings
'''

pygame.mixer.init()

def synthesize_and_play_sound(word):

    synthesized_audio = gTTS(text=word)
    temp_filename_for_audio = ".tmp_audio.mp3"

    synthesized_audio.save(temp_filename_for_audio)

    # Load the MP3 file
    pygame.mixer.music.load(temp_filename_for_audio)
    # Play the MP3 file
    pygame.mixer.music.play()

    # Optional: Wait for the song to finish
    while pygame.mixer.music.get_busy():
        pygame.time.wait(50)
    pygame.mixer.music.unload()


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
        # A stupid workaround to play the sound earlier than calling input()
        # But after printing the word
        print(f"'{word}'") 
        # synthesize_and_play_sound(word)
        response = input("").lower()
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

def promt_language_choose():
    response = input("Choose your language (de, eng)").lower()
    if response in ["de", "eng"]:
        return response
    else:
        print("Please respond with 'de' or 'eng'. That are the only languages availiable.")


def main():
    lang_prefix = promt_language_choose()
    known_history = load_history(f"known_{lang_prefix}.txt")
    unknown_history = load_history(f"unknown_{lang_prefix}.txt")
    file_path = f"words_{lang_prefix}.txt"  # Path to your file with 30k most frequent words
    if not os.path.exists(file_path):
        print("Error: File not found.")
        return

    print("Please, tell yes if you know a word that will appear next. Answer no otherwise.")
    with open(file_path, "r") as f:
        for line in f:
            word = line.strip()
            if word in known_history or word in unknown_history:
                continue
            if prompt_user(word):
                unknown_history.add(word)
                save_history(unknown_history, f"unknown_{lang_prefix}.txt")
            else:
                known_history.add(word)
                filter_file(file_path, known_history)
                save_history(known_history, f"known_{lang_prefix}.txt")


if __name__ == "__main__":
    main()
