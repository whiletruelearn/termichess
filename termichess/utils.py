from termichess.assets.pieces.asciiart import computer_first, computer_second, computer_third, retro, geometric, minimalistic, char, glyph, got, mahabharat, potter, rad, scientist
import os 


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

CONF = {'board-theme' : "classic", 'difficulty' : 'beginner'}

ASSETS_PATH =  os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')

THEME_COLORS = {
    "classic": ("#ebecd0", "#739552"),
    "forest": ("#e8e5c2", "#3e5f2f"),
    "ocean": ("#e3f2fd", "#0077b6"),
    "midnight": ("#d1d5db", "#4b5563"),
    "autumn": ("#fde8e0", "#ca8a04"),
    "lavender": ("#f3e8ff", "#7e22ce"),
    "moss": ("#e3f9a6", "#3f6212"),
    "marble": ("#f5f5f5", "#bfbfbf"),
    "crimson": ("#f8f0f7", "#9b1b30"),
    "emerald": ("#f0feeb", "#1b5e20"),
    "sakura": ("#ffedf6", "#d16ba5"),
    "royal": ("#f2f2ff", "#3f3f8f"),
    "coffee": ("#f5f5eb", "#6f4e37"),
}

def get_theme_colors(theme: str) :
    try:
        return THEME_COLORS[theme]
    except KeyError:
        raise ValueError(f"Invalid theme: {theme}")
