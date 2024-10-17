from textual.widgets import Static
from textual.containers import Grid
import chess
from termichess.utils import CONF, get_theme_colors, PIECE_ASCII_ART, ASSETS_PATH
from rich_pixels import Pixels
from PIL import Image


class ChessSquare(Static):
    piece_set = "retro" 

    def __init__(self, id: str):
        super().__init__(id=id)
        self.piece = None
        self.add_class("light" if (ord(id[0]) - ord('a') + int(id[1])) % 2 == 0 else "dark")

    

    def set_piece(self, piece: chess.Piece | None):

        
        
        self.piece = piece
        if piece:
            color = "white" if piece.color == chess.WHITE else "black"
            piece_symbol = piece.symbol().lower()
            piece_name = chess.piece_name(piece.piece_type)
            if ChessSquare.piece_set in PIECE_ASCII_ART:
                ascii_art = PIECE_ASCII_ART[ChessSquare.piece_set][piece_symbol]
                colored_ascii_art = f"[bold {color}]{ascii_art}[/bold {color}]"
                self.update(colored_ascii_art)
            
            if ChessSquare.piece_set == "png-v1":
                image_path = f"{ASSETS_PATH}/pieces/v1/{color}_{piece_name}.png"
                img = Image.open(image_path)
                pixels = Pixels.from_image(img)
                self.update(pixels)
        else:
            self.update("")


    def on_click(self) -> None:
        self.app.handle_click(self)

class ChessBoard(Static):
    def __init__(self, classes:str = None):
        super().__init__(classes=classes)
        self.board = chess.Board()
        self.last_move = None
        self.possible_moves = set()
        self.is_flipped = False

    def compose(self):
        with Grid(id="board-grid"):
            for row in range(8):
                for col in range(8):
                    square_id = f"{chr(97 + col)}{8 - row}"
                    yield ChessSquare(square_id)





    def render_board(self):
        light_bg, dark_bg = get_theme_colors(CONF["board-theme"])

        for square in chess.SQUARES:
            square_name = chess.SQUARE_NAMES[square]
            display_square = chess.square_mirror(square) if self.is_flipped else square
            piece = self.board.piece_at(display_square)
            square_widget = self.query_one(f"#{square_name}", ChessSquare)

            selected_square = CONF.get('selected_square')

            if display_square not in self.possible_moves:
                square_widget.add_class("light" if (ord(square_name[0]) - ord('a') + int(square_name[1])) % 2 == 0 else "dark")
                square_widget.styles.background = light_bg if square_widget.has_class("light") else dark_bg

            if selected_square and selected_square.id == square_widget.id:
                square_widget.add_class("selected")
                square_widget.styles.background = "#aaa23a"

            if self.last_move and display_square in [self.last_move.from_square, self.last_move.to_square]:
                square_widget.add_class("highlight")
                square_widget.styles.background = "#aaa23a"

            if display_square in self.possible_moves:
                square_widget.add_class("possible-move-light" if (ord(square_name[0]) - ord('a') + int(square_name[1])) % 2 == 0 else "possible-move-dark")
                square_widget.styles.background = "#c896db" if square_widget.has_class("possible-move-light") else "#8b4b8b"

            square_widget.set_piece(piece)

    def get_possible_moves(self, from_square):
        return {move.to_square for move in self.board.legal_moves if move.from_square == from_square}

    def highlight_possible_moves(self, from_square):
        self.possible_moves = self.get_possible_moves(from_square)
        self.render_board()

    def clear_possible_moves(self):
        self.possible_moves.clear()
        self.render_board()