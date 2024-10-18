from textual.screen import ModalScreen
from textual.widgets import RadioSet, RadioButton, Label
import chess

class PawnPromotion(ModalScreen):
    CSS = """
    PawnPromotion {
        height: auto;
        width: 50%;
        background: $surface;
        border: tall $panel;
        padding: 2;
        layout: grid;
        grid-rows: auto 1fr;
        grid-gutter: 1 2;
        grid-columns: 1fr 1fr 1fr 1fr;
    }

    #title {
        dock: top;
        height: 4;
        background: $boost;
        padding: 0 1;
        column-span: 4;
    }

    #options {
        padding: 1;
        column-span: 4;
    }

    RadioButton {
        width: 100%;
    }
    """

    def __init__(self):
        super().__init__("Pawn Promotion")
        self.promotion_piece = None
        self.selected_button = None 

    def compose(self):
        yield Label("Select Promotion Piece", id="title")
        with RadioSet(id="options", name="promotion_piece") as radio_set:
            yield RadioButton("Queen", value=chess.QUEEN)
            yield RadioButton("Rook", value=chess.ROOK)
            yield RadioButton("Bishop", value=chess.BISHOP)
            yield RadioButton("Knight", value=chess.KNIGHT)
        radio_set.on_change = self.on_radio_set_changed

    def get_promotion_piece(self):
        self.notify(f"promotion piece {self.promotion_piece}")
        return self.promotion_piece

    def on_dismiss(self):
        self.remove_self()

    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        selected_button = event.radio_set.pressed_button
        if selected_button:
            self.promotion_piece = selected_button.value
        else:
            self.promotion_piece = None
        self.dismiss()