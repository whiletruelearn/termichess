from textual.screen import ModalScreen
from textual.widgets import Label, Button
import chess

class PawnPromotion(ModalScreen):
    CSS = """
        PawnPromotion {
        height: auto;
        width: 30%;
        background: $surface;
        border: tall $panel;
        padding: 1;
        layout: grid;
        grid-rows: auto 1fr;
        grid-columns: 1fr 1fr 1fr 1fr;
        align: center middle;
    }

    #title {
        dock: top;
        height: 3;
        background: $boost;
        padding: 0 1;
        column-span: 4;
    }

    Button {
        width: 50%;
        height: 3;
    }
    """

    def __init__(self, on_promotion_selected):
        super().__init__("Pawn Promotion")
        self.on_promotion_selected = on_promotion_selected
        self.mapping = {"Queen" : chess.QUEEN,
                        "Rook" : chess.ROOK,
                        "Bishop" : chess.BISHOP,
                        "Knight" : chess.KNIGHT} 

    def compose(self):
        yield Label("Select Promotion Piece", id="title")
        yield Button("Queen", id="queen")
        yield Button("Rook", id="rook")
        yield Button("Bishop", id="bishop")
        yield Button("Knight", id="knight")
    

    def on_dismiss(self):
        self.remove_self()


    def get_promotion_piece(self):
        return self.promotion_piece    
        

    def on_button_pressed(self, event: Button.Pressed):
        piece_id = event.button.id
        promotion_piece = self.mapping.get(piece_id.capitalize())
        self.on_promotion_selected(promotion_piece)
        self.dismiss()