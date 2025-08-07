import pygame
import sys
from typing import List, Tuple, Optional
from enum import Enum

# Inicializar pygame
pygame.init()

# Constantes
BOARD_SIZE = 8
SQUARE_SIZE = 80
WINDOW_WIDTH = BOARD_SIZE * SQUARE_SIZE
WINDOW_HEIGHT = BOARD_SIZE * SQUARE_SIZE + 120
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BROWN = (240, 217, 181)
DARK_BROWN = (181, 136, 99)
HIGHLIGHT_COLOR = (255, 255, 0, 128)
SELECTED_COLOR = (0, 255, 0, 128)
CAPTURE_COLOR = (255, 0, 0, 128)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class GameState(Enum):
    PLAYING = "playing"
    CHECK = "check"
    CHECKMATE = "checkmate"
    STALEMATE = "stalemate"

class Piece:
    def __init__(self, color: str, piece_type: str, row: int, col: int):
        self.color = color
        self.piece_type = piece_type
        self.row = row
        self.col = col
        self.has_moved = False
    
    def __str__(self):
        return f"{self.color} {self.piece_type} at ({self.row}, {self.col})"
    
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
    
    def copy(self):
        """Crear una copia de la pieza"""
        new_piece = Piece(self.color, self.piece_type, self.row, self.col)
        new_piece.has_moved = self.has_moved
        return new_piece
    
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
        self.game_state = GameState.PLAYING
        self.move_history = []
        self.captured_pieces = {'white': [], 'black': []}
        self._setup_board()
    
    def _setup_board(self):
        """Configurar el tablero inicial"""
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
        """Obtener pieza en una posición específica"""
        if 0 <= row < 8 and 0 <= col < 8:
            return self.board[row][col]
        return None
    
    def find_king(self, color: str) -> Optional[Tuple[int, int]]:
        """Encontrar la posición del rey de un color"""
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.piece_type == 'king' and piece.color == color:
                    return (row, col)
        return None
    
    def is_in_check(self, color: str) -> bool:
        """Verificar si el rey está en jaque"""
        king_pos = self.find_king(color)
        if not king_pos:
            return False
        
        opponent_color = 'black' if color == 'white' else 'white'
        
        # Verificar si alguna pieza enemiga puede atacar al rey
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == opponent_color:
                    possible_moves = piece.get_possible_moves(self.board)
                    if king_pos in possible_moves:
                        return True
        return False
    
    def would_be_in_check(self, from_row: int, from_col: int, to_row: int, to_col: int, color: str) -> bool:
        """Verificar si un movimiento dejaría al rey en jaque"""
        # Simular el movimiento
        original_piece = self.board[to_row][to_col]
        moving_piece = self.board[from_row][from_col]
        
        # Realizar movimiento temporal
        self.board[to_row][to_col] = moving_piece
        self.board[from_row][from_col] = None
        if moving_piece:
            moving_piece.row = to_row
            moving_piece.col = to_col
        
        # Verificar jaque
        in_check = self.is_in_check(color)
        
        # Restaurar posición
        self.board[from_row][from_col] = moving_piece
        self.board[to_row][to_col] = original_piece
        if moving_piece:
            moving_piece.row = from_row
            moving_piece.col = from_col
        
        return in_check
    
    def get_valid_moves(self, piece: Piece) -> List[Tuple[int, int]]:
        """Obtener movimientos válidos que no dejen al rey en jaque"""
        possible_moves = piece.get_possible_moves(self.board)
        valid_moves = []
        
        for to_row, to_col in possible_moves:
            if not self.would_be_in_check(piece.row, piece.col, to_row, to_col, piece.color):
                valid_moves.append((to_row, to_col))
        
        return valid_moves
    
    def has_valid_moves(self, color: str) -> bool:
        """Verificar si un jugador tiene movimientos válidos"""
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    if self.get_valid_moves(piece):
                        return True
        return False
    
    def update_game_state(self):
        """Actualizar el estado del juego"""
        if self.is_in_check(self.current_player):
            if not self.has_valid_moves(self.current_player):
                self.game_state = GameState.CHECKMATE
            else:
                self.game_state = GameState.CHECK
        elif not self.has_valid_moves(self.current_player):
            self.game_state = GameState.STALEMATE
        else:
            self.game_state = GameState.PLAYING
    
    def move_piece(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        """Mover una pieza"""
        piece = self.board[from_row][from_col]
        if not piece or piece.color != self.current_player:
            return False
        
        valid_moves = self.get_valid_moves(piece)
        if (to_row, to_col) not in valid_moves:
            return False
        
        # Capturar pieza si existe
        captured_piece = self.board[to_row][to_col]
        if captured_piece:
            self.captured_pieces[captured_piece.color].append(captured_piece)
        
        # Registrar movimiento
        move = {
            'from': (from_row, from_col),
            'to': (to_row, to_col),
            'piece': piece.piece_type,
            'captured': captured_piece.piece_type if captured_piece else None
        }
        self.move_history.append(move)
        
        # Realizar el movimiento
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = None
        piece.row = to_row
        piece.col = to_col
        piece.has_moved = True
        
        # Promoción de peón
        if piece.piece_type == 'pawn':
            if (piece.color == 'white' and to_row == 0) or (piece.color == 'black' and to_row == 7):
                piece.piece_type = 'queen'  # Auto-promoción a reina
        
        # Cambiar turno
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        
        # Actualizar estado del juego
        self.update_game_state()
        
        return True
    
    def select_piece(self, row: int, col: int):
        """Seleccionar una pieza"""
        piece = self.board[row][col]
        
        if self.selected_piece and (row, col) in self.possible_moves:
            # Mover pieza seleccionada
            if self.move_piece(self.selected_piece.row, self.selected_piece.col, row, col):
                self.selected_piece = None
                self.selected_pos = None
                self.possible_moves = []
        elif piece and piece.color == self.current_player and self.game_state != GameState.CHECKMATE:
            # Seleccionar nueva pieza
            self.selected_piece = piece
            self.selected_pos = (row, col)
            self.possible_moves = self.get_valid_moves(piece)
        else:
            # Deseleccionar
            self.selected_piece = None
            self.selected_pos = None
            self.possible_moves = []
    
    def reset_game(self):
        """Reiniciar el juego"""
        self.__init__()

class ChessGUI:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Ajedrez Avanzado - Python")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 60)
        self.info_font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 36)
        self.game = ChessGame()
    
    def draw_board(self):
        """Dibujar el tablero"""
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
                    piece_at_target = self.game.board[row][col]
                    if piece_at_target:  # Casilla con pieza enemiga (captura)
                        color_to_use = CAPTURE_COLOR[:3]
                    else:  # Casilla vacía (movimiento)
                        color_to_use = HIGHLIGHT_COLOR[:3]
                    
                    highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
                    highlight_surface.set_alpha(100)
                    highlight_surface.fill(color_to_use)
                    self.screen.blit(highlight_surface, (col * SQUARE_SIZE, row * SQUARE_SIZE))
        
        # Dibujar coordenadas
        coord_font = pygame.font.Font(None, 20)
        for i in range(8):
            # Números (filas)
            text = coord_font.render(str(8-i), True, BLACK)
            self.screen.blit(text, (5, i * SQUARE_SIZE + 5))
            
            # Letras (columnas)
            text = coord_font.render(chr(ord('a') + i), True, BLACK)
            self.screen.blit(text, (i * SQUARE_SIZE + SQUARE_SIZE - 15, BOARD_SIZE * SQUARE_SIZE - 20))
    
    def draw_pieces(self):
        """Dibujar las piezas"""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.game.board[row][col]
                if piece:
                    symbol = piece.get_symbol()
                    text = self.font.render(symbol, True, BLACK)
                    text_rect = text.get_rect(center=(
                        col * SQUARE_SIZE + SQUARE_SIZE // 2,
                        row * SQUARE_SIZE + SQUARE_SIZE // 2
                    ))
                    self.screen.blit(text, text_rect)
    
    def draw_info(self):
        """Dibujar información del juego"""
        info_y = BOARD_SIZE * SQUARE_SIZE + 10
        
        # Estado del juego
        if self.game.game_state == GameState.CHECKMATE:
            winner = 'black' if self.game.current_player == 'white' else 'white'
            text = f"¡JAQUE MATE! {winner.capitalize()} gana"
            color = RED
        elif self.game.game_state == GameState.CHECK:
            text = f"¡JAQUE! Turno: {self.game.current_player.capitalize()}"
            color = RED
        elif self.game.game_state == GameState.STALEMATE:
            text = "¡EMPATE! (Ahogado)"
            color = BLUE
        else:
            text = f"Turno: {self.game.current_player.capitalize()}"
            color = BLACK
        
        title_text = self.title_font.render(text, True, color)
        self.screen.blit(title_text, (10, info_y))
        
        # Instrucciones
        instructions = [
            "Click para seleccionar y mover piezas",
            "Amarillo: movimiento válido, Rojo: captura",
            "R: Reiniciar juego"
        ]
        
        for i, instruction in enumerate(instructions):
            inst_text = self.info_font.render(instruction, True, BLACK)
            self.screen.blit(inst_text, (10, info_y + 35 + i * 20))
        
        # Mostrar capturas
        captured_y = info_y + 35
        if self.game.captured_pieces['white']:
            captured_white = "Capturadas (Blancas): " + " ".join([p.get_symbol() for p in self.game.captured_pieces['white']])
            cap_text = self.info_font.render(captured_white, True, BLACK)
            self.screen.blit(cap_text, (300, captured_y))
        
        if self.game.captured_pieces['black']:
            captured_black = "Capturadas (Negras): " + " ".join([p.get_symbol() for p in self.game.captured_pieces['black']])
            cap_text = self.info_font.render(captured_black, True, BLACK)
            self.screen.blit(cap_text, (300, captured_y + 20))
    
    def handle_click(self, pos):
        """Manejar clicks del mouse"""
        if pos[1] < BOARD_SIZE * SQUARE_SIZE:  # Click en el tablero
            col = pos[0] // SQUARE_SIZE
            row = pos[1] // SQUARE_SIZE
            self.game.select_piece(row, col)
    
    def run(self):
        """Ejecutar el juego"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Click izquierdo
                        self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # Reiniciar juego
                        self.game.reset_game()
            
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
