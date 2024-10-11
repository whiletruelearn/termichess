

```
████████╗███████╗██████╗ ███╗   ███╗██╗ ██████╗██╗  ██╗███████╗███████╗███████╗
╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║██╔════╝██║  ██║██╔════╝██╔════╝██╔════╝
   ██║   █████╗  ██████╔╝██╔████╔██║██║██║     ███████║█████╗  ███████╗███████╗
   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║     ██╔══██║██╔══╝  ╚════██║╚════██║
   ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║╚██████╗██║  ██║███████╗███████║███████║
   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝
```

A game of chess  in your terminal. Built using the amazing TUI framework `Textual`.

## Demo


https://github.com/user-attachments/assets/305f1e5b-9c76-474f-b30e-5bee12ac3be8

## Features

- ♟️ Play chess right in your terminal
- 🧠 Stockfish integration for chess engine
- ✅ Move validation and legal move highlighting
- 🎨 Change board themes
- 🤓 Variety of geeky board pieces
- ⚙️ Configuration menu for different options to change on the fly

## Installation

1. Please use Python 3.10 within your favourite venv. I have only tested currently only on `python 3.10`

2. Install Stockfish:

   - On Ubuntu or Debian: `sudo apt-get install stockfish`
   - On macOS with Homebrew: `brew install stockfish`
   - On Windows, download from [Stockfish's official website](https://stockfishchess.org/download/) and add it to your system PATH.

3. Install TermiChess:

`pip install termichess`

## Running the Game

After installation, you can start the game by simply running:

`termichess`

- To exit out at any time , Press `q` .
- To restart the game click on the `Restart` button

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the Apache License - see the LICENSE file for details.

## Acknowledgments

- [Textual](https://github.com/Textualize/textual) for the TUI framework
- [python-chess](https://github.com/niklasf/python-chess) for chess logic
- [Stockfish](https://stockfishchess.org/) for the chess engine
