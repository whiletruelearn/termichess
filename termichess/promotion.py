from textual.widgets import Modal, RadioSet, RadioButton
import chess 

class PawnPromotion(Modal):
    def __init__(self):
        super().__init__("Pawn Promotion")
        self.promotion_piece = None

    def compose(self):
        with RadioSet(name="promotion_piece"):
            yield RadioButton("Queen", value=chess.QUEEN)
            yield RadioButton("Rook", value=chess.ROOK)
            yield RadioButton("Bishop", value=chess.BISHOP)
            yield RadioButton("Knight", value=chess.KNIGHT)

    def get_promotion_piece(self):
        return self.promotion_piece

    def on_dismiss(self):
        self.remove_self()

    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        self.promotion_piece = event.value
        self.dismiss()