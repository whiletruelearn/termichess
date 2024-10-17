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
