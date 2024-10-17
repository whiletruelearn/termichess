from textual.widgets import Static
from textual.containers import Container, Horizontal
from textual.widgets import Button


class InfoPanel(Static):
    def update_info(self, turn: str, status: str, difficulty_level : str):
        self.update(f"[bold]Turn:[/bold] {turn}\n[bold]Status:[/bold] {status}\n[bold]Difficulty level:[/bold] {difficulty_level}")

class MoveHistory(Static):
    def on_mount(self):
        self.moves = []

    def add_move(self, move: str):
        self.moves.append(move)
        self.update("\n".join(self.moves[-25:])) 