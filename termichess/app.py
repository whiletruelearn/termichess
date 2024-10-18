from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Button
from textual import events
from textual.reactive import reactive
import simpleaudio as sa
from random import choice, random
import chess 
from chess.engine import SimpleEngine
from termichess.utils import ASSETS_PATH, CONF
from termichess.config_screen import ConfigScreen
from termichess.sidebar import InfoPanel, MoveHistory
from termichess.chess_board import ChessBoard, ChessSquare 
from termichess.promotion import PawnPromotion



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

    .hidden {
    display: none;
    }

    #restart-button {
        height: 3;
        border: solid white;
    }

    #menu-button {
        height: 3;
       border: solid white;
    }


    #config-container {
        width: 100%;
        height: auto;
        align: center top;
    }

    RetroTitle {
        content-align: center middle;
        padding:2;
        width: 100%;
        margin-bottom: 1;
    }

    #options-grid {
        grid-size: 5;
        grid-gutter: 1 2;
        grid-columns: 1fr 1fr 1fr 1fr 1fr;
        margin-bottom: 1;
    }

    ConfigBox {
        height: auto;
       
        padding: 1;
    }

    .box-title {
        text-align: center;
        text-style: bold;
        margin-bottom: 1;
    }

    RadioSet {
        width: 100%;
        height: auto;
    }

    #start-game {
        margin-top: 2;
        width: auto;
        min-width: 16;
    }

    #credit-line {
        margin-top: 2;
        text-align: center;
        color: $text-muted;
    }
    """

    selected_square = reactive(None)

    def __init__(self):
        super().__init__()
        self.engine = SimpleEngine.popen_uci("stockfish")
        self.move_sound = sa.WaveObject.from_wave_file(f"{ASSETS_PATH}/sound/move.wav")
        self.player_color = "white"
        self.sound_enabled = True
        
    def compose(self) -> ComposeResult:
        yield ConfigScreen()
        yield ChessBoard(classes="hidden")
        with Container(id="sidebar",classes="hidden"):
            yield InfoPanel()
            yield MoveHistory()
            with Horizontal():
                yield Button("Restart", id="restart-button", variant="primary")
                yield Button("Menu", id="menu-button", variant="primary")

    def on_mount(self):
        self.chess_board = self.query_one(ChessBoard)
        self.info_panel = self.query_one(InfoPanel)
        self.move_history = self.query_one(MoveHistory)
        self.restart_button = self.query_one("#restart-button")
        self.menu_button = self.query_one("#menu-button")
        self.config_screen = self.query_one(ConfigScreen)
        self.current_screen = "config"
        self.update_info()
        self.toggle_screen()

    def toggle_screen(self):
        
        if self.current_screen == "config":
            self.config_screen.remove_class("hidden")
            self.chess_board.add_class("hidden")
            self.query_one("#sidebar").add_class("hidden")
        else:
            self.config_screen.add_class("hidden")
            self.chess_board.remove_class("hidden")
            self.query_one("#sidebar").remove_class("hidden")
    
    def apply_config(self):
        
        ChessSquare.piece_set = CONF["piece-type"]
        self.player_color = CONF["player_color"]
        self.sound_enabled = (CONF["sound"] == "on")

        if self.player_color == "random":
            self.player_color = choice(["white","black"])

        self.chess_board.is_flipped = (self.player_color == "black")

        difficulty_mapping = {
            "beginner": {"depth": 1, "randomness": 0.9},
            "easy": {"depth": 1, "randomness": 0.1},
            "medium": {"depth": 2, "randomness": 0},
            "hard": {"depth": 3, "randomness": 0},
            "super hard": {"depth": 5, "randomness": 0}
        }
        self.engine_settings = difficulty_mapping.get(CONF["difficulty"], {"depth": 1, "randomness": 0.3})
        self.notify(f"Difficulty set to: {CONF['difficulty']}")
        self.notify(f"Player color: {self.player_color}")
        self.chess_board.render_board()


    def handle_click(self, square: ChessSquare) -> None:
        if self.selected_square is None:
            if square.piece and square.piece.color == (chess.BLACK if self.player_color == "black" else chess.WHITE):
                self.selected_square = square
                square.add_class("selected")
                CONF["selected_square"] = self.selected_square
                from_square = chess.parse_square(square.id)
                if self.chess_board.is_flipped:
                    from_square = chess.square_mirror(from_square)
                self.chess_board.highlight_possible_moves(from_square)
        else:
            if square != self.selected_square:
                self.move_piece(self.selected_square, square)
            self.selected_square.remove_class("selected")
            self.selected_square = None
            self.chess_board.clear_possible_moves()

    def move_piece(self, from_square: ChessSquare, to_square: ChessSquare):
        move = chess.Move.from_uci(f"{from_square.id}{to_square.id}")
        if self.chess_board.is_flipped:
            move = chess.Move(chess.square_mirror(move.from_square), chess.square_mirror(move.to_square))

        if self.chess_board.board.piece_at(move.from_square).piece_type == chess.PAWN:
            
            if move.to_square in chess.SquareSet(chess.BB_BACKRANKS):
                self.notify("Time for pawn promotion")
                if not self.handle_pawn_promotion(move):
                    return
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
        board = self.chess_board.board
        legal_moves = list(board.legal_moves)

        if self.engine_settings["randomness"] > 0 and random() < self.engine_settings["randomness"] and not board.is_check():
            move = choice(legal_moves)
        else:
            result = self.engine.play(board, chess.engine.Limit(depth=self.engine_settings["depth"]))
            move = result.move
        
        self.chess_board.board.push(move)
        self.chess_board.last_move = move
        displayed_move = move
        if self.chess_board.is_flipped:
            displayed_move = chess.Move(chess.square_mirror(move.from_square), chess.square_mirror(move.to_square))
        self.move_history.add_move(f"Computer ({('white' if self.player_color == 'black' else 'black')}): {displayed_move}")
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
            current_turn = "White" if self.chess_board.board.turn == chess.WHITE else "Black"
            turn = f"{current_turn} ({'Player' if current_turn.lower() == self.player_color else 'Computer'})"
            status = "Check!" if self.chess_board.board.is_check() else "Normal"
        self.info_panel.update_info(turn, status, CONF["difficulty"])

    def play_move_sound(self):
        if self.sound_enabled:
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





    def start_game(self):
        self.current_screen = "game"
        self.toggle_screen()
        self.chess_board.render_board()
        self.update_info()

        if self.player_color == "black":
            self.set_timer(1,self.make_computer_move)


    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "restart-button":
            self.restart_game()
        elif event.button.id == "menu-button":
            self.current_screen = "config"
            self.toggle_screen()


    def on_key(self, event: events.Key):
        if event.key == "q":
            self.exit()

    def handle_pawn_promotion(self, move):
        promotion_dialog = PawnPromotion()
        promotion_piece = self.push_screen(promotion_dialog)
        if self.check_promotion(move, promotion_piece):
            self.chess_board.board.push(move)
            self.chess_board.render_board()  
            self.move_history.add_move(f"Player: {move}")
            self.play_move_sound()
            self.update_info()
            self.check_game_over()
            if not self.chess_board.board.is_game_over():
                self.set_timer(1, self.make_computer_move)

    def check_promotion(self, move, promotion_piece):
        if promotion_piece is not None:
            move.promotion = promotion_piece
            return True
        return False

    

if __name__ == "__main__":
    app = ChessApp()
    app.run()