import pygame
import sys
import math
from typing import List, Tuple, Optional

# Inicializar pygame
pygame.init()

# Constantes
BOARD_SIZE = 8
SQUARE_SIZE = 100  # Más grande para mejor visualización
WINDOW_WIDTH = BOARD_SIZE * SQUARE_SIZE
WINDOW_HEIGHT = BOARD_SIZE * SQUARE_SIZE + 120
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BROWN = (240, 217, 181)
DARK_BROWN = (181, 136, 99)
HIGHLIGHT_COLOR = (255, 255, 0, 128)
SELECTED_COLOR = (0, 255, 0, 128)
CAPTURE_COLOR = (255, 0, 0, 128)

# Colores mejorados para las piezas
PIECE_WHITE_FILL = (250, 250, 250)
PIECE_WHITE_OUTLINE = (200, 200, 200)
PIECE_BLACK_FILL = (40, 40, 40)
PIECE_BLACK_OUTLINE = (80, 80, 80)
PIECE_SHADOW = (0, 0, 0, 50)

class Piece:
    def __init__(self, color: str, piece_type: str, row: int, col: int):
        self.color = color
        self.piece_type = piece_type
        self.row = row
        self.col = col
        self.has_moved = False
    
    def get_symbol(self) -> str:
        symbols = {
            'white': {
                'king': '♔', 'queen': '♕', 'rook': '♖',
                'bishop': '♗', 'knight': '♘', 'pawn': '♙'
            },
            'black': {
                'king': '♚', 'queen': '♛', 'rook': '♜',
                'bishop': '♝', 'knight': '♞', 'pawn': '♟'
            }
        }
        return symbols[self.color][self.piece_type]
    
    def get_colors(self) -> tuple:
        """Obtener colores de relleno y contorno"""
        if self.color == 'white':
            return PIECE_WHITE_FILL, PIECE_WHITE_OUTLINE
        else:
            return PIECE_BLACK_FILL, PIECE_BLACK_OUTLINE
    
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
        pygame.display.set_caption("♔ Ajedrez Visual Premium ♔")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 48)
        self.big_font = pygame.font.Font(None, 90)
        self.info_font = pygame.font.Font(None, 32)
        self.game = ChessGame()
    
    def draw_board(self):
        """Dibujar tablero con gradientes y efectos"""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x = col * SQUARE_SIZE
                y = row * SQUARE_SIZE
                
                # Color base
                if (row + col) % 2 == 0:
                    base_color = LIGHT_BROWN
                else:
                    base_color = DARK_BROWN
                
                # Dibujar casilla base
                rect = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(self.screen, base_color, rect)
                
                # Agregar efecto de borde
                pygame.draw.rect(self.screen, (0, 0, 0, 30), rect, 1)
                
                # Highlight casilla seleccionada
                if self.game.selected_pos == (row, col):
                    highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
                    highlight_surface.set_alpha(150)
                    highlight_surface.fill((0, 255, 0))
                    self.screen.blit(highlight_surface, (x, y))
                
                # Highlight movimientos posibles
                if (row, col) in self.game.possible_moves:
                    piece_at_target = self.game.board[row][col]
                    if piece_at_target:
                        # Captura - círculo rojo
                        pygame.draw.circle(self.screen, (255, 0, 0), 
                                         (x + SQUARE_SIZE//2, y + SQUARE_SIZE//2), 
                                         SQUARE_SIZE//3, 5)
                    else:
                        # Movimiento normal - círculo amarillo
                        pygame.draw.circle(self.screen, (255, 255, 0), 
                                         (x + SQUARE_SIZE//2, y + SQUARE_SIZE//2), 
                                         SQUARE_SIZE//6)
        
        # Dibujar coordenadas
        coord_font = pygame.font.Font(None, 24)
        for i in range(8):
            # Números (filas)
            text = coord_font.render(str(8-i), True, BLACK)
            self.screen.blit(text, (5, i * SQUARE_SIZE + 10))
            
            # Letras (columnas)
            text = coord_font.render(chr(ord('a') + i), True, BLACK)
            self.screen.blit(text, (i * SQUARE_SIZE + SQUARE_SIZE - 20, BOARD_SIZE * SQUARE_SIZE - 25))
    
    def draw_piece_shapes(self, piece: Piece, center_x: int, center_y: int):
        """Dibujar piezas con formas geométricas personalizadas"""
        fill_color, outline_color = piece.get_colors()
        piece_size = SQUARE_SIZE // 3
        
        if piece.piece_type == 'pawn':
            # Peón - círculo con base
            pygame.draw.circle(self.screen, fill_color, (center_x, center_y - 5), piece_size//2)
            pygame.draw.circle(self.screen, outline_color, (center_x, center_y - 5), piece_size//2, 3)
            pygame.draw.rect(self.screen, fill_color, 
                           (center_x - piece_size//3, center_y + 5, piece_size//1.5, piece_size//3))
            pygame.draw.rect(self.screen, outline_color, 
                           (center_x - piece_size//3, center_y + 5, piece_size//1.5, piece_size//3), 2)
        
        elif piece.piece_type == 'rook':
            # Torre - rectángulo con almenas
            base_rect = pygame.Rect(center_x - piece_size//2, center_y - piece_size//3, 
                                  piece_size, piece_size//1.5)
            pygame.draw.rect(self.screen, fill_color, base_rect)
            pygame.draw.rect(self.screen, outline_color, base_rect, 3)
            
            # Almenas
            for i in range(3):
                x_offset = (i - 1) * piece_size//4
                small_rect = pygame.Rect(center_x + x_offset - piece_size//8, 
                                       center_y - piece_size//2, piece_size//4, piece_size//4)
                pygame.draw.rect(self.screen, fill_color, small_rect)
                pygame.draw.rect(self.screen, outline_color, small_rect, 2)
        
        elif piece.piece_type == 'knight':
            # Caballo - forma de L estilizada
            points = [
                (center_x - piece_size//3, center_y + piece_size//3),
                (center_x - piece_size//4, center_y - piece_size//3),
                (center_x + piece_size//6, center_y - piece_size//2),
                (center_x + piece_size//3, center_y - piece_size//4),
                (center_x + piece_size//4, center_y + piece_size//3)
            ]
            pygame.draw.polygon(self.screen, fill_color, points)
            pygame.draw.polygon(self.screen, outline_color, points, 3)
        
        elif piece.piece_type == 'bishop':
            # Alfil - rombo con cruz
            points = [
                (center_x, center_y - piece_size//2),
                (center_x + piece_size//3, center_y),
                (center_x, center_y + piece_size//2),
                (center_x - piece_size//3, center_y)
            ]
            pygame.draw.polygon(self.screen, fill_color, points)
            pygame.draw.polygon(self.screen, outline_color, points, 3)
            
            # Cruz en la parte superior
            pygame.draw.line(self.screen, outline_color, 
                           (center_x - 5, center_y - piece_size//2), 
                           (center_x + 5, center_y - piece_size//2), 3)
            pygame.draw.line(self.screen, outline_color, 
                           (center_x, center_y - piece_size//2 - 5), 
                           (center_x, center_y - piece_size//2 + 5), 3)
        
        elif piece.piece_type == 'queen':
            # Reina - corona con puntas
            base_y = center_y + piece_size//4
            pygame.draw.circle(self.screen, fill_color, (center_x, base_y), piece_size//2)
            pygame.draw.circle(self.screen, outline_color, (center_x, base_y), piece_size//2, 3)
            
            # Corona con 5 puntas
            for i in range(5):
                angle = (i * 72 - 90) * math.pi / 180
                x = center_x + math.cos(angle) * piece_size//3
                y = center_y - piece_size//3 + math.sin(angle) * piece_size//3
                pygame.draw.circle(self.screen, fill_color, (int(x), int(y)), piece_size//8)
                pygame.draw.circle(self.screen, outline_color, (int(x), int(y)), piece_size//8, 2)
        
        elif piece.piece_type == 'king':
            # Rey - corona con cruz
            pygame.draw.circle(self.screen, fill_color, (center_x, center_y + 5), piece_size//2)
            pygame.draw.circle(self.screen, outline_color, (center_x, center_y + 5), piece_size//2, 3)
            
            # Cruz grande en la parte superior
            cross_size = piece_size//3
            pygame.draw.line(self.screen, outline_color,
                           (center_x - cross_size, center_y - piece_size//3),
                           (center_x + cross_size, center_y - piece_size//3), 4)
            pygame.draw.line(self.screen, outline_color,
                           (center_x, center_y - piece_size//2),
                           (center_x, center_y - piece_size//6), 4)
    
    def draw_pieces(self):
        """Dibujar todas las piezas"""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.game.board[row][col]
                if piece:
                    center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
                    center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2
                    
                    # Dibujar sombra
                    shadow_offset = 3
                    shadow_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    
                    # Opción 1: Usar formas geométricas (más moderno)
                    self.draw_piece_shapes(piece, center_x, center_y)
                    
                    # Opción 2: Usar símbolos Unicode mejorados (comentado)
                    # symbol = piece.get_symbol()
                    # fill_color, outline_color = piece.get_colors()
                    # 
                    # # Texto con sombra
                    # shadow_text = self.big_font.render(symbol, True, (0, 0, 0, 100))
                    # shadow_rect = shadow_text.get_rect(center=(center_x + 2, center_y + 2))
                    # self.screen.blit(shadow_text, shadow_rect)
                    # 
                    # # Texto principal
                    # piece_text = self.big_font.render(symbol, True, fill_color)
                    # piece_rect = piece_text.get_rect(center=(center_x, center_y))
                    # self.screen.blit(piece_text, piece_rect)
                    # 
                    # # Contorno
                    # outline_text = self.big_font.render(symbol, True, outline_color)
                    # for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    #     outline_rect = outline_text.get_rect(center=(center_x + dx, center_y + dy))
                    #     self.screen.blit(outline_text, outline_rect)
    
    def draw_info(self):
        """Dibujar información del juego"""
        info_y = BOARD_SIZE * SQUARE_SIZE + 10
        
        # Estado del juego con estilo
        if self.game.game_over:
            text = f"🏆 ¡{self.game.winner.upper()} GANA!"
            color = (255, 215, 0)  # Dorado
        else:
            player_symbol = "♔" if self.game.current_player == "white" else "♚"
            text = f"{player_symbol} Turno: {self.game.current_player.capitalize()}"
            color = BLACK
        
        # Fondo para el texto
        text_surface = self.info_font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.x = 10
        text_rect.y = info_y
        
        # Fondo semitransparente
        bg_rect = text_rect.inflate(20, 10)
        bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
        bg_surface.set_alpha(200)
        bg_surface.fill((255, 255, 255))
        self.screen.blit(bg_surface, bg_rect)
        
        # Texto
        self.screen.blit(text_surface, text_rect)
        
        # Instrucciones
        instructions = "🖱️ Click para seleccionar | 🎯 Amarillo=Movimiento | 🔴 Rojo=Captura | R=Reiniciar"
        inst_text = self.font.render(instructions, True, BLACK)
        self.screen.blit(inst_text, (10, info_y + 50))
    
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
            
            # Fondo con gradiente
            for y in range(WINDOW_HEIGHT):
                color_value = int(245 - (y / WINDOW_HEIGHT) * 20)
                color = (color_value, color_value, color_value + 10)
                pygame.draw.line(self.screen, color, (0, y), (WINDOW_WIDTH, y))
            
            self.draw_board()
            self.draw_pieces()
            self.draw_info()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    print("🎮 Iniciando Ajedrez Visual Premium...")
    print("✨ Nuevas características:")
    print("  • Piezas dibujadas con formas geométricas")
    print("  • Efectos visuales mejorados")
    print("  • Tablero con gradientes")
    print("  • Animaciones y sombras")
    print("=" * 50)
    
    game = ChessGUI()
    game.run()
