
import os
import sys
import pygame

from motor import Tablero, BLANCO, NEGRO, NOMBRE_POKEMON


TAM_CASILLA = 80                 
TABLERO_PX = TAM_CASILLA * 8     
PANEL_PX = 220                   
MARGEN = 24                      
ANCHO = TABLERO_PX + PANEL_PX + MARGEN * 3
ALTO = TABLERO_PX + MARGEN * 2


FONDO = (24, 26, 38)
PANEL = (38, 41, 58)
CASILLA_CLARA = (235, 236, 208)
CASILLA_OSCURA = (119, 153, 84)
SELECCION = (246, 246, 105)
MOV_PUNTO = (60, 120, 200)
CAPTURA_ANILLO = (215, 60, 70)
ULTIMO_MOV = (246, 200, 90)
TEXTO = (240, 240, 245)
TEXTO_TENUE = (150, 153, 170)
AMARILLO = (255, 214, 10)
ROJO_POKE = (215, 38, 61)

RUTA_BASE = os.path.dirname(os.path.abspath(__file__))
RUTA_ASSETS = os.path.join(RUTA_BASE, "assets")


class JuegoAjedrez:
    """Controla la ventana, el dibujo y la interaccion del juego."""

    def __init__(self):
        """Inicializa pygame, la ventana y carga los recursos."""
        pygame.init()
        pygame.display.set_caption("Ajedrez Pokemon")
        self.ventana = pygame.display.set_mode((ANCHO, ALTO))
        self.reloj = pygame.time.Clock()

        # Fuentes
        self.fuenteTitulo = pygame.font.SysFont("arialblack", 26)
        self.fuenteNormal = pygame.font.SysFont("arial", 20)
        self.fuentePeq = pygame.font.SysFont("arial", 15)

        self.sprites = {}
        self._cargarSprites()

        self.tablero = Tablero()
        self.seleccion = None
        self.movimientosValidos = []
        self.finJuego = None  


    def _cargarSprites(self):
        """Carga las imagenes de las piezas y las escala a la casilla."""
        tamPieza = TAM_CASILLA - 12
        for tipo in NOMBRE_POKEMON.values():
            for color in ("w", "b"):
                clave = f"{tipo}_{color}"
                ruta = os.path.join(RUTA_ASSETS, f"{clave}.png")
                if os.path.exists(ruta):
                    img = pygame.image.load(ruta).convert_alpha()
                    img = pygame.transform.smoothscale(img, (tamPieza, tamPieza))
                    self.sprites[clave] = img

    def _origenTablero(self):
        """Esquina superior izquierda del tablero en pixeles."""
        return MARGEN, MARGEN

    def _casillaDesdePixel(self, x, y):
        """Convierte un pixel de pantalla en (fila, col) o None."""
        ox, oy = self._origenTablero()
        if ox <= x < ox + TABLERO_PX and oy <= y < oy + TABLERO_PX:
            col = (x - ox) // TAM_CASILLA
            fila = (y - oy) // TAM_CASILLA
            return int(fila), int(col)
        return None

    def _dibujarTablero(self):
        """Dibuja las casillas, resaltados, piezas y movimientos."""
        ox, oy = self._origenTablero()
        ultimo = self.tablero.ultimoMovimiento

        for fila in range(8):
            for col in range(8):
                x = ox + col * TAM_CASILLA
                y = oy + fila * TAM_CASILLA
                claro = (fila + col) % 2 == 0
                color = CASILLA_CLARA if claro else CASILLA_OSCURA

               
                if ultimo is not None and ((fila, col) == ultimo[0] or
                                           (fila, col) == ultimo[1]):
                    color = ULTIMO_MOV

                pygame.draw.rect(self.ventana, color,
                                 (x, y, TAM_CASILLA, TAM_CASILLA))

      
        if self.seleccion is not None:
            f, c = self.seleccion
            x = ox + c * TAM_CASILLA
            y = oy + f * TAM_CASILLA
            pygame.draw.rect(self.ventana, SELECCION,
                             (x, y, TAM_CASILLA, TAM_CASILLA), 5)

        for fila in range(8):
            for col in range(8):
                pieza = self.tablero.piezaEn(fila, col)
                if pieza is None:
                    continue
                x = ox + col * TAM_CASILLA
                y = oy + fila * TAM_CASILLA
                sprite = self.sprites.get(pieza.claveSprite())
                if sprite is not None:
                    rect = sprite.get_rect(center=(x + TAM_CASILLA // 2,
                                                   y + TAM_CASILLA // 2))
                    self.ventana.blit(sprite, rect)
                else:
                    self._dibujarPiezaRespaldo(pieza, x, y)

       
        for (fila, col) in self.movimientosValidos:
            x = ox + col * TAM_CASILLA + TAM_CASILLA // 2
            y = oy + fila * TAM_CASILLA + TAM_CASILLA // 2
            destino = self.tablero.piezaEn(fila, col)
            if destino is None:
                pygame.draw.circle(self.ventana, MOV_PUNTO, (x, y), 12)
            else:
                pygame.draw.circle(self.ventana, CAPTURA_ANILLO, (x, y),
                                   TAM_CASILLA // 2 - 4, 5)

        pygame.draw.rect(self.ventana, ROJO_POKE,
                         (ox - 4, oy - 4, TABLERO_PX + 8, TABLERO_PX + 8), 4)

    def _dibujarPiezaRespaldo(self, pieza, x, y):
        """Dibuja una pieza simple si faltara su imagen (a prueba de fallos)."""
        cx = x + TAM_CASILLA // 2
        cy = y + TAM_CASILLA // 2
        relleno = (235, 235, 235) if pieza.color == BLANCO else (45, 45, 45)
        borde = (45, 45, 45) if pieza.color == BLANCO else (235, 235, 235)
        pygame.draw.circle(self.ventana, relleno, (cx, cy), TAM_CASILLA // 2 - 10)
        pygame.draw.circle(self.ventana, borde, (cx, cy), TAM_CASILLA // 2 - 10, 3)
        txt = self.fuenteNormal.render(pieza.tipo, True, borde)
        self.ventana.blit(txt, txt.get_rect(center=(cx, cy)))

    def _dibujarPanel(self):
        """Dibuja el panel lateral con turno, estado y capturas."""
        px = MARGEN * 2 + TABLERO_PX
        py = MARGEN
        ancho = PANEL_PX
        alto = TABLERO_PX
        pygame.draw.rect(self.ventana, PANEL, (px, py, ancho, alto),
                         border_radius=12)

        cx = px + 16
        y = py + 18

        titulo = self.fuenteTitulo.render("Ajedrez", True, AMARILLO)
        self.ventana.blit(titulo, (cx, y))
        y += 30
        sub = self.fuentePeq.render("Edicion Pokemon", True, TEXTO_TENUE)
        self.ventana.blit(sub, (cx, y))
        y += 34

        if self.finJuego is None:
            estado = self.tablero.estadoJuego()
            quien = "BLANCAS" if self.tablero.turno == BLANCO else "NEGRAS"
            txtTurno = self.fuenteNormal.render(f"Turno: {quien}", True, TEXTO)
            self.ventana.blit(txtTurno, (cx, y))
            y += 28
            if estado == "jaque":
                aviso = self.fuentePeq.render("JAQUE al rey!", True, ROJO_POKE)
                self.ventana.blit(aviso, (cx, y))
            y += 24
        else:
            for linea in self.finJuego.split("\n"):
                txt = self.fuenteNormal.render(linea, True, AMARILLO)
                self.ventana.blit(txt, (cx, y))
                y += 26
            y += 6
            txt = self.fuentePeq.render("Pulsa R para reiniciar", True, TEXTO_TENUE)
            self.ventana.blit(txt, (cx, y))
            y += 24

        y += 16
        self._dibujarCapturas(cx, y)

     
        ayuda = [
            "Clic: seleccionar / mover",
            "R: reiniciar",
            "ESC: salir",
        ]
        yy = py + alto - 70
        for linea in ayuda:
            txt = self.fuentePeq.render(linea, True, TEXTO_TENUE)
            self.ventana.blit(txt, (cx, yy))
            yy += 20

    def _dibujarCapturas(self, cx, y):
        """Muestra el conteo de piezas capturadas por cada bando."""
        def resumen(lista):
            if not lista:
                return "-"
            conteo = {}
            for p in lista:
                n = NOMBRE_POKEMON[p.tipo].capitalize()
                conteo[n] = conteo.get(n, 0) + 1
            return ", ".join(f"{n} x{c}" for n, c in conteo.items())

        etiqueta = self.fuentePeq.render("Capturas blancas:", True, MOV_PUNTO)
        self.ventana.blit(etiqueta, (cx, y))
        y += 18
        for trozo in self._envolver(resumen(self.tablero.capturas[BLANCO]), 26):
            self.ventana.blit(self.fuentePeq.render(trozo, True, TEXTO), (cx, y))
            y += 18
        y += 10
        etiqueta = self.fuentePeq.render("Capturas negras:", True, MOV_PUNTO)
        self.ventana.blit(etiqueta, (cx, y))
        y += 18
        for trozo in self._envolver(resumen(self.tablero.capturas[NEGRO]), 26):
            self.ventana.blit(self.fuentePeq.render(trozo, True, TEXTO), (cx, y))
            y += 18

    def _envolver(self, texto, maxCar):
        """Parte un texto en lineas de a lo sumo maxCar caracteres."""
        palabras = texto.split(" ")
        lineas, actual = [], ""
        for p in palabras:
            if len(actual) + len(p) + 1 <= maxCar:
                actual = (actual + " " + p).strip()
            else:
                lineas.append(actual)
                actual = p
        if actual:
            lineas.append(actual)
        return lineas or ["-"]


    def _clic(self, x, y):
        """Procesa un clic del raton en la posicion (x,y)."""
        if self.finJuego is not None:
            return
        casilla = self._casillaDesdePixel(x, y)
        if casilla is None:
            return
        fila, col = casilla
        pieza = self.tablero.piezaEn(fila, col)

      
        if self.seleccion is None:
            if pieza is not None and pieza.color == self.tablero.turno:
                self.seleccion = (fila, col)
                self.movimientosValidos = self.tablero.movimientosPieza(fila, col)
            return

        fo, co = self.seleccion

        if (fila, col) == self.seleccion:
            self._limpiarSeleccion()
            return

       
        if pieza is not None and pieza.color == self.tablero.turno:
            self.seleccion = (fila, col)
            self.movimientosValidos = self.tablero.movimientosPieza(fila, col)
            return

        
        if (fila, col) in self.movimientosValidos:
            self.tablero.mover(fo, co, fila, col)
            self._limpiarSeleccion()
            self._verificarFinal()
        else:
            self._limpiarSeleccion()

    def _limpiarSeleccion(self):
        """Borra la seleccion actual."""
        self.seleccion = None
        self.movimientosValidos = []

    def _verificarFinal(self):
        """Revisa si la partida termino y guarda el mensaje de resultado."""
        estado = self.tablero.estadoJuego()
        if estado == "jaque_mate":
            ganador = "NEGRAS" if self.tablero.turno == BLANCO else "BLANCAS"
            self.finJuego = f"JAQUE MATE\nGanan {ganador}"
        elif estado == "tablas":
            self.finJuego = "TABLAS\n(ahogado)"

    def _reiniciar(self):
        """Reinicia la partida desde cero."""
        self.tablero = Tablero()
        self._limpiarSeleccion()
        self.finJuego = None

    
    def ejecutar(self):
        """Bucle principal del juego."""
        corriendo = True
        while corriendo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False
                elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    self._clic(*evento.pos)
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        corriendo = False
                    elif evento.key == pygame.K_r:
                        self._reiniciar()

            self.ventana.fill(FONDO)
            self._dibujarTablero()
            self._dibujarPanel()
            pygame.display.flip()
            self.reloj.tick(60)

        pygame.quit()
        sys.exit()


def main():
    """Punto de entrada del programa."""
    JuegoAjedrez().ejecutar()


if __name__ == "__main__":
    main()
main.py
