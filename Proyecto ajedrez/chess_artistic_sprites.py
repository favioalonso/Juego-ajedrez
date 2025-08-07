import pygame
import sys
import math
from typing import List, Tuple, Optional

# Inicializar pygame
pygame.init()

# Constantes
BOARD_SIZE = 8
SQUARE_SIZE = 100
WINDOW_WIDTH = BOARD_SIZE * SQUARE_SIZE
WINDOW_HEIGHT = BOARD_SIZE * SQUARE_SIZE + 120
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BROWN = (240, 217, 181)
DARK_BROWN = (181, 136, 99)
HIGHLIGHT_COLOR = (255, 255, 0)
SELECTED_COLOR = (0, 255, 0)

# Colores para las piezas
PIECE_WHITE = (250, 248, 240)
PIECE_WHITE_DARK = (220, 218, 210)
PIECE_BLACK = (60, 60, 60)
PIECE_BLACK_DARK = (30, 30, 30)
GOLD = (255, 215, 0)

class PieceRenderer:
    """Clase para renderizar piezas con sprites dibujados"""
    
    @staticmethod
    def create_piece_surface(piece_type: str, color: str, size: int = 80) -> pygame.Surface:
        """Crear una superficie con la pieza dibujada"""
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        center = size // 2
        
        # Colores según el color de la pieza
        if color == 'white':
            main_color = PIECE_WHITE
            dark_color = PIECE_WHITE_DARK
            outline_color = (150, 150, 150)
        else:
            main_color = PIECE_BLACK
            dark_color = PIECE_BLACK_DARK
            outline_color = (100, 100, 100)
        
        if piece_type == 'pawn':
            PieceRenderer.draw_pawn(surface, center, center, main_color, dark_color, outline_color, size)
        elif piece_type == 'rook':
            PieceRenderer.draw_rook(surface, center, center, main_color, dark_color, outline_color, size)
        elif piece_type == 'knight':
            PieceRenderer.draw_knight(surface, center, center, main_color, dark_color, outline_color, size)
        elif piece_type == 'bishop':
            PieceRenderer.draw_bishop(surface, center, center, main_color, dark_color, outline_color, size)
        elif piece_type == 'queen':
            PieceRenderer.draw_queen(surface, center, center, main_color, dark_color, outline_color, size)
        elif piece_type == 'king':
            PieceRenderer.draw_king(surface, center, center, main_color, dark_color, outline_color, size)
        
        return surface
    
    @staticmethod
    def draw_pawn(surface, x, y, main_color, dark_color, outline_color, size):
        """Dibujar un peón"""
        scale = size / 80
        
        # Cuerpo principal
        head_radius = int(12 * scale)
        body_width = int(16 * scale)
        body_height = int(20 * scale)
        base_width = int(24 * scale)
        base_height = int(8 * scale)
        
        # Cabeza
        pygame.draw.circle(surface, main_color, (x, y - int(15 * scale)), head_radius)
        pygame.draw.circle(surface, outline_color, (x, y - int(15 * scale)), head_radius, 2)
        
        # Cuerpo
        body_rect = pygame.Rect(x - body_width//2, y - int(5 * scale), body_width, body_height)
        pygame.draw.ellipse(surface, main_color, body_rect)
        pygame.draw.ellipse(surface, outline_color, body_rect, 2)
        
        # Base
        base_rect = pygame.Rect(x - base_width//2, y + int(15 * scale), base_width, base_height)
        pygame.draw.ellipse(surface, dark_color, base_rect)
        pygame.draw.ellipse(surface, outline_color, base_rect, 2)
    
    @staticmethod
    def draw_rook(surface, x, y, main_color, dark_color, outline_color, size):
        """Dibujar una torre"""
        scale = size / 80
        
        # Base
        base_width = int(32 * scale)
        base_height = int(10 * scale)
        base_rect = pygame.Rect(x - base_width//2, y + int(15 * scale), base_width, base_height)
        pygame.draw.rect(surface, dark_color, base_rect)
        pygame.draw.rect(surface, outline_color, base_rect, 2)
        
        # Cuerpo principal
        body_width = int(24 * scale)
        body_height = int(35 * scale)
        body_rect = pygame.Rect(x - body_width//2, y - int(20 * scale), body_width, body_height)
        pygame.draw.rect(surface, main_color, body_rect)
        pygame.draw.rect(surface, outline_color, body_rect, 2)
        
        # Almenas (parte superior)
        battlements_y = y - int(20 * scale)
        battlement_width = int(6 * scale)
        battlement_height = int(8 * scale)
        
        for i in range(4):
            if i % 2 == 0:  # Solo dibujar en posiciones pares para crear el efecto de almenas
                batt_x = x - body_width//2 + i * (body_width // 3)
                batt_rect = pygame.Rect(batt_x, battlements_y - battlement_height, 
                                      battlement_width, battlement_height)
                pygame.draw.rect(surface, main_color, batt_rect)
                pygame.draw.rect(surface, outline_color, batt_rect, 1)
    
    @staticmethod
    def draw_knight(surface, x, y, main_color, dark_color, outline_color, size):
        """Dibujar un caballo"""
        scale = size / 80
        
        # Base
        base_width = int(30 * scale)
        base_height = int(8 * scale)
        base_rect = pygame.Rect(x - base_width//2, y + int(15 * scale), base_width, base_height)
        pygame.draw.ellipse(surface, dark_color, base_rect)
        pygame.draw.ellipse(surface, outline_color, base_rect, 2)
        
        # Cabeza del caballo (forma estilizada)
        head_points = [
            (x - int(8 * scale), y + int(10 * scale)),   # Base izquierda
            (x - int(12 * scale), y - int(5 * scale)),   # Cuello
            (x - int(8 * scale), y - int(20 * scale)),   # Parte superior cabeza
            (x + int(2 * scale), y - int(25 * scale)),   # Orejas
            (x + int(10 * scale), y - int(18 * scale)),  # Hocico
            (x + int(12 * scale), y - int(5 * scale)),   # Mandíbula
            (x + int(8 * scale), y + int(10 * scale)),   # Base derecha
        ]
        
        pygame.draw.polygon(surface, main_color, head_points)
        pygame.draw.polygon(surface, outline_color, head_points, 2)
        
        # Crin
        mane_points = [
            (x - int(12 * scale), y - int(5 * scale)),
            (x - int(15 * scale), y - int(15 * scale)),
            (x - int(8 * scale), y - int(20 * scale)),
        ]
        pygame.draw.polygon(surface, dark_color, mane_points)
        
        # Ojo
        pygame.draw.circle(surface, BLACK, (x + int(2 * scale), y - int(15 * scale)), int(2 * scale))
    
    @staticmethod
    def draw_bishop(surface, x, y, main_color, dark_color, outline_color, size):
        """Dibujar un alfil"""
        scale = size / 80
        
        # Base
        base_width = int(28 * scale)
        base_height = int(8 * scale)
        base_rect = pygame.Rect(x - base_width//2, y + int(15 * scale), base_width, base_height)
        pygame.draw.ellipse(surface, dark_color, base_rect)
        pygame.draw.ellipse(surface, outline_color, base_rect, 2)
        
        # Cuerpo (forma de gota)
        body_points = [
            (x, y - int(25 * scale)),                    # Punta superior
            (x - int(8 * scale), y - int(15 * scale)),   # Lado izquierdo superior
            (x - int(12 * scale), y),                    # Lado izquierdo medio
            (x - int(10 * scale), y + int(10 * scale)),  # Lado izquierdo inferior
            (x + int(10 * scale), y + int(10 * scale)),  # Lado derecho inferior
            (x + int(12 * scale), y),                    # Lado derecho medio
            (x + int(8 * scale), y - int(15 * scale)),   # Lado derecho superior
        ]
        
        pygame.draw.polygon(surface, main_color, body_points)
        pygame.draw.polygon(surface, outline_color, body_points, 2)
        
        # Hendidura característica en la parte superior
        pygame.draw.line(surface, outline_color, 
                        (x - int(3 * scale), y - int(25 * scale)), 
                        (x + int(3 * scale), y - int(25 * scale)), 3)
        
        # Líneas decorativas
        for i in range(3):
            y_line = y - int(10 * scale) + i * int(8 * scale)
            pygame.draw.line(surface, dark_color, 
                           (x - int(8 * scale), y_line), 
                           (x + int(8 * scale), y_line), 1)
    
    @staticmethod
    def draw_queen(surface, x, y, main_color, dark_color, outline_color, size):
        """Dibujar una reina"""
        scale = size / 80
        
        # Base
        base_width = int(32 * scale)
        base_height = int(10 * scale)
        base_rect = pygame.Rect(x - base_width//2, y + int(15 * scale), base_width, base_height)
        pygame.draw.ellipse(surface, dark_color, base_rect)
        pygame.draw.ellipse(surface, outline_color, base_rect, 2)
        
        # Cuerpo
        body_width = int(20 * scale)
        body_height = int(25 * scale)
        body_rect = pygame.Rect(x - body_width//2, y - int(5 * scale), body_width, body_height)
        pygame.draw.ellipse(surface, main_color, body_rect)
        pygame.draw.ellipse(surface, outline_color, body_rect, 2)
        
        # Corona con 5 puntas
        crown_base_y = y - int(5 * scale)
        crown_radius = int(12 * scale)
        
        # Base de la corona
        pygame.draw.circle(surface, main_color, (x, crown_base_y), crown_radius)
        pygame.draw.circle(surface, outline_color, (x, crown_base_y), crown_radius, 2)
        
        # Puntas de la corona
        crown_points = []
        for i in range(5):
            angle = (i * 72 - 90) * math.pi / 180
            point_x = x + math.cos(angle) * crown_radius
            point_y = crown_base_y + math.sin(angle) * crown_radius
            
            # Punta alta en el centro y las esquinas
            if i == 0 or i == 2 or i == 3:
                point_y -= int(8 * scale)
            else:
                point_y -= int(4 * scale)
            
            crown_points.append((int(point_x), int(point_y)))
        
        # Dibujar la corona
        if len(crown_points) >= 3:
            pygame.draw.polygon(surface, GOLD, crown_points)
            pygame.draw.polygon(surface, outline_color, crown_points, 2)
    
    @staticmethod
    def draw_king(surface, x, y, main_color, dark_color, outline_color, size):
        """Dibujar un rey"""
        scale = size / 80
        
        # Base
        base_width = int(34 * scale)
        base_height = int(10 * scale)
        base_rect = pygame.Rect(x - base_width//2, y + int(15 * scale), base_width, base_height)
        pygame.draw.ellipse(surface, dark_color, base_rect)
        pygame.draw.ellipse(surface, outline_color, base_rect, 2)
        
        # Cuerpo
        body_width = int(22 * scale)
        body_height = int(30 * scale)
        body_rect = pygame.Rect(x - body_width//2, y - int(10 * scale), body_width, body_height)
        pygame.draw.ellipse(surface, main_color, body_rect)
        pygame.draw.ellipse(surface, outline_color, body_rect, 2)
        
        # Corona base
        crown_width = int(20 * scale)
        crown_height = int(12 * scale)
        crown_rect = pygame.Rect(x - crown_width//2, y - int(22 * scale), crown_width, crown_height)
        pygame.draw.ellipse(surface, GOLD, crown_rect)
        pygame.draw.ellipse(surface, outline_color, crown_rect, 2)
        
        # Cruz en la corona
        cross_size = int(8 * scale)
        cross_thickness = int(3 * scale)
        cross_y = y - int(16 * scale)
        
        # Línea horizontal de la cruz
        pygame.draw.rect(surface, main_color, 
                        (x - cross_size//2, cross_y - cross_thickness//2, 
                         cross_size, cross_thickness))
        
        # Línea vertical de la cruz
        pygame.draw.rect(surface, main_color, 
                        (x - cross_thickness//2, cross_y - cross_size//2, 
                         cross_thickness, cross_size))
        
        # Contorno de la cruz
        pygame.draw.rect(surface, outline_color, 
                        (x - cross_size//2, cross_y - cross_thickness//2, 
                         cross_size, cross_thickness), 1)
        pygame.draw.rect(surface, outline_color, 
                        (x - cross_thickness//2, cross_y - cross_size//2, 
                         cross_thickness, cross_size), 1)

class Piece:
    def __init__(self, color: str, piece_type: str, row: int, col: int):
        self.color = color
        self.piece_type = piece_type
        self.row = row
        self.col = col
        self.has_moved = False
        # Crear el sprite de la pieza
        self.sprite = PieceRenderer.create_piece_surface(piece_type, color, 80)
    
    def get_possible_moves(self, board) -> List[Tuple[int, int]]:
        moves = []
        
        if self.piece_type == 'pawn':
            moves = self._get_pawn_moves(board)
        elif self.piece_type == 'rook':
            moves = self._get_rook_moves(board)
        elif self.piece_type == 'knight':
            moves = self._get_knight_moves(board)
        elif self.piece_type == 'bishop':
            moves = self._get_bishop_moves(board)
        elif self.piece_type == 'queen':
            moves = self._get_queen_moves(board)
        elif self.piece_type == 'king':
            moves = self._get_king_moves(board)
        
        return moves
    
    def _get_pawn_moves(self, board) -> List[Tuple[int, int]]:
        moves = []
        direction = -1 if self.color == 'white' else 1
        start_row = 6 if self.color == 'white' else 1
        
        new_row = self.row + direction
        if 0 <= new_row < 8 and board[new_row][self.col] is None:
            moves.append((new_row, self.col))
            
            if self.row == start_row and board[new_row + direction][self.col] is None:
                moves.append((new_row + direction, self.col))
        
        for col_offset in [-1, 1]:
            new_col = self.col + col_offset
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = board[new_row][new_col]
                if target and target.color != self.color:
                    moves.append((new_row, new_col))
        
        return moves
    
    def _get_rook_moves(self, board) -> List[Tuple[int, int]]:
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        for dr, dc in directions:
            for i in range(1, 8):
                new_row = self.row + i * dr
                new_col = self.col + i * dc
                
                if not (0 <= new_row < 8 and 0 <= new_col < 8):
                    break
                
                target = board[new_row][new_col]
                if target is None:
                    moves.append((new_row, new_col))
                elif target.color != self.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
        
        return moves
    
    def _get_knight_moves(self, board) -> List[Tuple[int, int]]:
        moves = []
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        
        for dr, dc in knight_moves:
            new_row = self.row + dr
            new_col = self.col + dc
            
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = board[new_row][new_col]
                if target is None or target.color != self.color:
                    moves.append((new_row, new_col))
        
        return moves
    
    def _get_bishop_moves(self, board) -> List[Tuple[int, int]]:
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dr, dc in directions:
            for i in range(1, 8):
                new_row = self.row + i * dr
                new_col = self.col + i * dc
                
                if not (0 <= new_row < 8 and 0 <= new_col < 8):
                    break
                
                target = board[new_row][new_col]
                if target is None:
                    moves.append((new_row, new_col))
                elif target.color != self.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
        
        return moves
    
    def _get_queen_moves(self, board) -> List[Tuple[int, int]]:
        return self._get_rook_moves(board) + self._get_bishop_moves(board)
    
    def _get_king_moves(self, board) -> List[Tuple[int, int]]:
        moves = []
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        
        for dr, dc in directions:
            new_row = self.row + dr
            new_col = self.col + dc
            
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = board[new_row][new_col]
                if target is None or target.color != self.color:
                    moves.append((new_row, new_col))
        
        return moves

class ChessGame:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.current_player = 'white'
        self.selected_piece = None
        self.selected_pos = None
        self.possible_moves = []
        self.game_over = False
        self.winner = None
        self._setup_board()
    
    def _setup_board(self):
        # Peones
        for col in range(8):
            self.board[1][col] = Piece('black', 'pawn', 1, col)
            self.board[6][col] = Piece('white', 'pawn', 6, col)
        
        # Piezas especiales
        piece_order = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
        
        for col, piece_type in enumerate(piece_order):
            self.board[0][col] = Piece('black', piece_type, 0, col)
            self.board[7][col] = Piece('white', piece_type, 7, col)
    
    def get_piece_at(self, row: int, col: int) -> Optional[Piece]:
        if 0 <= row < 8 and 0 <= col < 8:
            return self.board[row][col]
        return None
    
    def move_piece(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        piece = self.board[from_row][from_col]
        if not piece or piece.color != self.current_player:
            return False
        
        possible_moves = piece.get_possible_moves(self.board)
        if (to_row, to_col) not in possible_moves:
            return False
        
        captured_piece = self.board[to_row][to_col]
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = None
        piece.row = to_row
        piece.col = to_col
        piece.has_moved = True
        
        if captured_piece and captured_piece.piece_type == 'king':
            self.game_over = True
            self.winner = self.current_player
        
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        return True
    
    def select_piece(self, row: int, col: int):
        piece = self.board[row][col]
        
        if self.selected_piece and (row, col) in self.possible_moves:
            if self.move_piece(self.selected_piece.row, self.selected_piece.col, row, col):
                self.selected_piece = None
                self.selected_pos = None
                self.possible_moves = []
        elif piece and piece.color == self.current_player:
            self.selected_piece = piece
            self.selected_pos = (row, col)
            self.possible_moves = piece.get_possible_moves(self.board)
        else:
            self.selected_piece = None
            self.selected_pos = None
            self.possible_moves = []

class ChessGUI:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("♔ Ajedrez con Sprites Artísticos ♔")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 32)
        self.big_font = pygame.font.Font(None, 48)
        self.game = ChessGame()
    
    def draw_board(self):
        """Dibujar tablero con efectos visuales mejorados"""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x = col * SQUARE_SIZE
                y = row * SQUARE_SIZE
                
                # Color de la casilla
                if (row + col) % 2 == 0:
                    color = LIGHT_BROWN
                else:
                    color = DARK_BROWN
                
                # Dibujar casilla
                rect = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(self.screen, color, rect)
                
                # Agregar borde sutil
                pygame.draw.rect(self.screen, (0, 0, 0, 20), rect, 1)
                
                # Highlight casilla seleccionada
                if self.game.selected_pos == (row, col):
                    highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    highlight_surface.fill((*SELECTED_COLOR, 120))
                    self.screen.blit(highlight_surface, (x, y))
                    
                    # Borde brillante
                    pygame.draw.rect(self.screen, SELECTED_COLOR, rect, 4)
                
                # Highlight movimientos posibles
                if (row, col) in self.game.possible_moves:
                    piece_at_target = self.game.board[row][col]
                    
                    if piece_at_target:
                        # Captura - círculo rojo con pulsación
                        pygame.draw.circle(self.screen, (255, 100, 100), 
                                         (x + SQUARE_SIZE//2, y + SQUARE_SIZE//2), 
                                         SQUARE_SIZE//3, 6)
                        pygame.draw.circle(self.screen, (255, 0, 0), 
                                         (x + SQUARE_SIZE//2, y + SQUARE_SIZE//2), 
                                         SQUARE_SIZE//4, 3)
                    else:
                        # Movimiento normal - círculo amarillo elegante
                        pygame.draw.circle(self.screen, (255, 255, 150), 
                                         (x + SQUARE_SIZE//2, y + SQUARE_SIZE//2), 
                                         SQUARE_SIZE//5)
                        pygame.draw.circle(self.screen, HIGHLIGHT_COLOR, 
                                         (x + SQUARE_SIZE//2, y + SQUARE_SIZE//2), 
                                         SQUARE_SIZE//5, 3)
        
        # Coordenadas del tablero
        coord_font = pygame.font.Font(None, 24)
        for i in range(8):
            # Números (filas)
            text = coord_font.render(str(8-i), True, BLACK)
            self.screen.blit(text, (5, i * SQUARE_SIZE + 10))
            
            # Letras (columnas)
            text = coord_font.render(chr(ord('a') + i), True, BLACK)
            self.screen.blit(text, (i * SQUARE_SIZE + SQUARE_SIZE - 20, BOARD_SIZE * SQUARE_SIZE - 25))
    
    def draw_pieces(self):
        """Dibujar piezas usando sprites generados"""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.game.board[row][col]
                if piece:
                    x = col * SQUARE_SIZE + (SQUARE_SIZE - 80) // 2
                    y = row * SQUARE_SIZE + (SQUARE_SIZE - 80) // 2
                    
                    # Dibujar sombra sutil
                    shadow_surface = piece.sprite.copy()
                    shadow_surface.fill((0, 0, 0, 60), special_flags=pygame.BLEND_RGBA_MULT)
                    self.screen.blit(shadow_surface, (x + 3, y + 3))
                    
                    # Dibujar la pieza
                    self.screen.blit(piece.sprite, (x, y))
    
    def draw_info(self):
        """Dibujar información del juego con estilo"""
        info_y = BOARD_SIZE * SQUARE_SIZE + 15
        
        # Fondo para la información
        info_bg = pygame.Rect(0, BOARD_SIZE * SQUARE_SIZE, WINDOW_WIDTH, 120)
        pygame.draw.rect(self.screen, (250, 250, 250), info_bg)
        pygame.draw.rect(self.screen, (200, 200, 200), info_bg, 2)
        
        # Estado del juego
        if self.game.game_over:
            text = f"🏆 ¡{self.game.winner.upper()} GANA!"
            color = (220, 20, 60)  # Crimson
        else:
            player_icon = "♔" if self.game.current_player == "white" else "♚"
            text = f"{player_icon} Turno: {self.game.current_player.capitalize()}"
            color = (50, 50, 150)  # Azul oscuro
        
        text_surface = self.big_font.render(text, True, color)
        self.screen.blit(text_surface, (15, info_y))
        
        # Instrucciones con iconos
        instructions = [
            "🖱️ Click para seleccionar piezas",
            "🎯 Círculos amarillos = movimientos válidos",
            "🔴 Círculos rojos = capturas posibles",
            "⌨️ Presiona 'R' para reiniciar"
        ]
        
        for i, instruction in enumerate(instructions):
            inst_surface = self.font.render(instruction, True, (80, 80, 80))
            self.screen.blit(inst_surface, (15, info_y + 50 + i * 20))
    
    def handle_click(self, pos):
        if pos[1] < BOARD_SIZE * SQUARE_SIZE:
            col = pos[0] // SQUARE_SIZE
            row = pos[1] // SQUARE_SIZE
            self.game.select_piece(row, col)
    
    def run(self):
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.game.game_over:
                        self.game = ChessGame()
            
            # Fondo con gradiente sutil
            for y in range(WINDOW_HEIGHT):
                intensity = int(240 + 15 * math.sin(y * 0.01))
                color = (intensity, intensity, intensity + 5)
                pygame.draw.line(self.screen, color, (0, y), (WINDOW_WIDTH, y))
            
            self.draw_board()
            self.draw_pieces()
            self.draw_info()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    print("🎨 Iniciando Ajedrez con Sprites Artísticos...")
    print("✨ Características:")
    print("  • Piezas dibujadas con sprites detallados")
    print("  • Efectos de sombra y gradientes")
    print("  • Animaciones visuales suaves")
    print("  • Interfaz completamente rediseñada")
    print("=" * 60)
    
    game = ChessGUI()
    game.run()
