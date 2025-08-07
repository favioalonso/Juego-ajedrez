import pygame
import sys
from typing import List, Tuple, Optional

# Inicializar pygame
pygame.init()

# Constantes
BOARD_SIZE = 8
SQUARE_SIZE = 90  # Aumentado para piezas más grandes
WINDOW_WIDTH = BOARD_SIZE * SQUARE_SIZE
WINDOW_HEIGHT = BOARD_SIZE * SQUARE_SIZE + 100  # Espacio extra para información
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BROWN = (240, 217, 181)
DARK_BROWN = (181, 136, 99)
HIGHLIGHT_COLOR = (255, 255, 0, 128)
SELECTED_COLOR = (0, 255, 0, 128)
PIECE_SHADOW_COLOR = (50, 50, 50)
PIECE_WHITE_COLOR = (245, 245, 245)
PIECE_BLACK_COLOR = (50, 50, 50)

class Piece:
    def __init__(self, color: str, piece_type: str, row: int, col: int):
        self.color = color  # 'white' or 'black'
        self.piece_type = piece_type  # 'pawn', 'rook', 'knight', 'bishop', 'queen', 'king'
        self.row = row
        self.col = col
        self.has_moved = False
      def get_symbol(self) -> str:
        # Usando símbolos Unicode más grandes y mejor definidos
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
    
    def get_piece_color(self) -> tuple:
        """Obtener el color de renderizado de la pieza"""
        return PIECE_WHITE_COLOR if self.color == 'white' else PIECE_BLACK_COLOR
    
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
        
        # Movimiento hacia adelante
        new_row = self.row + direction
        if 0 <= new_row < 8 and board[new_row][self.col] is None:
            moves.append((new_row, self.col))
            
            # Doble movimiento desde posición inicial
            if self.row == start_row and board[new_row + direction][self.col] is None:
                moves.append((new_row + direction, self.col))
        
        # Capturas diagonales
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
        
        # Realizar el movimiento
        captured_piece = self.board[to_row][to_col]
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = None
        piece.row = to_row
        piece.col = to_col
        piece.has_moved = True
        
        # Verificar si es jaque mate
        if captured_piece and captured_piece.piece_type == 'king':
            self.game_over = True
            self.winner = self.current_player
        
        # Cambiar turno
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        return True
    
    def select_piece(self, row: int, col: int):
        piece = self.board[row][col]
        
        if self.selected_piece and (row, col) in self.possible_moves:
            # Mover pieza seleccionada
            if self.move_piece(self.selected_piece.row, self.selected_piece.col, row, col):
                self.selected_piece = None
                self.selected_pos = None
                self.possible_moves = []
        elif piece and piece.color == self.current_player:
            # Seleccionar nueva pieza
            self.selected_piece = piece
            self.selected_pos = (row, col)
            self.possible_moves = piece.get_possible_moves(self.board)
        else:
            # Deseleccionar
            self.selected_piece = None
            self.selected_pos = None
            self.possible_moves = []

class ChessGUI:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("♔ Ajedrez Premium - Python ♔")
        self.clock = pygame.time.Clock()
        # Fuentes más grandes y mejor renderizado
        self.font = pygame.font.Font(None, 85)  # Aumentado considerablemente
        self.info_font = pygame.font.Font(None, 36)
        self.game = ChessGame()
        
        # Configurar antialiasing para mejor calidad
        pygame.font.init()
    
    def draw_board(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
                rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(self.screen, color, rect)
                
                # Highlight casilla seleccionada
                if self.game.selected_pos == (row, col):
                    highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
                    highlight_surface.set_alpha(128)
                    highlight_surface.fill(SELECTED_COLOR[:3])
                    self.screen.blit(highlight_surface, (col * SQUARE_SIZE, row * SQUARE_SIZE))
                
                # Highlight movimientos posibles
                if (row, col) in self.game.possible_moves:
                    highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
                    highlight_surface.set_alpha(100)
                    highlight_surface.fill(HIGHLIGHT_COLOR[:3])
                    self.screen.blit(highlight_surface, (col * SQUARE_SIZE, row * SQUARE_SIZE))
      def draw_pieces(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.game.board[row][col]
                if piece:
                    symbol = piece.get_symbol()
                    piece_color = piece.get_piece_color()
                    
                    # Calcular posición central
                    center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
                    center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2
                    
                    # Dibujar sombra de la pieza para efecto 3D
                    shadow_text = self.font.render(symbol, True, PIECE_SHADOW_COLOR)
                    shadow_rect = shadow_text.get_rect(center=(center_x + 2, center_y + 2))
                    self.screen.blit(shadow_text, shadow_rect)
                    
                    # Dibujar la pieza principal con antialiasing
                    piece_text = self.font.render(symbol, True, piece_color)
                    piece_rect = piece_text.get_rect(center=(center_x, center_y))
                    self.screen.blit(piece_text, piece_rect)
                    
                    # Agregar brillo para piezas blancas
                    if piece.color == 'white':
                        highlight_text = self.font.render(symbol, True, (255, 255, 255))
                        highlight_rect = highlight_text.get_rect(center=(center_x - 1, center_y - 1))
                        self.screen.blit(highlight_text, highlight_rect)
    
    def draw_info(self):
        info_y = BOARD_SIZE * SQUARE_SIZE + 10
        
        if self.game.game_over:
            text = f"¡{self.game.winner.capitalize()} gana!"
            color = BLACK
        else:
            text = f"Turno: {self.game.current_player.capitalize()}"
            color = BLACK
        
        info_text = self.info_font.render(text, True, color)
        self.screen.blit(info_text, (10, info_y))
        
        # Instrucciones
        instructions = "Haz clic para seleccionar y mover piezas"
        inst_text = self.info_font.render(instructions, True, BLACK)
        self.screen.blit(inst_text, (10, info_y + 40))
    
    def handle_click(self, pos):
        if pos[1] < BOARD_SIZE * SQUARE_SIZE:  # Click en el tablero
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
                    if event.button == 1:  # Click izquierdo
                        self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.game.game_over:
                        # Reiniciar juego
                        self.game = ChessGame()
            
            self.screen.fill(WHITE)
            self.draw_board()
            self.draw_pieces()
            self.draw_info()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = ChessGUI()
    game.run()
