from PIL import Image
import os

GRID = 16
SCALE = 8
SIZE = GRID * SCALE

CARPETA = os.path.join(os.path.dirname(__file__), "assets")
os.makedirs(CARPETA, exist_ok=True)

T = None


def dibujar(matriz, paleta, archivo):
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    px = img.load()
    for fila, texto in enumerate(matriz):
        for col, ch in enumerate(texto):
            color = paleta.get(ch, None)
            if color is None:
                continue
            r, g, b = color
            for dy in range(SCALE):
                for dx in range(SCALE):
                    x = col * SCALE + dx
                    y = fila * SCALE + dy
                    if 0 <= x < SIZE and 0 <= y < SIZE:
                        px[x, y] = (r, g, b, 255)
    img.save(archivo)


# RATTATA (peon)
RATTATA = [
    "................",
    "................",
    ".....P....P.....",
    "....PP....PP....",
    "....PPP..PPP....",
    "...PPPPPPPPPP...",
    "..PPWWPPPPWWPP..",
    "..PPWBPPPPBWPP..",
    "..PPPPPNPPPPPP..",
    "..PPPPNNNPPPPP..",
    "...PPPPPPPPPP...",
    "....FFF..FFF....",
    "...PPPPPPPPPP...",
    "....PP....PP....",
    "....F......F....",
    "................",
]
PAL_RATTATA = {
    ".": T,
    "P": (150, 111, 196),
    "W": (255, 255, 255),
    "B": (40, 40, 40),
    "N": (244, 200, 120),
    "F": (230, 215, 170),
}

# RATICATE (evolucion del peon)
RATICATE = [
    "................",
    "....O.......O...",
    "...OO.......OO..",
    "...OOO.....OOO..",
    "..OOOOO...OOOOO.",
    "..OOOOOOOOOOOOO.",
    ".OOWWOOOOOOWWOO.",
    ".OOWBOOOOOOBWOO.",
    ".OOOOOOWWOOOOOO.",
    ".OOOOOWWWWOOOOO.",
    "..OOOOOOOOOOOO..",
    "...CCC....CCC...",
    "..OOOOOOOOOOOO..",
    "...OO......OO...",
    "...C........C...",
    "................",
]
PAL_RATICATE = {
    ".": T,
    "O": (196, 140, 90),
    "W": (255, 255, 255),
    "B": (40, 40, 40),
    "C": (235, 220, 180),
}

# ARCEUS (rey)
ARCEUS = [
    ".......GG.......",
    "......GWWG......",
    ".....GWWWWG.....",
    "....GWWWWWWG....",
    "...GWWWWWWWWG...",
    "..GGWWWWWWWWGG..",
    ".GWWGWWWWWWGWWG.",
    ".GWWWWBWWBWWWWG.",
    ".GWWWWWWWWWWWWG.",
    "..GWWWYYYYWWWG..",
    "...GWWWWWWWWG...",
    "...GGWWWWWWGG...",
    "..GWWGWWWWGWWG..",
    "..GWG.GWWG.GWG..",
    "..GG...GG...GG..",
    "................",
]
PAL_ARCEUS = {
    ".": T,
    "G": (212, 175, 55),
    "W": (245, 245, 250),
    "B": (60, 120, 160),
    "Y": (212, 175, 55),
}

# RAYQUAZA (dama)
RAYQUAZA = [
    ".....YYYY.......",
    "....YGGGGY......",
    "...YGGGGGGY.....",
    "...YGRGGRGY.....",
    "...YGGGGGGY.....",
    "....YGGGGY......",
    ".....YGGY.......",
    "...YYGGGGYY.....",
    "..YGGGGGGGGY....",
    ".YGGYGGGGYGGY...",
    ".YGG.YGGY.GGY...",
    "..YG..YGY..GY...",
    "...Y..YGY..Y....",
    "......YGY.......",
    ".....YGGGY......",
    "......YYY.......",
]
PAL_RAYQUAZA = {
    ".": T,
    "G": (46, 139, 87),
    "Y": (220, 210, 70),
    "R": (200, 50, 50),
}

