from PIL import Image, ImageDraw

def create_piece(color, shape):
    img = Image.new('RGBA', (16, 16), color=(0,0,0,0))
    draw = ImageDraw.Draw(img)
    
    if color == 'white':
        main_color = (240, 240, 240)
        outline_color = (180, 180, 180)
    else:
        main_color = (60, 60, 60)
        outline_color = (20, 20, 20)
    
    draw.rectangle([4, 13, 11, 15], fill=main_color, outline=outline_color)
    
    if shape == 'pawn':
    
        draw.ellipse([5, 2, 9, 6], fill=main_color, outline=outline_color)
        draw.polygon([(4, 6), (10, 6), (9, 12), (5, 12)], fill=main_color, outline=outline_color)

    elif shape == 'rook':
        draw.rectangle([5, 3, 10, 13], fill=main_color, outline=outline_color)
        draw.line([(5, 3), (10, 3)], fill=outline_color)
        draw.line([(5, 3), (5, 1)], fill=outline_color)
        draw.line([(10, 3), (10, 1)], fill=outline_color)
    elif shape == 'knight':

        draw.polygon([(7, 1), (4, 13), (11, 13)], fill=main_color, outline=outline_color)
        draw.line([(6, 3), (7, 1), (8, 3)], fill=outline_color)
        draw.ellipse([6, 4, 10, 8], fill=outline_color if color == 'white' else main_color)
    
    elif shape == 'bishop':
        draw.polygon([(5, 13), (10, 13), (10, 5), (8, 2), (6, 2), (5, 5)], fill=main_color, outline=outline_color)
        draw.point((8, 4), fill=main_color)
        draw.line([(6, 3), (5, 6)], fill=outline_color)

    elif shape == 'queen':
        draw.polygon([(7, 1), (3, 13), (12, 13)], fill=main_color, outline=outline_color)
        draw.line([(3, 13), (7, 1), (12, 13)], fill=outline_color)
    elif shape == 'king':
        draw.polygon([(7, 3), (3, 13), (12, 13)], fill=main_color, outline=outline_color)
        draw.line([(7, 1), (7, 5)], fill=outline_color)
        draw.line([(5, 3), (9, 3)], fill=outline_color)
    
    return img

def save_pieces():
    pieces = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
    colors = ['white', 'black']
    
    for color in colors:
        for piece in pieces:
            img = create_piece(color, piece)
            img.save(f"{color}_{piece}.png")

if __name__ == "__main__":
    save_pieces()