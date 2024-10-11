from textual.app import App, ComposeResult
from textual.containers import Container, Grid, Center, Vertical, Horizontal
from textual.widgets import Static, Button, RadioButton, RadioSet
from textual import events
from textual.reactive import reactive
from termichess.assets.pieces.asciiart import computer_first, computer_second, computer_third, retro, geometric, minimalistic,char, glyph, got, mahabharat, potter, rad, scientist
import chess
import chess.engine
import simpleaudio as sa
from rich_pixels import Pixels
from PIL import Image
import pkg_resources
 

PIECE_ASCII_ART = {
    
    "retro": retro.PIECE_ASCII_ART,
    "geometric": geometric.PIECE_ASCII_ART,
    "minimalistic": minimalistic.PIECE_ASCII_ART,
    "char" : char.PIECE_ASCII_ART,
    "computer1" : computer_first.PIECE_ASCII_ART,
    "computer2" : computer_second.PIECE_ASCII_ART,
    "computer3" : computer_third.PIECE_ASCII_ART,
    "glyph" : glyph.PIECE_ASCII_ART,
    "got" : got.PIECE_ASCII_ART,
    "mahabharat" : mahabharat.PIECE_ASCII_ART,
    "potter" : potter.PIECE_ASCII_ART,
    "rad" : rad.PIECE_ASCII_ART,
    "scientist" : scientist.PIECE_ASCII_ART
}

CONF = {'board-theme' : "classic"}

ASSETS_PATH = pkg_resources.resource_filename('termichess', 'assets')


def get_theme_colors(theme: str):
    
    if theme == "classic":
        light_bg = "#ebecd0"
        dark_bg = "#739552"
    elif theme == "forest":
        light_bg = "#ebecd0"
        dark_bg = "#2c003e"
    elif theme == "ocean":
        light_bg = "#ebecd0"
        dark_bg = "#001f3f"
    else:
        raise ValueError(f"Invalid theme: {theme}")
    return light_bg, dark_bg


class ChessSquare(Static):
    piece_set = "retro" #default piece set

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

    def compose(self) -> ComposeResult:
        with Grid(id="board-grid"):
            for row in range(8):
                for col in range(8):
                    square_id = f"{chr(97 + col)}{8 - row}"
                    yield ChessSquare(square_id)





    def render_board(self):

        light_bg, dark_bg = get_theme_colors(CONF["board-theme"])

        for square in chess.SQUARES:
            square_name = chess.SQUARE_NAMES[square]
            piece = self.board.piece_at(square)
            square_widget = self.query_one(f"#{square_name}", ChessSquare)

            selected_square = CONF.get('selected_square')

            if square not in self.possible_moves:
                square_widget.add_class("light" if (ord(square_name[0]) - ord('a') + int(square_name[1])) % 2 == 0 else "dark")
                square_widget.styles.background = light_bg if square_widget.has_class("light") else dark_bg

            if selected_square and selected_square.id == square_widget.id:
                square_widget.add_class("selected")
                square_widget.styles.background = "#aaa23a"

            if self.last_move and square in [self.last_move.from_square, self.last_move.to_square]:
                square_widget.add_class("highlight")
                square_widget.styles.background = "#aaa23a"

            if square in self.possible_moves:
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

class InfoPanel(Static):
    def update_info(self, turn: str, status: str):
        self.update(f"[bold]Turn:[/bold] {turn}\n[bold]Status:[/bold] {status}")

class MoveHistory(Static):
    def on_mount(self):
        self.moves = []

    def add_move(self, move: str):
        self.moves.append(move)
        self.update("\n".join(self.moves[-25:])) 


class RetroTitle(Static):
    def render(self):
        return """
████████╗███████╗██████╗ ███╗   ███╗██╗ ██████╗██╗  ██╗███████╗███████╗███████╗
╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║██╔════╝██║  ██║██╔════╝██╔════╝██╔════╝
   ██║   █████╗  ██████╔╝██╔████╔██║██║██║     ███████║█████╗  ███████╗███████╗
   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║     ██╔══██║██╔══╝  ╚════██║╚════██║
   ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║╚██████╗██║  ██║███████╗███████║███████║
   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝
        """
    
class ConfigBox(Static):
    def __init__(self, title: str, id: str, options: list[str]):
        super().__init__()
        self.title = title
        self.box_id = id
        self.options = options

    def compose(self) -> ComposeResult:
        yield Static(self.title, classes="box-title")
        with RadioSet(id=self.box_id):
            for option in self.options:
                yield RadioButton(option, value=option.lower())

class ConfigScreen(Static):
    

    def compose(self):
        with Center():
            with Vertical(id="config-container"):
                yield RetroTitle()
                
                with Grid(id="options-grid", classes="options"):
                    yield ConfigBox("Piece Type", "piece-type", ["retro","png-v1","geometric", "minimalistic","char","computer1","computer2","computer3","glyph","got","mahabharat","potter","rad","scientist"])
                    yield ConfigBox("Board Theme", "board-theme", ["classic", "forest", "ocean"])
                    yield ConfigBox("Player Color", "player_color", ["white", "black", "random"])
                    yield ConfigBox("Difficulty Level", "difficulty", ["easy", "medium", "hard", "super hard"])

                with Center():
                    yield Button("Start Game", id="start-game", variant="primary")
                
                yield Static("Built with ❤️  by @whiletruelearn", id="credit-line")

    def on_mount(self):

        self.set_radio_button("piece-type", "retro")
        self.set_radio_button("board-theme", "classic")
        self.set_radio_button("player_color", "white")
        self.set_radio_button("difficulty", "easy")

    def set_radio_button(self, radio_set_id: str, value: str):
        radio_set = self.query_one(f"#{radio_set_id}")
        for child in radio_set.children:
            if isinstance(child, RadioButton) and child.value == value:
                child.value = True
                break

    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        radio_set = event.radio_set
        selected_button = radio_set.pressed_button
        if selected_button:
            CONF[radio_set.id] = selected_button.label._text[0]
            

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start-game":
            self.app.apply_config()
            self.app.start_game()




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
        grid-size: 4;
        grid-gutter: 1 2;
        grid-columns: 1fr 1fr 1fr 1fr;
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
        self.engine = chess.engine.SimpleEngine.popen_uci("stockfish")
        self.move_sound = sa.WaveObject.from_wave_file(f"{ASSETS_PATH}/sound/move.wav")

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
        player_color = CONF["player_color"]


        difficulty_mapping = {"easy": 5, "medium": 10, "hard": 15, "super hard": 20}
        self.engine_depth = difficulty_mapping.get(CONF["difficulty"], 10)
        self.chess_board.render_board()


    def handle_click(self, square: ChessSquare) -> None:
        if self.selected_square is None:
            if square.piece and square.piece.color == self.chess_board.board.turn:
                self.selected_square = square
                square.add_class("selected")
                CONF["selected_square"] = self.selected_square
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





    def start_game(self):
        self.current_screen = "game"
        self.toggle_screen()
        self.chess_board.render_board()


    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "restart-button":
            self.restart_game()
        elif event.button.id == "menu-button":
            self.current_screen = "config"
            self.toggle_screen()


    def on_key(self, event: events.Key):
        if event.key == "q":
            self.exit()

if __name__ == "__main__":
    app = ChessApp()
    app.run()