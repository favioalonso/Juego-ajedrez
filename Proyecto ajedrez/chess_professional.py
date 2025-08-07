import pygame
import sys
import json
from datetime import datetime
from typing import List, Tuple, Optional, Dict
from enum import Enum

# Inicializar pygame
pygame.init()

# Constantes mejoradas
BOARD_SIZE = 8
SQUARE_SIZE = 80
WINDOW_WIDTH = BOARD_SIZE * SQUARE_SIZE + 300  # Espacio extra para panel lateral
WINDOW_HEIGHT = BOARD_SIZE * SQUARE_SIZE + 50
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
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)

class GameState(Enum):
    PLAYING = "playing"
    CHECK = "check"
    CHECKMATE = "checkmate"
    STALEMATE = "stalemate"
    PAUSED = "paused"

class Piece:
    def __init__(self, color: str, piece_type: str, row: int, col: int):
        self.color = color
        self.piece_type = piece_type
        self.row = row
        self.col = col
        self.has_moved = False
        self.value = self._get_piece_value()
    
    def _get_piece_value(self) -> int:
        """Obtener el valor de la pieza para evaluación"""
        values = {
            'pawn': 1, 'knight': 3, 'bishop': 3,
            'rook': 5, 'queen': 9, 'king': 100
        }
        return values.get(self.piece_type, 0)
    
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
        self.move_count = 0
        self.start_time = datetime.now()
        self.game_time = {'white': 0, 'black': 0}
        self.last_move_time = datetime.now()
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
    
    def find_king(self, color: str) -> Optional[Tuple[int, int]]:
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.piece_type == 'king' and piece.color == color:
                    return (row, col)
        return None
    
    def is_in_check(self, color: str) -> bool:
        king_pos = self.find_king(color)
        if not king_pos:
            return False
        
        opponent_color = 'black' if color == 'white' else 'white'
        
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == opponent_color:
                    possible_moves = piece.get_possible_moves(self.board)
                    if king_pos in possible_moves:
                        return True
        return False
    
    def would_be_in_check(self, from_row: int, from_col: int, to_row: int, to_col: int, color: str) -> bool:
        original_piece = self.board[to_row][to_col]
        moving_piece = self.board[from_row][from_col]
        
        self.board[to_row][to_col] = moving_piece
        self.board[from_row][from_col] = None
        if moving_piece:
            moving_piece.row = to_row
            moving_piece.col = to_col
        
        in_check = self.is_in_check(color)
        
        self.board[from_row][from_col] = moving_piece
        self.board[to_row][to_col] = original_piece
        if moving_piece:
            moving_piece.row = from_row
            moving_piece.col = from_col
        
        return in_check
    
    def get_valid_moves(self, piece: Piece) -> List[Tuple[int, int]]:
        possible_moves = piece.get_possible_moves(self.board)
        valid_moves = []
        
        for to_row, to_col in possible_moves:
            if not self.would_be_in_check(piece.row, piece.col, to_row, to_col, piece.color):
                valid_moves.append((to_row, to_col))
        
        return valid_moves
    
    def has_valid_moves(self, color: str) -> bool:
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    if self.get_valid_moves(piece):
                        return True
        return False
    
    def calculate_material_balance(self) -> Dict[str, int]:
        """Calcular balance de material"""
        balance = {'white': 0, 'black': 0}
        
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.piece_type != 'king':
                    balance[piece.color] += piece.value
        
        return balance
    
    def update_game_state(self):
        if self.is_in_check(self.current_player):
            if not self.has_valid_moves(self.current_player):
                self.game_state = GameState.CHECKMATE
            else:
                self.game_state = GameState.CHECK
        elif not self.has_valid_moves(self.current_player):
            self.game_state = GameState.STALEMATE
        else:
            self.game_state = GameState.PLAYING
    
    def update_timer(self):
        """Actualizar el tiempo de juego"""
        current_time = datetime.now()
        time_diff = (current_time - self.last_move_time).total_seconds()
        
        opponent = 'black' if self.current_player == 'white' else 'white'
        self.game_time[opponent] += time_diff
        self.last_move_time = current_time
    
    def move_piece(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        piece = self.board[from_row][from_col]
        if not piece or piece.color != self.current_player:
            return False
        
        valid_moves = self.get_valid_moves(piece)
        if (to_row, to_col) not in valid_moves:
            return False
        
        # Actualizar tiempo
        self.update_timer()
        
        # Capturar pieza si existe
        captured_piece = self.board[to_row][to_col]
        if captured_piece:
            self.captured_pieces[captured_piece.color].append(captured_piece)
        
        # Registrar movimiento en notación algebraica simplificada
        from_pos = f"{chr(ord('a') + from_col)}{8 - from_row}"
        to_pos = f"{chr(ord('a') + to_col)}{8 - to_row}"
        notation = f"{piece.get_symbol()}{from_pos}-{to_pos}"
        if captured_piece:
            notation += f"x{captured_piece.get_symbol()}"
        
        move = {
            'from': (from_row, from_col),
            'to': (to_row, to_col),
            'piece': piece.piece_type,
            'captured': captured_piece.piece_type if captured_piece else None,
            'notation': notation,
            'move_number': self.move_count + 1
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
                piece.piece_type = 'queen'
        
        # Cambiar turno
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        self.move_count += 1
        
        # Actualizar estado del juego
        self.update_game_state()
        
        return True
    
    def select_piece(self, row: int, col: int):
        piece = self.board[row][col]
        
        if self.selected_piece and (row, col) in self.possible_moves:
            if self.move_piece(self.selected_piece.row, self.selected_piece.col, row, col):
                self.selected_piece = None
                self.selected_pos = None
                self.possible_moves = []
        elif piece and piece.color == self.current_player and self.game_state not in [GameState.CHECKMATE, GameState.STALEMATE]:
            self.selected_piece = piece
            self.selected_pos = (row, col)
            self.possible_moves = self.get_valid_moves(piece)
        else:
            self.selected_piece = None
            self.selected_pos = None
            self.possible_moves = []
    
    def get_last_move_notation(self) -> str:
        """Obtener notación del último movimiento"""
        if self.move_history:
            return self.move_history[-1]['notation']
        return ""
    
    def save_game(self, filename: str):
        """Guardar el juego en un archivo JSON"""
        game_data = {
            'move_history': self.move_history,
            'current_player': self.current_player,
            'game_state': self.game_state.value,
            'move_count': self.move_count,
            'game_time': self.game_time,
            'captured_pieces': {
                'white': [{'type': p.piece_type, 'color': p.color} for p in self.captured_pieces['white']],
                'black': [{'type': p.piece_type, 'color': p.color} for p in self.captured_pieces['black']]
            }
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(game_data, f, indent=2)
            return True
        except Exception:
            return False
    
    def reset_game(self):
        self.__init__()

class ChessGUI:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("♔ Ajedrez Profesional - Python ♔")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 60)
        self.info_font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 20)
        self.game = ChessGame()
        self.show_coordinates = True
        self.show_last_move = True
    
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
                    piece_at_target = self.game.board[row][col]
                    if piece_at_target:
                        color_to_use = CAPTURE_COLOR[:3]
                    else:
                        color_to_use = HIGHLIGHT_COLOR[:3]
                    
                    highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
                    highlight_surface.set_alpha(100)
                    highlight_surface.fill(color_to_use)
                    self.screen.blit(highlight_surface, (col * SQUARE_SIZE, row * SQUARE_SIZE))
        
        # Dibujar coordenadas si está habilitado
        if self.show_coordinates:
            for i in range(8):
                # Números (filas)
                text = self.small_font.render(str(8-i), True, BLACK)
                self.screen.blit(text, (5, i * SQUARE_SIZE + 5))
                
                # Letras (columnas)
                text = self.small_font.render(chr(ord('a') + i), True, BLACK)
                self.screen.blit(text, (i * SQUARE_SIZE + SQUARE_SIZE - 15, BOARD_SIZE * SQUARE_SIZE - 20))
    
    def draw_pieces(self):
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
    
    def draw_side_panel(self):
        """Dibujar panel lateral con información del juego"""
        panel_x = BOARD_SIZE * SQUARE_SIZE + 10
        panel_width = 280
        
        # Fondo del panel
        panel_rect = pygame.Rect(panel_x, 0, panel_width, WINDOW_HEIGHT)
        pygame.draw.rect(self.screen, LIGHT_GRAY, panel_rect)
        pygame.draw.rect(self.screen, BLACK, panel_rect, 2)
        
        y_offset = 10
        
        # Título
        title = self.title_font.render("🎮 Estado del Juego", True, BLACK)
        self.screen.blit(title, (panel_x + 10, y_offset))
        y_offset += 40
        
        # Estado actual
        if self.game.game_state == GameState.CHECKMATE:
            winner = 'black' if self.game.current_player == 'white' else 'white'
            status = f"🏆 ¡{winner.upper()} GANA!"
            color = RED
        elif self.game.game_state == GameState.CHECK:
            status = f"⚠️ JAQUE - {self.game.current_player.upper()}"
            color = RED
        elif self.game.game_state == GameState.STALEMATE:
            status = "🤝 EMPATE (Ahogado)"
            color = BLUE
        else:
            status = f"▶️ Turno: {self.game.current_player.upper()}"
            color = BLACK
        
        status_text = self.info_font.render(status, True, color)
        self.screen.blit(status_text, (panel_x + 10, y_offset))
        y_offset += 30
        
        # Número de movimientos
        moves_text = self.info_font.render(f"Movimientos: {self.game.move_count}", True, BLACK)
        self.screen.blit(moves_text, (panel_x + 10, y_offset))
        y_offset += 25
        
        # Balance de material
        balance = self.game.calculate_material_balance()
        balance_text = f"Material - B:{balance['white']} N:{balance['black']}"
        material_text = self.info_font.render(balance_text, True, BLACK)
        self.screen.blit(material_text, (panel_x + 10, y_offset))
        y_offset += 25
        
        # Tiempo de juego
        self.game.update_timer()
        white_time = int(self.game.game_time['white'])
        black_time = int(self.game.game_time['black'])
        time_text = f"Tiempo - B:{white_time//60}:{white_time%60:02d} N:{black_time//60}:{black_time%60:02d}"
        timer_text = self.info_font.render(time_text, True, BLACK)
        self.screen.blit(timer_text, (panel_x + 10, y_offset))
        y_offset += 35
        
        # Piezas capturadas
        captured_title = self.info_font.render("🏴 Piezas Capturadas:", True, BLACK)
        self.screen.blit(captured_title, (panel_x + 10, y_offset))
        y_offset += 25
        
        if self.game.captured_pieces['white']:
            white_captured = "Blancas: " + " ".join([p.get_symbol() for p in self.game.captured_pieces['white']])
            cap_text = self.small_font.render(white_captured, True, BLACK)
            self.screen.blit(cap_text, (panel_x + 10, y_offset))
            y_offset += 20
        
        if self.game.captured_pieces['black']:
            black_captured = "Negras: " + " ".join([p.get_symbol() for p in self.game.captured_pieces['black']])
            cap_text = self.small_font.render(black_captured, True, BLACK)
            self.screen.blit(cap_text, (panel_x + 10, y_offset))
            y_offset += 30
        
        # Último movimiento
        if self.show_last_move and self.game.move_history:
            last_move_title = self.info_font.render("📝 Último Movimiento:", True, BLACK)
            self.screen.blit(last_move_title, (panel_x + 10, y_offset))
            y_offset += 20
            
            last_notation = self.game.get_last_move_notation()
            last_text = self.small_font.render(last_notation, True, BLUE)
            self.screen.blit(last_text, (panel_x + 10, y_offset))
            y_offset += 30
        
        # Controles
        controls_title = self.info_font.render("🎮 Controles:", True, BLACK)
        self.screen.blit(controls_title, (panel_x + 10, y_offset))
        y_offset += 25
        
        controls = [
            "Click: Seleccionar/Mover",
            "R: Reiniciar juego",
            "S: Guardar partida",
            "C: Mostrar coordenadas",
            "ESC: Salir"
        ]
        
        for control in controls:
            control_text = self.small_font.render(control, True, BLACK)
            self.screen.blit(control_text, (panel_x + 10, y_offset))
            y_offset += 18
    
    def handle_click(self, pos):
        if pos[0] < BOARD_SIZE * SQUARE_SIZE:  # Click en el tablero
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
                    if event.key == pygame.K_r:
                        # Reiniciar juego
                        self.game.reset_game()
                    elif event.key == pygame.K_s:
                        # Guardar partida
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"partida_{timestamp}.json"
                        if self.game.save_game(filename):
                            print(f"Partida guardada como: {filename}")
                    elif event.key == pygame.K_c:
                        # Toggle coordenadas
                        self.show_coordinates = not self.show_coordinates
                    elif event.key == pygame.K_ESCAPE:
                        running = False
            
            self.screen.fill(WHITE)
            self.draw_board()
            self.draw_pieces()
            self.draw_side_panel()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    print("🎮 Iniciando Ajedrez Profesional...")
    print("=" * 50)
    print("Controles:")
    print("  Click: Seleccionar y mover piezas")
    print("  R: Reiniciar juego")
    print("  S: Guardar partida")
    print("  C: Mostrar/ocultar coordenadas")
    print("  ESC: Salir")
    print("=" * 50)
    
    game = ChessGUI()
    game.run()
