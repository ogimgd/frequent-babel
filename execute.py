import os

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
        response = input(f"Next word:      '{word}'?").lower()
        if response in ["y", "n"]:
            return response == "no"
        else:
            print("Please respond with 'y' or 'n'.")

# Function to filter out known words and update the file
def filter_file(file_path, history):
    new_lines = []
    with open(file_path, "r") as f:
        for line in f:
            if line not in history:
                new_lines.append(line)
    with open(file_path, "w") as f:
        f.write("\n".join(new_lines))

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
            if prompt_user(word):
                unknown_history.add(word)
                save_history(unknown_history, "known.txt")
            else:
                known_history.add(word)
                filter_file(file_path, known_history)
                save_history(known_history, "unknown.txt")
                break

    print("Done.")

if __name__ == "__main__":
    main()