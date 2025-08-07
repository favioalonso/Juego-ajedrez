#!/usr/bin/env python3
"""
Script de prueba para verificar que el juego de ajedrez funciona correctamente.
"""

import sys
import os

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_pygame_import():
    """Verificar que pygame se puede importar"""
    try:
        import pygame
        print("✅ Pygame importado correctamente")
        print(f"   Versión de Pygame: {pygame.version.ver}")
        return True
    except ImportError as e:
        print(f"❌ Error importando pygame: {e}")
        return False

def test_chess_game_import():
    """Verificar que el juego de ajedrez se puede importar"""
    try:
        from chess_game import ChessGame, Piece, ChessGUI
        print("✅ Módulo de ajedrez básico importado correctamente")
        return True
    except ImportError as e:
        print(f"❌ Error importando chess_game: {e}")
        return False

def test_chess_advanced_import():
    """Verificar que el juego de ajedrez avanzado se puede importar"""
    try:
        from chess_advanced import ChessGame, Piece, ChessGUI, GameState
        print("✅ Módulo de ajedrez avanzado importado correctamente")
        return True
    except ImportError as e:
        print(f"❌ Error importando chess_advanced: {e}")
        return False

def test_basic_game_functionality():
    """Probar funcionalidad básica del juego"""
    try:
        from chess_advanced import ChessGame, Piece
        
        # Crear un juego
        game = ChessGame()
        print("✅ Juego creado correctamente")
        
        # Verificar que el tablero se configuró
        white_king = None
        black_king = None
        piece_count = 0
        
        for row in range(8):
            for col in range(8):
                piece = game.board[row][col]
                if piece:
                    piece_count += 1
                    if piece.piece_type == 'king':
                        if piece.color == 'white':
                            white_king = piece
                        else:
                            black_king = piece
        
        print(f"✅ Tablero configurado con {piece_count} piezas")
        
        if white_king and black_king:
            print("✅ Ambos reyes encontrados en el tablero")
        else:
            print("❌ Falta algún rey en el tablero")
            return False
        
        # Probar un movimiento
        pawn = game.board[6][4]  # Peón blanco en e2
        if pawn and pawn.piece_type == 'pawn':
            moves = game.get_valid_moves(pawn)
            if moves:
                print(f"✅ Peón puede moverse a {len(moves)} posiciones")
            else:
                print("❌ Peón no tiene movimientos válidos")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error en prueba de funcionalidad: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🎮 Probando el juego de ajedrez...")
    print("=" * 50)
    
    tests = [
        test_pygame_import,
        test_chess_game_import,
        test_chess_advanced_import,
        test_basic_game_functionality
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Resultados: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todos los tests pasaron! El juego está listo para usar.")
        print("\nPara jugar:")
        print("  python chess_game.py      (versión básica)")
        print("  python chess_advanced.py  (versión avanzada)")
    else:
        print("⚠️  Algunos tests fallaron. Revisa los errores arriba.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