# KYOGRE (alfil)
KYOGRE = [
    "................",
    "....BBBBBB......",
    "...BBBBBBBB.....",
    "..BBWBBBBWBB....",
    "..BBRBBBBRBB....",
    "..BBBBBBBBBB....",
    "..BBPPBBBPPB....",
    ".BBBBBBBBBBBB...",
    "BBBBBBBBBBBBBB..",
    "BBPBBBBBBBBPBB..",
    ".BBBBBBBBBBBB...",
    "..BBB.BB.BBB....",
    "...BB....BB.....",
    "..BB......BB....",
    ".BB........BB...",
    "................",
]
PAL_KYOGRE = {
    ".": T,
    "B": (38, 78, 156),
    "W": (255, 255, 255),
    "R": (200, 60, 60),
    "P": (180, 30, 60),
}

# GROUDON (caballo)
GROUDON = [
    "................",
    "..........RR....",
    ".........RRRR...",
    "........RRGGR...",
    ".......RRRRRR...",
    "......RRRWBRR...",
    ".....RRRRRRRR...",
    "....RRRRRRRR....",
    "...RRGGRRRR.....",
    "..RRGGGRRRRR....",
    "..RRRRRRRRRRR...",
    "..RR.RRRR.RRR...",
    "..R...RR...RR...",
    ".RR...RR...R....",
    ".R....RR........",
    "................",
]
PAL_GROUDON = {
    ".": T,
    "R": (178, 45, 38),
    "G": (90, 90, 90),
    "W": (255, 255, 255),
    "B": (40, 40, 40),
}

# MEWTWO (torre)
MEWTWO = [
    ".......PP.......",
    "......PPPP......",
    ".....PWWWWP.....",
    ".....PWVWVP.....",
    ".....PWWWWP.....",
    "......PWWP......",
    ".....PPPPPP.....",
    "....PPWWWWPP....",
    "...PPWWWWWWPP...",
    "...PPWWWWWWPP...",
    "...PPWWWWWWPP...",
    "....PWWWWWWP....",
    "....PPWWWWPP....",
    "....PP....PP....",
    "...PP......PP...",
    "................",
]
PAL_MEWTWO = {
    ".": T,
    "P": (160, 120, 180),
    "W": (235, 230, 240),
    "V": (120, 60, 160),
}

POKEMONES = {
    "rattata": (RATTATA, PAL_RATTATA),
    "raticate": (RATICATE, PAL_RATICATE),
    "arceus": (ARCEUS, PAL_ARCEUS),
    "rayquaza": (RAYQUAZA, PAL_RAYQUAZA),
    "kyogre": (KYOGRE, PAL_KYOGRE),
    "groudon": (GROUDON, PAL_GROUDON),
    "mewtwo": (MEWTWO, PAL_MEWTWO),
}


def aplicar_tinte(matriz, paleta, factor):
    nueva = {}
    for ch, color in paleta.items():
        if color is None:
            nueva[ch] = None
        else:
            r, g, b = color
            r = max(0, min(255, int(r * factor)))
            g = max(0, min(255, int(g * factor)))
            b = max(0, min(255, int(b * factor)))
            nueva[ch] = (r, g, b)
    return nueva


def generar_todo():
    for nombre, (matriz, paleta) in POKEMONES.items():
        pal_blanca = aplicar_tinte(matriz, paleta, 1.08)
        dibujar(matriz, pal_blanca, os.path.join(CARPETA, f"{nombre}_w.png"))
        pal_negra = aplicar_tinte(matriz, paleta, 0.62)
        dibujar(matriz, pal_negra, os.path.join(CARPETA, f"{nombre}_b.png"))
    print("Sprites generados en:", CARPETA)
    for f in sorted(os.listdir(CARPETA)):
        print("  ", f)


if __name__ == "__main__":
    generar_todo()
