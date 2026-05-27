BLANCO = "w"
NEGRO = "b"

NOMBRE_POKEMON = {
    "P": "rattata",
    "N": "groudon",
    "B": "kyogre",
    "R": "mewtwo",
    "Q": "rayquaza",
    "K": "arceus",
}


class Pieza:
    def __init__(self, tipo, color):
        self.tipo = tipo
        self.color = color
        self.seHaMovido = False

    def claveSprite(self):
        return f"{NOMBRE_POKEMON[self.tipo]}_{self.color}"


class Tablero:
    def __init__(self):
        self.matriz = [[None for _ in range(8)] for _ in range(8)]
        self.turno = BLANCO
        self.ultimoMovimiento = None
        self.capturas = {BLANCO: [], NEGRO: []}
        self.colocarPosicionInicial()

    def colocarPosicionInicial(self):
        ordenPrincipal = ["R", "N", "B", "Q", "K", "B", "N", "R"]
        for col, tipo in enumerate(ordenPrincipal):
            self.matriz[0][col] = Pieza(tipo, NEGRO)
            self.matriz[1][col] = Pieza("P", NEGRO)
            self.matriz[6][col] = Pieza("P", BLANCO)
            self.matriz[7][col] = Pieza(tipo, BLANCO)

    def dentro(self, fila, col):
        return 0 <= fila < 8 and 0 <= col < 8

    def piezaEn(self, fila, col):
        return self.matriz[fila][col]

    def colorContrario(self, color):
        return NEGRO if color == BLANCO else BLANCO

    def movimientosPieza(self, fila, col, validarJaque=True):
        pieza = self.matriz[fila][col]
        if pieza is None:
            return []
        bruto = self._movimientosBrutos(fila, col, pieza)
        if not validarJaque:
            return bruto
        legales = []
        for (fd, cd) in bruto:
            if not self._dejaReyEnJaque(fila, col, fd, cd, pieza.color):
                legales.append((fd, cd))
        return legales

    def _movimientosBrutos(self, fila, col, pieza):
        if pieza.tipo == "P":
            return self._movPeon(fila, col, pieza)
        if pieza.tipo == "N":
            return self._movCaballo(fila, col, pieza)
        if pieza.tipo == "B":
            return self._movDeslizante(fila, col, pieza,
                                       [(-1, -1), (-1, 1), (1, -1), (1, 1)])
        if pieza.tipo == "R":
            return self._movDeslizante(fila, col, pieza,
                                       [(-1, 0), (1, 0), (0, -1), (0, 1)])
        if pieza.tipo == "Q":
            return self._movDeslizante(fila, col, pieza,
                                       [(-1, -1), (-1, 1), (1, -1), (1, 1),
                                        (-1, 0), (1, 0), (0, -1), (0, 1)])
        if pieza.tipo == "K":
            return self._movRey(fila, col, pieza)
        return []

    def _movPeon(self, fila, col, pieza):
        movs = []
        direccion = -1 if pieza.color == BLANCO else 1
        inicio = 6 if pieza.color == BLANCO else 1

        unPaso = fila + direccion
        if self.dentro(unPaso, col) and self.matriz[unPaso][col] is None:
            movs.append((unPaso, col))
            dosPasos = fila + 2 * direccion
            if fila == inicio and self.matriz[dosPasos][col] is None:
                movs.append((dosPasos, col))

        for dc in (-1, 1):
            fd, cd = fila + direccion, col + dc
            if self.dentro(fd, cd):
                objetivo = self.matriz[fd][cd]
                if objetivo is not None and objetivo.color != pieza.color:
                    movs.append((fd, cd))
        return movs

    def _movCaballo(self, fila, col, pieza):
        saltos = [(-2, -1), (-2, 1), (2, -1), (2, 1),
                  (-1, -2), (-1, 2), (1, -2), (1, 2)]
        movs = []
        for df, dc in saltos:
            fd, cd = fila + df, col + dc
            if self.dentro(fd, cd):
                objetivo = self.matriz[fd][cd]
                if objetivo is None or objetivo.color != pieza.color:
                    movs.append((fd, cd))
        return movs

    def _movDeslizante(self, fila, col, pieza, direcciones):
        movs = []
        for df, dc in direcciones:
            fd, cd = fila + df, col + dc
            while self.dentro(fd, cd):
                objetivo = self.matriz[fd][cd]
                if objetivo is None:
                    movs.append((fd, cd))
                else:
                    if objetivo.color != pieza.color:
                        movs.append((fd, cd))
                    break
                fd, cd = fd + df, cd + dc
        return movs

    def _movRey(self, fila, col, pieza):
        movs = []
        for df in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if df == 0 and dc == 0:
                    continue
                fd, cd = fila + df, col + dc
                if self.dentro(fd, cd):
                    objetivo = self.matriz[fd][cd]
                    if objetivo is None or objetivo.color != pieza.color:
                        movs.append((fd, cd))
        return movs

    def buscarRey(self, color):
        for f in range(8):
            for c in range(8):
                p = self.matriz[f][c]
                if p is not None and p.tipo == "K" and p.color == color:
                    return (f, c)
        return None

    def casillaAtacada(self, fila, col, porColor):
        for f in range(8):
            for c in range(8):
                p = self.matriz[f][c]
                if p is not None and p.color == porColor:
                    if (fila, col) in self._movimientosBrutos(f, c, p):
                        return True
        return False

    def enJaque(self, color):
        pos = self.buscarRey(color)
        if pos is None:
            return False
        return self.casillaAtacada(pos[0], pos[1], self.colorContrario(color))

    def _dejaReyEnJaque(self, fo, co, fd, cd, color):
        piezaOrigen = self.matriz[fo][co]
        piezaDestino = self.matriz[fd][cd]
        self.matriz[fd][cd] = piezaOrigen
        self.matriz[fo][co] = None
        jaque = self.enJaque(color)
        self.matriz[fo][co] = piezaOrigen
        self.matriz[fd][cd] = piezaDestino
        return jaque

    def tieneMovimientosLegales(self, color):
        for f in range(8):
            for c in range(8):
                p = self.matriz[f][c]
                if p is not None and p.color == color:
                    if self.movimientosPieza(f, c, validarJaque=True):
                        return True
        return False

    def estadoJuego(self):
        tieneMov = self.tieneMovimientosLegales(self.turno)
        if self.enJaque(self.turno):
            return "jaque_mate" if not tieneMov else "jaque"
        return "tablas" if not tieneMov else "normal"

    def mover(self, fo, co, fd, cd):
        pieza = self.matriz[fo][co]
        capturada = self.matriz[fd][cd]

        if capturada is not None:
            self.capturas[pieza.color].append(capturada)

        self.matriz[fd][cd] = pieza
        self.matriz[fo][co] = None
        pieza.seHaMovido = True

        if pieza.tipo == "P":
            filaFinal = 0 if pieza.color == BLANCO else 7
            if fd == filaFinal:
                pieza.tipo = "Q"

        self.ultimoMovimiento = ((fo, co), (fd, cd))
        self.turno = self.colorContrario(self.turno)
