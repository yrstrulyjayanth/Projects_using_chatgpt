import os
import re
import json
import sqlite3
import glob
import urllib.request

# Function to download archives and games
def download_chess_games(username, directory, exclude_loss_by_time=False, include_previous=False):
    base_url = f"https://api.chess.com/pub/player/{username}/games/"
    archives_url = base_url + "archives"

    if not os.path.exists(directory):
        os.makedirs(directory)

    # Create a file to store downloaded archive URLs
    download_history_file = os.path.join(directory, f"{username}_download_history.json")
    previously_downloaded = set()

    # Load previously downloaded archives if the history file exists
    if os.path.exists(download_history_file):
        with open(download_history_file, 'r') as f:
            previously_downloaded = set(json.load(f))

    # Get list of archives
    with urllib.request.urlopen(archives_url) as response:
        archives = response.read().decode("utf-8")
        archives_list = json.loads(archives)["archives"]

    # Determine which archives to process
    if include_previous:
        archives_to_process = archives_list
    else:
        archives_to_process = [url for url in archives_list if url not in previously_downloaded]

    if not archives_to_process:
        print("No new games to download!")
        return

    # Function to check if the game was lost by time
    def is_loss_by_time(pgn):
        result = re.search(r'\[Result "([^"]+)"\]', pgn).group(1)
        termination = re.search(r'\[Termination "([^"]+)"\]', pgn).group(1)
        if username in re.search(r'\[White "([^"]+)"\]', pgn).group(1):
            if result == "0-1" and "time" in termination.lower():
                return True
        if username in re.search(r'\[Black "([^"]+)"\]', pgn).group(1):
            if result == "1-0" and "time" in termination.lower():
                return True
        return False

    # Download and save PGN files
    for archive_url in archives_to_process:
        print(f"Processing archive: {archive_url}")
        with urllib.request.urlopen(archive_url + "/pgn") as response:
            pgn_data = response.read().decode("utf-8")
            games = pgn_data.split('\n\n\n')

        for game in games:
            if not game.strip():
                continue
            
            if exclude_loss_by_time and is_loss_by_time(game):
                continue

            white_player = re.search(r'\[White "([^"]+)"\]', game).group(1)
            black_player = re.search(r'\[Black "([^"]+)"\]', game).group(1)
            filename = f"{white_player}_vs_{black_player}.pgn"
            file_path = os.path.join(directory, filename)
            with open(file_path, 'w') as file:
                file.write(game)
            print(f"Downloaded: {filename}")
        
        # Add the processed archive to the downloaded set
        previously_downloaded.add(archive_url)

    # Save the updated download history
    with open(download_history_file, 'w') as f:
        json.dump(list(previously_downloaded), f)

# Function to insert games into a SQLite database
def insert_games_into_db(directory, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS games (
        id INTEGER PRIMARY KEY,
        white TEXT,
        black TEXT,
        date TEXT,
        result TEXT,
        pgn TEXT
    )
    ''')

    def extract_game_info(pgn):
        white = re.search(r'\[White "([^"]+)"\]', pgn).group(1)
        black = re.search(r'\[Black "([^"]+)"\]', pgn).group(1)
        date = re.search(r'\[Date "([^"]+)"\]', pgn).group(1)
        result = re.search(r'\[Result "([^"]+)"\]', pgn).group(1)
        return white, black, date, result, pgn

    for pgn_file in glob.glob(os.path.join(directory, '*.pgn')):
        with open(pgn_file, 'r') as file:
            pgn = file.read()
            white, black, date, result, pgn_text = extract_game_info(pgn)
            cursor.execute('''
            INSERT INTO games (white, black, date, result, pgn)
            VALUES (?, ?, ?, ?, ?)
            ''', (white, black, date, result, pgn_text))
            print(f"Inserted: {white} vs {black}")

    conn.commit()
    conn.close()
    print("All games inserted into the database.")

# Function to merge PGN files into a single file
def merge_pgn_files(directory, output_file_path):
    with open(output_file_path, 'w') as outfile:
        for pgn_file in glob.glob(os.path.join(directory, '*.pgn')):
            with open(pgn_file, 'r') as infile:
                outfile.write(infile.read())
                outfile.write("\n\n\n")
            print(f"Merged: {pgn_file}")
    print(f"All games merged into {output_file_path}")

# Interactive Script
def main():
    print("Welcome to the Chess.com Game Utility!")

    # Get initial details only once
    username = input("Enter your Chess.com username: \n(e.g., johndoe): ")
    directory = input("Enter the directory to save games: \n(e.g., ./chess_games): ")
    db_path = input("Enter the database path: \n(e.g., chess_games.db): ")
    output_file_path = input("Enter the output file path for merged PGN: \n(e.g., merged_games.pgn): ")

    while True:
        print("\nSelect an action:")
        print("1. Download games")
        print("2. Insert games into database")
        print("3. Merge PGN files")
        print("4. Exit")
        
        action = input("Enter choice (1/2/3/4): ")

        if action == "1":
            # Check if there are previously downloaded games
            history_file = os.path.join(directory, f"{username}_download_history.json")
            if os.path.exists(history_file):
                print("\nPreviously downloaded games found!")
                include_previous = input("Do you want to include previously downloaded games? (yes/no): ").lower() == "yes"
            else:
                include_previous = True  # First time download
            
            exclude_loss_by_time = input("Exclude games lost by time? (yes/no): ").lower() == "yes"
            download_chess_games(username, directory, exclude_loss_by_time, include_previous)

        elif action == "2":
            insert_games_into_db(directory, db_path)

        elif action == "3":
            merge_pgn_files(directory, output_file_path)

        elif action == "4":
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

