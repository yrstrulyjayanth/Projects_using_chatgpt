
```markdown
# Chess.com Game Utility

A Python utility to download, manage, and analyze your Chess.com games with ease. This tool allows you to download your chess games, store them in a SQLite database, and merge them into a single PGN file.

## 🎯 Features

- Download chess games from Chess.com using their public API
- Filter out games lost by time (optional)
- Track downloaded game archives to avoid duplicates
- Store games in a SQLite database for easy querying
- Merge multiple PGN files into a single file
- Interactive command-line interface

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/yrstrulyjayanth/chess-game-utility.git
cd chess-game-utility
```

2. Install required dependencies:
```bash
pip install sqlite3
```

## 💻 Usage

Run the script using Python:

```bash
python download_chess_games.py
```

The interactive menu will guide you through the following options:
1. Download games
2. Insert games into database
3. Merge PGN files
4. Exit

### Configuration

You'll need to provide:
- Your Chess.com username
- Directory path to save games
- Database file path
- Output path for merged PGN file

## 🛠️ Functions

### `download_chess_games(username, directory, exclude_loss_by_time=False, include_previous=False)`
Downloads chess games from Chess.com and saves them as individual PGN files.

### `insert_games_into_db(directory, db_path)`
Inserts downloaded games into a SQLite database for efficient storage and querying.

### `merge_pgn_files(directory, output_file_path)`
Combines all PGN files in the specified directory into a single file.

## 📝 Database Schema

The SQLite database includes the following fields:
- id (PRIMARY KEY)
- white (player name)
- black (player name)
- date
- result
- pgn (full game notation)

## 🤝 Contributing

Feel free to contribute to this project:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**yrstrulyjayanth**
- GitHub: [@yrstrulyjayanth](https://github.com/yrstrulyjayanth)

## 🙏 Acknowledgments

- Chess.com for providing the public API


⭐️ If you find this tool useful, please consider giving it a star!
