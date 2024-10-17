from textual.containers import  Grid, Center, Vertical
from textual.widgets import Static, Button, RadioButton, RadioSet
from termichess.utils import CONF, THEME_COLORS


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

    def compose(self):
        yield Static(self.title, classes="box-title")
        with RadioSet(id=self.box_id):
            for option in self.options:
                yield RadioButton(option, value=option.lower())



PIECE_TYPES = ["retro","png-v1","geometric", "minimalistic","char","computer1","computer2","computer3","glyph","got","mahabharat","potter","rad","scientist"]

class ConfigScreen(Static):
    

    def compose(self):
        with Center():
            with Vertical(id="config-container"):
                yield RetroTitle()
                
                with Grid(id="options-grid", classes="options"):
                    yield ConfigBox("Piece Type", "piece-type", PIECE_TYPES )
                    yield ConfigBox("Board Theme", "board-theme", THEME_COLORS.keys())
                    yield ConfigBox("Player Color", "player_color", ["white", "black", "random"])
                    yield ConfigBox("Difficulty Level", "difficulty", ["beginner","easy", "medium", "hard", "super hard"])

                with Center():
                    yield Button("Start Game", id="start-game", variant="primary")
                
                yield Static("Built with ❤️  by @whiletruelearn", id="credit-line")

    def on_mount(self):

        self.set_radio_button("piece-type", "retro")
        self.set_radio_button("board-theme", "classic")
        self.set_radio_button("player_color", "white")
        self.set_radio_button("difficulty", "beginner")

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
