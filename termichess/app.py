from textual.app import App, ComposeResult
from textual.containers import Container, Grid
from textual.widgets import Static, Button
from textual import events
from textual.reactive import reactive
import chess
import chess.engine
import simpleaudio as sa
from rich_pixels import Pixels
from PIL import Image
import os 
import pkg_resources 

ASSETS_PATH = pkg_resources.resource_filename('termichess', 'assets')


class ChessSquare(Static):
    def __init__(self, id: str):
        super().__init__(id=id)
        self.piece = None
        self.add_class("light" if (ord(id[0]) - ord('a') + int(id[1])) % 2 == 0 else "dark")

    def set_piece(self, piece: chess.Piece | None):
        self.piece = piece
        if piece:
            color = "white" if piece.color == chess.WHITE else "black"
            piece_name = chess.piece_name(piece.piece_type)
            image_path = f"{ASSETS_PATH}/pieces/{color}_{piece_name}.png"
            img = Image.open(image_path)
            pixels = Pixels.from_image(img)
            self.update(pixels)
        else:
            self.update("")

    def on_click(self) -> None:
        self.app.handle_click(self)

class ChessBoard(Static):
    def __init__(self):
        super().__init__()
        self.board = chess.Board()
        self.last_move = None
        self.possible_moves = set()

    def compose(self) -> ComposeResult:
        with Grid(id="board-grid"):
            for row in range(8):
                for col in range(8):
                    square_id = f"{chr(97 + col)}{8 - row}"
                    yield ChessSquare(square_id)

    def on_mount(self):
        self.render_board()

    def render_board(self):
        for square in chess.SQUARES:
            square_name = chess.SQUARE_NAMES[square]
            piece = self.board.piece_at(square)
            square_widget = self.query_one(f"#{square_name}", ChessSquare)
            
            square_widget.remove_class("highlight")
            square_widget.remove_class("possible-move")
            
            if self.last_move and square in [self.last_move.from_square, self.last_move.to_square]:
                square_widget.add_class("highlight")
            
            if square in self.possible_moves:
                square_widget.add_class("possible-move")
            
            square_widget.set_piece(piece)

    def get_possible_moves(self, from_square):
        return {move.to_square for move in self.board.legal_moves if move.from_square == from_square}

    def highlight_possible_moves(self, from_square):
        self.possible_moves = self.get_possible_moves(from_square)
        self.render_board()

    def clear_possible_moves(self):
        self.possible_moves.clear()
        self.render_board()

class InfoPanel(Static):
    def update_info(self, turn: str, status: str):
        self.update(f"[bold]Turn:[/bold] {turn}\n[bold]Status:[/bold] {status}")

class MoveHistory(Static):
    def on_mount(self):
        self.moves = []

    def add_move(self, move: str):
        self.moves.append(move)
        self.update("\n".join(self.moves[-25:])) 

class ChessApp(App):
    CSS = """
    Screen {
        layout: horizontal;
    }

    ChessBoard {
        width: 80%;
        height: 100%;
    }

    #board-grid {
        width: 100%;
        height: 100%;
        layout: grid;
        grid-size: 8 8;
        grid-gutter: 0;
    }

    ChessSquare {
        width: 100%;
        height: 1fr;
        min-width: 8;
        min-height: 8;
        content-align: center middle;
    }

    ChessSquare.light {
        background: #ebecd0;
    }

    ChessSquare.dark {
        background: #739552;
    }

    ChessSquare.highlight {
        background: #aaa23a;
    }

    ChessSquare.selected {
        background: #aaa23a;
    }

    ChessSquare.possible-move {
        background: #85139c;
    }

    ChessSquare.possible-move.light {
        background: #c896db;
    }

    ChessSquare.possible-move.dark {
        background: #8b4b8b;
    }

    #sidebar {
        width: 20%;
        height: 100%;
        layout: vertical;
    }

    InfoPanel {
        height: 20%;
        border: solid green;
        padding: 1;
    }

    MoveHistory {
        height: 70%;
        border: solid yellow;
        padding: 1;
    }

    #restart-button {
        height: 3;
    }
    """

    selected_square = reactive(None)

    def __init__(self):
        super().__init__()
        self.engine = chess.engine.SimpleEngine.popen_uci("stockfish")
        self.move_sound = sa.WaveObject.from_wave_file(f"{ASSETS_PATH}/sound/move.wav")

    def compose(self) -> ComposeResult:
        yield ChessBoard()
        with Container(id="sidebar"):
            yield InfoPanel()
            yield MoveHistory()
            yield Button("Restart Game", id="restart-button", variant="primary")

    def on_mount(self):
        self.chess_board = self.query_one(ChessBoard)
        self.info_panel = self.query_one(InfoPanel)
        self.move_history = self.query_one(MoveHistory)
        self.restart_button = self.query_one("#restart-button")
        self.update_info()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "restart-button":
            self.restart_game()

    def handle_click(self, square: ChessSquare) -> None:
        if self.selected_square is None:
            if square.piece and square.piece.color == self.chess_board.board.turn:
                self.selected_square = square
                square.add_class("selected")
                from_square = chess.parse_square(square.id)
                self.chess_board.highlight_possible_moves(from_square)
        else:
            if square != self.selected_square:
                self.move_piece(self.selected_square, square)
            self.selected_square.remove_class("selected")
            self.selected_square = None
            self.chess_board.clear_possible_moves()

    def move_piece(self, from_square: ChessSquare, to_square: ChessSquare):
        move = chess.Move.from_uci(f"{from_square.id}{to_square.id}")
        if move in self.chess_board.board.legal_moves:
            self.chess_board.board.push(move)
            self.chess_board.last_move = move
            self.move_history.add_move(f"Player: {move}")
            self.chess_board.render_board()
            self.play_move_sound()
            self.update_info()
            self.check_game_over()
            if not self.chess_board.board.is_game_over():
                self.set_timer(1, self.make_computer_move)

    def make_computer_move(self):
        result = self.engine.play(self.chess_board.board, chess.engine.Limit(time=2.0))
        move = result.move
        self.chess_board.board.push(move)
        self.chess_board.last_move = move
        self.move_history.add_move(f"Computer: {move}")
        self.chess_board.render_board()
        self.play_move_sound()
        self.update_info()
        self.check_game_over()

    def update_info(self):
        if self.chess_board.board.is_game_over():
            result = self.chess_board.board.result()
            if result == "1-0":
                status = "Game Over - White wins!"
            elif result == "0-1":
                status = "Game Over - Black wins!"
            else:
                status = "Game Over - Draw!"
            turn = "Game Ended"
        else:
            turn = "White" if self.chess_board.board.turn == chess.WHITE else "Black"
            status = "Check!" if self.chess_board.board.is_check() else "Normal"
        self.info_panel.update_info(turn, status)

    def play_move_sound(self):
        self.move_sound.play()

    def check_game_over(self):
        if self.chess_board.board.is_game_over():
            self.update_info()

    def restart_game(self):
        self.chess_board.board.reset()
        self.chess_board.last_move = None
        self.chess_board.clear_possible_moves()
        self.chess_board.render_board()
        self.move_history.moves = []
        self.move_history.update("")
        self.update_info()

    def on_key(self, event: events.Key):
        if event.key == "q":
            self.exit()

if __name__ == "__main__":
    app = ChessApp()
    app.run()